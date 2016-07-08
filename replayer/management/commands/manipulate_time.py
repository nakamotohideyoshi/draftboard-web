#
# replayer/management/commands/manipulate_time.py

from dateutil import parser
from django.utils import timezone
from replayer.classes import ReplayManager
from util.timeshift import reset_system_time
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    USAGE_STR = './manage.py manipulate_time [get|reset|set] [--when=\'06-15-2016 23:00:00\']'

    # help is a Command inner variable
    help = 'usage: ' + USAGE_STR

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('cmd', choices=['get','reset','set'])

        # Named (optional) arguments
        parser.add_argument(
            '--when',
            dest='when',
            default=False,
            help='When should we time travel to? Format "06-15-2016 23:00:00',
        )

    def handle(self, *args, **options):
        """
        adjust time for local replayer
        """

        cmd = options['cmd']

        if cmd == 'get':
            print(timezone.now())

        elif cmd == 'reset':
            reset_system_time()
            print('Time reset.')
            print(timezone.now())

        elif cmd == 'set' and options['when']:
            dt = parser.parse(options['when'])
            rp = ReplayManager()
            rp.set_system_time( dt )

            print('Time travel worked!')
            print(timezone.now())



