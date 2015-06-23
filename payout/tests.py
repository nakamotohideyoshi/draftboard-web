from django.test import TestCase
from test.classes import AbstractTest
from contest.models import Contest, Entry
from prize.classes import CashPrizeStructureCreator
from lineup.models import Lineup
from .classes import PayoutManager
from .models import Payout
class PayoutTest(AbstractTest):
    def setUp(self):
        self.first = 100.0
        self.second = 50.0
        self.third = 25.0
        #
        # create a simple Rank and Prize Structure
        cps = CashPrizeStructureCreator(name='test')
        cps.add(1, self.first)
        cps.add(2, self.second)
        cps.add(3, self.third)
        cps.save()
        self.prize_structure = cps.prize_structure
        self.ranks = cps.ranks

        #
        # create the Contest
        self.contest = Contest()
        self.contest.status = Contest.COMPLETED
        self.contest.prize_structure = self.prize_structure
        self.contest.name = 'test_contest'
        self.contest.save()

    def create_simple_teams(self):
        #
        # create Lineups
        max = 5
        for i in range(1,max):
            lineup = Lineup()
            lineup.fantasy_points = max - i
            lineup.user = self.get_user(username=str(i))
            lineup.save()

            entry = Entry()
            entry.contest = self.contest
            entry.lineup = lineup
            entry.save()
    def create_last_place_tie_teams(self):
        #
        # create Lineups
        max = 6
        for i in range(1,max):
            lineup = Lineup()
            if i ==3 or i == 4:
                lineup.fantasy_points = max -3
            else:
                lineup.fantasy_points = max -i

            lineup.user = self.get_user(username=str(i))
            lineup.save()

            entry = Entry()
            entry.contest = self.contest
            entry.lineup = lineup
            entry.save()


    def test_simple_payout(self):
        self.create_simple_teams()
        pm = PayoutManager()
        pm.payout()
        payouts = Payout.objects.order_by('contest', '-rank')
        for payout in payouts:
            print("\n"+str(payout))


    def test_simple_tie_payout(self):
        self.create_last_place_tie_teams()
        pm = PayoutManager()
        pm.payout()
        payouts = Payout.objects.order_by('contest', '-rank')
        for payout in payouts:
            print("\n"+str(payout))