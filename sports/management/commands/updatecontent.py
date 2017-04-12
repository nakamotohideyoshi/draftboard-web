from django.core.management.base import BaseCommand

from dataden.classes import DataDen
from sports.parser import DataDenParser


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
        self.stdout.write(msg)

        dd = DataDen()

        site_sport = None
        for sport in options['sport']:
            # # print the # of content items for this sport total to test
            # items = dd.find( sport, 'item', 'content' )
            # self.stdout.write('')
            # self.stdout.write('')
            # self.stdout.write('-------------------------- items -------------------------')
            # self.stdout.write('%+6s ... %+6s items'% (sport, str(items.count())))
            # # debug print the items
            # self.print_objects( items )

            # the objects in the 'content' collection are the master objects with a list of all the item ids for a day
            # all_content = dd.find( sport, 'content', 'content' )
            # self.stdout.write('')
            # self.stdout.write('')
            # self.stdout.write('-------------------------- content -------------------------')
            # self.stdout.write('%+6s ... %+6s content master lists'% (sport, str(all_content.count())))
            # # debug print the items
            # self.print_objects( all_content )


            #
            # TODO - make the models
            #       --> test the models we made

            #
            # TODO - parse the objects into their distinct things
            #       --> in progress
            # content_parser = TsxContentParser( sport )
            # for content_obj in all_content:
            #     msg = content_parser.parse( content_obj )
            #     self.stdout.write('')
            #     self.stdout.write( msg )
            #     self.stdout.write('')

            #
            # TODO - figure out the best way and/or place to hook up content text to sports.<sport>.models.Team / Player objects
            #  ----> api call     (leave existing injury parsing doing what its doing)

            #
            # this is simply a test that parses ALL the content in DataDen/mongo for the sport
            p = DataDenParser()
            p.setup(sport, force_triggers=DataDenParser.CONTENT_TRIGGERS)

    def print_objects(self, items):
        pass
        for item in items:
            self.stdout.write('')
            self.stdout.write(str(item))
