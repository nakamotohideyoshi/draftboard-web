import django.test
from django.contrib.auth.models import User
import threading
from django.db import connections
import traceback
from sports.classes import SiteSport

from test.models import PlayerChild, PlayerStatsChild, GameChild
from django.utils import timezone
from datetime import timedelta
from random import randint
from sports.models import SiteSport, Position
from roster.models import RosterSpot, RosterSpotPosition
from salary.models import SalaryConfig, Pool, TrailingGameWeight, Salary
from dataden.util.timestamp import DfsDateTimeUtil
from draftgroup.models import DraftGroup, Player
from datetime import timedelta, time
from salary.classes import SalaryGenerator
#
class MasterAbstractTest():

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



class AbstractTestTransaction(django.test.TransactionTestCase, MasterAbstractTest):

    def setUp(self):
        pass

    def concurrent_test(self, times, test_func, *args, **kwargs ):
        exceptions = []
        def call_test_func():
            try:
                test_func(*args, **kwargs)
            except Exception as e:
                exceptions.append(e)
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

class BuildWorldForTesting(object):

    def build_world(self):
        self.create_sport_and_rosters()
        self.create_simple_player_stats_list()
        self.create_pool_and_draftgroup()
        pass
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
        start = DfsDateTimeUtil.create(now.date(), time(23,0))
        end = DfsDateTimeUtil.create(now.date() + timedelta(days=1), time(0,0))
        self.draftgroup = DraftGroup()
        self.draftgroup.start = start
        self.draftgroup.end = end
        self.draftgroup.salary_pool = Pool.objects.all()[0]
        self.draftgroup.save()


        player_stats_classes = [
            PlayerStatsChild
        ]

        salary_gen =SalaryGenerator(player_stats_classes, self.pool)
        salary_gen.generate_salaries()
        player_salaries = Salary.objects.all()
        for player in player_salaries:
            dgp = Player()
            dgp.draft_group = self.draftgroup
            dgp.salary_player = player
            dgp.salary = player.amount
            dgp.save()


    def createTrailingGameWeight(self, salary_config, through, weight):
        trailing_game_weight                        = TrailingGameWeight()
        trailing_game_weight.salary                 = salary_config
        trailing_game_weight.through                = through
        trailing_game_weight.weight                 = weight
        trailing_game_weight.save()