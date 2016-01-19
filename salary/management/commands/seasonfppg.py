#
# sports/management/commands/fppg.py

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from dataden.classes import DataDen
from salary.classes import PlayerFppgGenerator

class Command(BaseCommand):
    """
    This adds the django manage.py command called "seasonfppg"

    This command updates the season_fppg property of Player objects
    for specified sports. You can use the keyword 'all' to update
    all sports

    Usage:

        $> ./manage.py seasonfppg <sport>                           # single sport
        $> ./manage.py seasonfppg <sport1> <sport2> ... <sport4>    # multiple sports
        $> ./manage.py seasonfppg all                               # all sports

    """

    # help is a Command inner variable
    help = 'usage: ./manage.py updatecontent <sport>'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('sport', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        generate a salary pool with a default config

        :param args:
        :param options:
        :return:
        """
        msg = '* Player.season_fppg updater'
        self.stdout.write( msg )

        site_sport  = None
        for sport in options['sport']:
            if sport == 'all':
                player_fppg_generator = PlayerFppgGenerator()
                player_fppg_generator.update()
            else:
                player_fppg_generator = PlayerFppgGenerator()
                player_fppg_generator.update_sport(sport)
