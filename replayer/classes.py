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

from django.conf import settings
import ast
import sys
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
import sports.parser
import time

class ReplayManager(object):
    """
    The four methods involved with creating a replay are (in order):

        1) db_dump()
            - you need to save a snapshot of the current database
        2) record()
            - this will start logging all the mongo triggered stats in replayer_update,
              and there is a master replayer_replay entry made for this recording
        3) stop()
            - stop logging stats
        4) db_dump()
            - with replay=True which will put the db dump with the stats
              into the replay directory

    In order to play a replay the server time must be reset to the start time
    of the Replay entry. Then restore the database to a restore point,
    and then we need to run the related Update objects thru the parser.

        1) set_system_time()
            - changes the time of the system

        2) db_restore()
            - reload the database to a certain restore point

        3) play()
            - start executing stats on the same time intervals they occurred on in real-time.
    """

    class RecordingInProgressException(Exception): pass

    class InvalidStateException(Exception): pass

    # directory for pg_dump'ed restore points for the database
    RESTORE_DIR                     = 'replayer/restore/'

    # directory for pg_dump'ed databases where all we care about are the replayer_* tables
    REPLAY_DIR                      = 'replayer/replay/'

    DEFAULT_CACHE                   = 'default'
    CACHE_KEY_RECORDING_IN_PROGRESS = 'recording_in_progress'
    db_name                         = settings.DATABASES['default']['NAME']

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

    def record(self, name, create_restore_point=False):
        """
        since the restore points will break if there have been migrations
        since they are captured, the feature is optional, but you can use

            'create_restore_point' = True,

        this would result in a restore dump being placed in replayer/restore/
        at the moment just before you start recording. this would be useful
        for testing potentially. however, the restore point is not created by default.

        :param name:
        :param create_restore_point:
        :return:
        """
        if self.replay:
            raise self.RecordingInProgressException('record() was already called on this ReplayManager instance')

        print('resetting the current system time to the actual time...')
        self.reset_system_time()

        try:
            Replay.objects.get( name=name )
            print('the replay "%s" already exists. call play() with a unique name.' % name)
            return
        except Replay.DoesNotExist:
            pass # this is good, we dont want a new recording with the same name to already exist

        try:
            existing_replay = Replay.objects.get( end__isnull=True )

            print('')
            print('Do you want to end the current recording and start a new one? [yN]:' )
            user_input = sys.stdin.readline().strip()
            if 'y' in user_input:
                print(' ... stopped current recording.')
                self.stop()
            else:
                print(' ... exiting.')
                return
            #raise self.RecordingInProgressException('there is an existing recording in progress')
        except Replay.DoesNotExist:
            pass

        if create_restore_point:
            # self.db_name should return the postgres database name for the branch
            # we are on. ie: "dfs_replayer_sprint"
            print( '...creating restore dump in %s' % self.RESTORE_DIR )
            self.db_dump( db_name=self.db_name, dump_name=name, replay=False ) # replay=False indicates a restore point
        else:
            print( '...not creating restore point (to enable, set "create_restore_point" = True)')

        print( 'new recording "%s" in progress...'%name)

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

        # now save the current database as a replay file
        self.db_dump( db_name=self.db_name, dump_name=self.replay.name, replay=True )

        # set the system time back to the hardware clock time.
        # the hwclock should still be the actual real time.
        print('resetting the current system time to the actual time...')
        self.reset_system_time()

    def play(self, replay_name='', start_from=None, fast_forward=1.0, no_delay=False, pk=None, tick=6.0, offset_minutes=0):
        """
        Run the stat object thru sports.parser.DataDenParser.parse_obj(db, collection, obj)

        by default tries to play the replay file the instance has set internally.
        use 'replay' (give it the string name of the replay file) to override
        and play that particular replay

        'start_from' param defaults to None which means: start at the beginning,
            but if it is set to a valid datetime (within the range of the replay)
            start from there instead.

        'fast_forward' is a float multiplier that speeds up the replay (TODO - unimplemented).
            1.0 means 1second == 1second, 2.0 means 1second (actual) == 2seconds of replay time, etc..

        'no_delay' is False by default. If set to True, all the updates are run with no delay.
            this can result in tens of thousands of updates (the whole replay) being run
            as fast as the system can process them.

        'pk' param overrides the Replay object gets the Replay by its primary key

        'tick' is the interval in seconds we delay before processing more objects

        'offset_minutes' are added to the start time (whether default or from start_time param)

        :return:
        """

        self.clear()
        self.db_load_replay(self.db_name, replay_name )

        self.replay = Replay.objects.get( name = replay_name )

        if self.replay is None:
            raise Exception('instance of ReplayManager has no Replay object set')

        #
        # about to start playing, let the programmer know which Replay!


        # TODO - reload the specific restore point for this Replay

        # TODO - reset the system time to the start of this Replay

        # TODO - reload the replayer_update table for this Replay

        # TODO - get all the updates for this Replay

        # TODO - determine the start and end times of the Replay

        start   = self.replay.start
        if start_from is not None: start = start_from   # start from here, if specified
        start   = start + timedelta(minutes=offset_minutes)
        end     = self.replay.end
        last    = start # trailing time since which we have no parsed Updates

        # update the system time to the start time of the replay
        print('set system time to:')
        self.set_system_time( start )
        print( '' )

        parser = sports.parser.DataDenParser()

        while last <= end: # break out of while once our 'last' update time is past the end
            time.sleep( tick ) # every 'tick' seconds, get all the updates since the last update
            now = timezone.now()
            updates = replayer.models.Update.objects.filter( ts__range=( last, now ) )
            print( '%s | %s updates this tick' % (str(now), str(len(updates))))
            for update in updates:
                ns_parts    = update.ns.split('.') # split namespace on dot for db and coll
                db          = ns_parts[0]
                collection  = ns_parts[1]
                # send it thru parser! Triggers do NOT need to be running for this to work!
                parser.parse_obj( db, collection, ast.literal_eval( update.o ) )

            last = now # update last, now that we've parsed up until now

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

    def db_dump(self, db_name, dump_name, replay=False):
        # basically, to save the current state of the db, do this:
        #   $> sudo -u postgres pg_dump -Fc --no-acl --no-owner dfs_master > dfs_exported.dump
        #pass
        # use the name specified by the record() method for the dump?
        # proc = subprocess.call(['sudo','-u','postgres','pg_dump',
        #             '-Fc','--no-acl','--no-owner','dfs_master','>','%s.dump' % name])

        dump_filename = self.get_restore_filename( dump_name, replay=replay )
        if os.path.isfile(dump_filename):
            raise Exception('the file [%s] already exists' % dump_filename)
        with open(dump_filename, 'w') as dumpfile:
            subprocess.call("sudo -u postgres pg_dump -Fc --no-acl --no-owner %s" % db_name,
                                                                stdout=dumpfile, shell=True)

    def get_restore_filename(self, restore_dump_name, replay=False):
        if replay:
            return '%s%s' % (self.REPLAY_DIR, restore_dump_name)
        else:
            return '%s%s' % (self.RESTORE_DIR, restore_dump_name)

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
        return '%s%s' % (self.REPLAY_DIR, replay_dump_name)

    def db_load_replay(self, db_name, replay_dump_name):
        """
        given the database to pg_restore into, and the database dump file where the
        replay objects are, DUMP ONLY THE REPLAYER tables into the specified database.
        """

        self.clear()

        replay_filename     = self.get_replay_filename( replay_dump_name )
        restore_cmd_format  = 'sudo -u postgres pg_restore --no-acl --no-owner -d %s -t replayer_replay -t replayer_update %s'
        restore_cmd         = restore_cmd_format % (db_name, replay_filename)
        subprocess.call( restore_cmd, shell=True)

    def clear(self):
        """
        deletes all objects in the Replay, and Update table to make
        way for a new recording, so be sure youve dumped / saved
        any existing replay data you need to hang onto!

        :return:
        """
        # to be able to be restored into the database, we need to make sure
        # no existing objects are present or there could be conflicts
        Replay.objects.all().delete()
        replayer.models.Update.objects.all().delete()

    @staticmethod
    def list():
        """
        print out the restore dumps and the replay dumps. (prints the filenames of the dumps)
        :return:
        """
        # print('restore points:')
        # restore_points = [ print('    ', str(f)) for f in listdir(ReplayManager.RESTORE_DIR) if isfile(join(ReplayManager.RESTORE_DIR,f)) ]

        print('replays:')
        replay_files   = [ print('    ', str(f)) for f in listdir(ReplayManager.REPLAY_DIR) if isfile(join(ReplayManager.REPLAY_DIR,f)) ]

        print( '' )
