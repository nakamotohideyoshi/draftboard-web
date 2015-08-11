#
# draftgroup/signals.py

from django.dispatch import receiver
from sports.models import Game, GameStatusChangedSignal

@receiver(GameStatusChangedSignal.signal, sender=Game)
def on_game_status_changed(sender, **kwargs):
    print( 'on_game_status_changed' )
