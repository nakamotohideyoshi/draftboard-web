#
# sports/management/commands/dfsdate.py

from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    """

    """

    # help is a Command inner variable
    help = 'usage: ./manage.py dfsdate'

    def add_arguments(self, parser):
        # Positional arguments
        #parser.add_argument('sport', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        generate a salary pool with a default config

        :param args:
        :param options:
        :return:
        """
        msg = '* dfsdate'
        self.stdout.write( msg )

        


