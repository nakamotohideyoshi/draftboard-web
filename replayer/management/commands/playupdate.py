#
# replayer/management/commands/playupdate.py

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from replayer.classes import ReplayManager

class Command(BaseCommand):

    USAGE_STR = './manage.py playupdate UPDATE_ID <optional end update id>'

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

        update_pks = []
        for update_pk in options['pk']:
            update_pks.append( update_pk )

        # if there is only one update pk, run it:
        size = len(update_pks)
        if size == 0:
            self.stdout.write('you must specify at least one update pk, or two update pks to specify a range')
        elif len(update_pks) == 1:
            rp = ReplayManager()
            rp.play_single_update( update_pks[0], async=False )

        else:
            rp = ReplayManager()
            # truncate chars is how many characters of each object to print out.
            rp.play_range( update_pks[0], update_pks[1], async=False, truncate_chars=99999 )