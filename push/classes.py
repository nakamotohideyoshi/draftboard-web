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
from django.core.cache import caches, cache
from mysite.celery_app import app, locking
from .tasks import pusher_send_task
from .exceptions import ChannelNotSetException, EventNotSetException
import ast
import json
from dataden.cache.caches import (
    LiveStatsCache,
    LinkableObject,
    LinkedExpiringObjectQueueTable,
)
from push.tasks import linker_pusher_send_task, PUSH_TASKS_STATS_LINKER


#
# on production this will be an empty string,
# but you should change it for your local/testing purposes.
PUSHER_CHANNEL_PREFIX = settings.PUSHER_CHANNEL_PREFIX

PUSHER_CONTEST      = 'contest'

PUSHER_BOXSCORES    = 'boxscores'

PUSHER_MLB_PBP                  = 'mlb_pbp'
PUSHER_MLB_STATS                = 'mlb_stats'
#PUSHER_MLB_LINKABLE_PBP_STATS   = ('mlb_queue_pbp_stats', [PUSHER_MLB_PBP, PUSHER_MLB_STATS])

PUSHER_NBA_PBP                  = 'nba_pbp'
PUSHER_NBA_STATS                = 'nba_stats'
#PUSHER_NBA_LINKABLE_PBP_STATS   = ('nba_queue_pbp_stats', [PUSHER_NBA_PBP, PUSHER_NBA_STATS])

PUSHER_NFL_PBP                  = 'nfl_pbp'
PUSHER_NFL_STATS                = 'nfl_stats'
#PUSHER_NFL_LINKABLE_PBP_STATS   = ('nfl_queue_pbp_stats', [PUSHER_NFL_PBP, PUSHER_NFL_STATS])

PUSHER_NHL_PBP                  = 'nhl_pbp'
PUSHER_NHL_STATS                = 'nhl_stats'
#PUSHER_NHL_LINKABLE_PBP_STATS   = ('nhl_queue_pbp_stats', [PUSHER_NHL_PBP, PUSHER_NHL_STATS])

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

    class Linker(object):
        """
        gets or create the proper instance of LinkedExpiringObjectQueueTable
        for this a pusher channel / event.
        """

        linker_queues = [
            ('mlb_queue_pbp_stats', [PUSHER_MLB_PBP, PUSHER_MLB_STATS]),
            ('nba_queue_pbp_stats', [PUSHER_NBA_PBP, PUSHER_NBA_STATS]),
            ('nfl_queue_pbp_stats', [PUSHER_NFL_PBP, PUSHER_NFL_STATS]),
            ('nhl_queue_pbp_stats', [PUSHER_NHL_PBP, PUSHER_NHL_STATS]),
        ]

        def __init__(self):
            self.cache = caches['default']
            self.linker_queue_name = None

        def get_linked_expiring_queue(self, channel):
            """
            return the LinkedExpiringObjectQueueTable for the channel, otherwise returns None
            """
            for linker_queue_name, channel_list in self.linker_queues:
                print('channel', str(channel), 'in channel_list:', channel in channel_list, 'channel_list:', str(channel_list))
                if channel in channel_list:
                    self.linker_queue_name = linker_queue_name
                    linker_queue = self.cache.get(linker_queue_name)
                    print('linker_queue_name:', str(linker_queue_name))
                    if linker_queue is not None:
                        print('   linker_queue is not None')
                        return linker_queue
                    else:
                        print('   linker_queue should be created')
                        # create a linker queue using the channel_list for the queue names
                        linker_queue = LinkedExpiringObjectQueueTable(channel_list)
                        # self.cache.add( linker_queue_name, linker_queue, 48*60*60 )
                        #self.linker_queue_name = linker_queue_name
                        print('self.linker_queue_name:', str(self.linker_queue_name))
                        return linker_queue
            return None

        def save(self, linked_expiring_object_queue_table_instance):
            """
            put it back in the cache
            """
            self.cache.set( self.linker_queue_name, linked_expiring_object_queue_table_instance, 48*60*60 )

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

    def send(self, data, async=False, force=True ):
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

        print(data) # TODO remove

        #
        # get the linkedExpiringObjectQueueTable (ie: pbp+stats combiner
        # check if its the type of object we should throw in the pbp+stats linker queue
        if not force:
            #
            # run this object thru the stat linker to see if we can match it up
            linker = self.Linker()
            linker_queue = linker.get_linked_expiring_queue( self.channel )
            print('linker_queue:', str(linker_queue)) # TODO remove
            if linker_queue is not None:
                #
                # adding an object will result in us getting back the identifier
                # for the object if it was added (or None if it was linked)
                # and the linked object data which is in the form:
                #   [
                #       (channel_name, (identifier, datetime, pusherableJson)),
                #       (channel_name, (identifier, datetime, pusherableJson)),
                #       ...
                #   ]

                # xxx START LOCK HERE  - same as linker_pusher_send_task uses
                # identifier, new_linked_object_data = linker_queue.add( self.channel, LinkableObject( data ) )
                # linker.save(linker_queue)
                identifier, new_linked_object_data = self.edit_linker_queue( self.channel, LinkableObject( data ), linker, linker_queue )
                # xxx END LOCK HERE - same as linker_pusher_send_task uses

                #
                # if identifier is valid, the object was just added
                if identifier is not None:
                    # add it to cache
                    cache.set( identifier, identifier, 30 )
                    # fire a pending task -- when it launches it should check if it still needs to send.
                    # this task must use the same blocking lock as the edit_linker_queue method (?)
                    print('adding task with countdown: ', str(data))
                    linker_pusher_send_task.apply_async( (self, data, identifier ), countdown=5, serializer='pickle' )

                elif new_linked_object_data is not None:
                    # reshape the data a little bit, then pusher out the new linked data
                    obj = {}
                    for queue_name, json_data in new_linked_object_data:
                        obj[ queue_name ] = json_data
                    LinkedPbpStatsDataDenPush( self.channel ).send( obj, async=True )

                # bypass the rest of the method, because we have taken care of clean with countdown task
                return
        #
        # send it
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

    @locking(unique_lock_name=PUSH_TASKS_STATS_LINKER, timeout=30)
    def edit_linker_queue(self, channel, linkable_object, linker, linker_queue):
        """
        acquire a lock (blocking) to be able to edit the linker_queue
        """
        identifier, new_linked_object_data = linker_queue.add( channel, linkable_object )
        linker.save(linker_queue)
        return identifier, new_linked_object_data

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

class LinkedPbpStatsDataDenPush( AbstractPush ):
    """
    linked object data sent with this class for PBP+STATS linked objects
    """

    def __init__(self, channel):
        """
        channel: the string name of the stream (ie: 'boxscores', or 'nba_pbp'
        event: 'linked' for this object always
        """
        super().__init__(channel) # init pusher object
        self.event = 'linked'

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
