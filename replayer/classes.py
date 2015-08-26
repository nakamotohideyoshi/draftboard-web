#
# replayer/classes.py

##################################################
#        WARNING !!!
##################################################
# In order for the replayer to work in VirtualBox
# you must turn off time sync !
#
#   >>>> https://gist.github.com/X0nic/4724674
##################################################

import json
import subprocess
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils import timezone
from replayer.models import Replay
import replayer.models
from django.dispatch import receiver
from dataden.signals import Update
from django.core.cache import caches

class ReplayManager(object):
    """
    Begins capturing live data objects from the stat provider.

    There can only be one recording being run at a time.
    """

    class RecordingInProgressException(Exception): pass

    class InvalidStateException(Exception): pass

    DEFAULT_CACHE = 'default'
    CACHE_KEY_RECORDING_IN_PROGRESS = 'recording_in_progress'

    def __init__(self):
        self.replay = None
        self.original_time = timezone.now()

    @staticmethod
    def recording_in_progress():
        # look in the cache to check if there is a recording in progress
        c = caches[ ReplayManager.DEFAULT_CACHE ].get(ReplayManager.CACHE_KEY_RECORDING_IN_PROGRESS)
        return c != None

    def save(self, oplog_object):
        update = replayer.models.Update()
        update.ts = timezone.now()
        update.ns = oplog_object.get_ns()
        update.o = json.loads( json.dumps( oplog_object.get_o() ) )
        update.save()

    def record(self, name):
        if self.replay:
            raise self.RecordingInProgressException('record() was already called')

        try:
            existing_replay = Replay.objects.get( end__isnull=True )
            raise self.RecordingInProgressException('there is an existing recording in progress')
        except Replay.DoesNotExist:
            pass

        self.replay = Replay()
        self.replay.name   = name
        self.replay.start  = timezone.now()
        self.replay.save()

        self.__flag_cache(True)   # flag we've begun recording

    def stop(self):
        if self.replay is None:
            # to see if a Replay currently running exists.
            try:
                self.replay = Replay.objects.get( end__isnull=True )
            except Replay.DoesNotExist:
                raise self.InvalidStateException('no recording to be stopped')

        self.replay.end = timezone.now()
        self.replay.save()
        self.__flag_cache(False)   # flag cache we've stopped recording

    def __flag_cache(self, enable):
        if enable:
            caches[ ReplayManager.DEFAULT_CACHE ].set(self.CACHE_KEY_RECORDING_IN_PROGRESS, True, 86400)
        else:
            caches[ ReplayManager.DEFAULT_CACHE ].set(self.CACHE_KEY_RECORDING_IN_PROGRESS, None, 0)

    def set_system_time(self, dt):
        dt2  = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, tzinfo=dt.tzinfo )
        #proc    = subprocess.call(['sudo','hwclock','--set','--date',str(dt2)])
        proc   = subprocess.call(['sudo','date','-s',str(dt2)])

    def reset_system_time(self):
        proc = subprocess.call(['sudo','hwclock','-s'])

    def db_snapshot(self):
        # basically, to save the current state of the db, do this:
        #   $> sudo -u postgres pg_dump -Fc --no-acl --no-owner dfs_master > dfs_exported.dump
        pass
        # use the name specified by the record() method for the dump?

    def load_replay(self, tables=[]):
        #
        pass