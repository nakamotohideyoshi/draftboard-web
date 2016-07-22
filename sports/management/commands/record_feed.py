#
# record_feed.py

from django.core.management.base import BaseCommand, CommandError
import requests
import time
import json
from sports.mlb.models import LiveFeed
from util.timesince import timeit

class Command(BaseCommand):
    """
    downloads any url that returns JSON (currently using the database table: sports.mlb.models.LiveFeed)

    """

    class RecordFeedJson(object):

        def __init__(self, url, name, game_srid, model_class):
            self.game_srid = game_srid
            self.url = url
            self.name = name
            self.session = requests.Session()
            self.r = None  # the HttpResponse from the last download()
            self.feed_model_class = model_class

        def start(self, iterations=10, delay_ms=3000.0):
            print('%s iterations' % str(iterations))
            i = 1
            while i <= iterations:
                try:
                    # TODO convert to json
                    self.et = self.download()
                    # self.parse() it and webhooks maybe ?
                except Exception as e:
                    print(str(e))
                    pass

                if i % 10 == 0:
                    print('%s of %s' % (str(i), str(iterations)))
                time.sleep(float(float(delay_ms) / float(1000.0)))  # divide millis by 1000 to get values in seconds
                i += 1

        @timeit
        def download(self):
            """ download and return the ElementTree, after its initialized with the feed xml """
            self.r = self.session.get(self.url)
            data = json.loads(self.r.text)
            self.add_to_db(data)
            return data

        @timeit
        def add_to_db(self, data):
            """
            save the json into the database
            """

            model = self.feed_model_class.objects.create(
                name=self.name,
                game_srid=self.game_srid,
                data=data
            )
            return model

    # help is a Command inner variable
    help = 'usage: ./manage.py record_feed <url> <name> <gameSrid> <iterations> <delayMillis>'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('cmdline', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        generate a salary pool with a default config

        :param args:
        :param options:
        :return:
        """

        arguments = []
        for arg in options['cmdline']:
            arguments.append(arg)
        #
        url = arguments[0]
        name = arguments[1]
        game_srid = arguments[2]
        iterations = int(arguments[3])
        delay_ms = int(arguments[4])

        # print args
        self.stdout.write(str(arguments))

        recorder = self.RecordFeedJson(url, name, game_srid, LiveFeed)
        recorder.start(iterations=iterations, delay_ms=delay_ms)