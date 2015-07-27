#
# lineup/tests.py

from test.classes import AbstractTest, AbstractTestTransaction
from salary.dummy import Dummy
from django.utils import timezone
from datetime import timedelta
from datetime import time
from dataden.util.timestamp import DfsDateTimeUtil
import mysite.exceptions
from lineup.models import Lineup
from lineup.exceptions import LineupDoesNotMatchUser
from draftgroup.classes import DraftGroupManager
from sports.classes import SiteSportManager

class SimpleLineupNBATest(AbstractTest):
    """
    create a basic lineup, and use the BuyinManager to buy into it.
    """

    def setUp(self):

        self.sport = 'nfl'

        # lineups need a user associated with them
        self.user   = self.get_basic_user()

        # get the site_sport we want to make this lineup for
        self.site_sport_manager = SiteSportManager()
        self.site_sport         = self.site_sport_manager.get_site_sport()

        # generate a salary pool so we will be able to generate a draft group
        salary_generator = Dummy.generate_salaries()
        self.salary_pool = salary_generator.pool

        # create a start and end time, so we can create a draftgroup
        now          = timezone.now()
        self.start   = DfsDateTimeUtil.create(now.date(), time(23,0))
        self.end     = DfsDateTimeUtil.create(now.date() + timedelta(days=1), time(0,0))

        # the lineup needs a reference to the draft_group
        # which determines the set of draftable players which could possibly be in the lineup
        #
        # it just so happens that Dummy.generate_salaries() creates fake games
        # to make its fake salaries. and all the games get (created at timezone.now()).
        # lets
        self.draft_group_manager    = DraftGroupManager()
        self.draft_group = self.draft_group_manager.create(self.site_sport, self.start, self.end)

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
        lineup.draftgroup = self.draftgroup
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
        lineup.draftgroup = self.draftgroup
        lineup.user = self.user

        self.contest.draft_group =draftgroup2
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
        lineup.draftgroup = self.draftgroup
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
    pass
    #TODO add the Race condition test
    # def test_race_condition_to_fill_last_spot_of_contest(self):
    #     self.contest.max_entries = 5
    #     self.contest.entries = 3
    #     self.contest.save()
    #
    #     def run_now(self_obj):
    #         bm = BuyinManager(self_obj.user)
    #         bm.buyin(self_obj.contest)
    #
    #     exceptions_list = self.test_concurrently(4, run_now, self)
    #     self.assertEqual(len(exceptions_list), 1)
    #     ct = CashTransaction(self.user)
    #     print("User Balance: "+str(ct.get_balance_amount())+ " pointer:"+str(ct.get_balance_transaction_pk()))

