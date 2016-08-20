#
# draftgroup/tests.py

import json
from dataden.util.timestamp import DfsDateTimeUtil
from datetime import datetime, time
from test.models import GameChild
from mysite.exceptions import (
    InvalidSiteSportTypeException,
    InvalidStartTypeException,
    InvalidEndTypeException,
    SalaryPoolException,
    NoGamesInRangeException,
)
from draftgroup.models import (
    GameTeam,
    PlayerUpdate,
    GameUpdate,
)
from draftgroup.classes import (
    DraftGroupManager,
    PlayerUpdateManager,
    GameUpdateManager,
)
from sports.models import SiteSport
from salary.dummy import Dummy as SalaryDummy
from test.classes import (
    AbstractTest,
    BuildWorldMixin,
)
from salary.dummy import Dummy
from prize.classes import CashPrizeStructureCreator
from django.utils import timezone
from datetime import timedelta
from cash.classes import CashTransaction
from django.test.utils import override_settings
from contest.models import Contest
from contest.classes import ContestCreator
from draftgroup.tasks import on_game_closed
from sports.classes import SiteSportManager
from swish.classes import UpdateData

class PlayerUpdateManagerEmptyDraftGroup(PlayerUpdateManager):
    """
    sub-class so we dont need valid SRIDs.
    tests everything else to do with PlayerUpdateManager.
    """

    player_srid = 'Srid-PlayerUpdateManagerEmptyDraftGroup'.lower()

    def get_draft_groups(self):
        return []

class PlayerUpdateTest(AbstractTest, BuildWorldMixin):

    def setUp(self):
        # use the custom test-only subclass
        self.manager_class = PlayerUpdateManagerEmptyDraftGroup

        # self.sport = 'nfl' # build_world() would default to create a sport called 'test'
        # self.build_world()
        # self.draft_group = self.world.draftgroup
        #
        # # creates some dummy players
        # self.user = self.get_admin_user()
        # self.create_valid_lineup(self.user)
        #
        # # get the sports.<sport>.models.Player model class for this sport
        # self.ssm = SiteSportManager()
        # self.site_sport = self.ssm.get_site_sport(self.sport)
        # self.player_class = self.ssm.get_player_class(self.site_sport)
        #
        # self.player = self.player_class.objects.filter()[0]
        # print(self.player.srid) # TODO # lineup/classes.py line 365 in __validate_lineup: counter[player.team.pk] += 1 NoneType object has no attribute 'pk'
        pass

    def __player_update_manager_add(self, swish_update):
        #

        # the sport, and the player's srid will be required to create the PlayerUpdate using the manager
        sport = swish_update.get_sport()
        # get out the fields required to create a PlayerUpdate model
        player_name = swish_update.get_field(UpdateData.field_player_name)
        player_srid = 'some-srid-todo' # TODO we have to infer the player by name-matching

        # get the fields required to create a draftgroup.models.PlayerUpdate
        update_id = swish_update.get_update_id()
        updated_at = swish_update.get_updated_at()

        # hard code this to use the category: 'injury' for testing
        category = 'injury'
        type = swish_update.get_field(UpdateData.field_source)
        value = swish_update.get_field(UpdateData.field_text)

        # create a PlayerUpdate model in the db
        player_update_manager = self.manager_class(sport)
        update_model = player_update_manager.add(
            update_id,
            category,
            type,
            value,
            published_at=updated_at
        )
        print(update_model.update_id, update_model.category,
              update_model.type, update_model.value, update_model.updated_at)
        return update_model

    def test_1(self):
        data = """{"id": 295783, "date": "2016-08-16", "time": "18:11:55", "datetime": "2016-08-16 18:11:55",
                "datetimeUtc": "2016-08-16 22:11:55", "sportId": 2, "sport": "NFL", "teamId": 348, "teamAbbr": "NE",
                "playerId": 381091, "playerName": "Rob Gronkowski", "position": "TE",
                "text": "Rob Gronkowski: The unspecified injury that caused Gronkowski to miss practice Tuesday is being described as a bruise, the  Boston Herald reports.",
                "type": null, "sourceId": 5, "source": "rotowire", "sourceOrigin": "rotowire",
                "urlOrigin": "https://rotowire.com", "swishStatusId": 9, "swishStatus": "week-to-week",
                "swishStatusConfidence": 0.344101}"""
        data = json.loads(data)
        swish_update = UpdateData(data)

        # have the PlayerUpdateManager return a PlayerUpdate model
        update_model = self.__player_update_manager_add(swish_update)
        # TODO - validate its ok

class GameUpdateTest(AbstractTest):

    def setUp(self):
        pass # set anything that all tests will use

    def test_1(self):
        pass

# class DraftGroupOnGameClosedRaceCondition(AbstractTest):
#
#     def setUp(self):
#         self.user = self.get_basic_user()
#         ct = CashTransaction(self.user)
#         ct.deposit(100)
#
#         # updated Dummy so we can get an instance for a sport, ie: 'nfl'
#         # call generate and it works for that sport. this is the latest
#         # and greatest Dummy.
#         self.dummy          = Dummy('nfl')
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
#         cps.save()
#         cps.prize_structure.buyin = self.buyin
#         cps.prize_structure.save()
#
#         self.prize_structure = cps.prize_structure
#         self.ranks = cps.ranks
#
#         #
#         # create the Contest
#         now     = timezone.now()
#         start   = now - timedelta(days=1) # behind 24 hours
#         end     = now + timedelta(days=1) # ahead 24 hours to capture all games
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
#     @override_settings(TEST_RUNNER=AbstractTest.CELERY_TEST_RUNNER,
#                        CELERY_ALWAYS_EAGER=True,
#                        CELERYD_CONCURRENCY=3)
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
#         # ensure the contest isnt already in the completed state !
#         self.assertNotEquals( self.contest.status, Contest.COMPLETED )
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
#         # magically, now the Contest should be updated too !
#         #  ... because each game.save() fires a signal
#         #      and draftgroup is listening for that to close stuff if necessary
#         contest = Contest.objects.get(pk = self.contest.pk )
#         self.assertEquals(contest.status, Contest.COMPLETED )

class DraftGroupManagerCreateParams(AbstractTest):

    def setUp(self):
        self.site_sport, created = SiteSport.objects.get_or_create(name='nfl')
        self.start              = timezone.now()        # a (timezone aware) datetime object
        self.end                = timezone.now()        # a (timezone aware) datetime object
        self.invalid_site_sport = 'invalidsitesport'
        self.invalid_start      = 1420000000 # int is invalid here
        self.invalid_end        = datetime.now().date() # invalid because just date() wont work!

    def test_draft_group_manager_create_invalid_site_sport(self):
        manager = DraftGroupManager()
        date_time = datetime.now()
        self.assertRaises(InvalidSiteSportTypeException,
                  lambda: manager.create(self.invalid_site_sport, self.start, self.end))

    def test_draft_group_manager_create_invalid_start(self):
        manager = DraftGroupManager()
        self.assertRaises(InvalidStartTypeException,
                  lambda: manager.create(self.site_sport, self.invalid_start, self.end ))

    def test_draft_group_manager_create_invalid_end(self):
        manager = DraftGroupManager()
        self.assertRaises(InvalidEndTypeException,
                  lambda: manager.create(self.site_sport, self.start, self.invalid_end ))

    def test_draft_group_manager_create_no_games_in_range_exception(self):
        manager = DraftGroupManager()
        #
        # create a start & end range that cant possibly have games in it
        start   = timezone.now()
        end     = start - timedelta(days=1) # subtract a day from start
        self.assertRaises(NoGamesInRangeException,
                  lambda: manager.create(self.site_sport, start, end ))

class DraftGroupManagerNoSalaryPool(AbstractTest):

    def setUp(self):
        self.site_sport, created = SiteSport.objects.get_or_create(name='sitesporttest')

    def test_draft_group_manager_create_salary_pool_exception(self):
        manager = DraftGroupManager()
        self.assertRaises(SalaryPoolException, lambda: manager.get_active_salary_pool(self.site_sport))

#
# Needs to take into account new Dummy.generate()
# class DraftGroupCreate(AbstractTest):
#
#     def setUp(self):
#         """
#         create the underlying objects like SiteSport instance
#         and salary pool players to be able to create draft group
#         """
#         self.sport = 'test'  # doesnt HAVE to be a valid site_sport value though
#         self.site_sport, created = SiteSport.objects.get_or_create(name=self.sport)
#
#         # dummy.generate_salaries will use the current time
#         # when it creates games, so lets capture the time now, and then after
#         # it generates stuff to make sure we have a start & end range
#         # that will include the games it created                                                                                             more
#         now             = timezone.now()
#         self.start      = DfsDateTimeUtil.create( now.date() - timedelta(days=1), time(0,0) )
#
#         #
#         # we MUST create games, players, teams, salary pool stuff:
#         self.salary_generator = SalaryDummy.generate_salaries(sport=self.sport)
#         #self.__print_games_in_db()
#
#         # create end datetime after generate_salaries() is run
#         self.end        = DfsDateTimeUtil.create( now.date() + timedelta(days=1), time(0,0) )
#
#     def __print_games_in_db(self):
#         print( 'GameChild instances in db...')
#         for g in GameChild.objects.all():
#             print( '    ', str(g), str(g.start) )
#
#     def test_draftgroupmanager_create(self):
#         """
#         will fail if create() method returns None ! possible if no games, or no salary pool exists
#         """
#         dgm = DraftGroupManager()
#         draft_group = dgm.create( self.site_sport, self.start, self.end )
#         self.assertIsNotNone(draft_group)
#
#     def test_draftgroup_create_makes_game_team_entries(self):
#         dgm = DraftGroupManager()
#         draft_group = dgm.create( self.site_sport, self.start, self.end )
#         # make sure num_games is non zero -- it should really be the # of games spanned
#         self.assertGreater( draft_group.num_games, 0)
#         gameteams = GameTeam.objects.filter( draft_group=draft_group )
#         num_gameteams = len(gameteams)
#         if num_gameteams <= 0:
#             raise Exception('i assumed there was going to be at least one game here')
#         self.assertGreater( num_gameteams, 0 )
#
#         # get one o the games and change the status to 'closed',
#         # which should fire the GameStatusChangedSignal... and result
#         # in the DraftGroupManager method being called which checks
#         # to see if it should change any Contest statuses which reference that draftgroup
#         game = GameChild.objects.get( srid=gameteams[0].game_srid )
#         print( 'game.status', str(game.status) )
#         game.status = 'steve'
#         game.save()
#
#         game.status = 'closed' # back to closed
#         game.save() # should signal all DraftGroups to close Contests with matching draftgroup!

    # def test_live_game_status_change_signals_draftgroup_on_game_status_changed(self):
    #
    #     # dgm = DraftGroupManager()
    #     # draft_group = dgm.create( self.site_sport, self.start, self.end )
    #     #
    #     # # get one of the underlying games, and change its status
    #     # games = GameChild.objects.filter()
    #     pass # TODO




