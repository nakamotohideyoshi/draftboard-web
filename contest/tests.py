#
# contest/tests.py

from test.classes import AbstractTest, AbstractTestTransaction
from salary.dummy import Dummy
from prize.classes import CashPrizeStructureCreator
from django.utils import timezone
from datetime import timedelta
from datetime import time
from dataden.util.timestamp import DfsDateTimeUtil
from cash.classes import CashTransaction
#from draftgroup.models import DraftGroup
from draftgroup.classes import DraftGroupManager
from django.test.utils import override_settings
from contest.models import Contest
from contest.classes import ContestCreator
from contest.tasks import on_game_closed

class ContestSimpleTest(AbstractTest):

    def setUp(self):
        pass # this is a stub for a new test

class ContestOnGameClosedRaceCondition(AbstractTestTransaction):

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
        cps.save()
        cps.prize_structure.buyin = self.buyin
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

    @override_settings(TEST_RUNNER=AbstractTestTransaction.CELERY_TEST_RUNNER,
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

        # the trick is a hack to make this realistic.
        # because we dont have celery working fully properly
        # in the manage.py test stuff, we're going to
        # modify the draftgroup games within each thread

        self.concurrent_test(3, run_now, self)
        # assert contest is ready to be paid out