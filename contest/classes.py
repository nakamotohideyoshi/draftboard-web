#
# contest/classes.py

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

class ContestPoolCreator(object):

    def __init__(self, sport, prize_structure, start, duration, draft_group=None):
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
        if draft_group is not None:
            self.draft_group = self.validate_draft_group(draft_group)

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
        contest_pool, created = ContestPool.objects.get_or_create()

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
#
# class ContestPoolCreator(ContestPoolCreator):
#
#     def __init__(self, sport):
#         # call parents constructor __init__(sport, prize_structure, start, duration, draft_group=None)
#         super().__init__(sport, prize_structure, start, duration, draft_group=None)

class AbstractContestCreator(object):

    def __init__(self, name, sport, prize_structure):
        self.name               = None
        self.site_sport         = None
        self.prize_structure    = None
        self.start              = None  # start of the contest
        self.end                = None  # live games must start before this datetime

    def create(self):
        """
        Validate all the internal fields which will make this contest.
        Then create the underlying model and return it.
        """
        c =  Contest(name=self.name,
                     site_sport=self.site_sport,
                     prize_structure=self.prize_structure,
                     start=self.start,
                     end=self.end)
        c.save()
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

    def __init__(self, name, sport, prize_structure, start, end):
        self.name               = name
        self.site_sport         = SiteSport.objects.get( name=sport )
        self.prize_structure    = prize_structure
        self.start              = start     # start of the contest
        self.end                = end       # live games must start before this datetime

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

# %cpaste
# from random import Random, shuffle
# class EntryFiller(object):
#     def __init__(self, entries=[], contest_size=2):
#         self.r = Random()
#         self.original_entries = list(entries)
#         self.entries = list(entries)
#         self.first_entries = None
#         self.contest_size = contest_size
#     def get_uniques_from_pool(self, limit=0, excludes=[]):
#         # get uniques from the pool.
#         # if limit is non-zero, return equal to or less than limit.
#         # does not return any values contains in exclude list.
#         ret_entries = list(set(self.entries))
#         for e in excludes:
#             if e in ret_entries:
#                 ret_entries.remove(e)
#         shuffle(ret_entries)
#         return ret_entries[:limit]
#     def make_contest(self, entries):
#         print('making contest:', str(entries))
#     def remove_from_pool(self, remove_entries):
#         for e in remove_entries:
#             self.entries.remove(e)
#     def cleanup_post_round_unfilled_entries(self, entries_to_fill):
#         # combine entries to fill with the extras.
#         # create contest if possible
#         num_entries_needed = contest_size - len(entries_to_fill)
#         extras = self.get_uniques_from_pool(limit=num_entries_needed, excludes=entries_to_fill)
#         combined_entries = entries_to_fill + extras
#         if len(combined_entries) < self.contest_size:
#             # check if we have to bonus out any remainders here, we're at the end.
#             print('check only entry not filled:', str(combined_entries))
#         else:
#             # make a contest
#             self.make_contest(combined_entries)
#     def print_match(self, list_entries=[]):
#         print('print_match:', str(list_entries))
#     def fair_match(self):
#         # stash everyones first entry
#         self.first_entries = list(set(self.entries))
#         self.fair_match_h(self.first_entries)
#     def fair_match_h(self, entries_to_fill=[], round=1):
#         if entries_to_fill == [] and self.entries == []:
#             print('done.')
#             return # we are done
#         print('round:', str(round))
#         if entries_to_fill == []:
#             # do the next round. get unique set from self.entries and recurse
#             entries_to_fill = self.get_uniques_from_pool()
#             self.remove_from_pool(entries_to_fill)
#             self.fair_match_h(entries_to_fill)
#         elif len(entries_to_fill) < self.contest_size:
#             # we had an odd number leftover.
#             # get additional entries from to match with
#             self.cleanup_post_round_unfilled_entries(entries_to_fill)
#         else:
#             self.make_contest(entries_to_fill[:self.contest_size])
#             self.fair_match_h(entries_to_fill[self.contest_size:], round=round+1)
# --
# test_entries = [1,1,2,3,4,5,5,5,6,7,8,9,9,9,9,9,9,9]
# contest_size = 2
# filler = EntryFiller(test_entries, contest_size)
# filler.fair_match()
