#
# contest/buyin/tests.py

import decimal
from test.classes import (
    BuildWorldForTesting,
    AbstractTest,
    TestSalaryScoreSystem,
)
from contest.models import Contest
from prize.classes import CashPrizeStructureCreator, TicketPrizeStructureCreator
from lineup.models import Lineup
from .classes import PayoutManager
from .models import Payout
from contest.buyin.classes import BuyinManager
from cash.classes import CashTransaction
from ticket.classes import TicketManager
from contest.payout.models import Rake, FPP
from fpp.classes import FppTransaction
from mysite.classes import  AbstractManagerClass
from promocode.bonuscash.classes import BonusCashTransaction
from cash.models import CashTransactionDetail

class PayoutTest(AbstractTest):

    def setUp(self):
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
        cps.set_buyin( 10 )
        cps.save()
        self.prize_structure = cps.prize_structure
        self.prize_structure.generator.prize_pool = 54.0 # minus rake
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
        for i in range(1,max+1):
            user = self.get_user(username=str(i))

            self.fund_user_account(user)

            lineup = Lineup()
            lineup.fantasy_points = max - i
            lineup.user = self.get_user(username=str(i))
            lineup.draft_group = self.draftgroup
            lineup.save()

            bm = BuyinManager(lineup.user)
            bm.buyin(self.contest, lineup)

        self.contest.status = Contest.COMPLETED
        self.contest.save()

    def create_simple_teams_all_tie(self, max=6):
        #
        # create Lineups
        for i in range(1,max+1):
            user = self.get_user(username=str(i))

            self.fund_user_account(user)

            lineup = Lineup()
            lineup.fantasy_points =1
            lineup.user = self.get_user(username=str(i))
            lineup.draft_group = self.draftgroup
            lineup.save()

            bm = BuyinManager(lineup.user)
            bm.buyin(self.contest, lineup)

        self.contest.status = Contest.COMPLETED
        self.contest.save()


    def create_last_place_tie_teams(self):
        #
        # create Lineups
        max = 6
        for i in range(1,max+1):
            user = self.get_user(username=str(i))
            self.fund_user_account(user)

            lineup = Lineup()
            if i ==3 or i == 4:
                lineup.fantasy_points = max -3
            else:
                lineup.fantasy_points = max -i

            lineup.user = user
            lineup.draft_group = self.draftgroup
            lineup.save()


            bm = BuyinManager(lineup.user)
            bm.buyin(self.contest, lineup)

        self.contest.status = Contest.COMPLETED
        self.contest.save()

    def create_last_place_tie_teams_three_way(self):
        """
        create Lineups such that there is a 3 way tie amongst the last 3 ranks.
        """

        max = 6
        tie_amount = 10.0
        for i in range(1, max+1):
            user = self.get_user(username=str(i))
            self.fund_user_account(user)

            lineup = Lineup()
            if  i <= 3:
                # for 1, 2, 3
                lineup.test_fantasy_points = tie_amount
            else:
                # teams 4, 5, 6 should have unique test_fantasy_points
                lineup.test_fantasy_points = tie_amount + i

            lineup.user = user
            lineup.draft_group = self.draftgroup
            lineup.save()

            bm = BuyinManager(lineup.user)
            bm.buyin(self.contest, lineup)

        self.contest.status = Contest.COMPLETED
        self.contest.save()

    def __create_lineups_with_fantasy_points(self, contest, lineup_points=[]):
        """
        contest is the contest to associate lineups with
        lineup_points is an array of the points to give to the lineups in creation order.
        """

        max = contest.entries
        for i in range(1, max+1):
            # get the user for the lineup
            user = self.get_user(username=str(i))
            self.fund_user_account(user)

            # set the rest of the lineup properties
            lineup = Lineup()
            lineup.fantasy_points   = lineup_points[i-1]
            lineup.user             = user
            lineup.draft_group      = self.draftgroup
            lineup.save()

            # buy this lineup into the contest
            bm = BuyinManager(lineup.user)
            bm.buyin(self.contest, lineup)

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
        #self.create_ticket_contest()
        self.create_simple_teams()
        pm = PayoutManager()
        pm.payout(finalize_score=False)
        payouts = Payout.objects.order_by('contest', '-rank')
        for payout in payouts:
            self.assertEqual(str(payout.rank), payout.entry.lineup.user.username)
        self.validate_side_effects_of_transaction()

    def test_simple_ticket_payout_tie(self):
        #self.create_ticket_contest()
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

    def test_complex_tie_payout(self):
        #
        lineup_points   = [10,10,10,10,11,12]
        lineup_ranks    = [3, 3, 3, 3, 2, 1]
        self.__create_lineups_with_fantasy_points(self.contest, lineup_points=lineup_points)
        pm = PayoutManager()
        pm.payout(finalize_score=False)
        # ranked descending because of order or lineup_points/lineup_ranks
        payouts = Payout.objects.order_by('contest', '-rank')
        i = 0
        for payout in payouts:
            self.assertEquals(payout.rank, lineup_ranks[i])
            i += 1
        self.validate_side_effects_of_transaction()

    def test_complex_tie_payout_2(self):
        #
        lineup_points   = [9, 10,10,10,11,12]
        lineup_ranks    = [6, 3, 3, 3, 2, 1]
        #
        # this test doesnt set the rank of the last spot ... (or does it... just not in the payout!)
        # (Rank:3, $3.34, fp:10.00) | 2 | test_contest (pk: 1) rank:3   should be lineup_rank[3]:6
        # (Rank:3, $3.33, fp:10.00) | 3 | test_contest (pk: 1) rank:3   should be lineup_rank[3]:3
        # (Rank:3, $3.33, fp:10.00) | 4 | test_contest (pk: 1) rank:3   should be lineup_rank[3]:3
        # (Rank:2, $10.00, fp:11.00) | 5 | test_contest (pk: 1) rank:2   should be lineup_rank[2]:3
        # (Rank:1, $34.00, fp:12.00) | 6 | test_contest (pk: 1) rank:1   should be lineup_rank[1]:2
        # F
        # ======================================================================
        # FAIL: test_complex_tie_payout_2 (contest.payout.tests.PayoutTest)
        # ----------------------------------------------------------------------
        # Traceback (most recent call last):
        #   File "/vagrant/contest/payout/tests.py", line 274, in test_complex_tie_payout_2
        #     self.assertEquals(payout.rank, lineup_ranks[i])
        # AssertionError: 3 != 6
        #
        # ----------------------------------------------------------------------
        # Ran 1 test in 1.902s
        #
        # FAILED (failures=1)

        self.__create_lineups_with_fantasy_points(self.contest, lineup_points=lineup_points)
        pm = PayoutManager()
        pm.payout(finalize_score=False)
        # ranked descending because of order or lineup_points/lineup_ranks
        payouts = Payout.objects.order_by('contest', '-rank')
        i = 0
        for payout in payouts:
            print(str(payout), 'rank:%s' % payout.rank, '  should be lineup_rank[%s]:%s' % (str(payout.rank), str(lineup_ranks[i])) )
            i += 1
        i = 0
        for payout in payouts:
            #print(str(payout), 'rank:%s' % payout.rank, '  should be lineup_rank[%s]:%s' % (str(payout.rank), str(lineup_ranks[i])) )
            self.assertEquals(payout.rank, lineup_ranks[i])
            i += 1
        self.validate_side_effects_of_transaction()

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

        cps.set_buyin( 1.0 )
        cps.save()
        self.prize_structure = cps.prize_structure
        self.prize_structure.generator.prize_pool = 1.8 # minus rake
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
            trans = CashTransactionDetail.objects.get(transaction=payout.transaction, user=payout.user)
            self.assertAlmostEqual(trans.amount, decimal.Decimal(.90))

    def validate_escrow_is_zero(self):
        ct = CashTransaction(AbstractManagerClass.get_escrow_user())
        ct.get_balance_amount()
        self.assertEqual(ct.get_balance_amount(), decimal.Decimal(0.0))

    def validate_fpp(self):
        payouts = Payout.objects.order_by('contest', '-rank')
        for payout in payouts:
            fpp = FPP.objects.get(transaction=payout.transaction, contest=self.contest)
            fppt= FppTransaction(payout.transaction.user)
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

