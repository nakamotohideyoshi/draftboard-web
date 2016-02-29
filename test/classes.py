#
# test/classes.py

import django.test
from django.contrib.auth.models import User
import threading
from django.db import connections

from prize.classes import CashPrizeStructureCreator
from cash.classes import CashTransaction
from test.models import PlayerChild, PlayerStatsChild, GameChild
from django.utils import timezone
from random import randint
from sports.models import SiteSport, Position
from roster.models import RosterSpot, RosterSpotPosition
from salary.models import SalaryConfig, Pool, TrailingGameWeight, Salary
from dataden.util.timestamp import DfsDateTimeUtil
from draftgroup.models import DraftGroup, Player, GameTeam
from draftgroup.classes import DraftGroupManager
from datetime import timedelta, time, datetime
from salary.classes import SalaryGenerator                 # for testing celery
from django.test.utils import override_settings             # for testing celery
from contest.classes import ContestCreator
from contest.models import Contest
from sports.classes import SiteSportManager
from ticket.classes import TicketManager
from util.timeshift import set_system_time, reset_system_time
from random import Random
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from django.contrib.contenttypes.models import ContentType
from lineup.classes import LineupManager

class BuildWorldMixin( object ):
    """
    this class is intended to be inherited by test classes that require
    fundamental things required for submitting lineups (ie: contests)
    """

    DEFAULT_USER_PASSWORD = 'test'

    def build_world(self):
        self.world = BuildWorldForTesting()
        self.world.build_world()

    def create_valid_lineup(self, user):
        self.one = PlayerChild.objects.filter(position =self.world.position1)[0]
        self.two = PlayerChild.objects.filter(position=self.world.position2)[0]
        self.three = PlayerChild.objects.filter(position=self.world.position1)[1]
        self.four = PlayerChild.objects.filter(position=self.world.position2)[1]

        team = [self.one, self.two, self.three]
        for player in team:
            c_type = ContentType.objects.get_for_model(player)
            draftgroup_player = Player.objects.get(salary_player__player_type=c_type,
                                               salary_player__player_id=player.pk,
                                               draft_group=self.world.draftgroup)
            draftgroup_player.salary = 10000
            draftgroup_player.save()

        self.lm = LineupManager(user)
        self.team = [self.one.pk, self.two.pk, self.three.pk]
        self.lineup = self.lm.create_lineup(self.team, self.world.draftgroup)
        return self.lineup

    def create_user(self, username):
        """
        creates a user and gives them $10,000
        :param username:
        :return:
        """
        user = User.objects.create(username=username)
        user.set_password(self.DEFAULT_USER_PASSWORD)
        user.save()

        ct = CashTransaction(user)
        ct.deposit(10000.00)
        return user

class ForceAuthenticateAndRequestMixin( object ):

    def force_authenticate_and_GET(self, user, view_class, url, data=None, **kwargs):
        return self.force_authenticate_and_request(user, view_class, url, data=data, request_type='get', **kwargs)

    def force_authenticate_and_POST(self, user, view_class, url, data=None):
        return self.force_authenticate_and_request(user, view_class, url, data=data, request_type='post')

    def force_authenticate_and_request(self, user, view_class, url, data=None, request_type=None, **kwargs):
        """
        major helper method for testing rest_framework APIs
        so that we dont have to perform prerequisite calls to login
        or use multiple lines of boiler-plate code.

        read this link for more info:
            http://www.django-rest-framework.org/api-guide/testing/
        """
        request = None
        factory = APIRequestFactory()
        view = view_class.as_view()
        # Make an authenticated request to the view...
        if request_type == 'get':
            request = factory.get( url, data )
        elif request_type == 'post':
            request = factory.post( url, data )
        else:
            raise Exception('invalid request_type: %s' % request_type)
        force_authenticate(request, user=user)
        response = view(request, **kwargs)   # response = view(request, param1='val1') will pass GET args between slashes
        return response

# class ReplayNbaTest(object):
#
#     def __init__(self, headsup_contests=10):
#         # the name of the primary user
#         self.hero_username = 'Hero'
#
#         self.r = Random() # we will use a random number generator for a few things
#         # create default ticket amounts
#         TicketManager.create_default_ticket_amounts()
#
#         # number headsups, and GPPs
#         self.max_headsups = headsup_contests
#
#         # the site sport for NBA
#         site_sport_manager = SiteSportManager()
#         self.site_sport = site_sport_manager.get_site_sport( 'nba' )
#         # set the start and end time for contests associated with this replay test (7pm EST)
#         self.start  = timezone.now().replace(year=2015, month=10, day=15, hour=23, minute=0, second=0, microsecond=0)
#         self.end    = self.start + timedelta(hours = 8) # 8 hours ahead of start.
#         # create prize structures to associate with contests
#         self.prize_structure_headsup = self.build_prize_structure_headsup()
#         # create (or get) draft group
#         self.draft_group = self.build_draft_group( self.start, self.end )
#         # create contests
#         self.contest_headsup    = self.build_contest_headsup()
#         self.contest_headsup_id = self.contest_headsup.pk
#
#         #
#         # use replay manager to rewind to before this the time of the contest/draft_group !
#         set_system_time( self.start - timedelta(minutes=5) ) # 3 min previous to start
#
#         #
#         # now that we have rewound time to before the  contest,
#         # use the random lineup create to add lineups, but all validation appplies except for salary!
#         for x in range(0,self.max_headsups):
#             self.clone_and_fill_contest( self.contest_headsup_id )
#
#     def clone_and_fill_contest(self, contest_id):
#         contest = Contest.objects.get( pk = contest_id )
#         contest.spawn() # creates a new copy of the original contest
#         rlc = RandomLineupCreator( self.site_sport.name, self.hero_username ) # always the name of our hero
#         rlc.create( contest.pk )
#         rlc = RandomLineupCreator( self.site_sport.name, self.__get_villain_name() )
#         rlc.create( contest.pk )
#
#     def __get_villain_name(self):
#         """
#         :return: random villain name from: Villain0 thru Villain99
#         """
#         return 'Villain' + str(self.r.randint(0, 100))
#
#     def build_prize_structure_headsup(self):
#         creator = CashPrizeStructureCreator()
#         creator.set_buyin( 5.00 )
#         creator.add( 1, 9.00 )
#         creator.save()
#         return creator.prize_structure
#
#     def build_draft_group(self, start, end):
#         dgm = DraftGroupManager()
#         return dgm.get_for_site_sport( self.site_sport, start, end )
#
#     def build_contest_headsup(self):
#         contest = Contest()
#         contest.site_sport      = self.site_sport
#         contest.start           = self.start
#         contest.end             = self.end
#         contest.draft_group     = self.draft_group
#         contest.name            = 'NBA $5 Head-to-Head'
#         contest.max_entries     = 1
#         contest.entries         = 2
#         contest.respawn         = True
#         contest.prize_structure = self.prize_structure_headsup
#         contest.save()
#
#         return contest
#
#     def play(self, replay_name='nba-thursday-oct-15-2015', offset_minutes=12):
#         """
#
#         :param replay_name:     the name of the replay
#         :param offset_minutes:  the number of minutes to add to the start time, if we want to start in the middle
#         :return:
#         """
#         self.replay_manager.play( replay_name=replay_name, offset_minutes=offset_minutes)
#
#         # print('play() - TODO - replaymanager causes circular import')
#         # pass

class MasterAbstractTest():
    CELERY_TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'

    PASSWORD = 'password'
    def get_user(self, username='username', is_superuser=False,
                 is_staff=False, permissions=[]):
        #
        # get the user if they exist.
        # if they don't exist, create them with the specified status and permissions
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=self.PASSWORD)
            user.email = 'admin@test.com'
        if is_superuser:
            # superuser, by default is also staff
            user.is_superuser   = True
            user.is_staff       = True
        elif is_staff == True and is_superuser == False:
            # staff , but not super user
            user.is_superuser = False
            user.is_staff = True

            # if there are specified permissions, apply them to the staff
            for perm in permissions:
                user.user_permissions.add( perm )
        else:
            # basic user
            user.is_superuser = False
            user.is_staff   = False

        user.save()

        return user

    def get_admin_user(self, username='admin'):
        user = self.get_user(username=username, is_superuser=True,
                        is_staff=True)
        return user

    def get_staff_user(self, username='staff', permissions=[]):
        user = self.get_user(username=username, is_superuser=False,
                        is_staff=True, permissions=permissions)
        return user

    def get_basic_user(self, username='basic'):
        user = self.get_user(username=username, is_superuser=False,
                        is_staff=False)
        return user

    def get_alternate_user(self, existing_user):
        """
        return a user who is different from the existing user argument,
        by at least its primary key (pk) and username.

        is_superuser & is_staff should also match.

        permissions will not match however

        :param existing_user:
        :return:
        """
        return self.get_user(username=existing_user.username + 'alt',
                             is_superuser=existing_user.is_superuser,
                             is_staff=existing_user.is_staff )

    def get_password(self):
        return self.PASSWORD



class AbstractTest(django.test.TestCase, MasterAbstractTest):

    def setUp(self):
        pass

    def concurrent_test(self, times, test_func, *args, **kwargs ):
        exceptions = []
        def call_test_func():
            try:
                test_func(*args, **kwargs)
            except Exception as e:
                exceptions.append(e)
                print(str(e))
                #print(traceback.format_exc())

            for conn in connections.all():
                conn.close()
        threads = []
        for i in range(times):
            threads.append(threading.Thread(target=call_test_func))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        return exceptions

# class AbstractTestTransaction(django.test.TransactionTestCase, MasterAbstractTest):
#     """
#     WARNING: AbstractTestTransaction PRE-WIPES the test database when it runs!
#
#     this is very annoying, since we install a few basic objects for the site
#     during migrations! make sure you know what you are doing if you use
#     this class, and dont expect ANYTHING to exist when it calls its setUp() method!
#     """
#     pre_flush = True
#
#     def setUp(self):
#         pass
#
#     def concurrent_test(self, times, test_func, *args, **kwargs ):
#         exceptions = []
#         def call_test_func():
#             try:
#                 test_func(*args, **kwargs)
#             except Exception as e:
#                 exceptions.append(e)
#                 print(str(e))
#                 #print(traceback.format_exc())
#
#             for conn in connections.all():
#                 conn.close()
#         threads = []
#         for i in range(times):
#             threads.append(threading.Thread(target=call_test_func))
#         for t in threads:
#             t.start()
#         for t in threads:
#             t.join()
#
#         return exceptions

class BuildWorldForTesting(object):

    def build_world(self):
        TicketManager.create_default_ticket_amounts()
        self.create_sport_and_rosters()
        self.create_simple_player_stats_list()
        self.create_pool_and_draftgroup()
        self.create_contest()

    #-------------------------------------------------------------------
    #-------------------------------------------------------------------
    # Shared setup methods for the test cases
    def create_sport_and_rosters(self):
        self.sitesport       = SiteSport()
        self.sitesport.name  = 'test'
        self.sitesport.save()

        position1                = Position()
        position1.name           = "1"
        position1.site_sport     = self.sitesport
        position1.save()
        self.position1 = position1

        position2                = Position()
        position2.name           = "2"
        position2.site_sport     = self.sitesport
        position2.save()
        self.position2 = position2

        rosterspot1             = RosterSpot()
        rosterspot1.name        = 'one'
        rosterspot1.site_sport  = self.sitesport
        rosterspot1.amount      = 1
        rosterspot1.idx         = 0
        rosterspot1.save()

        rosterspot2             = RosterSpot()
        rosterspot2.name        = 'two'
        rosterspot2.site_sport  = self.sitesport
        rosterspot2.amount      = 1
        rosterspot2.idx         = 1
        rosterspot2.save()

        rosterspot3             = RosterSpot()
        rosterspot3.name        = 'flex'
        rosterspot3.site_sport  = self.sitesport
        rosterspot3.amount      = 1
        rosterspot3.idx         = 2
        rosterspot3.save()

        maptable                = RosterSpotPosition()
        maptable.position       = position1
        maptable.roster_spot    = rosterspot1
        maptable.is_primary     = True
        maptable.save()

        maptable                = RosterSpotPosition()
        maptable.position       = position1
        maptable.roster_spot    = rosterspot3
        maptable.is_primary     = False

        maptable.save()

        maptable                = RosterSpotPosition()
        maptable.position       = position2
        maptable.roster_spot    = rosterspot2
        maptable.is_primary     = True

        maptable.save()

        maptable                = RosterSpotPosition()
        maptable.position       = position2
        maptable.roster_spot    = rosterspot3
        maptable.is_primary     = False

        maptable.save()

        return self.sitesport


    def create_simple_player_stats_list(self):

        players = []
        position1 = Position.objects.get(name="1")
        position2 = Position.objects.get(name="2")

        for i in range(10,20):
            player                          = PlayerChild()
            player.srid                     = ""+str(i)
            player.first_name               = ""+str(i)
            player.last_name                = ""+str(i)
            player.created                  = timezone.now()
            if(i < 15):
                player.position             = position1
            else:
                player.position             = position2

            player.save()
            players.append(player)

        for i in range(1,30):

            d =timezone.now() - timedelta(days=i)
            game                            = GameChild()
            game.created                    = d
            game.srid                       = i
            game.start                      = d
            game.status                     = "closed"
            game.save()
            for player in players:
                num = int(player.srid)
                low = (num -4 if num -4 >= 0 else 0)
                high = num +4
                player_stats                    = PlayerStatsChild()
                player_stats.created            = d
                player_stats.fantasy_points     = randint(low,high)
                player_stats.game               = game
                player_stats.player             = player
                player_stats.srid_game          = game.srid
                player_stats.srid_player        = player.srid
                player_stats.position           = player.position
                player_stats.save()


    def create_pool_and_draftgroup(self):
        self.salary_conf                                    = SalaryConfig()
        self.salary_conf.trailing_games                     = 10
        self.salary_conf.days_since_last_game_flag          = 10
        self.salary_conf.min_games_flag                     = 7
        self.salary_conf.min_player_salary                  = 3000
        self.salary_conf.max_team_salary                    = 50000
        self.salary_conf.min_avg_fppg_allowed_for_avg_calc  = 5
        self.salary_conf.save()

        self.pool = Pool()
        self.pool.site_sport = self.sitesport
        self.pool.salary_config = self.salary_conf
        self.pool.save()

        self.createTrailingGameWeight(self.salary_conf, 3,3)
        self.createTrailingGameWeight(self.salary_conf, 7,2)
        self.createTrailingGameWeight(self.salary_conf, 10,1)


        now = timezone.now()
        start = DfsDateTimeUtil.create(now.date() + timedelta(days=1), time(23,0))
        end = DfsDateTimeUtil.create(now.date() + timedelta(days=2), time(0,0))
        self.draftgroup = DraftGroup()
        self.draftgroup.start = start
        self.draftgroup.end = end
        self.draftgroup.salary_pool = Pool.objects.all()[0]
        self.draftgroup.save()


        player_stats_classes = [
            PlayerStatsChild
        ]

        gameteam = GameTeam()
        gameteam.start = self.draftgroup.start
        gameteam.game_srid = "1"
        gameteam.draft_group = self.draftgroup
        gameteam.team_srid = "1"
        gameteam.save()

        salary_gen =SalaryGenerator(player_stats_classes, self.pool)
        salary_gen.generate_salaries()
        player_salaries = Salary.objects.all()
        for player in player_salaries:
            dgp = Player()
            dgp.draft_group = self.draftgroup
            dgp.salary_player = player
            dgp.game_team = gameteam
            dgp.salary = player.amount
            dgp.start = timezone.now() + timedelta(hours=1)
            dgp.save()

    def create_contest(self):

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
        cps.set_buyin(self.buyin)
        cps.save()
        #cps.prize_structure.buyin = self.buyin
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

    def createTrailingGameWeight(self, salary_config, through, weight):
        trailing_game_weight                        = TrailingGameWeight()
        trailing_game_weight.salary                 = salary_config
        trailing_game_weight.through                = through
        trailing_game_weight.weight                 = weight
        trailing_game_weight.save()

    def get_scheduled_contest(self):
        original_contest_id = self.contest.pk
        self.contest.spawn()
        new_contest = self.contest
        self.contest = Contest.objects.get(pk=original_contest_id)

        new_contest.draft_group = self.draftgroup
        new_contest.start += timedelta(hours=1)
        new_contest.status = Contest.SCHEDULED
        new_contest.save()
        return new_contest