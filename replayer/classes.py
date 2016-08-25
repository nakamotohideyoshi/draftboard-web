#
# replayer/classes.py

from django.db.transaction import atomic
from django.db.models import Q
import subprocess
from django.conf import settings
import ast
import sys
import os.path
import json
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from cash.classes import CashTransaction
from ticket.classes import TicketManager
import prize.helpers
from replayer.models import Replay
import replayer.models
from django.core.cache import caches
import sports.parser
import time
import util.timeshift as timeshift
from draftgroup.models import Player
from contest.buyin.classes import BuyinManager
from lineup.classes import LineupManager
from contest.models import (
    ContestPool,
)
from sports.classes import SiteSportManager
from roster.classes import RosterManager
from random import Random
from ast import literal_eval

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

    # default, used in play_range/play_all method to determine how much of each object to print
    TRUNCATE_CHARS = 75

    # directory for pg_dump'ed restore points for the database
    RESTORE_DIR                     = 'replayer/restore/'

    # directory for pg_dump'ed databases where all we care about are the replayer_* tables
    REPLAY_DIR                      = 'replayer/replay/'

    DEFAULT_CACHE                   = 'default'
    CACHE_KEY_RECORDING_IN_PROGRESS = 'recording_in_progress'
    CACHE_KEY_PAUSE_ACTIVE_REPLAY   = 'CACHE_KEY_PAUSE_ACTIVE_REPLAY'

    db_name                         = settings.DATABASES['default']['NAME']

    def __init__(self, timemachine=None):
        self.replay         = None
        self.original_time  = timezone.now()
        self.timemachine    = timemachine

        #
        self.user_list      = None
        self.curr_user_idx  = 0

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
        #print(json.loads( json.dumps( oplog_object.get_o() ) ))
        #print('update.ts',str(update.ts), 'update.ns', str(update.ns), 'update.o', str(update.o))
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

    def set_time_before_replay_start(self):
        updates = replayer.models.Update.objects.filter().order_by('ts')
        if updates.count() > 0:
            update = updates[0]
            self.set_system_time(update.ts - timedelta(hours=3))
        else:
            print('warning: time not changed - there are no realtime objects in the db')

    def play(self, replay_name='', start_from=None, fast_forward=1.0,
             no_delay=False, pk=None, tick=6.0, offset_minutes=0, async=True,
             load_db=True, play_until=None):
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

        'play_until' datetime object will cause the replay to stop at the datetime (if in range)

        :return:
        """

        if load_db:
            self.clear()
            self.db_load_replay(self.db_name, replay_name )
            self.replay = Replay.objects.get( name = replay_name )

            if self.replay is None:
                raise Exception('instance of ReplayManager has no Replay object set')

            #
            # get the specified time range to run on
            start   = self.replay.start
            if start_from is not None: start = start_from   # start from here, if specified
            start   = start + timedelta(minutes=offset_minutes)
            end     = self.replay.end

        else:
            # since we simply replaying Update objects, we need to determine the time
            start   = start_from
            updates = replayer.models.Update.objects.filter().order_by('ts') # ascending
            if updates.count() <= 1:
                if self.timemachine:
                    self.timemachine.playback_status = 'ERR - NOTHING TO PLAY!'
                    self.timemachine.save()
                raise Exception('there are no Update objects to play thru')

            if start is None:
                start = updates[0].ts
            end     = start + timedelta(days=1) # never going to replay more than this

            #
            # if play_until is not None, check it to make
            # sure its valid, and set end = play_until
            if play_until and start < play_until:
                end = play_until

        # if timemachine exists, update the playback_status to started
        if self.timemachine:
            self.timemachine.playback_status = 'RUNNING'
            self.timemachine.save()

        # update the system time to the start time of the replay
        self.set_system_time( start )
        print('set system time to:', str(timezone.now()))
        print( '' )

        parser = sports.parser.DataDenParser()

        last    = start         # trailing time since which we have no parsed Updates
        while last <= end:      # break out of while once our 'last' update time is past the end
            time.sleep( tick )  # every 'tick' seconds, get all the updates since the last update

            # check if we are paused!
            # (Pause) ie: stash a value in the cache             /api/replayer/pause/1/
            # (Resume) ie: remove that value from the cache      /api/replayer/pause/0/
            if self.is_paused():
                self.set_system_time(last) # keep
                print('[%s] REPLAY IS PAUSED' % (str(timezone.now())))
                continue

            now = timezone.now()
            updates = replayer.models.Update.objects.filter( ts__range=( last, now ) )
            print( '%s | %s updates this tick' % (str(now), str(len(updates))))
            for update in updates:
                ns_parts    = update.ns.split('.') # split namespace on dot for db and coll
                db          = ns_parts[0]
                collection  = ns_parts[1]
                # send it thru parser! Triggers do NOT need to be running for this to work!
                if db == 'mlb' and collection == 'pitcher':
                    print('update.o:', str(update.o))
                parser.parse_obj( db, collection, ast.literal_eval( update.o ), async=async )

            last = now # update last, now that we've parsed up until now
            if self.timemachine:
                self.timemachine.current = last
                self.timemachine.save()

            anymore = replayer.models.Update.objects.filter( ts__gte=last )
            if anymore.count() <= 0:
                # if timemachine exists, update the playback_status to finished
                if self.timemachine:
                    self.timemachine.playback_status = 'FINISHED'
                    self.timemachine.save()
                return # because there are literally no more updates

    def flag_paused(self, enable):
        """
        set a value in the cache to pause the replayer (if it is active)
        """
        if enable:
            caches[ ReplayManager.DEFAULT_CACHE ].set(
                self.CACHE_KEY_PAUSE_ACTIVE_REPLAY, True, 60*60) # pause for an hour max
        else:
            caches[ ReplayManager.DEFAULT_CACHE ].set(
                self.CACHE_KEY_PAUSE_ACTIVE_REPLAY, None, 0)

    def is_paused(self):
        """
        returns whether the replay is currently paused as a boolean

        True: paused
        False: not paused
        """
        return caches[ ReplayManager.DEFAULT_CACHE ].get(self.CACHE_KEY_PAUSE_ACTIVE_REPLAY, False)

    def flag_cache(self, enable):
        """
        wrapper for __flag_cache
        """
        self.__flag_cache(enable)

    def __flag_cache(self, enable):
        if enable:
            caches[ ReplayManager.DEFAULT_CACHE ].set(self.CACHE_KEY_RECORDING_IN_PROGRESS, True, 86400)
        else:
            caches[ ReplayManager.DEFAULT_CACHE ].set(self.CACHE_KEY_RECORDING_IN_PROGRESS, None, 0)

    def set_system_time(self, dt):
        """
        set the system time to the datetime obj
        """

        timeshift.set_system_time( dt )

    def reset_system_time(self):
        """
        sets the system time back to the actual time
        """

        timeshift.reset_system_time()

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

        # subprocess call with sudo
        #restore_cmd_format  = 'sudo -u postgres pg_restore --no-acl --no-owner -d %s -t replayer_replay -t replayer_update %s'
        restore_cmd_format  = 'pg_restore --no-acl --no-owner -d %s -t replayer_replay -t replayer_update %s'

        restore_cmd         = restore_cmd_format % (db_name, replay_filename)
        subprocess.call( restore_cmd, shell=True)

    def sub_call(self, cmd):
        subprocess.call( cmd, shell=True )

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

        # print('replays:')
        # replay_files   = [ print('    ', str(f)) for f in listdir(ReplayManager.REPLAY_DIR) if isfile(join(ReplayManager.REPLAY_DIR,f)) ]
        #
        # print( '' )
        print('replays are not stored here anymore')

    def build_world(self):
        """
        The replayer tasks which wipes & installs a snapshot
        calls this method when its done to ensure all
        fundamental database things are setup.
        """

        # make sure Ticket amounts exist
        TicketManager.create_default_ticket_amounts()

        # ensure default headsup PrizeStructures exist
        prize.helpers.create_initial_data()

    def generate_users(self, num_users=200):
        """
        This method also creates 'num_users' users,
        and adds $10,000 to their cash accounts.
        """
        if num_users < 2:
            raise Exception('num_users should be more than 2')

        self.user_list = []         # initialize the self.user_list
        for x in range(num_users):
            user, created = User.objects.get_or_create( username='user%s'%str(x))
            self.user_list.append( user )
            user.set_password('test')
            # add 10000 to their cash account
            ct = CashTransaction( user )
            ct.deposit(10000.00) # add funds

        return self.user_list # return it

    def __get_user(self, idx=None):
        """
        gets the next user from the self.user_list like a circular array.

        if idx is specified (and is a valid index) the user at that idx is returned.
        :return:
        """
        if idx is not None:
            return self.user_list[idx]

        size = len(self.user_list)
        user = self.user_list[ self.curr_user_idx % size ]
        self.curr_user_idx += 1 # post increment
        return user

    def fill_contests(self):
        """
        Fills all remaining entry spots in registering contests
        using the list of users created by setup_world().

        This method uses the list of users circularly until
        all contest spots have been filled (or a user runs out of money).
        """

        # get the list of generated users if self.user_list is None
        if self.user_list is None:
            try:
                user0 = User.objects.get(username='user0')
                # get the users whose pk is >= user0.pk
                self.user_list = list(User.objects.filter(pk__gte=user0.pk))
            except User.DoesNotExist:
                self.user_list = self.generate_users()

        #
        ############################################################
        # this code needs to be rewritten to fill a contest pool!
        ############################################################
        # get all upcoming contests
        # contests = UpcomingContest.objects.all()
        # print('[%s] upcoming contests to fill...' % str(contests.count()))
        #
        # for c in contests:
        #
        #     # for each unfilled spot in the contest...
        #     for remaining_entry in range(c.entries - c.current_entries):
        #
        #         user = self.__get_user()
        #         rlc = RandomLineupCreator( c.site_sport.name,
        #                                                 user.username )
        #         rlc.create( c.pk )

    def play_single_update(self, update_id, async=False):
        """
        :param update_id: is the pk of the /admin/replayer/update/ to play back
        :param async: defaults to False. Set to True if you are running celery workers.
        """

        parser = sports.parser.DataDenParser()
        update = replayer.models.Update.objects.get(pk=update_id)
        print( 'playing replayer update (pk=%s) ...' % update_id)

        ns_parts    = update.ns.split('.') # split namespace on dot for db and coll
        db          = ns_parts[0]
        collection  = ns_parts[1]
        # send it thru parser! Triggers do NOT need to be running for this to work!
        parser.parse_obj( db, collection, ast.literal_eval( update.o ), async=async )

    def play_range(self, update_id, end_update_id, async=False, truncate_chars=None):
        updates = replayer.models.Update.objects.filter(pk__range=(update_id, end_update_id)).order_by('ts')
        if updates.count() <= 0:
            print('there are no updates in the range (%s, %s)' % (str(update_id), str(end_update_id) ))
            return

        self.play_all(updates=updates, async=async, truncate_chars=truncate_chars)

    def play_range_by_ts(self, ts_start, ts_end, max=None, async=False, truncate_chars=None):
        if ts_end < ts_start:
            raise Exception('ts_end < ts_start. hows that going to work exactly?')

        if max is None:
            max = 0 # ie: no limit of how many objects we will play thru

        # query by the timestamp inside the objects, not the time this was created.
        # typically results in a handful of objects (for a single time we parsed all objects in an xml feed))

        # get the first Update ever created for the ts_start, and the last one ever found for the ts_end
        # then get everything between those pks, and remove anything that is not in their range
        print('finding start of range...')
        updates = replayer.models.Update.objects.filter(o__contains=str(ts_start)).order_by('ts')
        if updates.count() == 0:
            print('No replayer Update(s) found!')
            return

        # get the first one
        update_0 = None
        for u in updates:
            update_0 = u
            break

        # get all updates matching the ts_end, is descending order.
        print('finding end of range...')
        updates = replayer.models.Update.objects.filter(o__contains=str(ts_end)).order_by('-ts')
        if updates.count() == 0:
            raise Exception('you need to choose a ts_end that actually matches something or is equal to ts_start')

        update_1 = None
        for u in updates:
            update_1 = u
            break

        dt_start    = update_0.ts # poorly named field, this is actually the 'created' field for Updates
        dt_end      = update_1.ts
        print('removing updates we dont need...')
        updates_in_range = replayer.models.Update.objects.filter(ts__range=(dt_start, dt_end))
        # now create a list of the objects whos 'o' field is really in the range [ts_start, ts_end]
        update_pks = []
        for u in updates_in_range:
            o_ts = literal_eval(u.o).get('dd_updated__id', 0)
            if o_ts >= ts_start and o_ts <= ts_end:
                update_pks.append(u.pk)
        print('getting the exact updates we need by pk...')
        updates = replayer.models.Update.objects.filter(pk__in=update_pks)

        print('playing soon...')
        self.play_all(updates=updates, async=async)

    def play_all(self, updates=None, async=False, truncate_chars=None):
        if truncate_chars is None:
            truncate_chars = self.TRUNCATE_CHARS

        parser = sports.parser.DataDenParser()
        if updates is None:
            updates = replayer.models.Update.objects.all()
        start_pk = updates[0].pk
        size = len(updates)

        print( 'playing %s updates, starting at pk %s ...' % (str(size), str(start_pk) ))

        i = 0
        total_updates = updates.count()
        for update in updates:
            i += 1
            print( '# %s of %s - pk %s - ' % (str(i), str(total_updates), update.pk), update.o[:truncate_chars], '...' ) #update.o[:75]
            ns_parts    = update.ns.split('.') # split namespace on dot for db and coll
            db          = ns_parts[0]
            collection  = ns_parts[1]
            # send it thru parser! Triggers do NOT need to be running for this to work!
            parser.parse_obj( db, collection, ast.literal_eval( update.o ), async=async )

class RandomLineupCreator(object):
    """
    for testing purposes, this class is used to create dummy
    lineups in a contest with randomly chosen players.

    the underlying transactions are not created for the buyins, etc...

    all teams are created with the admin user (pk: 1)
    """

    def __init__(self, sport, username=None, cash=None):
        """
        given a sport, get or create the username specified.

        if username is None, a random use will be gotten or created
        if cash is a positive number, give their account that much cash

        :param sport:
        :param username:
        :param cash:
        :return:
        """
        print( 'WARNING - This class can & will submit teams that EXCEED SALARY REQUIREMENTS')
        self.r = Random()
        self.username = username
        if self.username is None:
            self.username = 'user%s' % str(self.r.randint(1,99))

        self.user, created               = User.objects.get_or_create(username=username)
        self.user.set_password('test')
        self.user.save()

        if cash is not None:
            ct = CashTransaction(self.user)
            ct.deposit(cash)

        self.site_sport_manager = SiteSportManager()
        self.site_sport         = self.site_sport_manager.get_site_sport( sport )
        self.roster_manager     = RosterManager( self.site_sport )

        self.position_lists     = None
        self.lineup_player_ids  = None

    @atomic
    def create(self, contest_pool_id):
        """
        creates a loosly validated lineup (may be over max salary)
        and associates it (creates a contest.models.Entry) with the contest.

        the players for each roster spot are chosen at random

        :param contest_id:
        :return:
        """
        self.lineup_player_ids = [] # initialize the player ids list

        # from the contest, use the draft group to build positional player lists
        # from which we can select players for each roster spot
        contest_pool = ContestPool.objects.get( pk=contest_pool_id )
        self.build_positional_lists( contest_pool.draft_group )

        # select a random player for each roster spot,
        # making sure not to reuse players we have already chosen
        roster_size = self.roster_manager.get_roster_spots_count()
        for roster_idx in range(0, roster_size):
            player_id = self.get_random_player( roster_idx )
            self.lineup_player_ids.append( player_id )

        #
        #
        #  ** this hacks the total salary  for the contest ***
        #
        #
        salary_config = contest_pool.draft_group.salary_pool.salary_config
        original_max_team_salary = salary_config.max_team_salary
        salary_config.max_team_salary = 999999
        salary_config.save()

        # create the lineup
        lm = LineupManager( self.user )
        # this lineup will very likely exceed the total, salary, so
        # lets hack it to make sure it gets created
        lineup = lm.create_lineup( self.lineup_player_ids, contest_pool.draft_group )

        # give the admin just enough cash to buy this team into the contest
        admin = User.objects.get(username='admin')
        ct = CashTransaction( admin )
        ct.deposit( contest_pool.buyin )

        # attempt to buy the team into the contest
        bm = BuyinManager( self.user )
        bm.buyin( contest_pool, lineup )

        # set the salary back to its original value
        salary_config.max_team_salary = original_max_team_salary
        salary_config.save()

    def get_random_player(self, position_list_idx):
        players = self.position_lists[position_list_idx]
        while True: # keep trying
            random_number = self.r.randint(0, len(players) - 1)
            player_id = players[ random_number ].salary_player.player_id
            if player_id not in self.lineup_player_ids:
                return player_id
        # if we made it thru without finding one, raise exception -- not enough players
        raise Exception('get_random_player() couldnt find a player -- maybe the pool is too small?')

    def build_positional_lists(self, draft_group):
        self.position_lists = []
        roster_size = self.roster_manager.get_roster_spots_count()
        for roster_idx in range(0, roster_size):
            self.position_lists.append( [] ) # initialize with the # of lists as are roster spots

        # put each player in each list he could be drafted from
        draft_group_players = Player.objects.filter( draft_group=draft_group )
        for player in draft_group_players:
            for roster_idx in range(0, roster_size):
                sport_player = player.salary_player.player  # the sports.<sport>.models.Player
                if self.roster_manager.player_matches_spot( sport_player, roster_idx ):
                    # add the draft group player
                    self.position_lists[ roster_idx ].append( player )

