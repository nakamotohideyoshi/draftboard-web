#
# contest/buyin/tests.py

from rest_framework.test import APITestCase
from test.classes import AbstractTest
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
from contest.views import EnterLineupAPIView
from sports.classes import SiteSportManager
from cash.classes import CashTransaction
from contest import exceptions
import mysite.exceptions
from lineup.models import Lineup
from ticket.models import TicketAmount
from draftgroup.models import DraftGroup
from lineup.exceptions import LineupDoesNotMatchUser
from .tasks import buyin_task
from django.test.utils import override_settings
from test.classes import BuildWorldMixin, ForceAuthenticateAndRequestMixin
from rest_framework import status
from rest_framework.response import Response

# class BuyinTest(AbstractTest):


class BuyinTest(AbstractTest):
    """
    create a basic contest, and use the BuyinManager to buy into it.
    """

    def setUp(self):
        # ensure the default ticket
        TicketManager.create_default_ticket_amounts(verbose=False)
        # add funds to user
        self.user = self.get_basic_user()
        ct = CashTransaction(self.user)
        ct.deposit(100)

        # salary_generator = Dummy.generate_salaries()
        # self.salary_pool = salary_generator.pool
        # start
        #
        #
        self.verbose = True  # set to False to disable print statements

        #
        # The sport we are going to build fake stats for.
        # Lets use nfl, but it doesnt matter what sport we use
        self.sport = 'nfl'

        #
        # Ensure there are Games by using the Dummy to generate fake stats.
        # The ScheduleManager requires that Game objects exist
        # because when it creates scheduled Contest objects
        # it is required to create a draft group.
        self.dummy = Dummy(sport=self.sport)
        self.generator = self.dummy.generate()
        self.salary_pool = self.generator.pool
        self.site_sport = self.dummy.site_sport  # stash the site_sport for easy use

        self.site_sport_manager = SiteSportManager()
        self.game_model = self.site_sport_manager.get_game_class(
            self.site_sport)  # ie: sports.nfl.models.Game
        self.games = self.game_model.objects.all()  # there should be handful now, for today
        if self.games.count() <= 0:
            raise Exception(
                'buyin.tests.BuyinTest - we meant to create games.... but none were created!')
        # end

        # create a simple prize pool
        self.first = 100.0
        self.second = 50.0
        self.third = 25.0
        self.buyin = 10
        cps = CashPrizeStructureCreator(name='test')
        cps.add(1, self.first)
        cps.add(2, self.second)
        cps.add(3, self.third)
        cps.set_buyin(self.buyin)
        cps.save()
        cps.prize_structure.save()

        self.prize_structure = cps.prize_structure
        self.ranks = cps.ranks

        #
        # create the Contest
        # now = timezone.now()
        # start = DfsDateTimeUtil.create(now.date(), time(23,0))
        # end = DfsDateTimeUtil.create(now.date() + timedelta(days=1), time(0,0))
        start = self.games[0].start + timedelta(minutes=5)
        end = self.games[self.games.count() - 1].start  # set 'end' to start of last game
        cc = ContestCreator("test_contest", self.sport, self.prize_structure, start, end)
        self.contest = cc.create()
        self.contest.status = Contest.RESERVABLE
        self.contest.save()

        self.draft_group = DraftGroup()
        self.draft_group.salary_pool = self.salary_pool
        self.draft_group.start = start
        self.draft_group.end = end
        self.draft_group.save()

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
        lineup.draft_group = self.draft_group
        lineup.user = self.user

        self.contest.draft_group = draftgroup2
        self.contest.save()

        bm = BuyinManager(self.user)
        self.assertRaises(exceptions.ContestLineupMismatchedDraftGroupsException,
                          lambda: bm.buyin(self.contest, lineup))

    def test_contest_full(self):
        self.contest.current_entries = 19
        self.contest.save()
        bm = BuyinManager(self.user)
        self.assertRaises(exceptions.ContestIsFullException,
                          lambda: bm.buyin(self.contest))

    # def test_contest_is_in_progress(self):
    #     self.contest.status = self.contest.INPROGRESS
    #     self.contest.save()
    #     self.should_raise_contest_is_in_progress_or_closed_exception()
    #
    # def test_contest_is_cancelled(self):
    #     self.contest.status = self.contest.CANCELLED
    #     self.contest.save()
    #     self.should_raise_contest_is_in_progress_or_closed_exception()
    #
    # def test_contest_is_closed(self):
    #     self.contest.status = self.contest.CLOSED
    #     self.contest.save()
    #     self.should_raise_contest_is_in_progress_or_closed_exception()
    #
    # def test_contest_is_completed(self):
    #     self.contest.status = self.contest.COMPLETED
    #     self.contest.save()
    #     self.should_raise_contest_is_in_progress_or_closed_exception()
    #
    # def should_raise_contest_is_in_progress_or_closed_exception(self):
    #     bm = BuyinManager(self.user)
    #     self.assertRaises(exceptions.ContestIsInProgressOrClosedException,
    #               lambda: bm.buyin(self.contest))

    def test_user_owns_lineup(self):
        lineup = Lineup()
        lineup.draft_group = self.draft_group
        lineup.user = self.get_admin_user()

        self.contest.draft_group = self.draft_group
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

# class BuyinRaceTest(AbstractTest):
#
#     def setUp(self):
#
#         self.user = self.get_basic_user()
#         ct = CashTransaction(self.user)
#         ct.deposit(100)
#
#         salary_generator = Dummy.generate_salaries()
#         self.salary_pool = salary_generator.pool
#         self.first = 100.0
#         self.second = 50.0
#         self.third = 25.0
#
#         #
#         # create a simple Rank and Prize Structure
#         self.buyin =10
#         cps = CashPrizeStructureCreator(name='test')
#         cps.add(1, self.first)
#         cps.add(2, self.second)
#         cps.add(3, self.third)
#         cps.set_buyin(self.buyin)
#         cps.save()
#         cps.prize_structure.save()
#
#         self.prize_structure = cps.prize_structure
#         self.ranks = cps.ranks
#
#         #
#         # create the Contest
#         now = timezone.now()
#         start = DfsDateTimeUtil.create(now.date(), time(23,0))
#         end = DfsDateTimeUtil.create(now.date() + timedelta(days=1), time(0,0))
#         cc= ContestCreator("test_contest", "nfl", self.prize_structure, start, end)
#         self.contest = cc.create()
#         self.contest.status = Contest.RESERVABLE
#         self.contest.save()
#
#         self.draft_group = DraftGroup()
#         self.draft_group.salary_pool = self.salary_pool
#         self.draft_group.start = start
#         self.draft_group.end = end
#         self.draft_group.save()
#
#     @override_settings(TEST_RUNNER=BuyinTest.CELERY_TEST_RUNNER,
#                        CELERY_ALWAYS_EAGER=True,
#                        CELERYD_CONCURRENCY=3)
#     def test_race_condition_to_fill_last_spot_of_contest(self):
#         self.contest.max_entries = 3
#         self.contest.entries = 3
#         self.contest.save()
#
#         def run_now(self_obj):
#             task = buyin_task.delay(self_obj.user, self_obj.contest)
#             self.assertTrue(task.successful())
#
#         self.concurrent_test(3, run_now, self)
#         ct = CashTransaction(self.user)
#
#         self.assertEqual(70, ct.get_balance_amount())


class BuyinTaskTest(APITestCase, BuildWorldMixin, ForceAuthenticateAndRequestMixin):
    """
    creates the world (a contest with a draft_group)
    along with a contest which we can enter a lineup into.

    tests to make sure the 2 primary api calls involved in
    this task are working properly.

    those two api calls are:

        1. /api/contest/enter-lineup/               # try to do it non-blocking
        2. /api/contest/enter-lineup-status/        # check if it worked, need to poll this.


    """

    def setUp(self):
        """
        1. builds the world

        2. logs in a newly created user

        :return:
        """
        # build world, and create a user with username='user'
        self.build_world()

        # get a scheduled, draftable contest from the world.
        # the default self.world.contest doesnt have a draftgroup,
        # so make sure to use get_scheduled_contest()
        self.contest = self.world.get_scheduled_contest()
        print('BuyinTaskTest self.contest:', str(self.contest))

        # creates a user and also adds cash funds to their account
        # so they can buyin to contests
        self.user = self.create_user('user')

        # the endpoint to test
        self.url = '/api/contest/enter-lineup/'

        # create a valid lineup
        self.lineup = self.create_valid_lineup(self.user)

    # @override_settings(TEST_RUNNER=BuyinTest.CELERY_TEST_RUNNER,
    #                    CELERY_ALWAYS_EAGER=True,
    #                    CELERYD_CONCURRENCY=1)
