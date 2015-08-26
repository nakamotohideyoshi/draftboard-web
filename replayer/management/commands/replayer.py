#
# replayer/management/commands/replayer.py

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from replayer.classes import ReplayManager

class Command(BaseCommand):

    USAGE_STR = './manage.py replayer [play|record|list]'

    # help is a Command inner variable
    help = 'usage: ' + USAGE_STR

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('cmd', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        use the replayer

        :param args:
        :param options:
        :return:
        """

        for cmd in options['cmd']:
            if cmd == 'play':
                pass # TODO
                self.stdout.write('unimplemented')

            elif cmd == 'record':
                pass # TODO
                self.stdout.write('unimplemented')

            elif cmd == 'list':
                ReplayManager.list()

            else:
                raise CommandError('invalid command! usage: ' + self.USAGE_STR)


