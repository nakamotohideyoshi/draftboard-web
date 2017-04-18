#
# mysite/management/commands/testenv.py

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "prints the TEST_SETUP variable from settings file specified. ie: ./manage.py test_setup --settings=mysite.settings.production"

    def handle(self, *args, **options):
        # print TEST_SETUP from the django settings
        self.stdout.write('TEST_SETUP: %s\n' % str(settings.TEST_SETUP))
