#
# pusher/classes.py

from pusher import Pusher
from django.conf import settings
from .tasks import pusher_send_task
from .exceptions import ChannelNotSetException, EventNotSetException
import ast
import json

# class PushObjectQueue(object):
#     """
#     this queue holds information which can be
#     """
#     def __init__(self):
#         pass

class AbstractPush(object):
    """
    This class handles delegating to the proper channels when realtime sports data is received.
    """

    def __init__(self):

        print( 'settings.PUSHER_APP_ID', settings.PUSHER_APP_ID,
               'settings.PUSHER_KEY', settings.PUSHER_KEY,
               'settings.PUSHER_SECRET', settings.PUSHER_SECRET )
        self.pusher = Pusher( app_id=settings.PUSHER_APP_ID,
                                key=settings.PUSHER_KEY,
                                secret=settings.PUSHER_SECRET,
                                ssl=True,
                                port=443 )
        self.channel    = None
        self.event      = None

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
        if async:
            send_data = data.get_o()
            pusher_send_task.apply_async( (self, send_data), serializer='pickle' )
        else:
            # json.loads(json.dumps(data)) --> dumps json in a serialized form, so it can be re-loaded as a real json object
            self.pusher.trigger( self.channel, self.event, data )

class DataDenPush( AbstractPush ):
    """
    Anything that is sent from dataden should be pushed with this class.

    This class handles play by play, and boxscore objects currently.
    """

    def __init__(self, sport):
        super().__init__() # init pusher object
        self.channel    = sport
        self.event      = 'dd'

class FantasyPointsPush( AbstractPush ):
    """
    Any changes in fantasy player scoring should be pushed with this class.
    """

    def __init__(self, sport):
        super().__init__() # init pusher object
        self.channel    = sport
        self.event      = 'fp'



