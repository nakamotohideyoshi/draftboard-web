#
# replayer/management/commands/delete_updates.py

from django.utils import timezone
from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from replayer.models import Update

class Command(BaseCommand):

    USAGE_STR = './manage.py delete_updates <hoursAgo>'

    # help is a Command inner variable
    help = 'usage: ' + USAGE_STR

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('hours_ago', nargs='+', type=int)

    def handle(self, *args, **options):
        """
        generate a salary pool with a default config

        :param args:
        :param options:
        :return:
        """

        hours_ago = options['hours_ago'][0]
        dt_delete_before = timezone.now() - timedelta(hours=hours_ago)
        objects_to_delete = Update.objects.filter(ts__lt=dt_delete_before)
        objects_deleted = objects_to_delete.count()
        objects_to_delete.delete()
        self.stdout.write('%s Recorded Updates deleted from before %s' % (str(objects_deleted),str(dt_delete_before)))