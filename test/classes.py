import django.test
import threading
from django.db import connections
from mock import patch
from prize.classes import CashPrizeStructureCreator
from cash.classes import CashTransaction
from test.models import (
    PlayerChild,
    TeamChild,
    PlayerStatsChild,
    GameChild,
    Season as SeasonChild,
)
from django.utils import timezone
from random import randint, choice
from sports.models import SiteSport, Position
from roster.models import RosterSpot, RosterSpotPosition
from salary.models import SalaryConfig, Pool, TrailingGameWeight, Salary
from dataden.util.timestamp import DfsDateTimeUtil
from draftgroup.models import DraftGroup, Player, GameTeam
from datetime import timedelta, time, datetime
from salary.classes import SalaryGenerator  # for testing celery
# from django.test.utils import override_settings  # for testing celery
from contest.classes import ContestCreator
from contest.models import Contest
from ticket.classes import TicketManager
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from django.contrib.contenttypes.models import ContentType
from lineup.classes import LineupManager
from scoring.classes import AbstractScoreSystem
from scoring.models import ScoreSystem
from django.contrib.auth.models import User
from account.classes import AccountInformation
from account.models import Information
import datetime


class ResetDatabaseMixin(object):
    exclude_apps = ['admin', 'auth', 'contenttypes', 'sessions', 'django_celery_beat']

    def setUp(self):
        self.reset_db()

    def reset_db(self):
        # from django.contrib.contenttypes.models import ContentType
        start = timezone.now()
        for content_type in ContentType.objects.all().exclude(app_label__in=self.exclude_apps):
            # delete all rows of any models we find
            print(str(content_type.app_label), str(content_type.model))
            content_type.model_class().objects.all().delete()
        print('total delete time (seconds):', str((timezone.now() - start).total_seconds()))


class TestSalaryScoreSystem(AbstractScoreSystem):
    """
    defines a test score system
    """
    THE_SPORT = 'test'

    FANTASY_POINTS = 'fantasy_points'

    def __init__(self):
        self.score_system, created = ScoreSystem.objects.get_or_create(sport=self.THE_SPORT, name='salary')

        #
        # call super last - it will perform validation and ensure proper setup
        super().__init__(self.THE_SPORT)

    def get_primary_player_stats_class_for_player(self, player):
        """
        override
        """
        return PlayerStatsChild

    def score_player(self, player_stats, verbose=True):
        """
        return the fantasy points already set as the new fantasy_points for simplicity in testing
        """
        self.set_verbose(verbose)
        return player_stats.fantasy_points


class BuildWorldMixin(object):
    """
    this class is intended to be inherited by test classes that require
    fundamental things required for submitting lineups (ie: contests)
    """

    DEFAULT_USER_PASSWORD = 'test'

    def build_world(self):
        self.world = BuildWorldForTesting()
        self.world.build_world()

    def get_or_create_player(self):
        # player, created = PlayerChild.objects.get_or_create()
        # TODO
        pass

    def create_valid_lineup(self, user):
        players_pos_1 = PlayerChild.objects.filter(position=self.world.position1).distinct('team')
        players_pos_2 = PlayerChild.objects.filter(position=self.world.position2).order_by('-team').distinct('team')
        self.one = players_pos_1[0]
        self.two = players_pos_2[0]
        self.three = players_pos_1[1]
        self.four = players_pos_2[1]

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
        Information.objects.create(user=user)
        ct = CashTransaction(user)
        ct.deposit(10000.00)
        return user


class ForceAuthenticateAndRequestMixin(object):
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
            request = factory.get(url, data)
        elif request_type == 'post':
            request = factory.post(url, data)
        else:
            raise Exception('invalid request_type: %s' % request_type)
        force_authenticate(request, user=user)
        response = view(request, **kwargs)  # response = view(request, param1='val1') will pass GET args between slashes
        return response


class MasterAbstractTest():
    PASSWORD = 'password'

    def get_user(self, username='username', is_superuser=False,
                 is_staff=False, permissions=[]):
        #
        # get the user if they exist.
        # if they don't exist, create them with the specified status and permissions
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=self.PASSWORD)
            user.email = 'admin@test.com'
        if is_superuser:
            # superuser, by default is also staff
            user.is_superuser = True
            user.is_staff = True
        elif is_staff == True and is_superuser == False:
            # staff , but not super user
            user.is_superuser = False
            user.is_staff = True

            # if there are specified permissions, apply them to the staff
            for perm in permissions:
                user.user_permissions.add(perm)
        else:
            # basic user
            user.is_superuser = False
            user.is_staff = False

        user.save()

        return user

    def get_user_with_account_information(self, username='userWithInformation'):
        user = self.get_user(username)
        info = AccountInformation(user)
        info.set_fields(fullname='',  # user.first_name + ' ' + user.last_name,
                        address1='1 Draftboard Drive',
                        city='Draft City', state='NH',
                        dob=datetime.date(1995, 12, 25))
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
                             is_staff=existing_user.is_staff)

    def get_password(self):
        return self.PASSWORD


class TestSalaryScoreSystem(AbstractScoreSystem):
    """
    defines a test score system
    """
    THE_SPORT = 'test'
    THE_TYPE = 'salary'

    STAT_A = 'stat_a'  # a statistic named 'stat_a'
    STAT_B = 'stat_b'  # a statistic named 'stat_b'

    def __init__(self, the_sport=None, the_type=None):
        if the_sport is None:
            the_sport = self.THE_SPORT
        if the_type is None:
            the_type = self.THE_TYPE

        self.score_system, created = ScoreSystem.objects.get_or_create(sport=the_sport, name=the_type)

        #
        # call super last - it will perform validation and ensure proper setup
        super().__init__(self.THE_SPORT, validate=False)

    def get_primary_player_stats_class_for_player(self, player):
        """
        override
        """
        return PlayerStatsChild

    def score_player(self, player_stats, verbose=True):
        """
        return the fantasy points accrued by this nba PlayerStats object
        """
        self.set_verbose(verbose)

        total = 0
        total += self.points(player_stats.points)
        total += self.three_pms(player_stats.three_points_made)
        total += self.rebounds(player_stats.rebounds)
        total += self.assists(player_stats.assists)
        total += self.steals(player_stats.steals)
        total += self.blocks(player_stats.blocks)
        total += self.turnovers(player_stats.turnovers)

        #
        # to determined a dbl-dbl or triple-dbl, we have to pass the whole object
        if self.get_tpl_dbl(player_stats):
            total += self.triple_double(self.get_tpl_dbl(player_stats))
        else:
            total += self.double_double(self.get_dbl_dbl(player_stats))
        return total

    def points(self, value):
        if self.verbose: self.str_stats += '%s Pts ' % value
        return value * self.get_value_of(self.POINT)

    def three_pms(self, value):
        if self.verbose: self.str_stats += '%s ThreePm ' % value
        return value * self.get_value_of(self.THREE_PM)

    def rebounds(self, value):
        if self.verbose: self.str_stats += '%s Reb ' % value
        return value * self.get_value_of(self.REBOUND)

    def assists(self, value):
        if self.verbose: self.str_stats += '%s Ast ' % value
        return value * self.get_value_of(self.ASSIST)

    def steals(self, value):
        if self.verbose: self.str_stats += '%s Stl ' % value
        return value * self.get_value_of(self.STEAL)

    def blocks(self, value):
        if self.verbose: self.str_stats += '%s Blk ' % value
        return value * self.get_value_of(self.BLOCK)

    def turnovers(self, value):
        if self.verbose: self.str_stats += '%s TO ' % value
        return value * self.get_value_of(self.TURNOVER)

    def double_double(self, value):
        if self.verbose: self.str_stats += '%s DblDbl ' % value
        return value * self.get_value_of(self.DBL_DBL)

    def triple_double(self, value):
        if self.verbose: self.str_stats += '%s TrpDbl ' % value
        return value * self.get_value_of(self.TRIPLE_DBL)

    # return int(1) if player_stats have a double double.
    # a double-double is TWO or more categories from
    # the list with at least a value of 10:
    #           [points, rebs, asts, blks, steals]
    def get_dbl_dbl(self, player_stats):
        return int(self.__double_digits_count(player_stats) == 2)

    # return int(1) if player_stats have a triple double.
    # a triple double is THREE or more categories from
    # the list with at least a value of 10:
    #           [points, rebs, asts, blks, steals]
    def get_tpl_dbl(self, player_stats):
        return int(self.__double_digits_count(player_stats) >= 3)

    def __double_digits_count(self, player_stats):
        l = [
            player_stats.points,
            player_stats.rebounds,
            player_stats.assists,
            player_stats.blocks,
            player_stats.steals
        ]
        #
        # create a list where we have replaced 10.0+ with int(1),
        # and lesss than 10.0 with int(0).  then sum the list
        # and return that value - thats how many "doubles" we have
        return sum([1 if x >= 10.0 else 0 for x in l])


class AbstractTest(django.test.TestCase, MasterAbstractTest):
    def setUp(self):
        self.patcher = patch('push.classes.AbstractPush.send', lambda *args, **kwargs: '')
        self.patcher.start()

    def concurrent_test(self, times, test_func, *args, **kwargs):
        exceptions = []

        def call_test_func():
            test_func(*args, **kwargs)

            # try:
            # except Exception as e:
            #     exceptions.append(e)
            #     print(str(e))
                # print(traceback.format_exc())

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

    def tearDown(self):
        if hasattr(self, 'patcher'):
            self.patcher.stop()
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

def create_site_sports():
    sports = ['test', 'nfl', 'mlb', 'nba', 'nhl']
    # seasons = [  1999,    2015,   2016,   2015,   2015 ]

    current_season = timezone.now().year  # use the year that it is currently
    for sport in sports:
        site_sport = None
        created = False
        try:
            site_sport = SiteSport.objects.get(name=sport)
        except SiteSport.DoesNotExist:
            # create it
            site_sport, created = SiteSport.objects.get_or_create(name=sport,
                                                                  current_season=current_season)
        # print('SiteSport [%s] just created -> %s' % (str(site_sport), str(created)))


class BuildWorldForTesting(object):
    sport = 'test'

    def build_world(self):
        TicketManager.create_default_ticket_amounts()
        self.create_site_sports()
        self.create_sport_and_rosters()
        self.create_simple_player_stats_list()
        self.create_pool_and_draftgroup()
        self.create_contest()

    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    def create_site_sports(self):
        create_site_sports()

    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # Shared setup methods for the test cases
    def create_sport_and_rosters(self):
        self.sitesport = SiteSport.objects.get(name=self.sport)

        position1 = Position()
        position1.name = "1"
        position1.site_sport = self.sitesport
        position1.save()
        self.position1 = position1

        position2 = Position()
        position2.name = "2"
        position2.site_sport = self.sitesport
        position2.save()
        self.position2 = position2

        rosterspot1 = RosterSpot()
        rosterspot1.name = 'one'
        rosterspot1.site_sport = self.sitesport
        rosterspot1.amount = 1
        rosterspot1.idx = 0
        rosterspot1.save()

        rosterspot2 = RosterSpot()
        rosterspot2.name = 'two'
        rosterspot2.site_sport = self.sitesport
        rosterspot2.amount = 1
        rosterspot2.idx = 1
        rosterspot2.save()

        rosterspot3 = RosterSpot()
        rosterspot3.name = 'flex'
        rosterspot3.site_sport = self.sitesport
        rosterspot3.amount = 1
        rosterspot3.idx = 2
        rosterspot3.save()

        maptable = RosterSpotPosition()
        maptable.position = position1
        maptable.roster_spot = rosterspot1
        maptable.is_primary = True
        maptable.save()

        maptable = RosterSpotPosition()
        maptable.position = position1
        maptable.roster_spot = rosterspot3
        maptable.is_primary = False

        maptable.save()

        maptable = RosterSpotPosition()
        maptable.position = position2
        maptable.roster_spot = rosterspot2
        maptable.is_primary = True

        maptable.save()

        maptable = RosterSpotPosition()
        maptable.position = position2
        maptable.roster_spot = rosterspot3
        maptable.is_primary = False

        maptable.save()

        return self.sitesport

    def create_simple_player_stats_list(self):

        players = []
        position1 = Position.objects.get(name="1")
        position2 = Position.objects.get(name="2")
        team1 = TeamChild.objects.create(name='test1', srid='test1')
        team2 = TeamChild.objects.create(name='test2', srid='test2')
        team3 = TeamChild.objects.create(name='test3', srid='test3')
        for i in range(10,20):
            player = PlayerChild()
            player.srid = ""+str(i)
            player.first_name = ""+str(i)
            player.last_name = ""+str(i)
            if i < 14:
                player.team = team1
            elif i > 13 and i < 17:
                player.team = team2
            else:
                player.team = team3
            player.created = timezone.now()
            if(i < 15):
                player.position = position1
            else:
                player.position = position2

            player.save()
            players.append(player)

        for i in range(1, 30):

            d = timezone.now() - timedelta(days=i)
            game = GameChild()
            game.season, created = SeasonChild.objects.get_or_create(srid='seasonchild-srid', season_year=2015,
                                                                     season_type='reg')
            game.created = d
            game.srid = i
            game.start = d
            game.status = "closed"
            game.save()
            for player in players:
                num = int(player.srid)
                low = (num - 4 if num - 4 >= 0 else 0)
                high = num + 4
                player_stats = PlayerStatsChild()
                player_stats.created = d
                player_stats.fantasy_points = randint(low, high)
                player_stats.game = game
                player_stats.player = player
                player_stats.srid_game = game.srid
                player_stats.srid_player = player.srid
                player_stats.position = player.position
                player_stats.save()

    def create_pool_and_draftgroup(self):
        self.salary_conf = SalaryConfig()
        self.salary_conf.trailing_games = 10
        self.salary_conf.days_since_last_game_flag = 10
        self.salary_conf.min_games_flag = 7
        self.salary_conf.min_player_salary = 3000
        self.salary_conf.max_team_salary = 50000
        self.salary_conf.min_avg_fppg_allowed_for_avg_calc = 5
        self.salary_conf.save()

        self.pool = Pool()
        self.pool.site_sport = self.sitesport
        self.pool.salary_config = self.salary_conf
        self.pool.save()

        self.createTrailingGameWeight(self.salary_conf, 3, 3)
        self.createTrailingGameWeight(self.salary_conf, 7, 2)
        self.createTrailingGameWeight(self.salary_conf, 10, 1)

        now = timezone.now()
        start = DfsDateTimeUtil.create(now.date() + timedelta(days=1), time(23, 0))
        end = DfsDateTimeUtil.create(now.date() + timedelta(days=2), time(0, 0))
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

        salary_gen = SalaryGenerator(player_stats_classes, self.pool)
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
        # ensure it exists for testing purposes
        self.create_site_sports()

        self.first = 100.0
        self.second = 50.0
        self.third = 25.0

        #
        # create a simple Rank and Prize Structure
        self.buyin = 10
        cps = CashPrizeStructureCreator(name='test')
        cps.add(1, self.first)
        cps.add(2, self.second)
        cps.add(3, self.third)
        cps.set_buyin(self.buyin)
        cps.save()
        # cps.prize_structure.buyin = self.buyin
        cps.prize_structure.save()

        self.prize_structure = cps.prize_structure
        self.ranks = cps.ranks
        #
        # create the Contest
        now = timezone.now()
        start = DfsDateTimeUtil.create(now.date(), time(23, 0))
        end = DfsDateTimeUtil.create(now.date() + timedelta(days=1), time(0, 0))
        cc = ContestCreator("test_contest", "nfl", self.prize_structure, start, end)
        self.contest = cc.create()
        self.contest.status = Contest.RESERVABLE
        self.contest.save()

    def createTrailingGameWeight(self, salary_config, through, weight):
        trailing_game_weight = TrailingGameWeight()
        trailing_game_weight.salary = salary_config
        trailing_game_weight.through = through
        trailing_game_weight.weight = weight
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
