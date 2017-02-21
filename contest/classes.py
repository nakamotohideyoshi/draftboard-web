import os
import struct
from collections import (
    OrderedDict,
    Counter,
)
from datetime import (
    datetime,
    timedelta,
    time,
)
from logging import getLogger
from random import Random, shuffle

from django.db.transaction import atomic
from django.utils import timezone

import draftgroup.models
import lineup.models
import prize.models
from contest.buyin.models import Buyin
from contest.models import (
    Contest,
    Entry,
    ClosedContest,
)
from dataden.util.timestamp import DfsDateTimeUtil
from draftgroup.classes import DraftGroupManager
from lineup.classes import LineupManager
from mysite.exceptions import (
    IncorrectVariableTypeException,
)
from prize.classes import TicketPrizeStructureCreator
from roster.classes import RosterManager
from sports.classes import SiteSportManager as SSM
from sports.models import SiteSport
from ticket.classes import TicketManager
from ticket.models import TicketAmount
from util.dfsdate import DfsDate
from util.dicts import DictTools
from util.slack import WebhookContestInfo
from .models import (
    ContestPool,
    SkillLevel,
)

logger = getLogger('contests.classes')
slack = WebhookContestInfo()


class SkillLevelManager(object):
    class CanNotEnterSkillLevel(Exception):
        pass

    # the main model class
    model_class = SkillLevel

    # by default we only care about enforced skill levels
    enforced = True

    def __init__(self):
        self.skill_levels = self.get_skill_levels()

    def get_skill_levels(self):
        """ returns a QuerySet of the SkillLevel objects in ascending order """
        return self.model_class.objects.filter(enforced=self.enforced).order_by('-gte')

    def get_for_amount(self, amount):
        # when the skill level objects are ordered descending,
        # loop thru them and find the first skill level
        # for which this amount is greater than or equal to.
        for skill_level in self.skill_levels:
            if skill_level.gte <= amount:
                return skill_level

    def validate_can_enter(self, user, contest_pool):
        """
        will raise CanNotEnterSkillLevel if the user is blocked from that ContestPool.

        otherwise does nothing.

        :param user:
        :param contest_pool:
        :return:
        """

        # the contest attempting to be joined
        target_skill_level = contest_pool.skill_level
        if target_skill_level.enforced == False:
            return  # the skill level of this contest is not enforced -- anyone can join no matter what

        # find any enforced skill_levels we have an entry in not matching our target.
        # if any are found, that means we cant join and must raise exception
        entries = Entry.objects.filter(
            user=user,
            contest_pool__draft_group=contest_pool.draft_group,
            contest_pool__skill_level__enforced=True
        ).exclude(contest_pool__skill_level=target_skill_level)

        if entries.count() > 0:
            raise self.CanNotEnterSkillLevel()


class ContestPoolCreator(object):
    USER_ENTRY_LIMIT = 3
    ENTRY_CAP = 0  # 0 means there is no cap on the total # of entries

    def __init__(self, sport, prize_structure, start, duration,
                 draft_group=None, user_entry_limit=None, entry_cap=None, set_name=True):
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

        # whether or not to set a name at creation time
        self.set_name = set_name

        # skill level
        slm = SkillLevelManager()
        self.skill_level = slm.get_for_amount(self.prize_structure.buyin)

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
            self.draft_group = draft_group_manager.get_for_site_sport(self.site_sport, self.start,
                                                                      self.get_end())

        # now create the ContestPool model instance
        contest_pool, created = ContestPool.objects.get_or_create(site_sport=self.site_sport,
                                                                  prize_structure=self.prize_structure,
                                                                  start=self.start,
                                                                  end=self.get_end(),
                                                                  draft_group=self.draft_group,
                                                                  skill_level=self.skill_level)
        if self.set_name:
            contest_pool.name = self.build_name()
            # save() will get called later

        contest_pool.current_entries = 0
        contest_pool.max_entries = self.user_entry_limit
        contest_pool.entries = self.entry_cap
        contest_pool.save()
        return contest_pool, created

    def build_name(self):
        """
        :return: string name for the ContestPool
        """

        # format the buyin amount
        buyin_dollars = self.prize_structure.buyin
        buyin_cents = self.prize_structure.buyin - float(buyin_dollars)
        buyin_str = '$%s' % str(int(buyin_dollars))
        if buyin_cents >= 0.01:
            buyin_str += '%.2f' % buyin_cents

        # get the sport & tourney type (H2H, 50/50, 10-Man Tourney, etc...)
        sport_str = self.site_sport.name.upper()
        game_format_str = self.prize_structure.get_format_str()

        name = '%s %s %s' % (buyin_str, str(sport_str), str(game_format_str))
        return name

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
        contest_creator = ContestCreator(self.contest_pool.name, self.contest_pool.site_sport,
                                         self.contest_pool.prize_structure,
                                         self.contest_pool.start, self.contest_pool.end)
        return contest_creator.create()

    def add_entry(self, contest, entry):
        pass  # TODO remove
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
        self.name = name
        self.site_sport = site_sport
        if isinstance(site_sport, str):
            self.site_sport = SiteSport.objects.get(name=site_sport)
        self.prize_structure = prize_structure
        slm = SkillLevelManager()
        skill_level = slm.get_for_amount(self.prize_structure.buyin)
        self.skill_level = skill_level
        self.start = start  # start of the contest
        self.end = end  # live games must start before this datetime

    def create(self):
        """
        Validate all the internal fields which will make this contest.
        Then create the underlying model and return it.
        """
        c = Contest.objects.create(name=self.name,
                                   site_sport=self.site_sport,
                                   prize_structure=self.prize_structure,
                                   start=self.start,
                                   end=self.end,
                                   skill_level=self.skill_level)
        logger.info('Contest created: %s' % c)
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
        # ticket_amount.amount
        ticket_prize_creator = TicketPrizeStructureCreator(ticket_value=5.00,
                                                           number_of_prizes=1,
                                                           name='contest-dummy-prize-structure')
        prize_structure = ticket_prize_creator.save()
        # prize_structure.name
        now = timezone.now()
        start = DfsDateTimeUtil.create(now.date(), time(23, 0))
        end = DfsDateTimeUtil.create(now.date() + timedelta(days=1), time(0, 0))
        creator = ContestCreator(name=Dummy.DEFAULT_NAME,
                                 sport=sport,
                                 prize_structure=prize_structure,
                                 start=start, end=end)
        contest = creator.create()
        logger.info('created new dummy contest with pk: %s' % contest.pk)
        return contest


class ContestLineupManager(object):
    """
    In [12]: hex( 65535 ) # max short int
    Out[12]: '0xffff'

    """

    # invalid player or no player
    PLAYER_INVALID = 0
    PLAYER_NOT_STARTED = 65535

    # size in bytes of these portions of the payload
    SIZE_LINEUPS = 4
    SIZE_PLAYERS_PER_LINEUP = 2

    SIZE_LINEUP_ID = 4
    SIZE_PLAYER = 2  # a single player is 2 bytes

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
            self.contest = Contest.objects.get(pk=contest_id)
        elif contest is not None:
            self.contest = contest
        else:
            raise Exception('contest must not be None')

        dgm = DraftGroupManager()
        self.draft_group_players = dgm.get_players(self.contest.draft_group)

        # a map where the player id points to their own id if their game
        # has started, or to 0xffff if they havent started yet
        #
        # i can see a reason we would want to cache the get_starter_map result ....
        self.starter_map = self.get_starter_map(self.draft_group_players)

        # determine the size of a lineup in bytes
        rm = RosterManager(self.contest.site_sport)
        self.players_per_lineup = rm.get_roster_spots_count()

        self.entries = Entry.objects.filter(contest=self.contest)

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
                self.starter_map[p.salary_player.player_id] = p.salary_player.player_id
            else:
                self.starter_map[p.salary_player.player_id] = self.PLAYER_NOT_STARTED
        return self.starter_map

    def is_player_game_started(self, player_id):
        """
        return a boolean indicating if this players game has started

        :param player_id:
        :return:
        """
        return self.starter_map[player_id] < self.PLAYER_NOT_STARTED

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
        return (
                   self.SIZE_LINEUP_ID + self.players_per_lineup * self.SIZE_PLAYER) * self.entries.count()

    def get_size_in_bytes(self):
        # print( '__header_size() = %s' %str(self.__header_size()), '__payload_size() = %s' % str(self.__payload_size()))
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

        size = struct.calcsize(fmt)
        # print('<size so far>', str(size), 'raw:', str(bytes))
        struct.pack_into(fmt, bytes, offset, val)
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

        bytes = bytearray(self.get_size_in_bytes())
        # print( '# contest entries:', str(self.contest.entries))
        offset, bytes = self.pack_into_h('>i', bytes, 0, self.contest.entries)
        # print( '# players per lineup:', str(self.players_per_lineup))
        offset, bytes = self.pack_into_h('>H', bytes, offset, self.players_per_lineup)

        for e in self.entries:
            # pack the lineup id
            # print( '    <add lineup> %s' % str(e.lineup.pk), '  : bytes[%s]' % str(len(bytes) ) )
            offset, bytes = self.pack_into_h('>i', bytes, offset, e.lineup.pk)

            # pack in each player in the lineup, in order of course
            lm = LineupManager(e.user)
            for pid in lm.get_player_ids(e.lineup):
                # print( '        pid:', str(pid ))
                # offset, bytes = self.pack_into_h( '>h', bytes, offset, pid )
                # print( 'pid:', str( pid ) )

                offset, bytes = self.pack_into_h('>H', bytes, offset, pid)

        # all the bytes should be packed in there now!
        return bytes

    def dev_get_all_lineups(self, contest_id):
        """
        for testing purposes, get all the lineups as json.
        """

        settings_module_name = os.environ['DJANGO_SETTINGS_MODULE']
        # 'mysite.settings.local'   should let this method work
        if 'local' not in settings_module_name:
            raise Exception(
                'json from dev_get_all_lineups not allowed unless local settings being used')

        lineups = []

        for e in self.entries:

            lineup_id = e.lineup.pk
            player_ids = []

            # pack in each player in the lineup, in order of course
            lm = LineupManager(e.user)
            for pid in lm.get_player_ids(e.lineup):
                # player_ids.append( self.starter_map[ pid ] ) # masks out no-yet-started players
                player_ids.append(pid)

            lineups.append({
                'lineup_id': lineup_id,
                'player_ids': player_ids,
            })

        data = {
            'endpoint': '/contest/all-lineups/%s?json' % int(contest_id),
            'bytes_for_condensed_response': self.get_size_in_bytes(),
            'total_lineups': self.contest.entries,
            'players_per_lineup': self.players_per_lineup,
            'lineups': lineups,
        }
        return data

    def get_http_payload(self):
        return ''.join('{:02x}'.format(x) for x in self.get_raw_bytes())


class FairMatch(object):
    class ZeroEntriesException(Exception):
        pass

    class NotEnoughEntriesException(Exception):
        pass

    # size / prize_structure will come from ContestPool instance
    def __init__(self, entries=[], contest_size=2, contest_pool_id=None):
        # instance of random number generator
        self.r = Random()

        # size of contests to generate (ie: 10-mans)
        self.contest_size = contest_size

        # make a copy of original list of all the entries
        self.original_entries = list(entries)

        # This is just a way for us to look up how a contest was formed in the logs based
        # on it's ID.
        self.contest_pool_id = contest_pool_id

        # for debugging - a list of all the contests made
        self.contests = None

    def get_contests(self):
        """
        :return: a list of lists-of-entries to fill contests
        """
        return self.contests['contests'] + self.contests['contests_forced']

    def get_contests_forced(self):
        """
        :return: a list of lists-of-unfilled-entries, ie the superlay contest entries
        """
        return self.contests['contests_forced']

    def fill_contest(self, entries, size, force=False):
        """
        :param force: if force is true, skip the size check, and add the entries to contest regardless
        :return:
        """
        if len(entries) == 0:
            err_msg = '\t0 entries passed to fill_contest()'
            raise self.ZeroEntriesException(err_msg)

        if not force and len(entries) < size:
            err_msg = '\t%s needed, entries list: %s' % (size, str(entries))
            raise self.NotEnoughEntriesException(err_msg)

        ss = ''
        if force:
            ss = '** = superlay is possible here.'
        logger.info('\tmaking contest: %s force: %s %s' % (entries, force, ss))
        # TODO fill c

        self.__add_contest_debug(entries, size, force=force)

    def __add_contest_debug(self, entries, size, force=False):
        if force:
            # entries we need to enter into a contest no matter what (first entries)
            self.contests['contests_forced'].append(entries)
        else:
            # this
            self.contests['contests'].append(entries)
        self.contests['contest_size'] = size

    @atomic
    def run(self):
        """
        create all required contests using the FairMatch algorithm
        with the given user entries.
        """
        logger.info('running FairMatch for %s entries | contest size: %s | contests: %s' % (
            len(self.original_entries), self.contest_size, self.contests))
        self.contests = {
            'entry_pool_size': len(list(self.original_entries)),
            'entry_pool': list(self.original_entries),
            'contests': [],
            'contests_forced': []
        }

        # run the algorithm, starting it all off by passing
        # a mutable copy of all the unique entries to run_h()
        all_entries = list(self.original_entries)
        self.run_h(all_entries, 1, [], verbose=True)

        # now remove the unused entries
        unused_entries = self.contests['entry_pool']

        for contest in self.contests['contests'] + self.contests['contests_forced']:
            for entry in contest:
                logger.info("\tremoving matched entry `%s` the from 'unused_entries' list", entry)
                unused_entries.remove(entry)
        self.contests['unused_entries'] = unused_entries

        # Now refund unused entries.

        logger.info("FairMatch Summary for ContestPool.id=%s: %s" % (
            self.contest_pool_id, self.contests))

    @staticmethod
    def get_and_remove_uniques(entries, exclude):
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

    @staticmethod
    def remove_from_list(target, removes):
        for e in removes:
            target.remove(e)
        return target

    # I don't know why this exists, but it isn't used so I left it for posterity's sake (zach)
    # def get_additional_uniques(self, entries, n, exclude):
    #     """
    #     get 'n' uniques out of 'entries', excluding those in 'exclude' list
    #
    #     removes the entries return from the original 'entries' list
    #
    #     :param entries:
    #     :param n:
    #     :param exclude:
    #     :return:
    #     """
    #
    #     additional_uniques = list(set(entries))
    #     logger.info(
    #         'get %sx entry from %s ignoring entries in %s' % (n, additional_uniques, exclude))
    #     # excludes the entries we already have
    #     for e in exclude:
    #         try:
    #             additional_uniques.remove(e)
    #         except ValueError:
    #             pass  # e didnt exist
    #     shuffle(additional_uniques)
    #     additional_uniques = additional_uniques[:n]
    #
    #     entries = self.remove_from_list(entries, additional_uniques)
    #
    #     return additional_uniques, entries

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
                logger.info('Done FairMatching contest pool into contests.')
            return  # we are done

        if verbose:
            logger.info(
                '++++ beginning of round %s - (pre-round) entry pool: %s ++++' % (round, entries))

        # get the unique entries for this round
        # returns (unique entries (one from each user), all other entries)
        round_uniques, remaining_entries = self.get_and_remove_uniques(entries, exclude)
        # take all non-user-unique entries and remove any of those we've explicitly excluded.
        remaining_uniques = list(set(remaining_entries) - set(exclude))
        if verbose:
            logger.info('\texcluded(for fairness): %s' % exclude)
            logger.info('\tround uniques: %s' % round_uniques)
            logger.info(
                '\tremaining entries: %s including any entries in exclude (debug)' % remaining_entries)
            logger.info(
                ('\tremaining uniques: %s not including excludes. potential additional entries '
                 'this round') % remaining_uniques)

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
                    logger.info('\tthese entries didn\'t get matched %s.' % round_uniques)
                    # print('        -> selected_additional_entries = '
                    #       'list(set(remaining_uniques) - set(round_uniques))[:n]')
                    logger.info(
                        "\trandomly chose: %s from %s (next round's entries) in order to match %s" %
                        (selected_additional_entries, additional_uniques, round_uniques))

                # now make the last contest of the round, or issue refunds
                first_round = round == 1
                try:
                    self.fill_contest(round_uniques + selected_additional_entries,
                                      self.contest_size, force=first_round)
                except self.NotEnoughEntriesException as e:
                    # failed on the last time around, but there may be enough
                    # excludes required to create the last contest on
                    # one more round so break and try again
                    logger.warning(
                        ("\tContest creation failed. There are not enough entries. Another "
                         "round will be attempted - %s" % e)
                    )
                    break

                exclude_users_for_fairness = selected_additional_entries
                # be sure to remove successfully filled entries from the total remaining entries
                entries = self.remove_from_list(entries, exclude_users_for_fairness)
                break

        if verbose:
            logger.info('\t(exclude %s in round %s)' % (exclude_users_for_fairness, str(round + 1)))

        # post while loop
        self.run_h(entries, round + 1, exclude_users_for_fairness, verbose=verbose)

    def print_debug_info(self):
        logger.info('\t*** post run() information ***')
        # print(self.contests)
        for k, v in self.contests.items():
            logger.info('\t%s: %s' % (k, v))
            logger.info('\t%s contests created' % len(
                self.contests['contests'] + self.contests['forced_contests']))
            # This removes unused entries, but has been commented out. I have no idea why it is. (zach)
            # unused_entries = self.contests['entry_pool']
            # for c in self.contests['contests']:
            #     for entry in c:
            #         unused_entries.remove(entry)
            logger.info('\tunused entries: %s' % self.contests['unused_entries'])


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
    uses FairMatch object to determine how to fill contests based on all the entries of the
    ContestPool
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

        self.new_contests = None

    @atomic
    def fair_match(self):
        logger.info('Starting FairMatch for %s' % self.contest_pool)
        """
        create all required contests using the FairMatch algorithm
        with the given user entries.
        """
        self.new_contests = []

        # how many entries the contest should consist of. - this is based on the prize structure.
        contest_size = self.contest_pool.prize_structure.get_entries()
        # All entries that have registered for this contest pool.
        entry_pool = [e.user.pk for e in self.entries]
        # log + send a message to slack.
        count_msg = '> 💁 %s unique users and %s total entries' % (
            len(entry_pool), len(self.entries))
        logger.info(count_msg)
        slack.send(count_msg)

        # Create a dict of user PKs, each key containing a list of that user's entries.
        self.user_entries = {}
        for e in self.entries:
            try:
                self.user_entries[e.user.pk].append(e)
            except KeyError:
                self.user_entries[e.user.pk] = [e]

        # run the FairMatch algorithm to get the
        # information on how to fill the contests
        fm = FairMatch(entry_pool, contest_size, self.contest_pool.id)
        fm.run()

        # debug - can be removed
        fm.print_debug_info()

        # use the (random) contests + contests_forced lists of lists of entries
        # to generate the contests, extracting and removing 1 entry for each
        # user id we find along the way
        contest_entry_lists = fm.get_contests()
        for contest_entries in contest_entry_lists:
            msg = '> 🐣 Creating contest for users %s' % contest_entries
            logger.info(msg)
            slack.send(msg)
            c = self.create_contest_from_entry_list(contest_entries)
            self.new_contests.append(c)

        #
        # create any of the superlay contests if there are unfilled first-entries
        superlay_contest_entry_lists = fm.get_contests_forced()
        for contest_entries in superlay_contest_entry_lists:
            msg = '> 🐣 Creating contest for users (unfilled first-entries) %s' % contest_entries
            logger.info(msg)
            slack.send(msg)
            c = self.create_contest_from_entry_list(contest_entries)
            self.new_contests.append(c)

        # change the status of the contest pool to created now
        self.contest_pool.status = ContestPool.CREATED
        self.contest_pool.save()
        # self.contest_pool.refresh_from_db()
        return self.new_contests

    def create_contest_from_entry_list(self, entry_list):
        # 1. create a contest for the entries
        cpm = ContestPoolManager(self.contest_pool)
        contest = cpm.new_contest()
        contest.draft_group = self.contest_pool.draft_group
        contest.save()

        # 2. enter them into the contest
        for user_id in entry_list:
            entry = self.user_entries[user_id].pop()

            # find the contest pool entry for this user
            entry.contest = contest
            entry.save()

            # find the buyin and set the contest to that and save it
            buyin = Buyin.objects.get(entry=entry)
            buyin.contest = contest
            buyin.save()

        # set the number of entries for completeness
        contest.current_entries = len(entry_list)
        contest.save()

        # #
        # # pusher contest updates because entries were changed
        # ContestPoolPush(ContestPoolSerializer(contest_pool).data).send()

        # return the newly created (and filled) contest
        return contest


class ContestPlayerOwnership(object):
    """
    gathers the data about player ownership for the given contest
    """

    def __init__(self, contest):
        if not isinstance(contest, Contest):
            err_msg = 'contest param [%s] must be a contest.models.Contest' % type(contest)
            raise Exception(err_msg)
        self.contest = contest

        self.entries = None
        self.lineups = None
        self.lineup_players = None

        # store the results in a collections.Counter instance.
        # it will be initialized in update() method.
        self.player_counter = None

    def get_lineups(self):
        """
        return the list of Lineup objects
        """
        return self.lineups

    def update(self):
        """
        gather the lineup and player data and populate the internal data
        with sums of occurences of players, and the # of lineups
        """
        self.entries = Entry.objects.filter(contest=self.contest)
        self.lineups = [e.lineup for e in self.entries]
        self.lineup_players = lineup.models.Player.objects.filter(lineup__in=self.lineups)

        # add players to the data with an initial count of 1.
        # increment a players count if they already exist
        self.player_counter = Counter([p.player.srid for p in self.lineup_players]).items()

    def get_player_counter(self):
        """
        return an iterable of tuples where each tuple is of the form:
            (sports.models.Player.pk, number_of_lineup_occurrences)
        """
        if self.player_counter is None:
            self.update()

        return self.player_counter

    def count_for_srid(self, srid):
        """
        for the given player srid, return the count of their occurrences
        in lineups for this contest.
        """
        if self.player_counter is None:
            self.update()

        return self.player_counter.get(srid)


class RecentPlayerOwnership(object):
    """
    Gather player ownership data for the most recent days those players played.

    Only lineup.models.Lineup's which have been associated with ClosedContest(s),
    will be considered to ensure validity of the results.

    Lineups may span multiple DraftGroups so long as the DraftGroups
    are from the same "DFS Day"; that means early/regular/late block
    draft groups for a single day may be used.
    """

    class DfsDayOwnership(object):

        def __init__(self, lineups, ownerships):
            self.lineups = lineups
            self.ownerships = ownerships

        def get_lineup_count(self):
            return self.lineups

        def get_ownerships(self):
            return self.ownerships

        def __str__(self):
            return '%s Lineups | ("player_srid":"occurrences") %s' % (
                str(self.lineups), str(self.ownerships))

    # maximum number of days we will search for players,
    # looking back thru historical days of lineups.
    recent_days = 50

    def __init__(self, site_sport):
        # set the SiteSport instance. if its a string, try to get the SiteSport model
        self.site_sport = site_sport
        if isinstance(self.site_sport, str):
            self.site_sport = SiteSport.objects.get(name=site_sport)
        # validate the self.site_sport we ended up with...
        if not isinstance(self.site_sport, SiteSport):
            err_msg = 'site_sport must be an instance of ' \
                      'sports.models.SiteSport (or the string name of the sport)'
            raise Exception(err_msg)

        # these will be set in update() method
        self.contests = None
        self.draft_groups = None
        self.dfs_day_ownerships = None

    def get_players(self):
        """
        :return: a dictionary whose key-value-pairs are all in the form:
            {
                'player_srid': percent_owned_float,
                'player_srid': percent_owned_float,
                    ...
            }
        """
        if self.dfs_day_ownerships is None:
            self.dfs_day_ownerships = self.update()

        # use this data to generate some data that is easier to use
        data = {}
        for day in self.dfs_day_ownerships:
            # day will be a collections.Counter() class (ie: a dict, basically)
            lineup_count = day.get_lineup_count()
            for player_srid, occurrences in day.get_ownerships().items():
                data[player_srid] = occurrences / lineup_count
        return data

    def update(self):
        """
        :return: a list of DfsDayOwnership objects for the past 'recent_days'
        """

        # get all ClosedContest objects within the last 'recent_days'.
        # we get the ClosedContest's DraftGroups so we avoid DraftGroups
        # which werent used for contests!
        dt = timezone.now() - timedelta(days=self.recent_days)
        closed_contests = ClosedContest.objects.filter(site_sport=self.site_sport,
                                                       start__gte=dt).order_by('-start')
        # get the distinct DraftGroup(s) for those contests
        self.draft_groups = self.get_distinct_ordered_draft_groups(closed_contests)

        # group the draft groups by dfs date
        draft_groups_by_day = []
        i = 0
        while i < self.recent_days:
            # get the current datetime range for the dfs day. offset_hours should be negative
            start, end = DfsDate.get_current_dfs_date_range(offset_hours=24 * i * -1)
            # get the 'group', ie: the DraftGroups (a subset of our self.draft_groups) for the day.
            group = draftgroup.models.DraftGroup.objects.filter(start__range=(start, end),
                                                                pk__in=[dg.pk for dg in
                                                                        self.draft_groups])
            # print('%s draft groups added' % len(group))
            draft_groups_by_day.append(group)
            i += 1

        # for each days draft groups, collect contest lineup/player data,
        # and keep track of players we've update along the way.
        # do not add older dfs day's ownership data for any players.
        dfs_day_ownership_list = []
        player_ownerships = {}
        for group in draft_groups_by_day:
            # we need to keep track of all player ownerships for the day
            day_ownerships = {}
            num_lineups_in_group = 0
            for contest in closed_contests.filter(draft_group__in=group):
                # get the player ownerships for a contest
                cpo = ContestPlayerOwnership(contest)
                day_ownerships = DictTools.combine(day_ownerships, dict(cpo.get_player_counter()))
                num_lineups_in_group += len(cpo.get_lineups())

            # now we can simply use dict.update() on day_ownerships (reverse from
            # what you might expect!) to merge the overall 'player_ownerships'
            # and the 'day_ownerships' without replacing existing keys in 'player_ownerships'
            new_day_ownerships = DictTools.subtract(day_ownerships.copy(), player_ownerships)
            # print('new_day_ownerships', str(new_day_ownerships))
            dfs_day_ownership_list.append(
                self.DfsDayOwnership(num_lineups_in_group, new_day_ownerships))
            day_ownerships.update(player_ownerships)
            # replace player_ownerships with the updated copy of all ownerships we've seen thus far
            player_ownerships = day_ownerships.copy()

        # player_ownerships should contain the ownership results
        # for players on the first day they were found only
        self.dfs_day_ownerships = dfs_day_ownership_list
        return self.dfs_day_ownerships

    def get_distinct_ordered_draft_groups(self, contests):
        """
        extract, and return -- maintaining order -- the distinct draft groups from the 'contests'

        :param contests:
        :return:
        """
        draft_group_map = OrderedDict()
        for contest in contests:
            dg = contest.draft_group
            if dg.pk not in draft_group_map:
                draft_group_map[dg.pk] = dg
        return list(draft_group_map.values())
