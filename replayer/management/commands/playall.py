#
# replayer/management/commands/playall.py

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from replayer.classes import ReplayManager

class Command(BaseCommand):
    """
    play all the timemachine updates in /admin/replayer/update/ synchrounously (do NOT run them thru celery)
    """

    USAGE_STR = './manage.py playall'

    # help is a Command inner variable
    help = 'usage: ' + USAGE_STR

    def add_arguments(self, parser):
        # Positional arguments
        #parser.add_argument('pk', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        """
        generate a salary pool with a default config

        :param args:
        :param options:
        :return:
        """

        rp = ReplayManager()
        rp.play_all( async=False )