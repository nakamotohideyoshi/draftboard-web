import unittest

from django.utils import timezone
from django.core.urlresolvers import reverse
from contest.classes import (
    ContestPoolCreator,
    FairMatch,
    SkillLevelManager,
)
from contest.models import (
    ContestPool,
    Contest,
    Entry
)

from contest.views import (
    EnterLineupAPIView
)

from lineup.models import (
    Lineup
)
from mysite.exceptions import (
    IncorrectVariableTypeException,
)
from prize.models import (
    PrizeStructure,
)

from account.models import (
    Limit,
    Confirmation,
    Identity,
    Information
)

from sports.models import (
    SiteSport,
)
from test.classes import (
    AbstractTest,
    ForceAuthenticateAndRequestMixin
)
from test.classes import (
    BuildWorldMixin,
)
from logging import getLogger

logger = getLogger('contest.tests')


class FairMatchTest(unittest.TestCase):
    """
    unit tests (no database required) for contest.classes.FairMatch
    """

    def test_simple_h2h_contest_1(self):
        #            = [1   2 3 4 5     6 7 8 9            ]
        test_entries = [1, 1, 2, 3, 4, 5, 5, 5, 6, 7, 8, 9, 9, 9, 9, 9, 9, 9]
        contest_size = 2
        fm = FairMatch(test_entries, contest_size)
        fm.run()
        self.assertEqual(True, True)
        fm.print_debug_info()

    def test_simple_h2h_contest_2(self):
        #            = [1     2     3   4   5 6 7 8 9
        test_entries = [1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 6, 7, 8, 9]
        contest_size = 2
        fm = FairMatch(test_entries, contest_size)
        fm.run()
        self.assertEqual(True, True)
        fm.print_debug_info()

    def test_simple_h2h_contest_1_superlay(self):
        #
        test_entries = [1]
        contest_size = 2
        fm = FairMatch(test_entries, contest_size)
        fm.run()
        self.assertEqual(True, True)
        fm.print_debug_info()

    def test_simple_h2h_contest_2_superlay(self):
        #
        test_entries = [1, 2, 3]
        contest_size = 2
        fm = FairMatch(test_entries, contest_size)
        fm.run()
        self.assertEqual(True, True)
        fm.print_debug_info()

    def test_simple_3man_contest_1(self):
        #
        test_entries = [1, 2, 3]
        contest_size = 3
        fm = FairMatch(test_entries, contest_size)
        fm.run()
        self.assertEqual(True, True)
        fm.print_debug_info()

    def test_simple_3man_contest_2(self):
        #
        test_entries = [1, 2, 3, 9]
        contest_size = 3
        fm = FairMatch(test_entries, contest_size)
        fm.run()
        self.assertEqual(True, True)
        fm.print_debug_info()


class SkillLevelManagerTest(AbstractTest):
    def setUp(self):
        super().setUp()
        # check if it migrations the initial SkillLevels
        self.slm = SkillLevelManager()

    def test_1(self):
        """ default db has some SkillLevel objects """
        self.assertTrue(len(self.slm.skill_levels) > 0)

    def test_2(self):
        """
        test get_for_amount() for edges cases around the inflection points
        turn over skill levels, etc...
        """

        # expectations
        expected_data = [
            # amount   # skill_level
            (11.0, 'veteran'),
            (10.0, 'veteran'),
            (9.0, 'rookie'),
            (1.0, 'rookie'),
            (0.0, 'rookie'),
        ]

        manager = SkillLevelManager()
        logger.info('all skill levels:')
        for sl in manager.get_skill_levels():
            logger.info('    %s' % sl)

        for amount, expected_name in expected_data:
            sl = manager.get_for_amount(amount)
            name = sl.name
            logger.info('    amount: %s | expected_name[%s] name[%s]' % (amount, expected_name, name))
            self.assertEquals(expected_name, name)


class ContestPoolManagerTest(AbstractTest):  # , BuildWorldMixin):
    """
    test the constructor arguments to ensure we raise
    exceptions if they are not the proper type.

    Note: functionality / database stuff should be test in a different test class!
    """

    def setUp(self):
        super().setUp()
        # setup a salary pool and draft group
        self.sport = 'test'  # build_world() should create a sport called 'test'

        # if the "world" doesnt exist (ie: games, playerstats, draftgroups) create it.
        ContestPool.objects.all().delete()  # so we can run with --keepdb locally for quicker testing

        # create a custom class for an invalid type of object to pass as params
        class CustomInvalidType:
            def __init__(self):
                pass

        self.custom_invalid_type_class = CustomInvalidType
        self.invalid_type_obj = self.custom_invalid_type_class()

    def __call_creator_constructor_test(self, sport=None, prize_structure=None, start=None,
                                        duration=None,
                                        draft_group=None):
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

        # try to construct a ContestPool
        try:
            # print('sport:', str(sport))
            self.assertRaises(IncorrectVariableTypeException,
                              lambda: ContestPoolCreator(sport, prize_structure, start, duration,
                                                         draft_group))
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
        super().setUp()
        # setup a salary pool and draft group
        # print("WTF")
        self.sport = 'nfl'  # build_world() should create a sport called 'test'
        self.build_world()
        self.draft_group = self.world.draftgroup

        # get a headsup prize_structure (most recently created)
        self.prize_structure = PrizeStructure.objects.filter().order_by('-created')[0]

        # get instance of the SkillLevelManager
        self.skill_level_manager = SkillLevelManager()

        # if the "world" doesnt exist (ie: games, playerstats, draftgroups) create it.
        ContestPool.objects.all().delete()  # so we can run with --keepdb locally for quicker testing

        #
        ####### print some debug stuff so we know it exists (or doesnt ####
        all_site_sports = SiteSport.objects.all()
        logger.info('%s existing SiteSport objects' % all_site_sports.count())
        for ss in all_site_sports:
            logger.info(str(ss))

    def __call_construct(self, sport=None, prize_structure=None, start=None, duration=None,
                         draft_group=None):
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

        contest_pool_creator = ContestPoolCreator(sport, prize_structure, start, duration,
                                                  draft_group)
        return contest_pool_creator

    def test_create_simple_default_values_existing_draft_group(self):
        creator = self.__call_construct(draft_group=self.draft_group)
        contest_pool, created = creator.get_or_create()

    def test_skill_level_set_on_create(self):
        creator = self.__call_construct(draft_group=self.draft_group)
        contest_pool, created = creator.get_or_create()

        target_skill_level = self.skill_level_manager.get_for_amount(
            contest_pool.prize_structure.buyin)

        # the only comparison that doesnt really matter is the pk
        self.assertEquals(target_skill_level.name, contest_pool.skill_level.name)
        self.assertEquals(target_skill_level.gte, contest_pool.skill_level.gte)
        self.assertEquals(target_skill_level.enforced, contest_pool.skill_level.enforced)


class SetLimitsTest(AbstractTest, BuildWorldMixin, ForceAuthenticateAndRequestMixin):
    """
        test the enter-lineup view to ensure we raise
        exceptions if users reach their entry limits.
    """
    def setUp(self):
        super().setUp()
        self.build_world()
        self.user = self.get_user_with_account_information()
        self.view = EnterLineupAPIView
        # the url of the endpoint and a default user
        self.url = reverse('enter-lineup')
        self.create_valid_lineup(user=self.user)
        self.draft_group = self.world.draftgroup
        self.contest = self.world.contest
        prize_structure = self.contest.prize_structure
        sport = 'nfl'
        start = timezone.now()
        duration = int(300)
        self.contest_pool, created = ContestPoolCreator(sport, prize_structure, start, duration, self.draft_group).get_or_create()

        prize = prize_structure.buyin
        entry_alert_limit = Limit.objects.create(type=1, value=prize/4, user=self.user, time_period=7)
        entry_limit = Limit.objects.create(type=2, value=3, user=self.user, time_period=7)
        entry_fee_limit = Limit.objects.create(type=3, value=prize/2, user=self.user)

        Identity.objects.create(
            user=self.user,
            first_name='test',
            last_name='user',
            birth_day=1,
            birth_month=1,
            birth_year=1984,
            postal_code='80203',
        )
        Confirmation.objects.create(user=self.user,
                                    confirmed=True)

    def test_entry_fee(self):
        data = {'lineup': self.lineup.pk, 'contest_pool': self.contest_pool.pk}
        response = self.force_authenticate_and_POST(self.user, self.view, self.url, data)
        self.assertEqual(response.status_code, 500)

    def test_entry_limit(self):
        data = {'lineup': self.lineup.pk, 'contest_pool': self.contest_pool.pk}
        entries=[Entry(contest=self.contest, contest_pool=self.contest_pool, lineup=self.lineup, user=self.user),
              Entry(contest=self.contest, contest_pool=self.contest_pool, lineup=self.lineup, user=self.user),
              Entry(contest=self.contest, contest_pool=self.contest_pool, lineup=self.lineup, user=self.user)]
        Entry.objects.bulk_create(entries)
        response = self.force_authenticate_and_POST(self.user, self.view, self.url, data)
        self.assertEqual(response.status_code, 500)


class ContestManagerTest(AbstractTest):
    """
    tests the managers for:
        LobbyContest    - contests that havent been cancelled or paid out.
        UpcomingContest - contests that are still accepting Entry(s), aka buyins
        LiveContest     - contests with live real-life games happening
        HistoryContest  - contests in a final state, such as having been cancelled or paid out.
    """

    def setUp(self):
        super().setUp()
        # TODO


class ContestCreatorClone(AbstractTest):
    """
    test cloning a Contest does what we expect.
    """

    def setUp(self):
        super().setUp()
        # TODO


class ContestCreatorRespawn(AbstractTest):
    """
    test respawn functionality (similar to clone,
    but should only work on upcoming contests.
    """

    def setUp(self):
        super().setUp()
        # TODO




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
