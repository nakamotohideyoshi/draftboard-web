from django.core.management.base import BaseCommand

from dataden.classes import DataDen
from dataden.classes import Season


class Command(BaseCommand):
    """
    This adds the django manage.py command called "fppg" for a sport.

    Usage:

        $> ./manage.py fppg <sport>                                 # single sport
        $> ./manage.py fppg <sport1> <sport2> ... <sport4>          # you can list all sports

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

        msg = 'updating Fantasy Points Per Game (FPPG)'
        self.stdout.write(msg)

        dd = DataDen()

        site_sport = None
        for sport in options['sport']:
            print('   %s' % sport)
            #
            # get the <Sport>Season class
            season = Season.factory(sport)
            game_ids = season.get_game_ids_regular_season(2015)
