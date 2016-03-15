from __future__ import absolute_import

#
# sports/tasks.py

from django.core.cache import cache
from mysite.celery_app import app
from push.classes import DataDenPush

COUNTDOWN = 10

@app.task(bind=True)
def countdown_send_player_stats_data(self, cache_token, channel, event, data):
    """
    by default this task does not have a countdown value set.
    the caller should take care to call with a 'countdown' param, ie:

    countdown_send_player_stats_data.apply_async( (channel, event, data), countdown=X_SECONDS )

    :param channel:
    :param event:
    :param data:
    :return:
    """

    #
    # only pusher the player stats data if there is a cache_token existing.
    # immediately delete it upon sending the data.
    if cache.delete(cache_token) > 0:
        #
        DataDenPush(channel, event).send( data )