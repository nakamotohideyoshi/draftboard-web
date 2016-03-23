#
# contest/tests.py

from mysite.exceptions import (
    IncorrectVariableTypeException,
)
from test.classes import (
    AbstractTest,
    ResetDatabaseMixin,
)
from salary.dummy import Dummy
from prize.classes import CashPrizeStructureCreator
from prize.models import (
    PrizeStructure,
)
from django.utils import timezone
from datetime import timedelta
from cash.classes import CashTransaction
from draftgroup.classes import DraftGroupManager
from draftgroup.tasks import on_game_closed, on_game_inprogress
from draftgroup.models import (
    DraftGroup,
)
from django.test.utils import override_settings
from contest.models import (
    Contest,
    ContestPool,
    LiveContest,
    HistoryContest,
)
from contest.classes import (
    ContestCreator,
    ContestPoolCreator,
)
from sports.classes import SiteSportManager
from sports.models import (
    SiteSport,
)
from contest.views import (
    EnterLineupAPIView,
)
from test.classes import (
    BuildWorldMixin,
)

class TestResetDataBase(AbstractTest, ResetDatabaseMixin):

    def test_reset_it(self):
        self.reset_db()

class ContestPoolManagerTest(AbstractTest): #, BuildWorldMixin):
    """
    test the constructor arguments to ensure we raise
    exceptions if they are not the proper type.

    Note: functionality / database stuff should be test in a different test class!
    """

    def setUp(self):
        # setup a salary pool and draft group
        self.sport = 'test' # build_world() should create a sport called 'test'
        # if DraftGroup.objects.all().count() == 0:
        #     self.build_world()
        #     self.draft_group = self.world.draftgroup
        # else:
        #     self.draft_group = DraftGroup.objects.filter().order_by('-created')[0]
        #
        # # get a headsup prize_structure (most recently created)
        # self.prize_structure = PrizeStructure.objects.filter().order_by('-created')[0]

        # if the "world" doesnt exist (ie: games, playerstats, draftgroups) create it.
        ContestPool.objects.all().delete() # so we can run with --keepdb locally for quicker testing

        # create a custom class for an invalid type of object to pass as params
        class CustomInvalidType:
            def __init__(self):
                pass
        self.custom_invalid_type_class = CustomInvalidType
        self.invalid_type_obj = self.custom_invalid_type_class()

    def __call_creator_constructor_test(self, sport=None, prize_structure=None, start=None, duration=None, draft_group=None):
        """
        This method is simply to test that the constructor
        properly validates the parameters passed to it.
        It does NOT check to make sure the data backing
        the parameters are valid start times, etc...

        This method will select a VALID argument if None is passed for any variable.

        We can easily test INVALID variables one at a time with this method.
        """
        if sport is None:
            sport = self.sport
        if prize_structure is None:
            class PrizeStructureChild(PrizeStructure):
                def __init__(self):
                    pass
            prize_structure = PrizeStructureChild
        if start is None:
            start = timezone.now()
        if duration is None:
            duration = int(300)
        # if draft_group is not None:
        #     # create a dummy child of DraftGroup
        #     class DraftGroupChild(DraftGroup):
        #         def __init__(self):
        #             pass
        #     draft_group = DraftGroupChild()

        # try to construct a ContestPool
        try:
            #print('sport:', str(sport))
            self.assertRaises( IncorrectVariableTypeException,
                lambda:ContestPoolCreator(sport, prize_structure, start, duration, draft_group) )
        except:
            # there might be other exceptions from
            # inner objects, but those arent tested here!
            pass

    def test_constructor_arg_sport(self):
        self.__call_creator_constructor_test(sport=self.invalid_type_obj)

    def test_constructor_arg_prize_structure(self):
        self.__call_creator_constructor_test(prize_structure=self.invalid_type_obj)

    def test_constructor_arg_start(self):
        self.__call_creator_constructor_test(start=self.invalid_type_obj)

    def test_constructor_arg_duration(self):
        self.__call_creator_constructor_test(duration=self.invalid_type_obj)

    def test_constructor_arg_draft_group(self):
        self.__call_creator_constructor_test(duration=self.invalid_type_obj)

class ContestPoolManagerCreateTest(AbstractTest, BuildWorldMixin):
    """
    Test functionality of ContestPoolManager.create()

    BuildWorldMixin gives us these methods:
        self.build_world()
        self.create_valid_lineup()

    """

    def setUp(self):
        # setup a salary pool and draft group
        #print("WTF")
        self.sport = 'nfl' # build_world() should create a sport called 'test'
        self.build_world()
        self.draft_group = self.world.draftgroup

        # get a headsup prize_structure (most recently created)
        self.prize_structure = PrizeStructure.objects.filter().order_by('-created')[0]

        # if the "world" doesnt exist (ie: games, playerstats, draftgroups) create it.
        ContestPool.objects.all().delete() # so we can run with --keepdb locally for quicker testing

        #
        ####### print some debug stuff so we know it exists (or doesnt ####
        all_site_sports = SiteSport.objects.all()
        print('%s existing SiteSport objects' % all_site_sports.count())
        for ss in all_site_sports:
            print(str(ss))
            print('')

    def __call_construct(self, sport=None, prize_structure=None, start=None, duration=None, draft_group=None):
        """
        If any value is None, we will use a known good default value.
        """
        if sport is None:
            sport = self.sport
        if prize_structure is None:
            prize_structure = self.prize_structure
        if start is None:
            start = timezone.now()
        if duration is None:
            duration = int(300)

        contest_pool_creator = ContestPoolCreator(sport, prize_structure, start, duration, draft_group)
        return contest_pool_creator

    def test_create_simple_default_values_existing_draft_group(self):
        creator = self.__call_construct(draft_group=self.draft_group)
        contest_pool, created = creator.get_or_create()

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

# class ContestOnGameClosedRaceCondition(AbstractTest):
#
#     def setUp(self):
#         self.user = self.get_basic_user()
#         ct = CashTransaction(self.user)
#         ct.deposit(100)
#
#         # updated Dummy so we can get an instance for a sport, ie: 'nfl'
#         # call generate and it works for that sport. this is the latest
#         # and greatest Dummy.
#         self.sport          = 'nfl'
#         self.dummy          = Dummy(self.sport)
#
#         # does the same thing as generate_salaries()
#         # but creates it for a specific sport, whereas
#         # generate_salaries() uses the PlayerChild / GameChild/ test models only
#         salary_generator    = self.dummy.generate()
#
#         self.salary_pool    = salary_generator.pool
#         self.first = 100.0
#         self.second = 50.0
#         self.third = 25.0
#
#         #
#         # create a simple Rank and Prize Structure
#         self.buyin = 10
#
#         cps = CashPrizeStructureCreator(name='test-prizes')
#         cps.add(1, self.first)
#         cps.add(2, self.second)
#         cps.add(3, self.third)
#         cps.set_buyin( self.buyin )
#         cps.save()
#         cps.prize_structure.save()
#
#         self.prize_structure = cps.prize_structure
#         self.ranks = cps.ranks
#
#         #
#         # create the Contest
#         ssm = SiteSportManager()
#         site_sport = ssm.get_site_sport(self.sport)
#         game_model = ssm.get_game_class(site_sport)
#
#         now = timezone.now() # get the current time
#
#         # increase the start time of all the upcoming games by 20 minutes,
#         # then use the start time of the next game as the start time of the contest.
#         # and add a bunch of hours to start to spoof the end
#         for g in game_model.objects.filter(start__gte=now):
#             g.start + timedelta(minutes=20)
#             g.save()
#         upcoming_games = game_model.objects.filter(start__gte=now).order_by('start')
#         game = upcoming_games[0] # the closest upcoming game
#         start   = game.start
#         end     = start + timedelta(hours=12) # ahead 24 hours to capture all games
#         cc      = ContestCreator("test_contest", "nfl", self.prize_structure, start, end)
#
#         self.contest        = cc.create()
#         self.contest.status = Contest.RESERVABLE
#         self.contest.save()
#
#         # use the DraftGroupManager to create a draft group
#         # for the contest.
#         self.dgm = DraftGroupManager()
#         self.draft_group = self.dgm.create( self.contest.site_sport,
#                          self.contest.start, self.contest.end )
#
#         self.contest.draft_group = self.draft_group
#         self.contest.save()
#
#     # @override_settings(TEST_RUNNER=AbstractTest.CELERY_TEST_RUNNER,
#     #                    CELERY_ALWAYS_EAGER=True,
#     #                    CELERYD_CONCURRENCY=1)
#     def test_race_condition_on_game_closed(self):
#         """
#         when live games go to 'closed' status,
#         they send a signal which should attempt to
#         close Contests if ALL of the live games
#         in the contest's draftgroup are closed.
#         If this happens simultaneously we could potentially
#         skip from ever setting the contest to be ready to be paid out.
#         """
#
#         def run_now(self_obj):
#             task = on_game_closed.delay(self_obj.contest.draft_group)
#             self.assertTrue(task.successful())
#
#         # update all the games in the draft group to closed beforehand
#         ssm = SiteSportManager()
#         game_model = ssm.get_game_class(self.contest.site_sport)
#         for game in self.contest.games():
#             game.status = game_model.STATUS_CLOSED
#             game.save()
#             game.refresh_from_db()
#             self.assertEquals( game.status, game_model.STATUS_CLOSED ) # for sanity
#
#         # make sure contest status is not already completed
#         # self.contest.refresh_from_db()
#         # self.assertNotEquals( self.contest.status, Contest.COMPLETED )
#
#         # run it concurrently
#         self.concurrent_test(3, run_now, self)
#
#         # assert contest is ready to be paid out
#         self.contest.refresh_from_db()
#         self.assertEquals(self.contest.status, self.contest.COMPLETED )