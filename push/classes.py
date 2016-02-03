#
# pusher/classes.py

import collections
import hashlib
import six
import time
from pusher import Pusher
from pusher.http import Request, make_query_string, GET, POST, request_method
from pusher.signature import sign
from pusher.util import ensure_text, validate_channel, validate_socket_id, app_id_re, pusher_url_re, channel_name_re
import util.timeshift as timeshift
from django.conf import settings
from .tasks import pusher_send_task
from .exceptions import ChannelNotSetException, EventNotSetException
import ast
import json
from dataden.cache.caches import LiveStatsCache

#
# on production this will be an empty string,
# but you should change it for your local/testing purposes.
PUSHER_CHANNEL_PREFIX = settings.PUSHER_CHANNEL_PREFIX

PUSHER_CONTEST      = 'contest'

PUSHER_BOXSCORES    = 'boxscores'

PUSHER_MLB_PBP      = 'mlb_pbp'
PUSHER_MLB_STATS    = 'mlb_stats'
PUSHER_NBA_PBP      = 'nba_pbp'
PUSHER_NBA_STATS    = 'nba_stats'
PUSHER_NFL_PBP      = 'nfl_pbp'
PUSHER_NFL_STATS    = 'nfl_stats'
PUSHER_NHL_PBP      = 'nhl_pbp'
PUSHER_NHL_STATS    = 'nhl_stats'

class RealGoodRequest(Request):
    """
    Overides the pusher.http.Request in order that we might specify the auth_timestamp that we want
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _generate_auth(self):
        self.body_md5 = hashlib.md5(self.body).hexdigest()
        self.query_params.update({
            'auth_key': self.config.key,
            'body_md5': six.text_type(self.body_md5),
            'auth_version': '1.0',

            # this is what we want to override: the time.
            #'auth_timestamp': '%.0f' % time.time() # we want to make sure this is always valid, thus the next line:

            'auth_timestamp': '%.0f' % timeshift.actual_now().timestamp()  # '%s' formats to unix timestamp =)
        })

        auth_string = '\n'.join([
            self.method,
            self.path,
            make_query_string(self.query_params)
        ])
        self.query_params['auth_signature'] = sign(self.config.secret, auth_string)

class RealGoodPusher(Pusher):
    """
    The entire purpose of this subclass is to use
    the overridden object RealGoodRequest in place
    of the orginal pusher.http.Request object.

    This is all done so that we alwasy use the real
    world time when sending to Pusher. Their API does
    has a strict requirement of +/- 600 seconds (last i checked)
    within real world time.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # the magic override with our own RealGoodRequest used instead:
    @request_method
    def trigger(self, channels, event_name, data, socket_id=None):
        '''
        Trigger an event on one or more channels, see:
        http://pusher.com/docs/rest_api#method-post-event
        '''

        if isinstance(channels, six.string_types):
            channels = [channels]

        if isinstance(channels, dict) or not isinstance(channels, (collections.Sized, collections.Iterable)):
            raise TypeError("Expected a single or a list of channels")

        if len(channels) > 10:
            raise ValueError("Too many channels")

        channels = list(map(validate_channel, channels))

        event_name = ensure_text(event_name, "event_name")

        if len(event_name) > 200:
            raise ValueError("event_name too long")

        if isinstance(data, six.string_types):
            data = ensure_text(data, "data")
        else:
            data = json.dumps(data, cls=self._json_encoder)

        if len(data) > 10240:
            raise ValueError("Too much data")

        params = {
            'name': event_name,
            'channels': channels,
            'data': data
        }
        if socket_id:
            params['socket_id'] = validate_socket_id(socket_id)

        #
        # used instead of pusher.http.Request (it makes sure we use the right auth_timestamp)
        return RealGoodRequest(self, POST, "/apps/%s/events" % self.app_id, params)

class AbstractPush(object):
    """
    This class handles delegating to the proper channels when realtime sports data is received.
    """

    def __init__(self, channel):

        # print( 'settings.PUSHER_APP_ID', settings.PUSHER_APP_ID,
        #        'settings.PUSHER_KEY', settings.PUSHER_KEY,
        #        'settings.PUSHER_SECRET', settings.PUSHER_SECRET )
        #self.pusher = Pusher( app_id=settings.PUSHER_APP_ID,
        self.pusher = RealGoodPusher( app_id=settings.PUSHER_APP_ID,    #
                                key=settings.PUSHER_KEY,
                                secret=settings.PUSHER_SECRET,
                                ssl=True,
                                port=443 )
        self.channel    = PUSHER_CHANNEL_PREFIX + channel
        self.event      = None

        # async indicates whether to use celery (if async == True)
        # or block on the current thread to do the send.
        self.async      = settings.DATADEN_ASYNC_UPDATES

    def send(self, data, async=False ):
        """
        uses the internal channel ( likely the sport name) and pushes the data out
        with teh event name specified by the child classes

        :param data:  dictionary of the data to send down the specified channel
        :param async:  if async=True, a celery task is used to send the data w/ pusher.
                        else the code is executed inline/synchronously

        :return: the value returned is a tuple for ( TaskResult, dictionary ),
                 and in the case async=False, None will be used for the TaskResult
        """
        if self.channel is None:
            raise ChannelNotSetException()
        if self.event is None:
            raise EventNotSetException()

        #
        # THIS NETWORK CALL SOMETIMES TAKES ~1second and MUST be tasked off asynchronously!
        #
        # send the data on the channel with the specified event name.
        if not isinstance( data, dict ):
            data = data.get_o()
        if async:
            task_result = pusher_send_task.apply_async( (self, data), serializer='pickle' )
        else:
            # json.loads(json.dumps(data)) --> dumps json in a serialized form, so it can be re-loaded as a real json object
            # print( 'data:', str(data))
            # json_data = ast.literal_eval(data)
            # print( 'json_data:', json_data )
            #self.pusher.trigger( self.channel, self.event, data )
            self.trigger( data )

    def trigger(self, data):
        self.pusher.trigger( self.channel, self.event, data )

class DataDenPush( AbstractPush ):
    """
    Anything that is sent from dataden should be pushed with this class.

    This class handles objects from dataden which can
    always be pushered out.
    """

    def __init__(self, channel, event):
        """
        channel: the string name of the stream (ie: 'boxscores', or 'nba_pbp'
        event: the string name of the general type of the object, ie: 'player', or 'team'
        """
        super().__init__(channel) # init pusher object
        self.event      = event

class PbpDataDenPush( AbstractPush ):
    """
    Any Play by Play objects from dataden should be pushed with this class.

    This class handles play by play, and ensures pbp objects are not pushered more than 1 time!
    """

    def __init__(self, channel, event):
        """
        channel: the string name of the stream (ie: 'boxscores', or 'nba_pbp'
        event: the string name of the general type of the object, ie: 'player', or 'team'
        """
        super().__init__(channel) # init pusher object
        self.event = event

    def send(self, pbp_data, *args, **kwargs):
        """
        override the default behavior of send(), such that we check
        if the object has already been sent... if it has, then do not send it!
        """
        live_stats_cache = LiveStatsCache()
        just_added = live_stats_cache.update_pbp( pbp_data )
        if just_added:
            super().send( pbp_data, *args, **kwargs )

class ContestPush( AbstractPush ):
    """
    Anything that is sent from a Contest update
    """

    DEFAULT_EVENT = 'update'

    def __init__(self, data):
        """
        :param data: serialized contest data (likely from ContestSerializer(contest).data
        """
        super().__init__( PUSHER_CONTEST )
        self.event = self.DEFAULT_EVENT
        self.data = data

    def send(self):
        super().send(self.data, async=self.async)
