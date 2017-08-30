#
# update_player_stats.py

from django.core.management.base import BaseCommand
from sports.nfl.classes import (
    NflRecentGamePlayerStats,
)

class Command(BaseCommand):
    """
    This adds the django manage.py command called "update_player_stats"
    which updates player stats for a game based on the most recent parse of the stats feed

    Usage:

        $> ./manage.py update_player_stats <game srid>

    """

    # help is a Command inner variable
    help = 'usage: ./manage.py update_player_stats <game_srid>'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('game_srid', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        generate a salary pool with a default config

        :param args:
        :param options:
        :return:
        """

        msg = 'updating player stats with recent stats for specified game'
        self.stdout.write(msg)

        game_srid = None
        for srid in options['game_srid']:
            game_srid = srid

        self.stdout.write(game_srid)

        # TODO test
        nfl_recent_stats = NflRecentGamePlayerStats()
        nfl_recent_stats.update(game_srid) # diffs the sports PlayerStats models and updates them if necessary

        # # TODO debug
        # player_stats_data = nfl_recent_stats.build_data(game_srid)
        # self.stdout.write(str(player_stats_data))
        #
        # # iterate this data and print each complete, recent object
        # for player_srid, stats in player_stats_data.items():
        #     self.stdout.write(str(player_srid) + str(stats))