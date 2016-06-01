#
# sports/signals.py

from django.dispatch import receiver
from dataden.signals import Ping, Update
from draftgroup.signals import (
    CheckForGameUpdatesSignal,
)
from sports.classes import (
    SiteSportManager,
)
from sports.parser import (
    ProviderParser,
    DataDenParser,
)

class DataDenReceiver(object):
    """
    receiver methods of this class should not get the 'self' argument.
    giving methods 'self' will break the signal mechanism!
    """

    @receiver(signal=Ping.signal)
    def ping(sender, **kwargs):
        """
        dataden's mongodb is sending triggers. this does not indicate
        specifically that dataden is actively parsing. it does mean
        that we are listening to all the transactions which are
        being processed by mongo for any namespaces we have configured.
        """
        print(str(sender), 'ping')
        # TODO

    @receiver(signal=Update.signal)
    def update(sender, **kwargs):
        #print('update signal')
        obj = kwargs['o']
        parser = ProviderParser.get_for_provider('dataden')
        parser.parse( obj ) # routes the object to its proper sport

    @receiver(signal=CheckForGameUpdatesSignal.signal)
    def check_for_game_updates(sender, **kwargs):
        """
        listen for newly created DraftGroup models so we can
        add any necessary initial GameUpdates

        :param sender:
        :param kwargs:
        :return:
        """
        game_srids = kwargs.get('game_srids', [])
        draft_group_id = kwargs.get('draft_group_id')
        sport = kwargs.get('sport')

        #
        print('initialize GameUpdates for draft_group_id:',
                    str(draft_group_id), 'sport:', str(sport))

        #
        if sport == SiteSportManager.MLB:
            #
            print('updating MLB probable pitchers')
            parser = ProviderParser.get_for_provider('dataden')

            # use DataDenParser's setup() method to parse
            # the probable pitchers which will in turn create
            # any necessary GameUpdate(s)
            triggers = [('mlb','probable_pitcher','daily_summary')]
            # specifically target the game_srids
            # coming from the CheckForGameUpdatesSignal to get only
            # the probable pitcher data for the relevant games
            target = {'game__id':{'$in':game_srids}}

            # async=True will asyncronously parse each probable pitcher object found in a task,
            # although the query will be done on the calling thread.
            parser.setup(sport, async=True, force_triggers=triggers, target=target)

        else:
            print('CheckForGameUpdatesSignal -- didnt catch signal')