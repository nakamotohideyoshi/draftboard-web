from test.classes import AbstractTest
import mysite.exceptions
from test.models import PlayerChild, PlayerStatsChild, GameChild
from django.utils import timezone
from .classes import SalaryPlayerStatsObject, SalaryGenerator, SalaryPlayerObject
from datetime import date, timedelta
from random import randint
from .models import SalaryConfig, TrailingGameWeight, Pool
from sports.models import SiteSport, Position
from roster.models import RosterSpot, RosterSpotPosition

#
# quick caleb test of dummy data class
from salary.dummy import Dummy
class SomeTest(AbstractTest):
    def setUp(self):
        #self.roster_spot_positions  = Dummy.create_roster()
        #self.player_stats_list      = Dummy.create_player_stats_list()

        # generate_salaries()
        Dummy.generate_salaries()

    def test_it(self):
        pass

#-------------------------------------------------------------------
#-------------------------------------------------------------------
# Shared setup methods for the test cases
def create_sport_and_rosters():
    sitesport       = SiteSport()
    sitesport.name  = 'testsport'
    sitesport.save()

    position1                = Position()
    position1.name           = "1"
    position1.site_sport     = sitesport
    position1.save()

    position2                = Position()
    position2.name           = "2"
    position2.site_sport     = sitesport
    position2.save()

    rosterspot1             = RosterSpot()
    rosterspot1.name        = 'one'
    rosterspot1.site_sport  = sitesport
    rosterspot1.amount      = 1
    rosterspot1.idx         = 0
    rosterspot1.save()

    rosterspot2             = RosterSpot()
    rosterspot2.name        = 'two'
    rosterspot2.site_sport  = sitesport
    rosterspot2.amount      = 1
    rosterspot2.idx         = 1
    rosterspot2.save()

    rosterspot3             = RosterSpot()
    rosterspot3.name        = 'flex'
    rosterspot3.site_sport  = sitesport
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

    return sitesport

def create_basic_player_stats():
    position = Position.objects.get(name="1")

    game                            = GameChild()
    game.created                    = timezone.now()
    game.srid                       = "1121231232"
    game.start                      = timezone.now()
    game.status                     = "closed"
    game.save()

    player                          = PlayerChild()
    player.srid                     = "111111111"
    player.first_name               = "Jon"
    player.last_name                = "Doe"
    player.created                  = timezone.now()
    player.position                 = position
    player.save()

    player_stats                    = PlayerStatsChild()
    player_stats.created            = timezone.now()
    player_stats.fantasy_points     = 15
    player_stats.game               = game
    player_stats.player             = player
    player_stats.srid_game          = game.srid
    player_stats.srid_player        = player.srid
    player_stats.position           = position
    player_stats.save()

    return player_stats


def create_simple_player_stats_list():

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

#-------------------------------------------------------------------
#-------------------------------------------------------------------
# Tests the Player Stats Object
class PlayerStatsObjectTest(AbstractTest):
    def setUp(self):
        create_sport_and_rosters()
        self.player_stats = create_basic_player_stats()

    def test_proper_init(self):
        self.assertIsNotNone(SalaryPlayerStatsObject(self.player_stats))

    def test_improper_init(self):
        self.assertRaises(mysite.exceptions.IncorrectVariableTypeException,
                          lambda: SalaryPlayerStatsObject(1))

    def test_missing_data_types (self):
        self.player_stats.fantasy_points = None
        self.assertRaises(mysite.exceptions.NullModelValuesException,
                          lambda: SalaryPlayerStatsObject(self.player_stats))

#-------------------------------------------------------------------
#-------------------------------------------------------------------
# Tests the Salary Generator
class SalaryGeneratorTest(AbstractTest):
    def setUp(self):
        self.site_sport = create_sport_and_rosters()

        self.salary_conf                                    = SalaryConfig()
        self.salary_conf.trailing_games                     = 10
        self.salary_conf.days_since_last_game_flag          = 10
        self.salary_conf.min_games_flag                     = 7
        self.salary_conf.min_player_salary                  = 3000
        self.salary_conf.max_team_salary                    = 50000
        self.salary_conf.min_avg_fppg_allowed_for_avg_calc  = 5
        self.salary_conf.save()

        self.pool = Pool()
        self.pool.site_sport = self.site_sport
        self.pool.salary_config = self.salary_conf
        self.pool.save()

        self.createTrailingGameWeight(self.salary_conf, 3,3)
        self.createTrailingGameWeight(self.salary_conf, 7,2)
        self.createTrailingGameWeight(self.salary_conf, 10,1)

        self.position1 = Position.objects.get(name="1")

    def createTrailingGameWeight(self, salary_config, through, weight):
        trailing_game_weight                        = TrailingGameWeight()
        trailing_game_weight.salary                 = salary_config
        trailing_game_weight.through                = through
        trailing_game_weight.weight                 = weight
        trailing_game_weight.save()



    def test_proper_init(self):
        self.assertIsNotNone(SalaryGenerator(PlayerStatsChild, self.pool))

    def test_improper_init(self):
        self.assertRaises(mysite.exceptions.IncorrectVariableTypeException,
                    lambda: SalaryGenerator(SalaryPlayerStatsObject, self.pool))

    def test_generate_salaries(self):
        create_simple_player_stats_list()
        player_stats_classes = [
            PlayerStatsChild
        ]
        salary_gen =SalaryGenerator(player_stats_classes, self.pool)
        salary_gen.generate_salaries()

    def test_helper_get_player_stats(self):
        create_simple_player_stats_list()
        player_stats_classes = [
            PlayerStatsChild
        ]
        salary_gen = SalaryGenerator(player_stats_classes, self.pool)
        players = salary_gen.helper_get_player_stats()

        self.assertEquals(len(players) , 10)
        self.assertEquals(len(players[0].player_stats_list) , 29)

    def test_helper_get_average_score_per_position(self):
        player_stats_classes = [
            PlayerStatsChild
        ]
        salary_gen = SalaryGenerator(player_stats_classes, self.pool)
        players = []

        #
        # Creates player stat with 1 fppg under the min for keeping the average
        d =timezone.now()
        game                            = GameChild()
        game.created                    = ""
        game.srid                       = ""
        game.start                      = d
        game.status                     = "closed"
        game.save()
        player                          = PlayerChild()
        player.srid                     = "111111111"
        player.first_name               = "Jon"
        player.last_name                = "Doe"
        player.created                  = timezone.now()
        player.position                 = self.position1
        player.save()
        player_stats                    = PlayerStatsChild()
        player_stats.created            = timezone.now()
        player_stats.fantasy_points     = 4
        player_stats.game               = game
        player_stats.player             = player
        player_stats.srid_game          = game.srid
        player_stats.srid_player        = player.srid
        player_stats.position           = self.position1
        player_stats.save()

        player_stats_object = SalaryPlayerStatsObject(player_stats)

        #
        # test to make sure that the player is not added
        player = SalaryPlayerObject()
        player.player_id = player_stats_object.player_id
        player.player =player_stats_object.player
        player.player_stats_list = [player_stats_object]
        players.append(player)
        self.assertEquals(0, len(salary_gen.helper_get_average_score_per_position(players)))

        #
        # tests equal to the min
        player_stats_object.fantasy_points     =5
        player = SalaryPlayerObject()
        player.player_id = player_stats_object.player_id
        player.player =player_stats_object.player
        player.player_stats_list = [player_stats_object]
        players.append(player)
        self.assertEquals(1, len(salary_gen.helper_get_average_score_per_position(players)))

class CreateActivePoolAndSideEffectExisting(AbstractTest):
    """
    There are 4 cases - "expected" is what each pools 'active' should
    be after both pools have been created

      1) existing_pool.active = False & new_pool.active = False
                      expected: False                     False

      2) existing_pool.active = True  & new_pool.active = False
                      expected: True                      False

      3) existing_pool.active = True  & new_pool.active = True
                      expected: False(!)                  True

      4) existing_pool.active = False & new_pool.active = True
                      expected: False                     True
    """

    def setUp(self):
        """
        create a fake site_sport for use by test functions
        """
        self.site_sport, c      = SiteSport.objects.get_or_create(name='test')

    def test_pool_save_method_case_1(self):
        """
        Case 1

        Create two pools which are both inactive, and make sure they both remain inactive
        after all are created
        """
        existing_config    = Dummy.create_salary_config()
        existing_pool, c   = Pool.objects.get_or_create(salary_config=existing_config,
                                                        site_sport=self.site_sport,
                                                        active=False)
        existing_inactive_pools = Pool.objects.filter(active=False, site_sport=self.site_sport)
        number_pools = len(existing_inactive_pools)
        self.assertEqual( int(1), number_pools )    # should only be one
        inactive_pool = existing_inactive_pools[0]    # later on well want this inactive pool

        # create a new pool, also as inactive
        new_pool                = Pool()
        new_pool.active         = False    # <----
        new_pool.salary_config  = Dummy.create_salary_config()
        new_pool.site_sport     = self.site_sport
        new_pool.save()

        # make sure all pools in the database for this site_sport are inactive still
        all_pools = Pool.objects.filter(site_sport=self.site_sport)
        self.assertEqual( 2, len(all_pools) )
        for p in all_pools:
            self.assertFalse( p.active ) # both should be inactive

    def test_pool_save_method_case_2(self):
        """
        Case 2

        Create the first pool as being active, and the new pool as being inactive,
        and make sure they remain that way after both are created.
        """
        existing_config    = Dummy.create_salary_config()
        existing_pool, c   = Pool.objects.get_or_create(salary_config=existing_config,
                                                        site_sport=self.site_sport,
                                                        active=True)

        existing_active_pools = Pool.objects.filter(active=True, site_sport=self.site_sport)
        number_pools = len(existing_active_pools)
        self.assertEqual( int(1), number_pools ) # should only be one
        active_pool = existing_active_pools[0]   # later on well want the active_pool

        # create a new pool, set to inactive
        new_pool                = Pool()
        new_pool.active         = False    # <----
        new_pool.salary_config  = Dummy.create_salary_config()
        new_pool.site_sport     = self.site_sport
        new_pool.save()

        # make sure the existing pool remains active, and the new pool inactive
        all_pools = Pool.objects.filter(site_sport=self.site_sport)
        self.assertEqual( 2, len(all_pools) )  # 2 total , the existing and new Pool
        for p in all_pools:
            if p.pk == existing_pool.pk:
                self.assertTrue( p.active ) # the new_pool should be the only active
            else:
                self.assertFalse( p.active ) # all other (ie: the new pool) should not be active

    def test_pool_save_method_case_3(self):
        """
        Case 3

        In this test, we create a pool as active, and then create
        another pool thats active and the FIRST pool should
        get its 'active' field set to False !!!
        """

        existing_config    = Dummy.create_salary_config()
        existing_pool, c   = Pool.objects.get_or_create(salary_config=existing_config,
                                                        site_sport=self.site_sport,
                                                        active=True)

        existing_active_pools = Pool.objects.filter(active=True, site_sport=self.site_sport)
        number_pools = len(existing_active_pools)
        self.assertEqual( int(1), number_pools ) # should only be one
        active_pool = existing_active_pools[0]   # later on well want the active_pool

        # now do what we came here to do - create a new active pool,
        # then requery for all active, and make sure the new one is the only one!
        new_pool                = Pool()
        new_pool.active         = True     # <----
        new_pool.salary_config  = Dummy.create_salary_config()
        new_pool.site_sport     = self.site_sport
        new_pool.save()

        # now get them all
        all_pools = Pool.objects.filter(site_sport=self.site_sport)
        self.assertEqual( 2, len(all_pools) ) # 1 because the new_pool should be the only active=True!
        for p in all_pools:
            if p.pk == new_pool.pk:
                self.assertTrue( p.active ) # the new_pool should be the only active
            else:
                self.assertFalse( p.active ) # else it should be false

    def test_pool_save_method_case_4(self):
        """
        Case 4

        Create the first pool as being inactive, and the second pool as being active,
        and make sure they remain that way after both are created.
        """
        existing_config    = Dummy.create_salary_config()
        existing_pool, c   = Pool.objects.get_or_create(salary_config=existing_config,
                                                        site_sport=self.site_sport,
                                                        active=False)
        existing_inactive_pools = Pool.objects.filter(active=False, site_sport=self.site_sport)
        number_pools = len(existing_inactive_pools)
        self.assertEqual( int(1), number_pools )    # should only be one
        inactive_pool = existing_inactive_pools[0]    # later on well want this inactive pool

        new_pool                = Pool()
        new_pool.active         = True     # <----
        new_pool.salary_config  = Dummy.create_salary_config()
        new_pool.site_sport     = self.site_sport
        new_pool.save()

        # get all the pools
        all_pools = Pool.objects.filter(site_sport=self.site_sport)
        self.assertEqual( 2, len(all_pools) ) # should be 2 pools, existing and new
        for p in all_pools:
            if p.pk == new_pool.pk:
                self.assertTrue( p.active ) # the new_pool should be the only active
            else:
                self.assertFalse( p.active ) # the existing pool should not be active

# class MyTest:
#     """
#     EXTREMELY IMPORTANT: Do not use this class on the live site
#     """
#     def __init__(self):
#         self.site_sport, c  = SiteSport.objects.get_or_create(name='test')
#         self.existing_pool  = None
#         self.new_pool       = None
#
#         # remove all existing pools for test purposes
#         for p in Pool.objects.all():
#             p.delete()
#
#     def create_pool_helper(self, existing=None, new=None):
#         salary_config = Dummy.create_salary_config()
#         existing_pool, c = Pool.objects.get_or_create(salary_config=salary_config,
#                                                         site_sport=self.site_sport,
#                                                         active=existing)
#         #existing_pool = Pool.objects.get(pk=existing_pool.pk)
#         existing_pool.refresh_from_db()
#
#         # create a second pool, and make sure active is overridden to False
#         new_config = Dummy.create_salary_config()
#         new_pool, c = Pool.objects.get_or_create(salary_config=new_config,
#                                                     site_sport=self.site_sport,
#                                                     active=new)
#         new_pool.refresh_from_db()
#         return existing_pool, new_pool   # return tuple
#
#     def create(self, existing=True, new=True):
#         self.existing_pool, self.new_pool = self.create_pool_helper( existing=existing, new=new )
#
#     def show(self):
#         for p in Pool.objects.all():
#             print(str(p))
#
#     def check(self):
#         existing_pool = Pool.objects.get(pk=self.existing_pool.pk)
#         print('existing_pool.active should be True and its:', existing_pool.active)
#         new_pool = Pool.objects.get(pk=self.new_pool.pk)
#         print('new_pool.active should be False and its:', new_pool.active)