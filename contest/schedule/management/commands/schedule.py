#
# custom command: manage.py schedule

from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):

    help = "listen for dataden mongo updates for currently active triggers"

    def handle_noargs(self, **options):
        """

        :param options:
        :return:
        """

        print('todo')

        # self.stdout.write('a msg\n')