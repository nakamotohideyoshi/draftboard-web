from test.classes import AbstractTest
import mysite.exceptions
from test.models import PlayerChild, PlayerStatsChild, GameChild
from django.utils import timezone
from .classes import SalaryPlayerStatsObject, SalaryGenerator
from datetime import date, timedelta
from random import randint
from .models import SalaryConfig, TrailingGameWeight

#-------------------------------------------------------------------
#-------------------------------------------------------------------
# Shared setup methods for the test cases

def create_basic_player_stats():
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
    player.save()

    player_stats                    = PlayerStatsChild()
    player_stats.created            = timezone.now()
    player_stats.fantasy_points     = 15
    player_stats.game               = game
    player_stats.player             = player
    player_stats.srid_game          = game.srid
    player_stats.srid_player        = player.srid
    player_stats.position           = "F-C"
    player_stats.primary_position   = "PF"
    player_stats.save()

    return player_stats


def create_simple_player_stats_list():

    players = []
    for i in range(10,20):
        player                          = PlayerChild()
        player.srid                     = ""+str(i)
        player.first_name               = ""+str(i)
        player.last_name                = ""+str(i)
        player.created                  = timezone.now()
        player.save()
        players.append(player)

    for i in range(1,30):

        d = date.today() - timedelta(days=i)
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
            player_stats.position           = "F-C"
            player_stats.primary_position   = "PF"
            player_stats.save()

#-------------------------------------------------------------------
#-------------------------------------------------------------------
# Tests the Player Stats Object
class PlayerStatsObjectTest(AbstractTest):
    def setUp(self):
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
        self.salary_conf                            = SalaryConfig()
        self.salary_conf.trailing_games             = 10
        self.salary_conf.days_since_last_game_flag  = 10
        self.salary_conf.min_games_flag             = 7
        self.salary_conf.min_player_salary          = 3000
        self.salary_conf.max_team_salary            = 50000
        self.salary_conf.save()

        self.createTrailingGameWeight(self.salary_conf, 3,3)
        self.createTrailingGameWeight(self.salary_conf, 7,2)
        self.createTrailingGameWeight(self.salary_conf, 10,1)

    def createTrailingGameWeight(self, salary_config, through, weight):
        trailing_game_weight                        = TrailingGameWeight()
        trailing_game_weight.salary                 = salary_config
        trailing_game_weight.through                = through
        trailing_game_weight.weight                 = weight
        trailing_game_weight.save()



    def test_proper_init(self):
        self.assertIsNotNone(SalaryGenerator(PlayerStatsChild,self.salary_conf))

    def test_improper_init(self):
        self.assertRaises(mysite.exceptions.IncorrectVariableTypeException,
                          lambda: SalaryGenerator(SalaryPlayerStatsObject, self.salary_conf)
                          )


    def test_generate_salaries(self):
        create_simple_player_stats_list()
        salary_gen =SalaryGenerator(PlayerStatsChild, self.salary_conf)
        salary_gen.generate_salaries()














