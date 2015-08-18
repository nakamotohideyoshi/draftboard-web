#
# contest/buyin/tests.py
from test.classes import AbstractTest, AbstractTestTransaction
from salary.dummy import Dummy
from prize.classes import CashPrizeStructureCreator
from ticket.classes import TicketManager
from django.utils import timezone
from datetime import timedelta
from datetime import time
from dataden.util.timestamp import DfsDateTimeUtil
from ..classes import ContestCreator
from ..models import Contest
from .classes import BuyinManager
from cash.classes import CashTransaction
from contest import exceptions
import mysite.exceptions
from lineup.models import Lineup
from ticket.models import TicketAmount
from draftgroup.models import DraftGroup
from lineup.exceptions import LineupDoesNotMatchUser
from .tasks import buyin_task
from django.test.utils import override_settings

class BuyinTest(AbstractTest):
    """
    create a basic contest, and use the BuyinManager to buy into it.
    """

    def setUp(self):

        TicketManager.create_default_ticket_amounts(verbose=False)

        self.user = self.get_basic_user()
        ct = CashTransaction(self.user)
        ct.deposit(100)

        salary_generator = Dummy.generate_salaries()
        self.salary_pool = salary_generator.pool
        self.first = 100.0
        self.second = 50.0
        self.third = 25.0

        #
        # create a simple Rank and Prize Structure
        self.buyin =10
        cps = CashPrizeStructureCreator(name='test')
        cps.add(1, self.first)
        cps.add(2, self.second)
        cps.add(3, self.third)
        cps.save()
        cps.prize_structure.buyin = self.buyin
        cps.prize_structure.save()

        self.prize_structure = cps.prize_structure
        self.ranks = cps.ranks

        #
        # create the Contest
        now = timezone.now()
        start = DfsDateTimeUtil.create(now.date(), time(23,0))
        end = DfsDateTimeUtil.create(now.date() + timedelta(days=1), time(0,0))
        cc= ContestCreator("test_contest", "nfl", self.prize_structure, start, end)
        self.contest = cc.create()
        self.contest.status = Contest.RESERVABLE
        self.contest.save()

        self.draftgroup = DraftGroup()
        self.draftgroup.salary_pool = self.salary_pool
        self.draftgroup.start = start
        self.draftgroup.end = end
        self.draftgroup.save()

    def test_incorrect_contest_type(self):
        bm = BuyinManager(self.user)
        self.assertRaises(mysite.exceptions.IncorrectVariableTypeException,
                          lambda: bm.buyin(0))

    def test_incorrect_lineup_type(self):
        bm = BuyinManager(self.user)
        self.assertRaises(mysite.exceptions.IncorrectVariableTypeException,
                          lambda: bm.buyin(self.contest, 0))

    def test_simple_buyin(self):
        bm = BuyinManager(self.user)
        bm.buyin(self.contest)

    def test_simple_ticket_buyin(self):
        tm = TicketManager(self.user)
        try:
            tm.get_ticket_amount(self.buyin)

        except Exception:
            ta = TicketAmount()
            ta.amount = self.buyin
            ta.save()
        tm.deposit(amount=self.buyin)
        bm = BuyinManager(self.user)
        bm.buyin(self.contest)
        tm.ticket.refresh_from_db()
        self.assertEqual((tm.ticket.consume_transaction is not None), True)

    def test_lineup_no_contest_draft_group(self):
        lineup = Lineup()
        lineup.draft_group = self.draft_group
        lineup.user = self.user
        bm = BuyinManager(self.user)
        self.assertRaises(exceptions.ContestIsNotAcceptingLineupsException,
                  lambda: bm.buyin(self.contest, lineup))

    def test_lineup_share_draft_group(self):
        draftgroup2 = DraftGroup()
        draftgroup2.salary_pool = self.salary_pool
        draftgroup2.start = self.contest.start
        draftgroup2.end = self.contest.end
        draftgroup2.save()

        lineup = Lineup()
        lineup.draft_group = self.draftgroup
        lineup.user = self.user

        self.contest.draft_group = draftgroup2
        self.contest.save()

        bm = BuyinManager(self.user)
        self.assertRaises(exceptions.ContestLineupMismatchedDraftGroupsException,
                  lambda: bm.buyin(self.contest, lineup))

    def test_contest_full(self):
        self.contest.entries = 3
        self.contest.current_entries = 3
        self.contest.save()
        bm = BuyinManager(self.user)
        self.assertRaises(exceptions.ContestIsFullException,
                  lambda: bm.buyin(self.contest))

    def test_contest_is_in_progress(self):
        self.contest.status = self.contest.INPROGRESS
        self.contest.save()
        self.should_raise_contest_is_in_progress_or_closed_exception()

    def test_contest_is_cancelled(self):
        self.contest.status = self.contest.CANCELLED
        self.contest.save()
        self.should_raise_contest_is_in_progress_or_closed_exception()

    def test_contest_is_closed(self):
        self.contest.status = self.contest.CLOSED
        self.contest.save()
        self.should_raise_contest_is_in_progress_or_closed_exception()

    def test_contest_is_completed(self):
        self.contest.status = self.contest.COMPLETED
        self.contest.save()
        self.should_raise_contest_is_in_progress_or_closed_exception()

    def should_raise_contest_is_in_progress_or_closed_exception(self):
        bm = BuyinManager(self.user)
        self.assertRaises(exceptions.ContestIsInProgressOrClosedException,
                  lambda: bm.buyin(self.contest))

    def test_user_owns_lineup(self):
        lineup = Lineup()
        lineup.draft_group = self.draftgroup
        lineup.user = self.get_admin_user()

        self.contest.draft_group =self.draftgroup
        self.contest.save()

        bm = BuyinManager(self.user)
        self.assertRaises(LineupDoesNotMatchUser,
                  lambda: bm.buyin(self.contest, lineup))

    def test_user_submits_past_max_entries(self):
        self.contest.max_entries = 1
        self.contest.entries = 3
        self.contest.save()

        bm = BuyinManager(self.user)
        bm.buyin(self.contest)

        bm = BuyinManager(self.user)
        self.assertRaises(exceptions.ContestMaxEntriesReachedException,
                  lambda: bm.buyin(self.contest))


class BuyinRaceTest(AbstractTestTransaction):

    def setUp(self):

        self.user = self.get_basic_user()
        ct = CashTransaction(self.user)
        ct.deposit(100)

        salary_generator = Dummy.generate_salaries()
        self.salary_pool = salary_generator.pool
        self.first = 100.0
        self.second = 50.0
        self.third = 25.0

        #
        # create a simple Rank and Prize Structure
        self.buyin =10
        cps = CashPrizeStructureCreator(name='test')
        cps.add(1, self.first)
        cps.add(2, self.second)
        cps.add(3, self.third)
        cps.save()
        cps.prize_structure.buyin = self.buyin
        cps.prize_structure.save()

        self.prize_structure = cps.prize_structure
        self.ranks = cps.ranks

        #
        # create the Contest
        now = timezone.now()
        start = DfsDateTimeUtil.create(now.date(), time(23,0))
        end = DfsDateTimeUtil.create(now.date() + timedelta(days=1), time(0,0))
        cc= ContestCreator("test_contest", "nfl", self.prize_structure, start, end)
        self.contest = cc.create()
        self.contest.status = Contest.RESERVABLE
        self.contest.save()

        self.draftgroup = DraftGroup()
        self.draftgroup.salary_pool = self.salary_pool
        self.draftgroup.start = start
        self.draftgroup.end = end
        self.draftgroup.save()

    @override_settings(TEST_RUNNER=BuyinTest.CELERY_TEST_RUNNER,
                       CELERY_ALWAYS_EAGER=True,
                       CELERYD_CONCURRENCY=3)
    def test_race_condition_to_fill_last_spot_of_contest(self):
        self.contest.max_entries = 3
        self.contest.entries = 3
        self.contest.save()

        def run_now(self_obj):
            task = buyin_task.delay(self_obj.user, self_obj.contest)
            self.assertTrue(task.successful())

        self.concurrent_test(3, run_now, self)
        ct = CashTransaction(self.user)

        self.assertEqual(70, ct.get_balance_amount())
