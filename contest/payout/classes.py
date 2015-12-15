import mysite.exceptions
from contest.models import Contest, Entry
from prize.models import Rank
from django.db.models import Q
from transaction.models import  AbstractAmount
import mysite.exceptions
from transaction.classes import  CanDeposit
from .models import Payout, Rake, FPP
from cash.classes import CashTransaction
import decimal
from dfslog.classes import Logger, ErrorCodes
from cash.classes import CashTransaction
from django.db.transaction import atomic
from promocode.bonuscash.classes import BonusCashTransaction
from django.conf import settings
from rakepaid.classes import RakepaidTransaction
from mysite.classes import AbstractManagerClass
from rakepaid.classes import LoyaltyStatusManager
from fpp.classes import FppTransaction
import math

class PayoutManager(AbstractManagerClass):
    """
    Responsible for performing the payouts for all active contests for both
    cash and ticket games.
    """

    def __init__(self):
        pass

    def payout(self, contests=None):
        """
        Takes in an array of contests to payout. If there are not contests passed
        then the payout mechanism will look for all contests who have not been
        paid out yet and pay them out.
        :param contests: an array of :class:`contest.models.Contest` models
        """

        #
        # validation if the contests are passed as an argument
        if contests is not None:
            #
            # validate that contests is an array
            if not issubclass(contests, list):
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
        # find contests that have not been paid out yet that need
        # to be paid out
        else:
            #
            # gets all the contests that are not set to closed
            contests = Contest.objects.filter(~Q(status=Contest.CLOSED))

            #
            # update the status for all of the contests
            for contest in contests:
                # TODO - update_status() method has 1 line of code: "pass"
                contest.update_status()


            #
            # gets all the contests that are completed
            contests = Contest.objects.filter(status=Contest.COMPLETED)

        #
        # If there are contests left to payout, pay them out.
        for contest in contests:
            self.__payout_contest(contest)


    @atomic
    def __payout_contest(self, contest):
        """
        Method assumes the contest has never been paid out and is ready
        to be paid out. This is why the method is private and should be
        called from a separate method that does the individual error checking.
        """

        #
        # get the prize pool ranks for the contest
        ranks = Rank.objects.filter(prize_structure= contest.prize_structure)

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
                    type(self).__name,
                    'rank')

            #
            # Get the transaction class and verify that it can deposit
            transaction_class = rank.amount.get_transaction_class()
            if not issubclass(transaction_class, CanDeposit):
                raise mysite.exceptions.IncorrectVariableTypeException(
                    type(self).__name,
                    'transaction_class')


        #
        # perform the payouts by going through each entry and finding
        # ties and ranks for the ties to chop.
        i = 0
        while i < len(ranks):
            entries_to_pay = list()
            ranks_to_pay = list()
            entries_to_pay.append(entries[i])
            ranks_to_pay.append(ranks[i])
            score = entries[i].lineup.fantasy_points
            #
            # For each tie add the user to the list to chop the payment
            # and add the next payout to be split with the ties.
            while score == entries[i+1].lineup.fantasy_points:
                i += 1
                entries_to_pay.append(entries[i])
                if len(ranks) > i:
                    ranks_to_pay.append(ranks[i])

            self.__payout_spot(ranks_to_pay, entries_to_pay, contest)
            i += 1


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

        #
        # links the contest with the rake payout
        rake = Rake()
        rake.contest = contest
        rake.transaction = rake_transaction
        rake.save()

    def __payout_spot(self, ranks_to_pay, entries_to_pay, contest):
        #
        # if there are the same number of ranks and entries to pay
        # and the ranks to pay are all equal, we can divide evenly
        if (self.array_objects_are_equal(ranks_to_pay) and len(ranks_to_pay) == len(entries_to_pay)) or len(entries_to_pay) == 1:
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
            print(str(ranks_to_pay))
            for rank in ranks_to_pay:
                cash_to_chop += rank.amount.get_cash_value()


            share_split = round(((cash_to_chop/ len(entries_to_pay)) - decimal.Decimal(.005)), 2)

            #
            # The extra free pennies that could not be divided
            extra_pennies = cash_to_chop - (share_split*len(entries_to_pay))
            if extra_pennies < 0:
                extra_pennies = 0
            #
            # Gives the first person in the array the extra pennies that could not
            # be divided

            for entry in entries_to_pay:
                self.__update_accounts(place, contest, entry, share_split+ extra_pennies)
                if extra_pennies > 0:
                    extra_pennies = 0

    def __update_accounts(self, place, contest, entry, amount):
        """
        Updates the accounts for Payout,  FPP, Bonus, and Rake
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
        fppt.deposit((rake_paid * lsm.BASE_LOYALTY_MULTIPLIER) * lsm.get_fpp_multiplier(), trans=ct.transaction)
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

        msg = "User["+payout.entry.lineup.user.username+"] was ranked #"+str(payout.rank)+" for contest #"+str(payout.contest.pk)+" and was paid out."
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

