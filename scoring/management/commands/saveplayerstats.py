#
# scoring/management/commands/saveplayerstats.py

from django.core.management.base import BaseCommand, CommandError
from sports.classes import SiteSportManager
from mysite.celery_app import save_model_instance

class Command(BaseCommand):
    """
    # TODO
    """
    # USAGE_STR   = './manage.py saveplayerstats <sport> <optionalArgument>'

    # help is a Command inner variable
    help = 'usage: ' + USAGE_STR

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('pk', nargs='+', type=int)

    def handle(self, *args, **options):
        """

        :param args:
        :param options:
        :return:
        """

        update_pks = []
        for update_pk in options['pk']:
            update_pks.append( update_pk )

        # if there is only one update pk, run it:
        size = len(update_pks)

        # self.stdout.write('something')
