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

from os import listdir
from os.path import isfile, join
import os.path
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

    # directory for pg_dump'ed restore points for the database
    RESTORE_DIR                     = 'replayer/restore/'

    # directory for pg_dump'ed databases where all we care about are the replayer_* tables
    REPLAY_DIR                      = 'replayer/replay/'

    DEFAULT_CACHE                   = 'default'
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
        """
        set the system time to the datetime obj
        """
        dt2  = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, tzinfo=dt.tzinfo )
        #proc    = subprocess.call(['sudo','hwclock','--set','--date',str(dt2)])
        proc   = subprocess.call(['sudo','date','-s',str(dt2)])

    def reset_system_time(self):
        """
        sets the system time back to whatever the hardware clock time is
        """
        proc = subprocess.call(['sudo','hwclock','-s'])

    def db_dump(self, db_name, dump_name):
        # basically, to save the current state of the db, do this:
        #   $> sudo -u postgres pg_dump -Fc --no-acl --no-owner dfs_master > dfs_exported.dump
        #pass
        # use the name specified by the record() method for the dump?
        # proc = subprocess.call(['sudo','-u','postgres','pg_dump',
        #             '-Fc','--no-acl','--no-owner','dfs_master','>','%s.dump' % name])

        dump_filename = self.get_restore_filename( dump_name )
        if os.path.isfile(dump_filename):
            raise Exception('the file [%s] already exists' % dump_filename)
        with open(dump_filename, 'w') as dumpfile:
            subprocess.call("sudo -u postgres pg_dump -Fc --no-acl --no-owner %s" % db_name,
                                                                stdout=dumpfile, shell=True)

    def get_restore_filename(self, restore_dump_name):
        return '%s/%s' % (self.RESTORE_DIR, restore_dump_name)

    def db_restore(self, db_name, restore_dump_name):
        """
        (re)create the database you want to restore into:
            $> sudo -u postgres createdb dfs_replayer_sprint

        the restore command:
            $> sudo -u postgres pg_restore --no-acl --no-owner -d dfs_replayer_sprint test.dump
        """

        # dropdb_cmd_format   = 'sudo -u postgres dropdb %s'
        # dropdb_cmd          = dropdb_cmd_format % db_name
        # subprocess.call( dropdb_cmd, shell=True )

        # createdb_cmd_format = 'sudo -u postgres createdb %s'
        # createdb_cmd        = createdb_cmd_format % db_name
        # subprocess.call( createdb_cmd , shell=True)

        restore_filename    = self.get_restore_filename( restore_dump_name )
        restore_cmd_format  = 'sudo -u postgres pg_restore --no-acl --no-owner --clean -d %s %s'
        restore_cmd         = restore_cmd_format % (db_name, restore_filename)
        subprocess.call( restore_cmd, shell=True)

    def get_replay_filename(self, replay_dump_name):
        return '%s/%s' % (self.RESTORE_DIR, replay_dump_name)

    def db_load_replay(self, db_name, replay_dump_name):
        """
        given the database to pg_restore into, and the database dump file where the
        replay objects are, DUMP ONLY THE REPLAYER tables into the specified database.
        """
        replay_filename     = self.get_replay_filename( replay_dump_name )
        restore_cmd_format  = 'sudo -u postgres pg_restore --no-acl --no-owner -d %s -t replayer_replay -t replayer_update %s'
        restore_cmd         = restore_cmd_format % (db_name, replay_filename)
        subprocess.call( restore_cmd, shell=True)

    @staticmethod
    def list():
        """
        print out the restore dumps and the replay dumps. (prints the filenames of the dumps)
        :return:
        """
        print('restore points:')
        restore_points = [ print('    ', str(f)) for f in listdir(ReplayManager.RESTORE_DIR) if isfile(join(ReplayManager.RESTORE_DIR,f)) ]

        print('replays:')
        replay_files   = [ print('    ', str(f)) for f in listdir(ReplayManager.REPLAY_DIR) if isfile(join(ReplayManager.REPLAY_DIR,f)) ]

        print( '' )