#
# replayer/signals.py

from django.conf import settings
import replayer.classes
from django.dispatch import receiver
from dataden.signals import Update
from django.core.cache import caches

class ReplayUpdateReceiver(object):

    @receiver(signal=Update.signal)
    def update(sender, **kwargs):
        #print('replayer: got signal')

        if settings.DISABLE_REPLAYER_UPDATE_RECORDING:
            return
        
        # #
        # # if we are currently recording, save this update.
        # if replayer.classes.ReplayManager.recording_in_progress():
        #     obj = kwargs['o']
        #     replayer.classes.ReplayManager().save( obj )

        # alwasy record
        obj = kwargs['o']
        #print(str(obj))

        replayer.classes.ReplayManager().save( obj )