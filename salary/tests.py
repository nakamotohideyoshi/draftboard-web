from test.classes import AbstractTest
import mysite.exceptions
from test.models import PlayerChild, PlayerStatsChild, GameChild
from django.utils import timezone
from .classes import PlayerStatsObject, SalaryGenerator
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
class SalaryGeneratorTest(AbstractTest):
    def setup(self):
        pass

    def test_proper_init(self):
        self.assertIsNotNone(SalaryGenerator(PlayerStatsChild, 1))

    def test_improper_init(self):
        self.assertRaises(mysite.exceptions.IncorrectVariableTypeException,
                          lambda: SalaryGenerator(PlayerStatsObject, 1))

















