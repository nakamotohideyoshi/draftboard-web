#
# contest/tests.py

from test.classes import AbstractTest
from salary.dummy import Dummy
from prize.classes import CashPrizeStructureCreator
from django.utils import timezone
from datetime import timedelta
from cash.classes import CashTransaction
from draftgroup.classes import DraftGroupManager
from draftgroup.tasks import on_game_closed, on_game_inprogress
from django.test.utils import override_settings
from contest.models import Contest, LobbyContest, UpcomingContest, LiveContest, HistoryContest
from contest.classes import ContestCreator
from sports.classes import SiteSportManager
from contest.views import (
    EnterLineupAPIView,
)

class ContestManagerTest(AbstractTest):
    """
    tests the managers for:
        LobbyContest    - contests that havent been cancelled or paid out.
        UpcomingContest - contests that are still accepting Entry(s), aka buyins
        LiveContest     - contests with live real-life games happening
        HistoryContest  - contests in a final state, such as having been cancelled or paid out.
    """
    def setUp(self):
        pass # TODO

class ContestCreatorClone(AbstractTest):
    """
    test cloning a Contest does what we expect.
    """
    def setUp(self):
        pass # TODO

class ContestCreatorRespawn(AbstractTest):
    """
    test respawn functionality (similar to clone,
    but should only work on upcoming contests.
    """
    def setUp(self):
        pass # TODO

class ContestOnGameClosedRaceCondition(AbstractTest):

    def setUp(self):
        self.user = self.get_basic_user()
        ct = CashTransaction(self.user)
        ct.deposit(100)

        # updated Dummy so we can get an instance for a sport, ie: 'nfl'
        # call generate and it works for that sport. this is the latest
        # and greatest Dummy.
        self.dummy          = Dummy('nfl')

        # does the same thing as generate_salaries()
        # but creates it for a specific sport, whereas
        # generate_salaries() uses the PlayerChild / GameChild/ test models only
        salary_generator    = self.dummy.generate()

        self.salary_pool    = salary_generator.pool
        self.first = 100.0
        self.second = 50.0
        self.third = 25.0

        #
        # create a simple Rank and Prize Structure
        self.buyin = 10

        cps = CashPrizeStructureCreator(name='test-prizes')
        cps.add(1, self.first)
        cps.add(2, self.second)
        cps.add(3, self.third)
        cps.set_buyin( self.buyin )
        cps.save()
        cps.prize_structure.save()

        self.prize_structure = cps.prize_structure
        self.ranks = cps.ranks

        #
        # create the Contest
        now     = timezone.now()
        start   = now - timedelta(days=1) # behind 24 hours
        end     = now + timedelta(days=1) # ahead 24 hours to capture all games
        cc      = ContestCreator("test_contest", "nfl", self.prize_structure, start, end)

        self.contest        = cc.create()
        self.contest.status = Contest.RESERVABLE
        self.contest.save()

        # use the DraftGroupManager to create a draft group
        # for the contest.
        self.dgm = DraftGroupManager()
        self.draft_group = self.dgm.create( self.contest.site_sport,
                         self.contest.start, self.contest.end )

        self.contest.draft_group = self.draft_group
        self.contest.save()

    @override_settings(TEST_RUNNER=AbstractTest.CELERY_TEST_RUNNER,
                       CELERY_ALWAYS_EAGER=True,
                       CELERYD_CONCURRENCY=3)
    def test_race_condition_on_game_closed(self):
        """
        when live games go to 'closed' status,
        they send a signal which should attempt to
        close Contests if ALL of the live games
        in the contest's draftgroup are closed.
        If this happens simultaneously we could potentially
        skip from ever setting the contest to be ready to be paid out.
        """

        def run_now(self_obj):
            task = on_game_closed.delay(self_obj.contest.draft_group)
            self.assertTrue(task.successful())

        # update all the games in the draft group to closed beforehand
        ssm = SiteSportManager()
        game_model = ssm.get_game_class(self.contest.site_sport)
        for game in self.contest.games():
            game.status = game_model.STATUS_CLOSED
            game.save()
            game.refresh_from_db()
            self.assertEquals( game.status, game_model.STATUS_CLOSED ) # for sanity

        # make sure contest status is not already completed
        # self.contest.refresh_from_db()
        # self.assertNotEquals( self.contest.status, Contest.COMPLETED )

        # run it concurrently
        self.concurrent_test(3, run_now, self)

        # assert contest is ready to be paid out
        self.contest.refresh_from_db()
        self.assertEquals(self.contest.status, self.contest.COMPLETED )