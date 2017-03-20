import decimal
from logging import getLogger

from model_mommy import mommy

from cash.classes import CashTransaction
from cash.models import CashTransactionDetail
from contest.buyin.classes import BuyinManager
from contest.buyin.models import Buyin
from contest.models import Contest, Entry
from contest.payout.models import Rake, FPP
from fpp.classes import FppTransaction
from lineup.models import Lineup
from mysite.classes import AbstractManagerClass
from prize.classes import CashPrizeStructureCreator, TicketPrizeStructureCreator
from promocode.bonuscash.classes import BonusCashTransaction
from test.classes import (
    BuildWorldForTesting,
    AbstractTest,
    TestSalaryScoreSystem,
)
from ticket.classes import TicketManager
from .classes import PayoutManager
from .classes import calculate_rake
from .models import Payout
from ..classes import ContestPoolCreator

logger = getLogger('contest.payout.tests')


class PayoutTest(AbstractTest):
    def setUp(self):
        super().setUp()
        # creates very standard ticket amounts like 1,2,5, 10, 20, 50
        TicketManager.create_default_ticket_amounts(verbose=False)

        self.first = 34.0
        self.second = 10.0
        self.third = 10.0
        #
        # create a simple Rank and Prize Structure
        cps = CashPrizeStructureCreator(name='test1')
        cps.add(1, self.first)
        cps.add(2, self.second)
        cps.add(3, self.third)
        cps.set_buyin(10)
        cps.save()
        self.prize_structure = cps.prize_structure
        self.prize_structure.generator.prize_pool = 54.0  # minus rake
        self.prize_structure.save()
        self.ranks = cps.ranks

        self.world = BuildWorldForTesting()
        self.world.build_world()
        self.draftgroup = self.world.draftgroup

        self.contest = self.world.contest
        self.contest.status = Contest.SCHEDULED
        self.contest.prize_structure = self.prize_structure
        self.contest.draft_group = self.draftgroup
        self.contest.entries = 6
        self.contest.save()

        self.contest_pool, created = ContestPoolCreator(
            'nfl',
            self.prize_structure,
            self.draftgroup.start,
            (self.draftgroup.end - self.draftgroup.start).seconds * 60,
            self.draftgroup
        ).get_or_create()
        self.contest_pool.entries = 6
        self.contest_pool.save()
        self.scorer_class = TestSalaryScoreSystem

    def create_ticket_contest(self):
        #
        # Contest where the top 3 players get paid the value of self.third as a ticket
        # value.
        # ta, created = TicketAmount.objects.get_or_create( amount = self.third )

        tps = TicketPrizeStructureCreator(self.third, 3, "ticket_prize")
        tps.save()
        self.prize_structure = tps.prize_structure
        self.prize_structure.buyin = self.third
        self.ranks = tps.ranks
        self.contest.prize_structure = self.prize_structure
        self.contest.save()

    def fund_user_account(self, user):
        ct = CashTransaction(user)
        ct.deposit(100)

    def create_simple_teams(self, max=6):
        #
        # create Lineups
        for i in range(1, max + 1):
            user = self.get_user(username=str(i))

            self.fund_user_account(user)

            lineup = Lineup()
            lineup.fantasy_points = max - i
            lineup.user = self.get_user(username=str(i))
            lineup.draft_group = self.draftgroup
            lineup.save()

            bm = BuyinManager(lineup.user)
            bm.buyin(self.contest_pool, lineup)
        Entry.objects.filter(contest_pool=self.contest_pool).update(contest=self.contest)
        self.contest.status = Contest.COMPLETED
        self.contest.save()

    def create_simple_teams_all_tie(self, max=6):
        #
        # create Lineups
        for i in range(1, max + 1):
            user = self.get_user(username=str(i))

            self.fund_user_account(user)

            lineup = Lineup()
            lineup.fantasy_points = 1
            lineup.user = self.get_user(username=str(i))
            lineup.draft_group = self.draftgroup
            lineup.save()

            bm = BuyinManager(lineup.user)
            bm.buyin(self.contest_pool, lineup)
        Entry.objects.filter(contest_pool=self.contest_pool).update(contest=self.contest)
        self.contest.status = Contest.COMPLETED
        self.contest.save()

    def create_last_place_tie_teams(self):
        #
        # create Lineups
        max = 6
        for i in range(1, max + 1):
            user = self.get_user(username=str(i))
            self.fund_user_account(user)

            lineup = Lineup()
            if i == 3 or i == 4:
                lineup.fantasy_points = max - 3
            else:
                lineup.fantasy_points = max - i

            lineup.user = user
            lineup.draft_group = self.draftgroup
            lineup.save()

            bm = BuyinManager(lineup.user)
            bm.buyin(self.contest_pool, lineup)
        Entry.objects.filter(contest_pool=self.contest_pool).update(contest=self.contest)
        self.contest.status = Contest.COMPLETED
        self.contest.save()

    def create_last_place_tie_teams_three_way(self):
        """
        create Lineups such that there is a 3 way tie amongst the last 3 ranks.
        """

        max = 6
        tie_amount = 10.0
        for i in range(1, max + 1):
            user = self.get_user(username=str(i))
            self.fund_user_account(user)

            lineup = Lineup()
            if i <= 3:
                # for 1, 2, 3
                lineup.test_fantasy_points = tie_amount
            else:
                # teams 4, 5, 6 should have unique test_fantasy_points
                lineup.test_fantasy_points = tie_amount + i

            lineup.user = user
            lineup.draft_group = self.draftgroup
            lineup.save()

            bm = BuyinManager(lineup.user)
            bm.buyin(self.contest_pool, lineup)
        Entry.objects.filter(contest_pool=self.contest_pool).update(contest=self.contest)
        self.contest.status = Contest.COMPLETED
        self.contest.save()

    def __create_lineups_with_fantasy_points(self, contest_pool, lineup_points=[]):
        """
        contest is the contest to associate lineups with
        lineup_points is an array of the points to give to the lineups in creation order.
        """

        max = contest_pool.entries
        for i in range(1, max + 1):
            # get the user for the lineup
            user = self.get_user(username=str(i))
            self.fund_user_account(user)

            # set the rest of the lineup properties
            lineup = Lineup()
            lineup.fantasy_points = lineup_points[i - 1]
            lineup.user = user
            lineup.draft_group = self.draftgroup
            lineup.save()

            # buy this lineup into the contest
            bm = BuyinManager(lineup.user)
            bm.buyin(self.contest_pool, lineup)
        Entry.objects.filter(contest_pool=self.contest_pool).update(contest=self.contest)
        # set the contest as payout-able
        self.contest.status = Contest.COMPLETED
        self.contest.save()

    def test_simple_payout(self):
        self.create_simple_teams()
        pm = PayoutManager()
        pm.payout(finalize_score=False)
        payouts = Payout.objects.order_by('contest', '-rank')
        for payout in payouts:
            self.assertEqual(str(payout.rank), payout.entry.lineup.user.username)
        self.validate_side_effects_of_transaction()

    def test_simple_tie_payout(self):
        self.create_last_place_tie_teams()
        pm = PayoutManager()
        pm.payout(finalize_score=False)
        payouts = Payout.objects.order_by('contest', '-rank')
        for payout in payouts:
            if payout.entry.lineup.user.username == str(4):
                self.assertEqual(payout.rank, 3)
            else:
                self.assertEqual(str(payout.rank), payout.entry.lineup.user.username)
        self.validate_side_effects_of_transaction()

    def test_simple_ticket_payout(self):
        self.create_simple_teams()
        pm = PayoutManager()
        pm.payout(finalize_score=False)
        payouts = Payout.objects.order_by('contest', '-rank')
        for payout in payouts:
            self.assertEqual(str(payout.rank), payout.entry.lineup.user.username)
        self.validate_side_effects_of_transaction()

    def test_simple_ticket_payout_tie(self):
        self.create_last_place_tie_teams()
        pm = PayoutManager()
        pm.payout(finalize_score=False)
        payouts = Payout.objects.order_by('contest', '-rank')
        for payout in payouts:
            if payout.entry.lineup.user.username == str(4):
                self.assertEqual(payout.rank, 3)
            else:
                self.assertEqual(str(payout.rank), payout.entry.lineup.user.username)
        self.validate_side_effects_of_transaction()

    def __run_payouts(self, lineup_points, lineup_ranks, payout_ranks):
        """
        helper method that a) creates lineups with the points in 'lineup_points',
         b) does payouts, c) ensures all the ranks are set as expected
         based on the ranks in lineup_ranks and payout_ranks

        example of valid params:

            lineup_points   = [9, 10,10,10,11,12]
            lineup_ranks    = [6, 3, 3, 3, 2, 1]
            payout_ranks    = [   3, 3, 3, 2, 1]    # only 5 spots paid (of the 6)

        :param lineup_points:
        :param lineup_ranks:
        :param payout_ranks:
        :return:
        """
        self.__create_lineups_with_fantasy_points(self.contest_pool, lineup_points=lineup_points)
        pm = PayoutManager()
        pm.payout(finalize_score=False)

        # test payout ranks
        payouts = Payout.objects.order_by('contest', '-rank')
        i = 0
        for payout in payouts:
            msg = str(payout), 'rank:%s' % payout.rank, '  should be payout_ranks[%s]:%s' % (
                str(payout.rank), str(payout_ranks[i]))
            logger.info(msg)
            i += 1
        i = 0
        for payout in payouts:
            # print(str(payout), 'rank:%s' % payout.rank, '  should be lineup_rank[%s]:%s' % (str(payout.rank), str(lineup_ranks[i])) )
            self.assertEquals(payout.rank, payout_ranks[i])
            i += 1

        # test Entry ranks (each distinct buyin)
        lineups = Lineup.objects.order_by('fantasy_points')  # ascending
        i = 0
        for lineup in lineups:
            for entry in Entry.objects.filter(lineup=lineup):
                msg = ('    ', str(entry), 'entry.final_rank:', entry.final_rank,
                       '  should be entry rank:', lineup_ranks[i])
                logger.info(msg)
                self.assertEquals(entry.final_rank, lineup_ranks[i])
                i += 1

        self.validate_side_effects_of_transaction()

    def test_complex_tie_payout(self):
        # all spots paid, tie thru the last payout spot
        lineup_points = [10, 10, 10, 10, 11, 12]
        lineup_ranks = [3, 3, 3, 3, 2, 1]
        payout_ranks = [3, 3, 3, 3, 2, 1]  # note: there may be fewer Payouts than ranks
        self.__run_payouts(lineup_points, lineup_ranks, payout_ranks)

    def test_complex_tie_payout_2(self):
        # last place not paid (rank 6), tie thru bubble, (although 1st and 2nd unique payouts)
        lineup_points = [9, 10, 10, 10, 11, 12]
        lineup_ranks = [6, 3, 3, 3, 2, 1]
        payout_ranks = [3, 3, 3, 2, 1]  # only 5 spots paid (of the 6)
        self.__run_payouts(lineup_points, lineup_ranks, payout_ranks)

    def test_overlay(self):
        self.create_simple_teams(5)
        pm = PayoutManager()
        pm.payout(finalize_score=False)
        rake = Rake.objects.get(contest=self.contest)
        self.assertEqual(rake.amount, decimal.Decimal(-4.0))
        self.validate_escrow_is_zero()
        self.validate_fpp()

    def test_h2h_tie(self):
        self.first = 1.8

        #
        # create a simple Rank and Prize Structure
        cps = CashPrizeStructureCreator(name='test1')
        cps.add(1, self.first)

        cps.set_buyin(1.0)
        cps.save()
        self.prize_structure = cps.prize_structure
        self.prize_structure.generator.prize_pool = 1.8  # minus rake
        self.prize_structure.save()
        self.ranks = cps.ranks

        self.contest.status = Contest.SCHEDULED
        self.contest.prize_structure = self.prize_structure
        self.contest.draft_group = self.draftgroup
        self.contest.entries = 2
        self.contest.save()

        self.create_simple_teams_all_tie(2)
        pm = PayoutManager()
        pm.payout(finalize_score=False)
        payouts = Payout.objects.order_by('contest', '-rank')
        for payout in payouts:
            self.assertEqual(payout.rank, 1)
            trans = CashTransactionDetail.objects.get(transaction=payout.transaction,
                                                      user=payout.user)
            self.assertAlmostEqual(trans.amount, decimal.Decimal(.90))

    def validate_escrow_is_zero(self):
        ct = CashTransaction(AbstractManagerClass.get_escrow_user())
        ct.get_balance_amount()
        self.assertEqual(ct.get_balance_amount(), decimal.Decimal(0.0))

    def validate_fpp(self):
        payouts = Payout.objects.order_by('contest', '-rank')
        for payout in payouts:
            fpp = FPP.objects.get(transaction=payout.transaction, contest=self.contest)
            fppt = FppTransaction(payout.transaction.user)
            self.assertEqual(fppt.get_balance_amount(), decimal.Decimal(10.0))

    def test_bonus_cash_conversion(self):
        self.create_simple_teams(5)
        user = self.get_user(username="1")
        bct = BonusCashTransaction(user)
        bct.deposit(50.0)
        pm = PayoutManager()
        pm.payout(finalize_score=False)
        bct = BonusCashTransaction(user)
        self.assertAlmostEqual(decimal.Decimal(49.60), bct.get_balance_amount())

    def validate_side_effects_of_transaction(self):
        rake = Rake.objects.get(contest=self.contest)
        self.assertEqual(rake.amount, decimal.Decimal(6.0))
        self.validate_escrow_is_zero()
        self.validate_fpp()

    @staticmethod
    def createUserEntries(contest, user_id, quantity=1):
        entries = mommy.make(
            Entry,
            _quantity=quantity,
            contest=contest,
            user__id=user_id,
            make_m2m=True,
        )
        for entry in entries:
            mommy.make(Buyin, entry=entry)

    def test_calculate_rake_10_dollar_10_entry(self):
        from datetime import timedelta
        from django.utils import timezone

        # create a simple Rank and Prize Structure
        cps = CashPrizeStructureCreator(name='test1')
        cps.add(1, 20)
        cps.add(2, 10)
        cps.add(3, 5)
        cps.set_buyin(10)
        cps.save()
        prize_structure = cps.prize_structure
        # (10 entries * $10 buyin price - 10% rake fee)
        prize_structure.generator.prize_pool = 90.0
        prize_structure.save()
        # ranks = cps.ranks

        contest = mommy.make(
            Contest,
            entries=10,
            prize_structure=prize_structure,
            end=timezone.now() + timedelta(hours=1)
        )

        # 1 entry -- we took in 10 and paid out 20, net -10
        self.createUserEntries(contest, 1, 1)
        calculate_rake(contest)
        self.assertEqual(calculate_rake(contest), -10)

        # 2 entries -- we took in 20 and paid out 30, net -10
        self.createUserEntries(contest, 1, 1)
        calculate_rake(contest)
        self.assertEqual(calculate_rake(contest), -10)

        # 3 entries -- we took in 30 and paid out 35, net -5
        self.createUserEntries(contest, 1, 1)
        self.assertEqual(calculate_rake(contest), -5)

        # 4 entries -- took in 40, paid out 35, net 5
        self.createUserEntries(contest, 1, 1)
        self.assertEqual(calculate_rake(contest), 5)

        # 8 entries -- took in 80, paid out 35, net 45
        self.createUserEntries(contest, 1, 4)
        self.assertEqual(calculate_rake(contest), 45)

        # full contest, 10 entries -- took in 100, paid out 35, net 65
        self.createUserEntries(contest, 1, 2)
        self.assertEqual(calculate_rake(contest), 65)

    def test_calculate_rake_1_dollar_10_entry(self):
        from datetime import timedelta
        from django.utils import timezone

        # create a simple Rank and Prize Structure
        cps = CashPrizeStructureCreator(name='test1')
        cps.add(1, 4)
        cps.add(2, 3)
        cps.add(3, 2)
        cps.set_buyin(1)
        cps.save()
        prize_structure = cps.prize_structure
        # (10 entries * $10 buyin price - 10% rake fee)
        prize_structure.generator.prize_pool = 9
        prize_structure.save()
        # ranks = cps.ranks

        contest = mommy.make(
            Contest,
            entries=10,
            prize_structure=prize_structure,
            end=timezone.now() + timedelta(hours=1)
        )

        # 1 entry -- we took in 1 paid out 4, net -3
        self.createUserEntries(contest, 1, 1)
        calculate_rake(contest)
        self.assertEqual(calculate_rake(contest), -3)

        # 2 entries -- we took in 2 and paid out 7, net -5
        self.createUserEntries(contest, 1, 1)
        calculate_rake(contest)
        self.assertEqual(calculate_rake(contest), -5)

        # 3 entries -- we took in 3 and paid out 9, net -6
        self.createUserEntries(contest, 1, 1)
        self.assertEqual(calculate_rake(contest), -6)

        # 4 entries -- took in 4, paid out 9, net -5
        self.createUserEntries(contest, 1, 1)
        self.assertEqual(calculate_rake(contest), -5)

        # 8 entries -- took in 8, paid out 9, net -1
        self.createUserEntries(contest, 1, 4)
        self.assertEqual(calculate_rake(contest), -1)

        # full contest, 10 entries -- took in 10, paid out 9, net 1
        self.createUserEntries(contest, 1, 2)
        self.assertEqual(calculate_rake(contest), 1)
