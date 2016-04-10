#
# contest/classes.py

from random import Random, shuffle
from django.db.transaction import atomic
import os
import struct
from .models import (
    Contest,
    ContestPool,
)
from sports.models import (
    SiteSport,
    PlayerStats,
)
from mysite.exceptions import (
    IncorrectVariableTypeException,
)
from dataden.util.timestamp import DfsDateTimeUtil
from datetime import (
    datetime,
    timedelta,
    time,
    date,
)
from django.utils import timezone
from sports.classes import SiteSportManager as SSM
from ticket.classes import TicketManager
from ticket.models import TicketAmount
from contest.models import Contest, Entry
from lineup.classes import LineupManager
import lineup.models
import prize.models
from prize.classes import TicketPrizeStructureCreator
import draftgroup.models
from draftgroup.classes import DraftGroupManager
from roster.classes import RosterManager
from contest.buyin.models import Buyin

class ContestPoolCreator(object):

    USER_ENTRY_LIMIT    = 3
    ENTRY_CAP           = 0     # 0 means there is no cap on the total # of entries

    def __init__(self, sport, prize_structure, start, duration,
                 draft_group=None, user_entry_limit=None, entry_cap=None):
        """
        :param sport: the name of the sport
        :param prize_structure: the prize.models.PrizeStructure
        :param start: datetime object, the scheduled start time
        :param duration: the integer number of minutes from the start until the end
                         that makes a range of datetime objects, between which to use
                         the sport's games.
        :param draft_group: if specified, the DraftGroup to use. otherwise get an existing one
                            using the DraftGroupManager class.
        """
        site_sport_manager = SSM()
        self.sport = sport
        self.site_sport = site_sport_manager.get_site_sport(self.sport)

        # validate and set the start datetime
        self.start = self.validate_start(start)

        # validate and set the duration (integer minutes)
        self.duration = self.validate_duration(duration)

        # validate and set the prize_structure model
        self.prize_structure = self.validate_prize_structure(prize_structure)

        # if a draft_group is specified, validate it
        self.draft_group = draft_group
        if self.draft_group is not None:
            self.draft_group = self.validate_draft_group(draft_group)

        # set the user entry limit (the max # of Entrys from one user for this ContestPool)
        self.user_entry_limit = self.USER_ENTRY_LIMIT
        if user_entry_limit is not None:
            self.user_entry_limit = user_entry_limit

        # set the entry cap (if there is one, typically there is not)
        self.entry_cap = self.ENTRY_CAP
        if entry_cap is not None:
            self.entry_cap = entry_cap

    def get_or_create(self):
        """
        Gets a matching ContestPool or else creates and returns a new one for
        the parameters passed in the __init__ method.

        If a matching DraftGroup does not exist for the sport and timeframe,
        this class will use the DraftGroupManager class and attempt to create one,
        using DraftGroupManager.get_for_site_sport(site_sport, start, end).

        returns the newly created ContestPool, or raises the proper exception if errors exist
        """
        if self.draft_group is None:
            # use the DraftGroupManager class to create (or retrieve a matching) draft group
            draft_group_manager = DraftGroupManager()
            self.draft_group = draft_group_manager.get_for_site_sport(self.site_sport, self.start, self.get_end())

        # now create the ContestPool model instance
        contest_pool, created = ContestPool.objects.get_or_create(site_sport=self.site_sport,
                                                                  prize_structure=self.prize_structure,
                                                                  start=self.start,
                                                                  end=self.get_end(),
                                                                  draft_group=self.draft_group)
        contest_pool.current_entries = 0
        contest_pool.max_entries = self.user_entry_limit
        contest_pool.entries = self.entry_cap
        contest_pool.save()
        return contest_pool, created

    def get_end(self):
        """
        returns the datetime equivalent to the start time plus the duration minutes
        """
        return self.start + timedelta(minutes=self.duration)

    def validate_duration(self, duration):
        if not isinstance(duration, int):
            raise IncorrectVariableTypeException(self.__class__.__name__, 'duration')
        return duration

    def validate_start(self, start):
        if not isinstance(start, datetime):
           raise IncorrectVariableTypeException(self.__class__.__name__, 'start')
        return start

    def validate_prize_structure(self, prize_structure):
        if isinstance(prize_structure, prize.models.PrizeStructure):
            return prize_structure
        # else raise exception that this is not the proper type
        raise IncorrectVariableTypeException(self.__class__.__name__, 'prize_structure')

    def validate_draft_group(self, draft_group):
        if isinstance(draft_group, draftgroup.models.DraftGroup):
            return draft_group
        # else raise exception that this is not the proper type
        raise IncorrectVariableTypeException(self.__class__.__name__, 'draft_group')

class ContestPoolManager(object):

    def __init__(self, contest_pool):
        self.contest_pool = contest_pool

    def new_contest(self):
        """
        create and return a new contest based on the settings of this ContestPool
        """
        contest_creator = ContestCreator('new contest', self.contest_pool.site_sport,
                                         self.contest_pool.prize_structure,
                                         self.contest_pool.start, self.contest_pool.end )
        return contest_creator.create()

    def add_entry(self, contest, entry):
        pass # TODO remove
        # TODO - we are going to need the ContestPool to set the Contest(s)
        # TODO   it creates when it starts into the Entry and Buyin objects
        # TODO   which point to it. this way we

        #
        ###################################################
        # the below code shows a snippet from the buyinmanager
        # which shows the Entry and Buyin, and incrememnting/logging we need to do
        # to finish properly hooking up Entry objects to Contests for inprogress or later Contests!
        ##################################################
        # #
        # # Create the Entry
        # entry = Entry()
        # entry.contest_pool = contest_pool
        # #entry.contest = contest # the contest will be set later when the ContestPool starts
        # entry.contest = None
        # entry.lineup = lineup
        # entry.user = self.user
        # entry.save()
        #
        # #
        # # Create the Buyin model
        # buyin = Buyin()
        # buyin.transaction = transaction
        # buyin.contest_pool = contest_pool
        # #buyin.contest = contest # the contest will be set later when the ContestPool starts (?)
        # buyin.contest = None
        # buyin.entry = entry
        # buyin.save()
        #
        # #
        # # Increment the contest_entry variable
        # contest.current_entries = F('current_entries') + 1
        # contest.save()
        # contest.refresh_from_db()
        #
        # msg = "User["+self.user.username+"] bought into the contest #"\
        #               +str(contest.pk)+" with entry #"+str(entry.pk)
        # Logger.log(ErrorCodes.INFO, "Contest Buyin", msg )
        #
        # #
        # # pusher contest updates because entries were changed
        # ContestPush(ContestSerializer(contest).data).send()

    def start(self):
        """
        this method should be called to create the underlying contests
        and add entries to them and everything should be inprogress
        when this method is done!
        """
        cpf = ContestPoolFiller(self.contest_pool)
        cpf.fair_match()

class AbstractContestCreator(object):

    def __init__(self, name, site_sport, prize_structure, start=None, end=None):
        self.name               = name
        self.site_sport         = site_sport
        self.prize_structure    = prize_structure
        self.start              = start  # start of the contest
        self.end                = end  # live games must start before this datetime

    def create(self):
        """
        Validate all the internal fields which will make this contest.
        Then create the underlying model and return it.
        """
        c =  Contest.objects.create(name=self.name,
                     site_sport=self.site_sport,
                     prize_structure=self.prize_structure,
                     start=self.start,
                     end=self.end)
        return c

class ContestCreator(AbstractContestCreator):
    """
    this can be used to make a quick 'n dirty contest,
    but the admin form (ie: localhost/admin/contest/contest/add/)
    performs all the logic and validation behind the scenes
    and should be the primary tool for creating new Contests.

    To clone/respawn existing Contests, use Contest's own clone(), or
    respawn() methods, respectively.
    """

    def __init__(self, name, site_sport, prize_structure, start, end):
        super().__init__(name, site_sport, prize_structure, start, end)

class Dummy(object):
    """
    Create for the current day that starts in the evening
    """

    DEFAULT_NAME = 'dummy-contest'

    @staticmethod
    def create(sport='nfl'):

        TicketManager.create_default_ticket_amounts()
        ticket_amount = TicketAmount.objects.all()[0]
        #ticket_amount.amount
        ticket_prize_creator = TicketPrizeStructureCreator(ticket_value=5.00,
                                    number_of_prizes=1, name='contest-dummy-prize-structure')
        prize_structure = ticket_prize_creator.save()
        #prize_structure.name
        now = timezone.now()
        start = DfsDateTimeUtil.create( now.date(), time(23,0) )
        end = DfsDateTimeUtil.create( now.date() + timedelta(days=1), time(0,0) )
        creator = ContestCreator( name=Dummy.DEFAULT_NAME,
                                  sport=sport,
                                  prize_structure=prize_structure,
                                  start=start, end=end )
        contest = creator.create()
        print('created new dummy contest with pk:', contest.pk)
        return contest

class ContestLineupManager(object):
    """
    In [12]: hex( 65535 ) # max short int
    Out[12]: '0xffff'

    """

    # invalid player or no player
    PLAYER_INVALID      = 0
    PLAYER_NOT_STARTED  = 65535

    # size in bytes of these portions of the payload
    SIZE_LINEUPS                = 4
    SIZE_PLAYERS_PER_LINEUP     = 2

    SIZE_LINEUP_ID              = 4
    SIZE_PLAYER                 = 2     # a single player is 2 bytes

    def __init__(self, contest=None, contest_id=None):
        """
        given the contest, build the payload for the "get all contest lineups" api,

        takes care of not showing certain players in user lineups whose games
        have not yet started, and are thus not yet locked in and shouldnt be known

        :param contest:
        :param contest_id: overrides contest param
        :return:
        """

        if contest_id is not None:
            self.contest = Contest.objects.get( pk=contest_id )
        elif contest is not None:
            self.contest = contest
        else:
            raise Exception('contest must not be None')

        dgm = DraftGroupManager()
        self.draft_group_players    = dgm.get_players( self.contest.draft_group )

        # a map where the player id points to their own id if their game
        # has started, or to 0xffff if they havent started yet
        #
        # i can see a reason we would want to cache the get_starter_map result ....
        self.starter_map = self.get_starter_map(self.draft_group_players)

        # determine the size of a lineup in bytes
        rm = RosterManager( self.contest.site_sport )
        self.players_per_lineup = rm.get_roster_spots_count()

        self.entries = Entry.objects.filter( contest=self.contest )

    def get_starter_map(self, draft_group_players):
        """
        build a mapping of player ids to their 1) their own id if their game
        has started, or 2) to the PLAYER_NOT_STARTED value if they
        have not started their game yet!

        :param draft_group_players:
        :return:
        """
        self.starter_map = {}
        now = timezone.now()
        for p in self.draft_group_players:
            # print( str(now), ' >= ', str(p.start))
            if now >= p.start:
                self.starter_map[ p.salary_player.player_id ] = p.salary_player.player_id
            else:
                self.starter_map[ p.salary_player.player_id ] = self.PLAYER_NOT_STARTED
        return self.starter_map

    def is_player_game_started(self, player_id):
        """
        return a boolean indicating if this players game has started

        :param player_id:
        :return:
        """
        return self.starter_map[ player_id ] < self.PLAYER_NOT_STARTED

    def get_lineup_data(self, user, lineup_id):
        """
        get lineup data we can show to other users, with masked
        out players whos games have not started yet.

        this is the "single team" version of the ContestLineupManager
        method that gets all lineups in a contest,

        ... this gets all the player stats for players in games.

        :param lineup_id:
        :return:
        """
        lm = LineupManager(user)
        return lm.get_lineup_from_id(lineup_id, self.contest)

    def __header_size(self):
        """
        return the number of bytes in the header,
        which is everything before the individual teams

        :return:
        """
        return self.SIZE_LINEUPS + self.SIZE_PLAYERS_PER_LINEUP

    def __payload_size(self):
        """
        return the number of bytes in the payload (all the lineup players)

        :return:
        """
        return (self.SIZE_LINEUP_ID + self.players_per_lineup * self.SIZE_PLAYER) * self.entries.count()

    def get_size_in_bytes(self):
        #print( '__header_size() = %s' %str(self.__header_size()), '__payload_size() = %s' % str(self.__payload_size()))
        return self.__header_size() + self.__payload_size()

    def pack_into_h(self, fmt, bytes, offset, val):
        """
        calls struct.pack_into() on the given fmt, bytearray() with given offset and value
        and returns the new offset after adding the size of the format character to offset

        the 'fmt' param must be a single format character, like 'i' or 'h'

        returns a tuple of (new_offset, bytes_after_packing)

        :param fmt:
        :param bytes:
        :param offset:
        :param val:
        :raises UnsupportedFormatException: if there is a problem getting the size of the fmt character
        :return:
        """

        size = struct.calcsize( fmt )
        #print('<size so far>', str(size), 'raw:', str(bytes))
        struct.pack_into( fmt, bytes, offset, val )
        new_offset = offset + size
        return (new_offset, bytes)

    def get_raw_bytes(self):
        """
        generate the bytes of the payload which contains the
        number of lineups, players per lineup, and each lineup

        note:
            In [21]: struct.calcsize('i')       # 'i' is an integer
            Out[21]: 4

            In [22]: struct.calcsize('h')       # 'h' is a short
            Out[22]: 2

        :return: bytes
        """
        if self.contest.draft_group.start > timezone.now():
            return bytearray()

        bytes = bytearray( self.get_size_in_bytes() )
        #print( '# contest entries:', str(self.contest.entries))
        offset, bytes = self.pack_into_h( '>i', bytes, 0, self.contest.entries )
        #print( '# players per lineup:', str(self.players_per_lineup))
        offset, bytes = self.pack_into_h( '>H', bytes, offset, self.players_per_lineup )

        for e in self.entries:
            # pack the lineup id
            #print( '    <add lineup> %s' % str(e.lineup.pk), '  : bytes[%s]' % str(len(bytes) ) )
            offset, bytes = self.pack_into_h('>i', bytes, offset, e.lineup.pk )

            # pack in each player in the lineup, in order of course
            lm = LineupManager( e.user )
            for pid in lm.get_player_ids( e.lineup ):
                #print( '        pid:', str(pid ))
                # offset, bytes = self.pack_into_h( '>h', bytes, offset, pid )
                #print( 'pid:', str( pid ) )

                offset, bytes = self.pack_into_h( '>H', bytes, offset, pid )

        # all the bytes should be packed in there now!
        return bytes

    def dev_get_all_lineups(self, contest_id):
        """
        for testing purposes, get all the lineups as json.
        """

        settings_module_name = os.environ['DJANGO_SETTINGS_MODULE']
        # 'mysite.settings.local'   should let this method work
        if 'local' not in settings_module_name:
            raise Exception('json from dev_get_all_lineups not allowed unless local settings being used')

        lineups = []

        for e in self.entries:

            lineup_id = e.lineup.pk
            player_ids = []

            # pack in each player in the lineup, in order of course
            lm = LineupManager( e.user )
            for pid in lm.get_player_ids( e.lineup ):
                #player_ids.append( self.starter_map[ pid ] ) # masks out no-yet-started players
                player_ids.append( pid )

            lineups.append( {
                'lineup_id'     : lineup_id,
                'player_ids'    : player_ids,
            } )

        data = {
            'endpoint'                      : '/contest/all-lineups/%s?json' % int( contest_id ),
            'bytes_for_condensed_response'  : self.get_size_in_bytes(),
            'total_lineups'                 : self.contest.entries,
            'players_per_lineup'            : self.players_per_lineup,
            'lineups'                       : lineups,
        }
        return data

    def get_http_payload(self):
        return ''.join('{:02x}'.format(x) for x in self.get_raw_bytes() )

class FairMatch(object):

    class ZeroEntriesException(Exception): pass

    class NotEnoughEntriesException(Exception): pass

    def __init__(self, entries=[], contest_size=2):  # size / prize_structure will come from ContestPool instance
        # instance of random number generator
        self.r = Random()

        # size of contests to generate (ie: 10-mans)
        self.contest_size = contest_size

        # make a copy of original list of all the entries
        self.original_entries = list(entries)

        # for debugging - a list of all the contests made
        self.contests = None

    def get_contests(self):
        return self.contests['contests']

    def get_contests_forced(self):
        return self.contests['contests_forced']

    def fill_contest(self, entries, size, force=False):
        """
        :param force: if force is true, skip the size check, and add the entries to contest regardless
        :return:
        """
        if len(entries) == 0:
            err_msg = '0 entries passed to fill_contest()'
            raise self.ZeroEntriesException(err_msg)

        if not force and len(entries) < size:
            err_msg = '%s needed, entries list: %s' % (size, str(entries))
            raise self.NotEnoughEntriesException(err_msg)

        ss = ''
        if force:
            ss = '** = superlay is possible here.'
        print('    making contest:', str(entries), 'force:', str(force), '%s'%ss)
        # TODO fill c

        self.__add_contest_debug(entries, size, force=force)

    def __add_contest_debug(self, entries, size, force=False):
        if force:
            # entries we need to enter into a contest no matter what (first entries)
            self.contests['contests_forced'].append( entries )
        else:
            # this
            self.contests['contests'].append( entries )
        self.contests['contest_size'] = size

    @atomic
    def run(self):
        """
        create all required contests using the FairMatch algorithm
        with the given user entries.
        """

        self.contests = {
            'entry_pool_size'   : len(list(self.original_entries)),
            'entry_pool'        : list(self.original_entries),
            'contests'          : [],
            'contests_forced'   : []
        }

        # run the algorithm, starting it all off by passing
        # a mutable copy of all the unique entries to run_h()
        all_entries = list(self.original_entries)
        self.run_h(all_entries, 1, [], verbose=True)

        # now set the unused entries
        unused_entries = self.contests['entry_pool']
        for c in self.contests['contests']:
            for entry in c:
                unused_entries.remove(entry)
        self.contests['unused_entries'] = unused_entries

    def get_and_remove_uniques(self, entries, exclude):
        """
        breaks up the list of entries into two lists:
         a) all unique entries
         b) the remaining pool of entries after 1 of each unique has been removed

        :param entries: all entries pool
        :param exclude: ignore these entries
        :return: a tuple of two lists in the form: (unique_entries, remaining_entries)
        """
        uniques = list(set(entries) - set(exclude))
        for e in uniques:
            entries.remove(e)
        # also remove the excludes! they might not have been
        # entirely removed because uniques will not
        return uniques, entries

    def remove_from_list(self, target, removes):
        for e in removes:
            target.remove(e)
        return target

    def get_additional_uniques(self, entries, n, exclude):
        """
        get 'n' uniques out of 'entries', excluding those in 'exclude' list

        removes the entries return from the original 'entries' list

        :param entries:
        :param n:
        :param exclude:
        :return:
        """

        additional_uniques = list(set(entries))
        print('        get %sx entry from %s ignoring entries in %s' % (str(n), str(additional_uniques), str(exclude)))
        # excludes the entries we already have
        for e in exclude:
            try:
                additional_uniques.remove(e)
            except ValueError:
                pass # e didnt exist
        shuffle(additional_uniques)
        additional_uniques = additional_uniques[:n]

        entries = self.remove_from_list(entries, additional_uniques)

        return additional_uniques, entries

    def run_h(self, entries, round, exclude, verbose=False):
        """
        check for any priority entries from the previous round
        and get them into contests if possible.

        continue onto the main contest generation loop,
        and fill all the entries at this round that we can.

        :param remaining_uniques: all first entries for this round
        :param round: integer number of the round starting with 1
        :param priority: entries with priority (from previous round)
        :return:
        """
        if entries == [] and exclude == []:
            if verbose:
                print('done!')
            return # we are done

        if verbose:
            print('')
            print('++++ beginning of round %s ++++' % str(round))
            print('(pre-round) entry pool:', str(entries))

        # get the unique entries for this round
        round_uniques, remaining_entries = self.get_and_remove_uniques(entries, exclude)
        remaining_uniques = list(set(remaining_entries) - set(exclude))
        if verbose:
            print('excluded(for fairness):', str(exclude))
            print('round uniques         :', str(round_uniques))
            print('remaining entries     :', str(remaining_entries), 'including any entries in exclude (debug)')
            print('remaining uniques     :', str(remaining_uniques), 'not including excludes. potential additional entries this round')

        exclude_users_for_fairness = []
        while True:
            # shuffle the entries and then select enough for a contest
            shuffle(round_uniques)
            random_contest_entries = round_uniques[:self.contest_size]

            try:
                # create and fill a contest using the random entries
                self.fill_contest(random_contest_entries, self.contest_size)
                # remove entries from the round uniques once they are filled
                round_uniques = self.remove_from_list(round_uniques, random_contest_entries)

            except self.ZeroEntriesException:
                break

            except self.NotEnoughEntriesException:
                # attempt to fill one last contest by randomly
                # selecting additional entries from the remaining pool of uniques.
                # in order to be fair, add additional selected users to a
                # list of excludes to prevent them from getting fills
                # next round (because they would have had 2 fills this round).
                n = self.contest_size - len(round_uniques)
                # get n additional uniques from the remaining uniques, not including
                # whatever is currently in round_uniques
                additional_uniques = list(set(remaining_uniques) - set(round_uniques))
                shuffle(additional_uniques)
                selected_additional_entries = additional_uniques[:n]

                if verbose:
                    print('        -> %s didnt get filled.' % str(round_uniques))
                    # print('        -> selected_additional_entries = '
                    #       'list(set(remaining_uniques) - set(round_uniques))[:n]')
                    print('        -> randomly chose:', str(selected_additional_entries), 'from', str(additional_uniques), ''
                                        '(avoiding these obviously:', str(round_uniques),')')

                # now make the last contest of the round, or issue refunds
                first_round = round == 1
                try:
                    self.fill_contest(round_uniques + selected_additional_entries, self.contest_size, force=first_round)
                except:
                    # failed on the last time around, but there may be enough
                    # excludes required to create the last contest on
                    # one more round so break and try again

                    break

                exclude_users_for_fairness = selected_additional_entries
                # be sure to remove successfully filled entries from the total remaining entries
                entries = self.remove_from_list(entries, exclude_users_for_fairness)
                break

        if verbose: print('    (exclude %s in round %s)' % (str(exclude_users_for_fairness),str(round+1)))

        # post while loop
        self.run_h(entries, round+1, exclude_users_for_fairness, verbose=verbose)

    def print_debug_info(self):
        print('*** post run() information ***')
        # print(self.contests)
        for k,v in self.contests.items():
            print('%-16s:'%k, v)
        print(len(self.contests['contests']), 'contests created')
        #unused_entries = self.contests['entry_pool']
        # for c in self.contests['contests']:
        #     for entry in c:
        #         unused_entries.remove(entry)
        print('unused entries:', str(self.contests['unused_entries']))

# from contest.classes import ContestPoolCreator
# creator = ContestPoolCreator('nba', ps, start, duration)
# from prize.models import PrizeStructure
# ps = PrizeStructure.objects.get(pk = 1)
# from django.utils import timezone
# start = timezone.now()
# start = start.replace(2016, 3, 30, 23, 30, 0, 0) # 7:30pm est
# duration = 270
# creator = ContestPoolCreator('nba', ps, start, duration)
# cp, c = creator.get_or_create()
#
# username = 'steve'
# from django.contrib.auth.models import User
# user = User.objects.get(username=username)
# from cash.classes import CashTransaction
# ct = CashTransaction(user)
# ct.deposit(10.00)
# contest_pool_id = 2
# from contest.models import ContestPool
# cp = ContestPool.objects.get(pk = contest_pool_id)
# from replayer.classes import RandomLineupCreator
# rlc = RandomLineupCreator('nba',username)
# rlc.create(cp.pk)
#
# # get all LiveContestPool.objects.all()
# # ensure that some ContestPools exist upcoming for this to work
# %cpaste
# from contest.models import UpcomingContestPool, Entry
# from contest.classes import FairMatch
# from replayer.classes import RandomLineupCreator
# contest_pools = UpcomingContestPool.objects.all()
# for contest_pool in contest_pools:
#     for username in usernames:
#         rlc = RandomLineupCreator('nba',username)
#         rlc.create(contest_pool_id=contest_pool.pk)
#     fair_match = FairMatch(entries=Entry.objects.filter(contest_pool=contest_pool))

class ContestPoolFiller(object):
    """
    uses FairMatch object to determine how to fill contests based on all the entries of the ContestPool
    """

    def __init__(self, contest_pool):
        self.contest_pool = contest_pool
        if isinstance(self.contest_pool, int):
            self.contest_pool = ContestPool.objects.get(pk=self.contest_pool)

        # get all the Entry objects for the given contest pool
        self.entries = Entry.objects.filter(contest_pool=contest_pool)

        # # get the unique users entries
        # self.distinct_user_entries = self.entries.distinct('user')
        self.user_entries = None

    @atomic
    def fair_match(self):
        """
        create all required contests using the FairMatch algorithm
        with the given user entries.
        """
        contest_size = self.contest_pool.prize_structure.get_entries()
        entry_pool = [ e.user.pk for e in self.entries ]

        self.user_entries = {}
        for e in self.entries:
            try:
                self.user_entries[ e.user.pk ].append( e )
            except KeyError:
                self.user_entries[ e.user.pk ] = [ e ]

        # run the FairMatch algorithm to get the
        # information on how to fill the contests
        fm = FairMatch(entry_pool, contest_size)
        fm.run()

        # debug - can be removed
        fm.print_debug_info()

        # use the (random) contests + contests_forced lists of lists of entries
        # to generate the contests, extracting and removing 1 entry for each
        # user id we find along the way
        for contest_entries in fm.get_contests():
            # 1. create a contest for the entries
            cpm = ContestPoolManager(self.contest_pool)
            contest = cpm.new_contest()

            # 2. enter them into the contest
            for user_id in contest_entries:
                entry = self.user_entries[ user_id ].pop()

                # find the contest pool entry for this user
                entry.contest = contest
                entry.save()

                # find the buyin and set the contest to that and save it
                buyin = Buyin.objects.get(entry=entry)
                buyin.contest = contest
                buyin.save()

            # set the number of entries for completeness
            contest.current_entries = len(contest_entries)
            contest.save()

            # #
            # # pusher contest updates because entries were changed
            # ContestPoolPush(ContestPoolSerializer(contest_pool).data).send()

        # change the status of the contest pool to created now
        self.contest_pool.status = ContestPool.CREATED
        self.contest_pool.save()
        #self.contest_pool.refresh_from_db()
