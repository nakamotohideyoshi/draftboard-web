from mysite.exceptions import IncorrectVariableTypeException
from sports.game_status import GameStatus
from sports.models import SiteSport
from test.classes import AbstractTest
from .classes import SiteSportManager
from .exceptions import (
    GameClassNotFoundException,
    SiteSportWithNameDoesNotExistException,
)
from .models import Player, Game, PlayerStats


class GameStatusTest(AbstractTest):
    def setUp(self):
        super().setUp()
        self.invalid_sport = 'asdfawef'
        self.valid_sport = 'nfl'

    def test_game_status_bad_sport(self):
        self.assertRaises(
            GameStatus.InvalidSportException,
            lambda: GameStatus(self.invalid_sport)
        )

    def test_granular_status_does_not_exist(self):
        status_dne = 'status_dne_doesnt_exist'

        gs = GameStatus(self.valid_sport)

        self.assertRaises(
            GameStatus.InvalidGranularStatus,
            lambda: gs.get_primary_status(status_dne)
        )

    def test_granular_status_has_no_primary_status_mapping_exception(self):
        status_with_no_primary = 'status_with_no_primary_abc123'

        class TestGameStatus(GameStatus):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                # for testing purposes, add a granular status key with no primary status value
                self.status_map[status_with_no_primary] = None

        tgs = TestGameStatus(self.valid_sport)

        self.assertRaises(
            GameStatus.UnknownPrimaryStatusException,
            lambda: tgs.get_primary_status(status_with_no_primary)
        )


class SiteSportManagerGetPlayerClassTest(AbstractTest):
    def test_all_sports_get_player_class(self):
        """
        similar to another test, but iterates SiteSportManager.get_sport_names()
        so that if any new sports get added this will test them
        """
        for sport in SiteSportManager.SPORTS:
            site_sport = SiteSport.objects.get(name=sport)
            player_class = SiteSportManager().get_player_class(site_sport)
            self.assertTrue(issubclass(player_class, Player))


class SiteSportManagerGetPlayerStatsClassTest(AbstractTest):
    def test_get_player_stats_class_nfl(self):
        # nfl
        site_sport = SiteSport.objects.get(name='nfl')
        player_stats_class = SiteSportManager().get_player_stats_class(site_sport)
        for ps_class in player_stats_class:
            self.assertTrue(issubclass(ps_class, PlayerStats))

    def test_get_player_stats_class_nhl(self):
        # nhl
        site_sport = SiteSport.objects.get(name='nhl')
        player_stats_class = SiteSportManager().get_player_stats_class(site_sport)
        for ps_class in player_stats_class:
            self.assertTrue(issubclass(ps_class, PlayerStats))

    def test_all_sports_get_player_stats_class(self):
        """
        similar to another test, but iterates SiteSportManager.get_sport_names()
        so that if any new sports get added this will test them
        """
        for sport in SiteSportManager.SPORTS:
            site_sport = SiteSport.objects.get(name=sport)
            player_stats_class = SiteSportManager().get_player_stats_class(site_sport)
            for ps_class in player_stats_class:
                self.assertTrue(issubclass(ps_class, PlayerStats))


class SiteSportManagerGetGameClassTest(AbstractTest):
    def test_get_game_class_returns_proper_subclass(self):
        game_class = SiteSportManager().get_game_class('nfl')
        self.assertTrue(issubclass(game_class, Game))
        game_class = SiteSportManager().get_game_class('nhl')
        self.assertTrue(issubclass(game_class, Game))
        game_class = SiteSportManager().get_game_class('nba')
        self.assertTrue(issubclass(game_class, Game))
        game_class = SiteSportManager().get_game_class('mlb')
        self.assertTrue(issubclass(game_class, Game))

    def test_get_game_class_returns_proper_subclass_all(self):
        """
        similar to another test, but iterates SiteSportManager.get_sport_names()
        so that if any new sports get added this will test them
        """
        for str_sport_name in SiteSportManager.SPORTS:
            game_class = SiteSportManager().get_game_class(str_sport_name)
            self.assertTrue(issubclass(game_class, Game))

    def test_get_game_class_raises_error_on_invalid_string_sport(self):
        sport = 'steve_sport'
        self.assertRaises(SiteSportWithNameDoesNotExistException,
                          lambda: SiteSportManager().get_game_class(sport))

    def test_get_game_class_raises_error_on_invalid_site_sport(self):
        invalid_site_sport, c = SiteSport.objects.get_or_create(name='test_site_sport')
        self.assertRaises(GameClassNotFoundException,
                          lambda: SiteSportManager().get_game_class(invalid_site_sport))

    def test_get_game_class_raises_error_on_invalid_variable_type(self):
        invalid_argument = 123
        self.assertRaises(IncorrectVariableTypeException,
                          lambda: SiteSportManager().get_game_class(invalid_argument))
