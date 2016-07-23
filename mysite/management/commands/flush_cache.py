from django.core.cache import cache
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = "Wipe django's default cache & wipe Redis too."

    def handle_noargs(self, **options):
        # This is much better and works on redis.
        cache.clear()
        self.stdout.write('Default cache has been cleared.\n')

        try:
            from redis import Redis
            Redis().flushall()
            self.stdout.write('Redis cache has been cleared.\n')
        except Exception as e:
            self.stdout.write('no other caches to wipe...\n')