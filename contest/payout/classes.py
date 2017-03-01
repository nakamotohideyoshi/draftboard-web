from logging import getLogger
import math
import decimal
import mysite.exceptions
from contest.models import Contest, Entry, ClosedContest
from prize.models import Rank
from transaction.models import AbstractAmount
from transaction.classes import CanDeposit
from .models import Payout, Rake, FPP
from draftgroup.classes import DraftGroupManager
from draftgroup.exceptions import FantasyPointsAlreadyFinalizedException
from dfslog.classes import Logger, ErrorCodes
from cash.classes import CashTransaction
from django.db.transaction import atomic
from promocode.bonuscash.classes import BonusCashTransaction
from django.conf import settings
from rakepaid.classes import RakepaidTransaction
from mysite.classes import AbstractManagerClass
from rakepaid.classes import LoyaltyStatusManager
from fpp.classes import FppTransaction
from lineup.classes import LineupManager
from lineup.models import Lineup


logger = getLogger('contest.payout.classes')


class PayoutManager(AbstractManagerClass):
    """
    Responsible for performing the payouts for all active contests for both
    cash and ticket games.
    """

    def __init__(self):
        pass

    def payout(self, contests=None, finalize_score=True):
        """
        Takes in an array of contests to payout. If there are not contests passed
        then the payout mechanism will look for all contests who have not been
        paid out yet and pay them out.
        :param contests: an array of :class:`contest.models.Contest` models
        :param finalize_score: always True in production. (may be set to False to skip the re-scoring during payouts).
        """

        #
        # validation if the contests are passed as an argument
        if contests is not None:
            #
            # validate that contests is an array
            if not isinstance(contests, list):
                raise mysite.exceptions.IncorrectVariableTypeException(
                    type(self).__name__,
                    'contests')

            #
            # validate the contest array is an array of contests
            for contest in contests:
                if not isinstance(contest, Contest):
                    raise mysite.exceptions.IncorrectVariableTypeException(
                        type(self).__name__,
                        'contests')

        #
        # if payout() was called with no arguments,
        # find contests that need to be paid out.
        else:
            #
            # gets all the contests that are completed
            contests = Contest.objects.filter(status=Contest.COMPLETED)

        if finalize_score:
            #
            # get the unique draft group ids within this queryset of contests.
            # update the final scoring for the players in the distinct draft groups.
            draft_group_ids = list(set([c.draft_group.pk for c in contests if c.draft_group != None]))
            for draft_group_id in draft_group_ids:
                draft_group_manager = DraftGroupManager()
                try:
                    draft_group_manager.update_final_fantasy_points(draft_group_id)
                except FantasyPointsAlreadyFinalizedException:
                    pass  # its possible the contest we are trying to payout was already finalized

            #
            # update the fantasy_points for each unique Lineup.
            # get the unique lineups from the contests' entries,
            # so we're not doing extra processing...
            lineups = Lineup.objects.filter(draft_group__pk__in=draft_group_ids)
            for lineup in lineups:
                lineup_manager = LineupManager(lineup.user)
                lineup_manager.update_fantasy_points(lineup)

        #
        # finally, we can pay out the contests!
        for contest in contests:
            self.__payout_contest(contest)

    @atomic
    def __payout_contest(self, contest):
        """
        Method assumes the contest has never been paid out and is ready
        to be paid out. This is why the method is private and should be
        called from a separate method that does the individual error checking.
        """

        try:
            c = ClosedContest.objects.get(pk=contest.pk)
            # print('%s already closed & paid out.'%str(contest))
            return  # go no further
        except:
            pass

        #
        # get the prize pool ranks for the contest
        ranks = Rank.objects.filter(prize_structure=contest.prize_structure).order_by('rank')

        #
        # get the entries for the contest
        entries = Entry.objects.filter(contest=contest)
        entries = entries.order_by('-lineup__fantasy_points')

        #
        # Validate the ranks are setup properly
        for rank in ranks:
            #
            # verify the abstract amount is correct type
            if not isinstance(rank.amount, AbstractAmount):
                raise mysite.exceptions.IncorrectVariableTypeException(
                    type(self).__name__,
                    'rank')

            #
            # Get the transaction class and verify that it can deposit
            transaction_class = rank.amount.get_transaction_class()
            if not issubclass(transaction_class, CanDeposit):
                raise mysite.exceptions.IncorrectVariableTypeException(
                    type(self).__name__,
                    'transaction_class')

        # print('------- entries [%s] contest [%s] -------' %(str(len(entries)), str(contest)))
        #
        # perform the payouts by going through each entry and finding
        # ties and ranks for the ties to chop.
        # print('======= ranks [%s] =======' % (str(ranks)))

        #
        # we now need to check which is shorter: the list of ranks or the list of entries,
        # and only use that many ranks for calculating winners! (its possible for
        # fewer entries than the total number of ranks!

        if len(entries) < len(ranks):
            logger.info('SUPERLAY PAYOUT CONTEST: %s' % contest)

        i = 0
        while i < len(ranks[:len(entries)]):
            # print('++++ i (rank): %s +++++' % str(i) )
            entries_to_pay = list()
            ranks_to_pay = list()
            entries_to_pay.append(entries[i])
            ranks_to_pay.append(ranks[i])
            score = entries[i].lineup.fantasy_points
            #
            # For each tie add the user to the list to chop the payment
            # and add the next payout to be split with the ties.
            while i + 1 < len(entries) and score == entries[i + 1].lineup.fantasy_points:
                i += 1
                entries_to_pay.append(entries[i])
                if len(ranks) > i:
                    ranks_to_pay.append(ranks[i])

            self.__payout_spot(ranks_to_pay, entries_to_pay, contest)
            i += 1

        #
        ###############################################################
        # rank all of the entries with the same payout algorithm.
        ###############################################################
        # j = 0
        # last_fantasy_points = None
        # for entry in entries:
        #     if last_fantasy_points is None:
        #         last_fantasy_points = entry.lineup.fantasy_points
        #     count_at_rank = Entry.objects.filter(contest=contest, lineup__fantasy_points=)

        # using the fantasy_points as the key, add/increment the entry id to the list.
        # the length of that list will be the # of entries at that rank, and
        # the rank will be the order of the keys.
        entry_fantasy_points_map = {}
        for entry in entries:
            try:
                entry_fantasy_points_map[entry.lineup.fantasy_points] += [entry.pk]
            except KeyError:
                entry_fantasy_points_map[entry.lineup.fantasy_points] = [entry.pk]
        # sort the fantasy points map on the map key (ascending)
        sorted_list = sorted(entry_fantasy_points_map.items(), key=lambda x: x[0])
        sorted_list.reverse()  # so its descending ie: [(75.5, [432, 213]), (50.25, [431234, 234534]), (25.0, [1, 123])]

        entry_rank = 1
        for fantasy_points, entry_id_list in sorted_list:
            count_at_rank = len(entry_id_list)
            Entry.objects.filter(pk__in=entry_id_list).update(final_rank=entry_rank)
            entry_rank += count_at_rank

        #
        # get the total number of dollars leftover for rake
        buyin = contest.buyin
        rake_pre_buyin = (contest.entries * buyin) * .10
        overlay = (contest.entries - len(entries)) * buyin
        rake_post_overlay = rake_pre_buyin - overlay
        rake_transaction = None

        #
        # We made money on rake! No overlay, yaaay
        if rake_post_overlay > 0:
            #
            # Take cash out of escrow and deposit it into draftboard
            escrow_withdraw_trans = CashTransaction(self.get_escrow_user())
            escrow_withdraw_trans.withdraw(rake_post_overlay)
            draftboard_deposit_trans = CashTransaction(self.get_draftboard_user())
            draftboard_deposit_trans.deposit(rake_post_overlay, trans=escrow_withdraw_trans.transaction)
            rake_transaction = escrow_withdraw_trans.transaction
        elif rake_post_overlay < 0:
            #
            # Take cash out of draftboard and deposit it into escrow
            rake_post_overlay = abs(rake_post_overlay)
            draftboard_withdraw_trans = CashTransaction(self.get_draftboard_user())
            draftboard_withdraw_trans.withdraw(rake_post_overlay)
            escrow_deposit_trans = CashTransaction(self.get_escrow_user())
            escrow_deposit_trans.deposit(rake_post_overlay, trans=draftboard_withdraw_trans.transaction)
            rake_transaction = draftboard_withdraw_trans.transaction

        # links the contest with the rake payout
        rake = Rake()
        rake.contest = contest
        rake.transaction = rake_transaction
        rake.save()

        contest.status = Contest.CLOSED
        contest.save()

    def __payout_spot(self, ranks_to_pay, entries_to_pay, contest):
        #
        # if there are the same number of ranks and entries to pay
        # and the ranks to pay are all equal, we can divide evenly
        if (self.array_objects_are_equal(ranks_to_pay) and len(ranks_to_pay) == len(entries_to_pay)) or len(
                entries_to_pay) == 1:
            place = ranks_to_pay[0].rank
            for i in range(0, len(ranks_to_pay)):
                rank = ranks_to_pay[i]
                entry = entries_to_pay[i]
                self.__update_accounts(place, contest, entry, rank.amount.get_cash_value())

        #
        # We need to convert the rank amount to a cash value to payout
        else:
            place = ranks_to_pay[0].rank
            cash_to_chop = decimal.Decimal(0.0)
            logger.info('ranks to pay: %s' % ranks_to_pay)
            for rank in ranks_to_pay:
                cash_to_chop += decimal.Decimal(rank.amount.get_cash_value())
            share_split_pre_rounded = ((cash_to_chop / decimal.Decimal(len(entries_to_pay))) - decimal.Decimal(.005))
            share_split_pre_rounded = round(share_split_pre_rounded, 3)
            share_split = round(share_split_pre_rounded, 2)

            #
            # The extra free pennies that could not be divided
            extra_pennies = cash_to_chop - (share_split * len(entries_to_pay))
            if extra_pennies < 0:
                extra_pennies = 0
            #
            # Gives the first person in the array the extra pennies that could not
            # be divided

            for entry in entries_to_pay:
                self.__update_accounts(place, contest, entry, share_split + extra_pennies)
                if extra_pennies > 0:
                    extra_pennies = 0

    def __update_accounts(self, place, contest, entry, amount):
        """
        Updates the accounts for Payout, FPP, Bonus, and Rake


        This gets run on each contest entry once the contest is finished.
         It:
            1. Withdraws the payout amount from escrow's account.
            2. Deposits that amount into the entry owner's account.
            3. Pays out any Frequent Player Points earned.
            4.


        :param place:
        :param contest:
        :param entry:
        :param amount:
        :return:
        """
        payout = Payout()
        payout.rank = place
        payout.contest = contest
        payout.entry = entry
        tm = CashTransaction(entry.lineup.user)
        tm.deposit(amount)
        #
        # Take cash out of escrow
        ct = CashTransaction(self.get_escrow_user())
        ct.withdraw(amount, tm.transaction)

        payout.transaction = tm.transaction
        payout.save()

        user = payout.entry.lineup.user
        rake_paid = contest.buyin * .10

        #
        # Pays out FPP
        lsm = LoyaltyStatusManager(user)
        fppt = FppTransaction(user)
        # rake * base loyalty multiplier * the multiplier
        fppt.deposit(
            (rake_paid * lsm.BASE_LOYALTY_MULTIPLIER) * lsm.get_fpp_multiplier(),
            trans=ct.transaction
        )
        fpp = FPP()
        fpp.contest = contest
        fpp.transaction = ct.transaction
        fpp.save()

        #
        # convert the bonus_cash for the user
        self.__convert_bonus_cash(user, rake_paid, payout.transaction)

        #
        # Create a rake transaction for the user
        rpt = RakepaidTransaction(user)
        rpt.deposit(rake_paid, trans=payout.transaction)

        msg = "User[" + payout.entry.lineup.user.username + "] was ranked #" + str(
            payout.rank) + " for contest #" + str(payout.contest.pk) + " and was paid out."
        Logger.log(ErrorCodes.INFO, "Contest Payout", msg)

    def __convert_bonus_cash(self, user, rake_paid, transaction):
        """
        Creates the conversion from bonus cash to real cash
        based on the rake_paid for the given entry
        :param user:
        :param rake_paid:
        """
        bct = BonusCashTransaction(user)
        balance = bct.get_balance_amount()

        #
        #  Create the conversion if there is a balance
        # to the user's bonus cash account
        if balance > 0:
            #
            # get the conversion amount based on rake paid
            amount = rake_paid * settings.BONUS_CASH_RAKE_PERCENTAGE

            #
            # round to the nearest cent
            val = math.floor(amount * 100)
            amount = val / 100.0

            #
            # if the amount is greater than the balance make the
            # amount the balance
            if balance < amount:
                amount = balance
            #
            # create the withdraw from the bonus cash
            bct.withdraw(amount, transaction)

            #
            # create the deposit from the bonus cash
            ct = CashTransaction(user)
            ct.deposit(amount, trans=bct.transaction)

    def array_objects_are_equal(self, arr):
        prev = None
        for obj in arr:
            if prev is None:
                prev = obj

            elif prev != obj:
                return False

        return True
