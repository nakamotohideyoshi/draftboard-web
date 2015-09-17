#
# contest/classes.py

import struct
from .models import Contest
from sports.models import SiteSport, PlayerStats
from dataden.util.timestamp import DfsDateTimeUtil
from datetime import datetime
from datetime import timedelta
from datetime import time
from django.utils import timezone
from sports.classes import SiteSportManager as SSM
from ticket.classes import TicketManager
from ticket.models import TicketAmount
from contest.models import Contest, Entry
from lineup.classes import LineupManager
import lineup.models
from prize.classes import TicketPrizeStructureCreator
from draftgroup.classes import DraftGroupManager
from roster.classes import RosterManager

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
        print( 'TODO - dont forget to cache the starter_map -- it cant be too fast!!')
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

    def get_lineup_data(self, lineup_id):
        """
        get lineup data we can show to other users, with masked
        out players whos games have not started yet.

        this is the "single team" version of the ContestLineupManager
        method that gets all lineups in a contest,

        ... this gets all the player stats for players in games.

        :param lineup_id:
        :return:
        """

        data = []
        ssm = SSM()

        lineup_players = lineup.models.Player.objects.filter( lineup__pk=lineup_id ).order_by('idx')

        player_stats_models = ssm.get_player_stats_class( self.contest.site_sport )

        for lineup_player in lineup_players:
            player_stats = None # havent found them yet
            # check easy stats model type ( ie: baseball has PlayerStatsHitter & PlayerStatsPitcher
            started         = False
            category_stats  = []
            for player_stats_model in player_stats_models:
                #
                # if the player is masked out in the starter map, do not display which player it is
                started = self.is_player_game_started( lineup_player.player_id )
                if not started:
                    continue

                #
                # try to get actual stats for the player
                try:
                    player_stats = player_stats_model.objects.get( player_id=lineup_player.player_id,
                                        srid_game=lineup_player.draft_group_player.game_team.game_srid )
                except player_stats_model.DoesNotExist:
                    player_stats = None
                    pass # the stats werent found for this person ( possibly wont ever be found! )

                if player_stats is not None:
                    # at this point, if player_stats is not None, add it
                    # to the return data (if player game started!)
                    #data.append( player_stats.to_json() )
                    category_stats.append( player_stats.to_json() )

            # add the "category_stats" list  -- ie: the stats for each roster idx
            data.append( {
                'started'   : started,
                'i'         : lineup_player.idx,
                'data'      : category_stats,
            } )

            started         = False # reset flag after adding this player

        # this data is safe to return via the API because
        # the players whos games have not yet started have
        # not been shown!
        return data

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
        return (self.SIZE_LINEUP_ID + self.players_per_lineup * self.SIZE_PLAYER) * self.contest.entries

    def get_size_in_bytes(self):
        print( '__header_size() = %s' %str(self.__header_size()), '__payload_size() = %s' % str(self.__payload_size()))
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
        print('<size so far>', str(size), 'raw:', str(bytes))
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
                print( 'pid:', str( pid ) )
                offset, bytes = self.pack_into_h( '>H', bytes, offset, self.starter_map[ pid ] )

        # all the bytes should be packed in there now!
        return bytes

    def get_http_payload(self):
        return ''.join('{:02x}'.format(x) for x in self.get_raw_bytes() )

# # params: draft_group, games (ids), players (ids)
# class AbstractPlayerStatsManager(object):
#     """
#     this class will typically be held in cache, and can quickly
#     get, or update those player stats based on real-time data.
#     """
#
#     def __init__(self):
#         pass # TODO get from cache, else: initialize here
#
#         self.load_games( )   # TODO
#         self.load_players( ) # TODO
#
#     def get_players(self, player_ids):
#         pass # TODO
#
#
#     # def update_players(self, player_stats):
#     #     pass # TODO