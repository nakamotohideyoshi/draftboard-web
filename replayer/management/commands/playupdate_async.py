#
# replayer/management/commands/playupdate.py

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from replayer.classes import ReplayManager

class Command(BaseCommand):

    USAGE_STR = './manage.py playupdate UPDATE_ID'

    # help is a Command inner variable
    help = 'usage: ' + USAGE_STR

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('pk', nargs='+', type=int)

    def handle(self, *args, **options):
        """
        generate a salary pool with a default config

        :param args:
        :param options:
        :return:
        """

        rp = ReplayManager()
        for update_pk in options['pk']:
            rp.play_single_update( update_pk, async=True )