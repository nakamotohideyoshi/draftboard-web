#
# replayer/management/commands/delete_updates.py

from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from raven.contrib.django.raven_compat.models import client
from replayer.models import Update


class Command(BaseCommand):

    USAGE_STR = './manage.py delete_updates'

    # help is a Command inner variable
    help = 'usage: ' + USAGE_STR

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
        remove old replayer updates based on sport

        :param args:
        :param options:
        :return:
        """
        # key is sport name, value is hours to keep
        sports = {
            'mlb': 48,
            'nba': 48,
            'nfl': 192,
            'nhl': 48,
        }

        for sport, hours_ago in sports.items():
            try:
                dt_delete_before = timezone.now() - timedelta(hours=hours_ago)
                objects_to_delete = Update.objects.filter(ts__lt=dt_delete_before, ns__contains=sport)
                objects_deleted = objects_to_delete.count()
                objects_to_delete.delete()

                self.stdout.write(
                    '%s Recorded Updates deleted from before %s for sport %s' % (
                        str(objects_deleted), str(dt_delete_before), sport
                    )
                )
            except Exception as e:
                print(e)
                print('exception caught in ./manage.py delete_updates, sport was [%s]' % sport)
                client.captureException()
