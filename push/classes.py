#
# pusher/classes.py

from django.db.transaction import atomic
from django.utils import timezone
from django.db.models import F
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
from dataden.models import (
    PbpDebug,
)
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

    class LinkableObjectNotSetException(Exception): pass

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
                #print('channel', str(channel), 'in channel_list:', channel in channel_list, 'channel_list:', str(channel_list))
                if channel in channel_list:
                    self.linker_queue_name = linker_queue_name
                    linker_queue = self.cache.get(linker_queue_name)
                    #print('linker_queue_name:', str(linker_queue_name)) # TODO remove
                    if linker_queue is not None:
                        #print('   linker_queue is not None - and is being returned') # TODO remove
                        return linker_queue
                    else:
                        #print('   linker_queue should be created (and is being created right now)') # TODO remove
                        linker_queue = LinkedExpiringObjectQueueTable(channel_list)
                        return linker_queue
            #
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

        # by default, this object is not linkable
        self.linkable_object = None

    def set_linkable_object(self, obj, link_id=None):
        self.linkable_object = LinkableObject( obj, link_id=link_id )

    def get_linkable_object(self):
        if self.linkable_object is None:
            raise self.LinkableObjectNotSetException('the linkable object was never set')
        return self.linkable_object

    def send(self, data, async=True, force=True ):
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
        # send the data on the channel with the specified event name
        if not isinstance( data, dict ):
            data = data.get_o()

        #print(data) # TODO remove

        #
        # get the linkedExpiringObjectQueueTable (ie: pbp+stats combiner
        # check if its the type of object we should throw in the pbp+stats linker queue
        if not force:
            #
            # run this object thru the stat linker to see if we can match it up
            linker = self.Linker()
            linker_queue = linker.get_linked_expiring_queue( self.channel )
            #print('linker_queue:', str(linker_queue)) # TODO remove
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

                # new_linked_object_data = self.edit_linker_queue( self.channel, LinkableObject( data ), linker, linker_queue )
                new_linked_object_data = self.edit_linker_queue( self.channel,
                                                self.get_linkable_object(), linker, linker_queue )

                if new_linked_object_data is not None:
                    # reshape the data a little bit, then pusher out the new linked data
                    formatted_linked_data = self.format_linked_data( new_linked_object_data )
                    #print('SENDING FORMATTED_LINKED_DATA:', str(formatted_linked_data)) # TODO remove
                    LinkedPbpStatsDataDenPush( self.channel ).send( formatted_linked_data )

                # bypass the rest of the method, because we have taken care of clean with countdown task
                return
        #
        # send it
        if async:
            # print('')
            # print('----------  pusher_send_task -----------')
            # print('| type: %s' % type(data))
            # print('| data: %s' % str(data))
            # print('----------------------------------------')
            # print('')
            # print('')
            task_result = pusher_send_task.apply_async( (self, data), serializer='pickle' )
        else:
            self.trigger( data )

    def format_linked_data(self, unformatted_linked_data):
        """
        take the list of tuple data from the linker queue
        and format it for pusher before it gets sent to clients.

        returns data in a format expected by the client.
        """
        data = {}
        #print('unformatted_linked_data: %s' % str(unformatted_linked_data))
        for queue_name, queue_item in unformatted_linked_data:
            data[ queue_name ] = queue_item.get_linkable_object().get_obj()
        return data

    def trigger(self, data):
        """
        core method which actually sends the object out on the wire.

        note: if django.conf.settings.PUSHER_ENABLED = False,
         will block pusher objects from being sent!
        """

        #
        #############
        # main task debug
        #############
        # for debug purposes

        # for metrics and timing info (if ./manage.py record_pbp is running)
        # a dataden pbp object (for nba)
        #
        # linked pbp object (nba)
        # {
        #   "stats": [
        #     {
        #       "fields": {
        #         "offensive_rebounds": 0,
        #         "game_type": 71,
        #         "two_points_pct": 0.333,
        #         "three_points_att": 0,
        #         "srid_game": "fb9a28a6-23d9-4c01-9a6c-40c2863203bf",
        #         "updated": "2016-04-13T01:49:16.159Z",
        #         "minutes": 12,
        #         "tech_fouls": 0,
        #         "assists": 4,
        #         "three_points_pct": 0,
        #         "points": 5,
        #         "field_goals_pct": 33.3,
        #         "rebounds": 1,
        #         "assists_turnover_ratio": 2,
        #         "two_points_att": 6,
        #         "player_type": 73,
        #         "created": "2016-04-12T23:27:54.419Z",
        #         "defensive_rebounds": 1,
        #         "srid_player": "1db0df17-b3d5-4ddb-98d0-8f86239347bf",
        #         "two_points_made": 2,
        #         "three_points_made": 0,
        #         "game_id": 1314,
        #         "position": 2,
        #         "free_throws_att": 1,
        #         "fantasy_points": 13.25,
        #         "personal_fouls": 0,
        #         "field_goals_att": 6,
        #         "blocks": 1,
        #         "field_goals_made": 2,
        #         "steals": 0,
        #         "flagrant_fouls": 0,
        #         "free_throws_pct": 100,
        #         "free_throws_made": 1,
        #         "blocked_att": 0,
        #         "player_id": 332,
        #         "turnovers": 2
        #       },
        #       "model": "nba.playerstats",
        #       "pk": 36192
        #     }
        #   ],
        #   "pbp": {
        #     "quarter__id": "72b2d818-1ac2-460f-a1e9-b9ca1cc973d7",
        #     "description": "Delon Wright makes free throw 2 of 2",
        #     "dd_updated__id": 1460511785162,
        #     "location__list": {
        #       "coord_y": 307,
        #       "coord_x": 897
        #     },
        #     "attribution": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
        #     "id": "7b5ac7df-0a7a-47f9-86d1-2637d11db93d",
        #     "updated": "2016-04-13T01:42:43+00:00",
        #     "event_type": "freethrowmade",
        #     "clock": "3:57",
        #     "game__id": "fb9a28a6-23d9-4c01-9a6c-40c2863203bf",
        #     "statistics__list": {
        #       "freethrow__list": {
        #         "team": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
        #         "player": "1db0df17-b3d5-4ddb-98d0-8f86239347bf",
        #         "made": "true",
        #         "points": 1
        #       }
        #     },
        #     "possession": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
        #     "_id": "cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGZiOWEyOGE2LTIzZDktNGMwMS05YTZjLTQwYzI4NjMyMDNiZnF1YXJ0ZXJfX2lkNzJiMmQ4MTgtMWFjMi00NjBmLWExZTktYjljYTFjYzk3M2Q3cGFyZW50X2xpc3RfX2lkZXZlbnRzX19saXN0aWQ3YjVhYzdkZi0wYTdhLTQ3ZjktODZkMS0yNjM3ZDExZGI5M2Q=",
        #     "parent_api__id": "pbp",
        #     "parent_list__id": "events__list"
        #   }
        # }
        # {
        #   "game__id": "c7a78f76-9c2b-487d-906d-a7c7e927e1b7",
        #   "parent_api__id": "pbp",
        #   "updated": "2016-04-12T03:25:58+00:00",
        #   "clock": "00:01",
        #   "dd_updated__id": 1460431574411,
        #   "description": "Play review",
        #   "event_type": "review",
        #   "id": "e76504c5-1175-43d5-8180-2244febe7506",
        #   "quarter__id": "630a74ce-f4e2-495c-9f62-4248660d8966",
        #   "_id": "cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGM3YTc4Zjc2LTljMmItNDg3ZC05MDZkLWE3YzdlOTI3ZTFiN3F1YXJ0ZXJfX2lkNjMwYTc0Y2UtZjRlMi00OTVjLTlmNjItNDI0ODY2MGQ4OTY2cGFyZW50X2xpc3RfX2lkZXZlbnRzX19saXN0aWRlNzY1MDRjNS0xMTc1LTQzZDUtODE4MC0yMjQ0ZmViZTc1MDY=",
        #   "parent_list__id": "events__list",
        #   "possession": "583ecf50-fb46-11e1-82cb-f4ce4684ea4c"
        # }

        if self.channel == PUSHER_NBA_PBP:
            # just do this for nba pbp right now
            pbp_data = data
            if self.event == 'linked':
                pbp_data = pbp_data.get('pbp')
            game_srid = pbp_data.get('game__id')
            srid = pbp_data.get('id')
            dd_updated_id = pbp_data.get('dd_updated__id')
            description = pbp_data.get('description')

            # a string we can use for this play if its relevant
            game_srid_pbp_srid_desc = 'game_srid: %s, pbp srid: %s, ' \
                                 'dd_udpated__id: %s, description: %s' % (str(game_srid),
                                  str(srid), str(dd_updated_id), str(description))
            print('game_srid_pbp_srid_desc', str(game_srid_pbp_srid_desc))

            #try:
            with atomic():
                try:
                    pbpdebug = PbpDebug.objects.get(game_srid=game_srid, srid=srid)
                    print('pbpexisted')
                except PbpDebug.DoesNotExist:

                    pbpdebug = PbpDebug()
                    pbpdebug.url = 'na'
                    pbpdebug.game_srid = game_srid
                    pbpdebug.srid = srid
                    pbpdebug.description = description
                    pbpdebug.xml_str = ''
                    pbpdebug.delta_seconds_valid = False
                    print('pbp DID NOT EXIST saving.')
                    pbpdebug.save()
                    print('... saved!')

                # if we were able to retrieve an existing one,
                # check if theres a timestamp and set it if its None
                # because this is the first time its going out after being parsed
                if pbpdebug.timestamp_pushered is None:
                    print('updated timestamp_pushered. %s' % (game_srid_pbp_srid_desc))
                    pbpdebug.timestamp_pushered = timezone.now()
                    pbpdebug.save()
                    print('     \-> save() called at:', str(pbpdebug.timestamp_pushered))

            # except PbpDebug.DoesNotExist:
            #     print('pbpdebug.doesnotexist -', game_srid_pbp_srid_desc)
            #     pass
            # except Exception as e:
            #     print(str(e)[:100])
            #     pass

        #############
        #############

        if settings.PUSHER_ENABLED:
            #print('settings.PUSHER_ENABLED == True ... object sent')
            self.pusher.trigger( self.channel, self.event, data )

        else:
            # print to console if its disable to remind us
            print('settings.PUSHER_ENABLED == False ... pusher.trigger() blocked. object not sent.')

    @locking(unique_lock_name=PUSH_TASKS_STATS_LINKER, timeout=30)
    def edit_linker_queue(self, channel, linkable_object, linker, linker_queue):
        """
        acquire a lock (blocking) to be able to edit the linker_queue.

        if the linker_queue returns objects to send, we must delete their tokens from the cache also!
        """
        identifier, linked_objects_to_send = linker_queue.add( channel, linkable_object )

        #
        # we have a new object we just need to add its identifier and countdown a task
        if identifier is not None:
            # add it to cache
            cache.set( identifier, identifier, 30 )
            # fire a pending task -- when it launches it should check if it still needs to send.
            # this task must use the same blocking lock as the edit_linker_queue method (?)
            # print('adding (identifier: %s) and task with countdown: '%str(identifier),
            #                                     str(linkable_object.get_obj())) # TODO remove

            linker_pusher_send_task.apply_async( (self, linkable_object.get_obj(),
                                                identifier), countdown=5, serializer='pickle' )

        #
        # we need to delete the token from the
        elif linked_objects_to_send is not None:
            for queue_name, queue_item in linked_objects_to_send:
                #print('LINKED_OBJECTS_TO_SEND: %s' % str(linked_objects_to_send))
                item_identifier = queue_item.get_identifier()
                # item_identifier may be None -- if this item is being immediately sent!
                if item_identifier is not None:
                    #print('     >>>>>> DELETEING TOKEN: %s' % str(item_identifier)) # TODO remove
                    cache.delete( queue_item.get_identifier() )

        #
        # add this linker obj back into the cache
        linker.save(linker_queue)

        #
        # return the objects to send, after having delete the tokens.
        # when this method exists, the lock will unlock.
        return linked_objects_to_send

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

class StatsDataDenPush( AbstractPush ):
    """
    Any stats objects, which may be linkable from dataden, should be pushed with this class.
    """

    def __init__(self, channel, event):
        """
        channel: the string name of the stream (ie: 'boxscores', or 'nba_pbp'
        event: the string name of the general type of the object, ie: 'player', or 'team'
        """
        super().__init__(channel) # init pusher object
        self.event = event

    def send(self, stats_data, async=True, force=False):
        """
        override the default behavior of send(), such that we check
        if the object has already been sent... if it has, then do not send it!
        """
        #print('stats_data: %s' % str(stats_data))
        link_id = stats_data.get('fields').get('srid_player')
        #print('link_id: %s' % str(link_id))
        self.set_linkable_object( stats_data, link_id=link_id)
        super().send( stats_data, async=async, force=force)

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

    def send(self, pbp_data, async=True, force=False):
        """
        override the default behavior of send(), such that we check
        if the object has already been sent... if it has, then do not send it!
        """

        self.set_linkable_object( pbp_data )

        live_stats_cache = LiveStatsCache()
        just_added = live_stats_cache.update_pbp( pbp_data )
        if just_added:
            #print(' === PbpDataDenPush data === SENDING:', str(pbp_data)) # TODO - remove debugging print
            super().send( pbp_data, async=async, force=force)
        # else:
        #     print(' === PbpDataDenPush data === DID NOT DOUBLE-SEND:', str(pbp_data)[:100]) # TODO - remove debugging print

class LinkedPbpStatsDataDenPush( AbstractPush ):
    """
    this object is for PUSHING linked stats objects.
    (for example, linked object data sent with this class for PBP+STATS linked objects)

    if you want to create a pusherable object that can be linked with something else,
    see classes that inherit the mixin 'HasLinkableObjectMixin'
    """

    def __init__(self, channel):
        """
        channel: the string name of the stream (ie: 'boxscores', or 'nba_pbp'
        event: 'linked' for this object always
        """
        super().__init__(channel) # init pusher object
        self.event = 'linked'

    def send(self, data):
        super().send( data, async=True, force=True )

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
