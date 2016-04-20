#
# mysite/management/commands/testenv.py

from django.core.cache import cache
from django.core.management.base import NoArgsCommand
from django.conf import settings

class Command(NoArgsCommand):

    help = "prints the TEST_SETUP variable from settings file specified. ie: ./manage.py test_setup --settings=mysite.settings.production"

    def handle_noargs(self, **options):

        # print TEST_SETUP from the django settings
        self.stdout.write('TEST_SETUP: %s\n' % str(settings.TEST_SETUP))