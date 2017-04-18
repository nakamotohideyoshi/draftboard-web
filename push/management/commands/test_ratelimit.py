#
# test_ratelimit.py

from django.conf import settings
from django.core.management.base import BaseCommand
from pusher import Pusher

from util.timesince import timeit


class Command(BaseCommand):
    help = "send push on this thread as fast as possible until we get a non-empty response." \
           "you might have to run this in multiple terminals to get it to happen."

    # you should have open /push/receive/ with console open to see that this message went through
    def handle(self, *args, **options):
        # Referenced https://pusher.com/docs/javascript_quick_start#/lang=python
        p = Pusher(
            app_id=settings.PUSHER_APP_ID,
            key=settings.PUSHER_KEY,
            secret=settings.PUSHER_SECRET
        )

        # response = p.trigger(u'test_channel', u'my-event', {u'message': u'hello world'})
        # if response != {}: # {} is the default success response
        #     self.stdout.write('response: ', str(response))
        for x in range(25):
            self.sendit(p)
        self.stdout.write('done')

        # this is what we use that wraps the above code technically
        # push.classes.DataDenPush(
        #   self.pusher_sport_pbp,
        #   self.pusher_sport_pbp_event).send(self.get_send_data())  # pusher_sport_pbp_even

    @timeit
    def sendit(self, p):
        response = p.trigger(u'test', u'test', {u'test': u'test'})
        if response != {}:  # {} is the default success response
            self.stdout.write('response: ', str(response))
        return response
