#
# draftgroup/signals.py

from django.dispatch import (
    receiver,
    Signal,
)
from sports.models import Game, GameStatusChangedSignal

@receiver(GameStatusChangedSignal.signal, sender=Game)
def on_game_status_changed(sender, **kwargs):
    print( 'on_game_status_changed' )

class SignalNotSetupProperlyException(Exception):
    def __init__(self, class_name, variable_name):
       super().__init__('You must set "signal"')

class AbstractSignal(object):

    signal = None

    def __init__(self):
        self.__validate()

    def send(self, **kwargs):
        self.signal.send(sender=self.__class__, **kwargs)

    def __validate(self):
        if self.signal is None:
            raise SignalNotSetupProperlyException(self.__class__.__name__, 'signal')

class CheckForGameUpdatesSignal(AbstractSignal):
    """
    a signal with the id of the DraftGroup that was newly created

    usage:

        >>> from draftgroup.signals import CheckForGameUpdatesSignal
        >>> sig = CheckForGameUpdatesSignal( 1777, 'mlb' )
        >>> sig.send()

    """

    signal = Signal(providing_args=['draft_group_id','sport'])

    def __init__(self, draft_group_id, sport, game_srids):
        """

        :param draft_group_id: the DraftGroup model's primary key
        :param sport: the string name of the sport
        :param game_srids: list of game srids
        :return:
        """
        super().__init__()
        self.draft_group_id = draft_group_id
        self.sport = sport
        self.game_srids = game_srids

    def send(self):
        super().send(draft_group_id=self.draft_group_id, sport=self.sport, game_srids=self.game_srids)


