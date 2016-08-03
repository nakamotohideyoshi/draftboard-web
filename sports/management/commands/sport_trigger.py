#
# sports/management/commands/sport_trigger.py

from django.core.management.base import BaseCommand, CommandError
from sports.trigger import (
    SportTrigger,
    TriggerMlb,
)
from raven.contrib.django.raven_compat.models import client

class Command(BaseCommand):
    """
    uses the SportTrigger object to listen for parsed
    stat/pbp updates from the DataDen server

    requires that you start it with a SPORT, ie: 'nba' or 'nfl'
    """

    # help is a Command inner variable
    help = 'usage: ./manage.py sport_trigger <sport>'

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
        sport = arguments[0]

        # print args
        self.stdout.write('running trigger for: %s' % sport)

        while True:
            try:
                if sport == 'mlb':
                    # special trigger allows at_bats to pass filter
                    # as if they were changed objects until
                    # their 'description' is set (at bat over indicator)
                    sport_trigger = TriggerMlb(sport)

                else:
                    sport_trigger = SportTrigger(sport)

                sport_trigger.run()

            except Exception as e:
                print(str(e))
                print('exception caught in ./manage.py sport_trigger [%s]... restarting trigger!' % sport)
                #client.captureException()