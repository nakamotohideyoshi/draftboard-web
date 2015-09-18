#
# contest/buyin/tests.py

from test.classes import AbstractTest
from contest.models import Contest
from prize.classes import CashPrizeStructureCreator, TicketPrizeStructureCreator
from lineup.models import Lineup
from .classes import PayoutManager
from .models import Payout
from test.classes import BuildWorldForTesting
from contest.buyin.classes import BuyinManager
from cash.classes import CashTransaction
from ticket.classes import TicketManager

class PayoutTest(AbstractTest):

    def setUp(self):
        # creates very standard ticket amounts like 1,2,5, 10, 20, 50
        TicketManager.create_default_ticket_amounts(verbose=False)

        self.first = 10.0
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

    def create_simple_teams(self):
        #
        # create Lineups
        max = 5
        for i in range(1,max):
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


    def create_last_place_tie_teams(self):
        #
        # create Lineups
        max = 6
        for i in range(1,max):
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


    def test_simple_payout(self):
        self.create_simple_teams()
        pm = PayoutManager()
        pm.payout()
        payouts = Payout.objects.order_by('contest', '-rank')
        for payout in payouts:
            self.assertEqual(str(payout.rank), payout.entry.lineup.user.username)


    def test_simple_tie_payout(self):
        self.create_last_place_tie_teams()
        pm = PayoutManager()
        pm.payout()
        payouts = Payout.objects.order_by('contest', '-rank')
        for payout in payouts:
            if payout.entry.lineup.user.username == str(4):
                self.assertEqual(payout.rank, 3)
            else:
                self.assertEqual(str(payout.rank), payout.entry.lineup.user.username)


    def test_simple_ticket_payout(self):
        #self.create_ticket_contest()
        self.create_simple_teams()
        pm = PayoutManager()
        pm.payout()
        payouts = Payout.objects.order_by('contest', '-rank')
        for payout in payouts:
            self.assertEqual(str(payout.rank), payout.entry.lineup.user.username)


    def test_simple_ticket_payout_tie(self):
        #self.create_ticket_contest()
        self.create_last_place_tie_teams()
        pm = PayoutManager()
        pm.payout()
        payouts = Payout.objects.order_by('contest', '-rank')
        for payout in payouts:
            if payout.entry.lineup.user.username == str(4):
                self.assertEqual(payout.rank, 3)
            else:
                self.assertEqual(str(payout.rank), payout.entry.lineup.user.username)


    def validate_side_effects_of_transaction(self):
        #TODO test rake paid shows up

        #TODO test Bonus cash conversion on accounts that have bonus cash
        #   and ones that dont
        pass