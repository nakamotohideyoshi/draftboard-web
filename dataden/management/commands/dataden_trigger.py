from django.core.management.base import BaseCommand
from raven.contrib.django.raven_compat.models import client

from dataden.watcher import Trigger


class Command(BaseCommand):
    help = "listen for dataden mongo updates for currently active triggers"

    def handle(self, *args, **options):
        """
        call run() on intsance of dataden.watcher.Trigger -- thats it!

        :param options:
        :return:
        """

        while True:
            try:
                t = Trigger()
                t.run()
            except Exception as e:
                print(e)
                print('exception caught in ./manage.py dataden_trigger... restarting trigger!')
                client.captureException()
                # ... and continue

                # self.stdout.write('a msg\n')
