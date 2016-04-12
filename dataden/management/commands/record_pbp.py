#
# dataden/management/commands/record_pbp.py

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from dataden.classes import FeedTest
import time

class Command(BaseCommand):
    """
    uses the FeedTest object to keep downloading a feed, and updating the
    database the first time it sees new <event> nodes

    you can play with the class using this snippet:

        from dataden.classes import FeedTest
        url='http://api.sportsdatallc.org/nba-p3/games/bdbba253-b249-4747-8278-bf8be6c27960/pbp.xml?api_key='
        game_srid = 'bdbba253-b249-4747-8278-bf8be6c27960'
        sportradar_apikey = 'sxt5fqkte64k53nn2qvk5366'
        ft = FeedTest(game_srid=game_srid, url=url, apikey=sportradar_apikey)
        tree = ft.download()
        ft.parse(tree)

    """

    # help is a Command inner variable
    help = 'usage: ./manage.py record_pbp <urlMinusApiKey> <gameSrid> <apiKey> <iterations>'

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

        arguments = []
        for cmdlinearg in options['sport']:
            arguments.append(cmdlinearg)
        # exstra params
        url = arguments[0]
        game_srid = arguments[1]
        sportradar_apikey = arguments[2]
        iterations = int(arguments[3])

        # print args
        self.stdout.write(str(arguments))

        ft = FeedTest(game_srid=game_srid, url=url, apikey=sportradar_apikey)
        i = 0
        while i < iterations:
            tree = ft.download()
            ft.parse(tree)
            time.sleep(1.0)
            i += 1