from test.classes import AbstractTest
import mysite.exceptions
from test.models import PlayerChild, PlayerStatsChild, GameChild
from django.utils import timezone
from .classes import SalaryPlayerStatsObject, SalaryGenerator
from datetime import date, timedelta
from random import randint

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
        self.assertIsNotNone(PlayerStatsObject(self.player_stats))

    def test_improper_init(self):
        self.assertRaises(mysite.exceptions.IncorrectVariableTypeException,
                          lambda: PlayerStatsObject(1))

    def test_missing_data_types (self):
        self.player_stats.fantasy_points = None
        self.assertRaises(mysite.exceptions.NullModelValuesException,
                          lambda: PlayerStatsObject(self.player_stats))

#-------------------------------------------------------------------
#-------------------------------------------------------------------
# Tests the Salary Generator
class SalaryConf(object):
    def __init__(self):
        self.trailing_games  = 10


class SalaryGeneratorTest(AbstractTest):
    def setUp(self):
        self.salary_conf = SalaryConf()

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














