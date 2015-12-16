#
# sports/management/commands/updatecontent.py

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from dataden.classes import DataDen

class Command(BaseCommand):
    """
    This adds the django manage.py command called "updatecontent" for a sport.

    Usage:

        $> ./manage.py updatecontent <sport>                                 # single sport
        $> ./manage.py updatecontent <sport1> <sport2> ... <sport4>          # you can list all sports

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

        msg = 'updating The Sports Xchange news, injury info, and transactions'
        self.stdout.write( msg )

        dd = DataDen()

        site_sport  = None
        for sport in options['sport']:

            # print the # of content items for this sport total to test
            items = dd.find( sport, 'item', 'content' )
            self.stdout.write('')
            self.stdout.write('')
            self.stdout.write('-------------------------- items -------------------------')
            self.stdout.write('%+6s ... %+6s items'% (sport, str(items.count())))
            # debug print the items
            self.print_objects( items )

            # the objects in the 'content' collection are the master objects with a list of all the item ids for a day
            content = dd.find( sport, 'content', 'content' )
            self.stdout.write('')
            self.stdout.write('')
            self.stdout.write('-------------------------- content -------------------------')
            self.stdout.write('%+6s ... %+6s content master lists'% (sport, str(content.count())))
            # debug print the items
            self.print_objects( content )

            #
            # TODO - make the models
            #       --> test the models we made

            #
            # TODO - parse the objects into their distinct things
            #       --> in progress

            #
            # TODO - figure out the best way and/or place to hook up content text to sports.<sport>.models.Team / Player objects

    def print_objects(self, items):
        pass
        for item in items:
            self.stdout.write( '' )
            self.stdout.write( str(item) )