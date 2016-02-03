#
# replayer/management/commands/start_recording.py

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from replayer.classes import ReplayManager

class Command(BaseCommand):

    USAGE_STR = './manage.py start_recording'

    # help is a Command inner variable
    help = 'usage: ' + USAGE_STR

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('pk', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        generate a salary pool with a default config

        :param args:
        :param options:
        :return:
        """

        values = []
        for x in options['values']:
            values.append( x )

        # sport1 = values[0]
        # sport2 = values[1]

        rp = ReplayManager()

        msg = 'ReplayManager recording_in_progress: %s' % str(rp.recording_in_progress())
        self.stdout.write( msg )

        #
        # flag_cache() flags the system and indicates if it should
        # record live updates or not!
        #
        # a flagged cache will expire after 24 hours however.
        rp.flag_cache( True )