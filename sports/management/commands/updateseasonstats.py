#
# sports/management/commands/updateseasonstats.py

from django.core.management.base import BaseCommand

from dataden.classes import DataDen


class Command(BaseCommand):
    """
    This adds the django manage.py command called "updateseasonstats" for a sport.

    Usage:

        $> ./manage.py updateseasonstats <sport>                                 # single sport
        $> ./manage.py updateseasonstats <sport1> <sport2> ... <sport4>          # you can list all sports

    """

    # help is a Command inner variable
    help = 'usage: ./manage.py updateseasonstats <sport>'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('sport', nargs='+', type=str)

    def handle(self, *args, **options):
        """

        :param args:
        :param options:
        :return:
        """

        msg = 'updating season stats'
        self.stdout.write( msg )

        dd = DataDen()

        site_sport  = None
        for sport in options['sport']:


            # p = DataDenParser()
            # p.setup( sport, force_triggers=DataDenParser.SEASON_STATS_TRIGGERS )
            seasons = dd.find(sport, 'TODO_collection', 'TODO_parent_api')

    def print_objects(self, items):
        pass
        for item in items:
            self.stdout.write( '' )
            self.stdout.write( str(item) )