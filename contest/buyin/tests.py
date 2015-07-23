#
# contest/buyin/tests.py
from test.classes import AbstractTest
from salary.dummy import Dummy
from prize.classes import CashPrizeStructureCreator, TicketPrizeStructureCreator
from django.utils import timezone
from datetime import timedelta
from datetime import time
from dataden.util.timestamp import DfsDateTimeUtil
from ..classes import ContestCreator
from ..models import Contest
from .classes import BuyinManager
class BuyinTest(AbstractTest):
    def setUp(self):
        Dummy.generate_salaries()
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
        now = timezone.now()
        start = DfsDateTimeUtil.create(now.date(), time(23,0))
        end = DfsDateTimeUtil.create(now.date() + timedelta(days=1), time(0,0))
        cc= ContestCreator("test_contest", "nfl", self.prize_structure, start, end)
        self.contest = cc.create()
        self.contest.status = Contest.COMPLETED
        self.contest.save()



    def test_simple_buyin(self):
        bm = BuyinManager(self.get_basic_user())
        bm.buyin(self.contest)

