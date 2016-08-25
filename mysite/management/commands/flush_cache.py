#
# flush_cache.py

from django.conf import settings
from django.core.cache import caches
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):

    help = "Wipe django's caches. All of them that are found in settings.CACHES."

    def handle_noargs(self, **options):
        # This is much better and works on redis.
        for name in settings.CACHES.keys():
            cache = caches[name]
            cache.clear()
            self.stdout.write('[%s] cache cleared!\n' % name)


