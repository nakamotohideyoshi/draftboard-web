from django.conf import settings
from django.core.management.base import BaseCommand
from pusher import Pusher


class Command(BaseCommand):
    help = "Send test message to test_channel in pusher."

    # you should have open /push/receive/ with console open to see that this message went through
    def handle(self, *args, **options):
        # Referenced https://pusher.com/docs/javascript_quick_start#/lang=python
        p = Pusher(
            app_id=settings.PUSHER_APP_ID,
            key=settings.PUSHER_KEY,
            secret=settings.PUSHER_SECRET
        )

        p.trigger(u'test_channel', u'my-event', {u'message': u'hello world'})

        self.stdout.write('Successful')
