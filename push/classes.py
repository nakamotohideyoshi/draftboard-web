import collections
import hashlib
import json
import time
from logging import getLogger

import six
from django.conf import settings
from django.core.cache import caches, cache
from django.utils import timezone
from pusher import Pusher
from pusher.http import Request, make_query_string, POST, request_method
from pusher.signature import sign
from pusher.util import ensure_text, validate_channel, validate_socket_id
from raven.contrib.django.raven_compat.models import client

import util.timeshift as timeshift
from dataden.cache.caches import (
    LiveStatsCache,
    LinkableObject,
    LinkedExpiringObjectQueueTable,
)
from mysite.celery_app import locking
from push.tasks import linker_pusher_send_task, PUSH_TASKS_STATS_LINKER
from .exceptions import ChannelNotSetException, EventNotSetException
from .tasks import pusher_send_task

logger = getLogger('pusher.classes')

#
# on production this will be an empty string,
# but you should change it for your local/testing purposes.
PUSHER_CHANNEL_PREFIX = settings.PUSHER_CHANNEL_PREFIX

PUSHER_CONTEST = 'contest'
PUSHER_CONTEST_POOL = 'contest_pool'

PUSHER_BOXSCORES = 'boxscores'

PUSHER_MLB_PBP = 'mlb_pbp'
PUSHER_MLB_STATS = 'mlb_stats'
# PUSHER_MLB_LINKABLE_PBP_STATS   = ('mlb_queue_pbp_stats', [PUSHER_MLB_PBP, PUSHER_MLB_STATS])

PUSHER_NBA_PBP = 'nba_pbp'
PUSHER_NBA_STATS = 'nba_stats'
# PUSHER_NBA_LINKABLE_PBP_STATS   = ('nba_queue_pbp_stats', [PUSHER_NBA_PBP, PUSHER_NBA_STATS])

PUSHER_NFL_PBP = 'nfl_pbp'
PUSHER_NFL_STATS = 'nfl_stats'
# PUSHER_NFL_LINKABLE_PBP_STATS   = ('nfl_queue_pbp_stats', [PUSHER_NFL_PBP, PUSHER_NFL_STATS])

PUSHER_NHL_PBP = 'nhl_pbp'
PUSHER_NHL_STATS = 'nhl_stats'


# PUSHER_NHL_LINKABLE_PBP_STATS   = ('nhl_queue_pbp_stats', [PUSHER_NHL_PBP, PUSHER_NHL_STATS])

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
            # 'auth_timestamp': '%.0f' % time.time()
            #  we want to make sure this is always valid, thus the next line:
            'auth_timestamp': '%.0f' % timeshift.actual_now().timestamp()
            # '%s' formats to unix timestamp =)
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
        """
        Trigger an event on one or more channels, see:
        http://pusher.com/docs/rest_api#method-post-event
        """

        if isinstance(channels, six.string_types):
            channels = [channels]

        if isinstance(channels, dict) or not isinstance(channels,
                                                        (collections.Sized, collections.Iterable)):
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

    class LinkableObjectNotSetException(Exception):
        pass

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
                # print('channel', str(channel), 'in channel_list:', channel in channel_list,
                # 'channel_list:', str(channel_list))
                if channel in channel_list:
                    self.linker_queue_name = linker_queue_name
                    linker_queue = self.cache.get(linker_queue_name)
                    # print('linker_queue_name:', str(linker_queue_name))
                    if linker_queue is not None:
                        # print('   linker_queue is not None - and is being returned')
                        return linker_queue
                    else:
                        # print('   linker_queue should be created (and is being created now)')
                        linker_queue = LinkedExpiringObjectQueueTable(channel_list)
                        return linker_queue
            #
            return None

        def save(self, linked_expiring_object_queue_table_instance):
            """
            put it back in the cache
            """
            self.cache.set(self.linker_queue_name, linked_expiring_object_queue_table_instance,
                           48 * 60 * 60)

    # number of seconds to delay (using celery countdown) the task that sends the pusher data
    delay_seconds = None

    def __init__(self, channel):

        # print( 'settings.PUSHER_APP_ID', settings.PUSHER_APP_ID,
        #        'settings.PUSHER_KEY', settings.PUSHER_KEY,
        #        'settings.PUSHER_SECRET', settings.PUSHER_SECRET )
        # self.pusher = Pusher( app_id=settings.PUSHER_APP_ID,
        self.pusher = RealGoodPusher(app_id=settings.PUSHER_APP_ID,  #
                                     key=settings.PUSHER_KEY,
                                     secret=settings.PUSHER_SECRET,
                                     ssl=True,
                                     port=443)
        self.channel = PUSHER_CHANNEL_PREFIX + channel
        self.event = None

        # async indicates whether to use celery (if async == True)
        # or block on the current thread to do the send.
        self.async = settings.DATADEN_ASYNC_UPDATES

        # by default, this object is not linkable
        self.linkable_object = None

        # the hash to use to identify the most important object in the
        # case it is a composite (like Pbp Linked data is a pbp + list of stats).
        # hash is used explicitly for logging purposes to track stat items thru the system.
        self.hash = None

    def set_primary_object_hash(self, hsh):
        """
        must be set prior to send() being called for it to take effect.

        sets the hash for this object. this should only be done for
        composite objects, such as PBP Linked objects.

        :param hsh:
        :return:
        """
        self.hash = hsh

    def set_linkable_object(self, obj, link_id=None):
        self.linkable_object = LinkableObject(obj, link_id=link_id)

    def get_linkable_object(self):
        if self.linkable_object is None:
            raise self.LinkableObjectNotSetException('the linkable object was never set')
        return self.linkable_object

    def send(self, data, async=True, force=True):
        """
        uses the internal channel ( likely the sport name) and pushes the data out
        with teh event name specified by the child classes

        :param data:  dictionary of the data to send down the specified channel
        :param async:  if async=True, a celery task is used to send the data w/ pusher.
                        else the code is executed inline/synchronously
        :param force:
        
        :return: the value returned is a tuple for ( TaskResult, dictionary ),
                 and in the case async=False, None will be used for the TaskResult
        """
        if self.channel is None:
            raise ChannelNotSetException()
        if self.event is None:
            raise EventNotSetException()

        # THIS NETWORK CALL SOMETIMES TAKES ~1second and MUST be tasked off asynchronously!
        #
        # send the data on the channel with the specified event name
        if not isinstance(data, dict):
            data = data.get_o()

        # get the linkedExpiringObjectQueueTable (ie: pbp+stats combiner
        # check if its the type of object we should throw in the pbp+stats linker queue
        if not force:
            #
            # run this object thru the stat linker to see if we can match it up
            linker = self.Linker()
            linker_queue = linker.get_linked_expiring_queue(self.channel)
            # print('linker_queue:', str(linker_queue))
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
                # identifier, new_linked_object_data = linker_queue.add(
                #   self.channel, LinkableObject( data ) )
                # linker.save(linker_queue)

                # new_linked_object_data = self.edit_linker_queue(
                # self.channel, LinkableObject( data ), linker, linker_queue )
                new_linked_object_data = self.edit_linker_queue(
                    self.channel,
                    self.get_linkable_object(), linker,
                    linker_queue)

                if new_linked_object_data is not None:
                    # reshape the data a little bit, then pusher out the new linked data
                    formatted_linked_data = self.format_linked_data(new_linked_object_data)
                    # print('SENDING FORMATTED_LINKED_DATA:', str(formatted_linked_data))
                    LinkedPbpStatsDataDenPush(self.channel).send(formatted_linked_data)

                # bypass the rest of the method, because we have taken care of
                # clean with countdown task
                return

        # send it
        if async:
            # print('')
            # print('----------  pusher_send_task -----------')
            # print('| type: %s' % type(data))
            # print('| data: %s' % str(data))
            # print('----------------------------------------')
            # print('')
            # print('')
            countdown_seconds = 0
            if self.delay_seconds is not None:
                countdown_seconds = self.delay_seconds

            pusher_send_task.apply_async(
                (self, data),
                serializer='pickle',
                countdown=countdown_seconds)
        else:
            self.trigger(data)

    @staticmethod
    def format_linked_data(unformatted_linked_data):
        """
        take the list of tuple data from the linker queue
        and format it for pusher before it gets sent to clients.

        returns data in a format expected by the client.
        """
        data = {}
        # print('unformatted_linked_data: %s' % str(unformatted_linked_data))
        for queue_name, queue_item in unformatted_linked_data:
            data[queue_name] = queue_item.get_linkable_object().get_obj()
        return data

    def trigger(self, data):
        """
        core method which actually sends the object out on the wire.

        note: if django.conf.settings.PUSHER_ENABLED = False,
        will block pusher objects from being sent!
        """

        if settings.PUSHER_ENABLED:

            # get the current timestamp
            pusher_start_ts = int(time.time())
            # use pusher to send the data to clients!
            self.pusher.trigger(self.channel, self.event, data)

            pusher_completed_ts = int(time.time())
            log_msg = 'PSHR_NOW="%s", PSHR_NOW_TS=%s, PSHR_LOG=Send, PSHR_CHANNEL=%s, ' \
                      'PSHR_EVENT=%s, PSHR_DATA_ID="%s", PSHR_ITEM=Object, PSHR_VALUE=%s, ' \
                      'PSHR_START_TS=%s, PSHR_END_TS=%s, PSHR_DELTA_MS=%s, ' % (
                          str(timezone.now()),
                          int(time.time()),
                          self.channel,
                          self.event,
                          str(data.get('id')),
                          str(data), str(
                              pusher_start_ts), str(pusher_completed_ts),
                          str(int(
                              pusher_completed_ts - pusher_start_ts)))
            logger.debug(log_msg)

        else:
            # print to console if its disable to remind us
            logger.info(
                'settings.PUSHER_ENABLED == False ... pusher.trigger() blocked. object not sent.')

        # Should we write out to a local kinda-json-formatted text file?
        if settings.PUSHER_OUTPUT_TO_FILE:
            file_path = 'tmp/pusher_events__%s.%s.txt' % (self.channel, self.event)
            logger.info("Writing out pusher events to: `%s`" % file_path)

            try:
                # Open the file and append our event data in JSON format.
                with open(file_path, mode='a+', encoding='utf-8') as outfile:
                    outfile.write(json.dumps(data))
                    outfile.write('\n')

            except Exception as e:
                logger.error(e)
                client.captureException()

    @locking(unique_lock_name=PUSH_TASKS_STATS_LINKER, timeout=30)
    def edit_linker_queue(self, channel, linkable_object, linker, linker_queue):
        """
        acquire a lock (blocking) to be able to edit the linker_queue.

        if the linker_queue returns objects to send, we must delete their tokens from the 
        cache also!
        """
        identifier, linked_objects_to_send = linker_queue.add(channel, linkable_object)

        #
        # we have a new object we just need to add its identifier and countdown a task
        if identifier is not None:
            # add it to cache
            cache.set(identifier, identifier, 30)
            # fire a pending task -- when it launches it should check if it still needs to send.
            # this task must use the same blocking lock as the edit_linker_queue method (?)
            # print('adding (identifier: %s) and task with countdown: '%str(identifier),
            #                                     str(linkable_object.get_obj())) # TODO remove

            linker_pusher_send_task.apply_async((self, linkable_object.get_obj(),
                                                 identifier), countdown=5, serializer='pickle')

        #
        # we need to delete the token from the
        elif linked_objects_to_send is not None:
            for queue_name, queue_item in linked_objects_to_send:
                # print('LINKED_OBJECTS_TO_SEND: %s' % str(linked_objects_to_send))
                item_identifier = queue_item.get_identifier()
                # item_identifier may be None -- if this item is being immediately sent!
                if item_identifier is not None:
                    # print('     >>>>>> DELETEING TOKEN: %s' % str(item_identifier)) # TODO remove
                    cache.delete(queue_item.get_identifier())

        #
        # add this linker obj back into the cache
        linker.save(linker_queue)

        #
        # return the objects to send, after having delete the tokens.
        # when this method exists, the lock will unlock.
        return linked_objects_to_send


class DataDenPush(AbstractPush):
    """
    Anything that is sent from dataden should be pushed with this class.

    This class handles objects from dataden which can
    always be pushered out.
    """

    def __init__(self, channel, event, hash=False):
        """
        channel: the string name of the stream (ie: 'boxscores', or 'nba_pbp'
        event: the string name of the general type of the object, ie: 'player', or 'team' 
        """
        super().__init__(channel)  # init pusher object
        self.event = event

        # overrides / sets a single hash for composite objects (like pbp linked data)
        self.set_primary_object_hash(hash)


class PlayerStatsPush(DataDenPush):
    delay_seconds = 1


class StatsDataDenPush(AbstractPush):
    """
    Any stats objects, which may be linkable from dataden, should be pushed with this class.
    """

    def __init__(self, channel, event):
        """
        channel: the string name of the stream (ie: 'boxscores', or 'nba_pbp'
        event: the string name of the general type of the object, ie: 'player', or 'team'
        """
        super().__init__(channel)  # init pusher object
        self.event = event

    def send(self, stats_data, async=True, force=False):
        """
        override the default behavior of send(), such that we check
        if the object has already been sent... if it has, then do not send it!
        """
        # print('stats_data: %s' % str(stats_data))
        link_id = stats_data.get('fields').get('srid_player')
        # print('link_id: %s' % str(link_id))
        self.set_linkable_object(stats_data, link_id=link_id)
        super().send(stats_data, async=async, force=force)


class PbpDataDenPush(AbstractPush):
    """
    Any Play by Play objects from dataden should be pushed with this class.

    This class handles play by play, and ensures pbp objects are not pushered more than 1 time!
    """

    def __init__(self, channel, event):
        """
        channel: the string name of the stream (ie: 'boxscores', or 'nba_pbp'
        event: the string name of the general type of the object, ie: 'player', or 'team'
        """
        super().__init__(channel)  # init pusher object
        self.event = event

    def send(self, pbp_data, async=True, force=False):
        """
        override the default behavior of send(), such that we check
        if the object has already been sent... if it has, then do not send it!
        """

        self.set_linkable_object(pbp_data)

        live_stats_cache = LiveStatsCache()
        just_added = live_stats_cache.update_pbp(pbp_data)
        if just_added:
            # print(' === PbpDataDenPush data === SENDING:', str(pbp_data))
            super().send(pbp_data, async=async, force=force)
            # else:
            #     print(' === PbpDataDenPush data === DID NOT DOUBLE-SEND:', str(pbp_data)[:100])


class LinkedPbpStatsDataDenPush(AbstractPush):
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
        super().__init__(channel)  # init pusher object
        self.event = 'linked'

    def send(self, data):
        super().send(data, async=True, force=True)


class ContestPush(AbstractPush):
    """
    Anything that is sent from a Contest update
    """

    DEFAULT_EVENT = 'update'

    def __init__(self, data):
        """
        :param data: serialized contest data (likely from ContestSerializer(contest).data
        """
        super().__init__(PUSHER_CONTEST)
        self.event = self.DEFAULT_EVENT
        self.data = data

    def send(self):
        super().send(self.data, async=self.async)


class ContestPoolPush(AbstractPush):
    """
    Anything that is sent from a Contest update
    """

    DEFAULT_EVENT = 'update'

    def __init__(self, data):
        """
        :param data: serialized contest data (likely from ContestSerializer(contest).data
        """
        super().__init__(PUSHER_CONTEST_POOL)
        self.event = self.DEFAULT_EVENT
        self.data = data

    def send(self):
        super().send(self.data, async=self.async)
