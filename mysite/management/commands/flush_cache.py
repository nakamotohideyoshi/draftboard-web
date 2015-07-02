from django.core.cache import cache
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = "Wipe django's default cache."

    def handle_noargs(self, **options):
        # This is much better and works on redis.
        cache.clear()
        self.stdout.write('Default cache has been cleared.\n')
