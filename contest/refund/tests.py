#
# contest/refunds/tests.py

from test.classes import AbstractTest
from test.models import PlayerChild
from test.classes import BuildWorldForTesting
import lineup.exceptions
from draftgroup.models import Player
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta, time
from django.utils import timezone
from django.test.utils import override_settings             # for testing celery
from contest.models import Entry
from .classes import RefundManager
from lineup.classes import LineupManager
from contest.buyin.classes import BuyinManager
from cash.classes import CashTransaction
from ticket.classes import TicketManager
from ticket.models import TicketAmount
from ..exceptions import (
    ContestIsInProgressOrClosedException,
    ContestCanNotBeRefunded,
)
from .tasks import refund_task
from ..classes import ContestPoolCreator


class RefundBuildWorldMixin(object):

    def build_world(self):
        TicketManager.create_default_ticket_amounts()
        self.world = BuildWorldForTesting()
        self.world.build_world()
        self.world.contest.entries =3
        self.contest = self.world.contest
        draftgroup = self.world.draftgroup
        self.contest_pool, created = ContestPoolCreator(
            'nfl',
            self.contest.prize_structure,
            draftgroup.start,
            (draftgroup.end - draftgroup.start).seconds * 60,
            draftgroup
        ).get_or_create()
        # self.user1 = self.get_basic_user("test1")
        # self.user2 = self.get_basic_user("test2")
        # self.user3 = self.get_basic_user("test3")

        # self.user1_ct = CashTransaction(self.user1)
        # self.user1_ct.deposit(100)
        #
        #
        # self.user2_ct = CashTransaction(self.user2)
        # self.user2_ct.deposit(50)
        #
        #
        # ta = TicketAmount.objects.get(amount=10.00)
        # self.user3_tm = TicketManager(self.user3)
        # self.user3_tm.deposit(10)
        #
        # self.escrow_user = self.user2_ct.get_escrow_user()
        #
        # self.escrow_ct = CashTransaction(self.escrow_user)
        #
        # bm = BuyinManager(self.user1)
        # bm.buyin(self.contest)
        #
        #
        # bm = BuyinManager(self.user2)
        # bm.buyin(self.world.contest)
        #
        # bm = BuyinManager(self.user3)
        # bm.buyin(self.world.contest)

class RefundTest(AbstractTest, RefundBuildWorldMixin):

    def setUp(self):
        super().setUp()
        self.user1 = self.get_basic_user("test1")
        self.user2 = self.get_basic_user("test2")
        self.user3 = self.get_basic_user("test3")
        self.build_world()
        self.user1_ct = CashTransaction(self.user1)
        self.user1_ct.deposit(100)


        self.user2_ct = CashTransaction(self.user2)
        self.user2_ct.deposit(50)


        ta = TicketAmount.objects.get(amount=10.00)
        self.user3_tm = TicketManager(self.user3)
        self.user3_tm.deposit(10)

        self.escrow_user = self.user2_ct.get_escrow_user()

        self.escrow_ct = CashTransaction(self.escrow_user)

        bm = BuyinManager(self.user1)
        bm.buyin(self.contest_pool)

        bm = BuyinManager(self.user2)
        bm.buyin(self.contest_pool)

        bm = BuyinManager(self.user3)
        bm.buyin(self.contest_pool)
        Entry.objects.filter(contest_pool=self.contest_pool).update(contest=self.contest)

    def test_refund(self):

        self.assertEqual(self.user1_ct.get_balance_amount(), 90)
        self.assertEqual(self.user2_ct.get_balance_amount(), 40)
        self.assertEqual(self.escrow_ct.get_balance_amount(), 30)
        self.assertEqual(self.user3_tm.get_available_tickets().count(), 0)

        refund_manager = RefundManager()
        refund_manager.refund(self.contest, force=True)

        self.assertEqual(self.user1_ct.get_balance_amount(), 100)
        self.assertEqual(self.user2_ct.get_balance_amount(), 50)
        self.assertEqual(self.escrow_ct.get_balance_amount(), 0)
        self.assertEqual(self.user3_tm.get_available_tickets().count(), 1)

    # in progress should be refundable in cases
    # where its not a GPP and it did not fill
    # def test_contest_is_in_progress(self):
    #     self.contest.status = self.contest.INPROGRESS
    #     self.contest.save()
    #     self.should_raise_contest_is_in_progress_or_closed_exception()

    def test_contest_is_cancelled(self):
        self.contest.status = self.contest.CANCELLED
        self.contest.save()
        self.should_raise_contest_is_cancelled_or_closed()

    def test_contest_is_closed(self):
        self.contest.status = self.contest.CLOSED
        self.contest.save()
        self.should_raise_contest_is_cancelled_or_closed()

    # completed is an "in progress" status, which has
    # no more live inprogress games
    # def test_contest_is_completed(self):
    #     self.contest.status = self.contest.COMPLETED
    #     self.contest.save()
    #     self.should_raise_contest_is_in_progress_or_closed_exception()

    def should_raise_contest_is_cancelled_or_closed(self):

        self.assertEqual(self.user1_ct.get_balance_amount(), 90)
        self.assertEqual(self.user2_ct.get_balance_amount(), 40)
        self.assertEqual(self.escrow_ct.get_balance_amount(), 30)
        self.assertEqual(self.user3_tm.get_available_tickets().count(), 0)

        refund_manager = RefundManager()
        self.assertRaises(ContestCanNotBeRefunded,
            lambda: refund_manager.refund(self.contest, force=True))

        self.assertEqual(self.user1_ct.get_balance_amount(), 90)
        self.assertEqual(self.user2_ct.get_balance_amount(), 40)
        self.assertEqual(self.escrow_ct.get_balance_amount(), 30)
        self.assertEqual(self.user3_tm.get_available_tickets().count(), 0)

# class RefundConcurrentTest(AbstractTest, RefundBuildWorldMixin):
#
#     def setUp(self):
#         self.user1 = self.get_basic_user("test1")
#         self.user2 = self.get_basic_user("test2")
#         self.user3 = self.get_basic_user("test3")
#         self.build_world()
#         self.user1_ct = CashTransaction(self.user1)
#         self.user1_ct.deposit(100)
#
#
#         self.user2_ct = CashTransaction(self.user2)
#         self.user2_ct.deposit(50)
#
#
#         ta = TicketAmount.objects.get(amount=10.00)
#         self.user3_tm = TicketManager(self.user3)
#         self.user3_tm.deposit(10)
#
#         self.escrow_user = self.user2_ct.get_escrow_user()
#
#         self.escrow_ct = CashTransaction(self.escrow_user)
#
#         bm = BuyinManager(self.user1)
#         bm.buyin(self.contest)
#
#
#         bm = BuyinManager(self.user2)
#         bm.buyin(self.world.contest)
#
#         bm = BuyinManager(self.user3)
#         bm.buyin(self.world.contest)
#
#     @override_settings(TEST_RUNNER=AbstractTest.CELERY_TEST_RUNNER,
#                        CELERY_ALWAYS_EAGER=True,
#                        CELERYD_CONCURRENCY=3)
#     def test_refund_contest(self):
#
#         def run_test(contest):
#             task = refund_task.delay(contest, True)
#             print("threaded task:"+str(task.successful()) +" "+ str(task.result))
#             self.assertFalse(task.successful())
#
#         task = refund_task.delay(self.contest, True)
#         print("main task:"+str(task.successful())+" "+ str(task.result))
#
#         #
#         # TODO sometimes this actually deadlocks --
#         #self.concurrent_test(3, run_test, self.contest)
#         self.assertTrue(task.successful())


