#
# dataden custom command: manage.py dataden_trigger

from django.core.management.base import NoArgsCommand
from dataden.watcher import Trigger

class Command(NoArgsCommand):

    help = "listen for dataden mongo updates for currently active triggers"

    def handle_noargs(self, **options):
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
                print( e )
                print( 'exception caught in ./manage.py dataden_trigger... restarting trigger!')
                # ... and continue

        # self.stdout.write('a msg\n')