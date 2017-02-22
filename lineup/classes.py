import random
from collections import Counter
from logging import getLogger

from django.contrib.contenttypes.models import ContentType
from django.db.transaction import atomic
from django.utils import timezone

from contest.models import Contest, Entry
from draftgroup.models import DraftGroup, Player
from mysite.classes import AbstractSiteUserClass
from roster.classes import RosterManager
from sports.classes import SiteSportManager
from .exceptions import (
    LineupInvalidRosterSpotException,
    InvalidLineupSizeException,
    PlayerDoesNotExistInDraftGroupException,
    InvalidLineupSalaryException,
    DuplicatePlayerException,
    PlayerSwapGameStartedException,
    LineupUnchangedException,
    CreateLineupExpiredDraftgroupException,
    NotEnoughTeamsException,
)
from .models import (
    Lineup,
    Player as LineupPlayer,
)

logger = getLogger('lineup.classes')


class LineupManager(AbstractSiteUserClass):
    """
    Responsible for performing all lineup actions for all active contests for both
    cash and ticket games.
    """

    def __init__(self, user):
        super().__init__(user)

        self.draft_group_players = None

    def validate_arguments(self, player_ids, draftgroup=None, lineup=None, entry=None):
        if player_ids is not None:
            self.validate_variable_array(int, player_ids)
        if draftgroup is not None:
            self.validate_variable(DraftGroup, draftgroup)
        if lineup is not None:
            self.validate_variable(Lineup, lineup)
        if entry is not None:
            self.validate_variable(Entry, entry)

    def get_player_ids(self, lineup):
        """
        get an array of player ids for the given lineup, ordered by the roster

        :param lineup:
        :return:
        """
        return [p.player_id for p in self.get_players(lineup)]

    def get_player_srids(self, lineup):
        """
        get an array of sports.models.Player "srid"s
        for the given lineup, ordered by the roster

        :param lineup:
        :return:
        """
        return [p.player.srid for p in self.get_players(lineup)]

    @staticmethod
    def get_players(lineup):
        """
        return the LineupPlayer models for this Lineup

        :param lineup:
        :return:
        """
        return LineupPlayer.objects.filter(lineup=lineup).order_by('idx')

    def update_fantasy_points(self, lineup):
        """
        sum up the lineup players' draft_group_player.finalized_fantasy_points

        :return:
        """
        total_fantasy_points = 0.0
        for player in self.get_players(lineup):
            # player is a lineup.models.Player object
            total_fantasy_points += player.draft_group_player.final_fantasy_points
        #
        # and save the lineup
        lineup.fantasy_points = total_fantasy_points
        lineup.save()

    @atomic
    def create_lineup(self, player_ids, draftgroup, name=''):
        """
        Creates a Lineup based off the draftgroup and player_ids

        :param player_ids:
        :param draftgroup:

        :raise :class:`lineup.exception.LineupInvalidRosterSpotException`: When a player
            does not match the corresponding roster spot.
        :raise :class:`lineup.exception.PlayerDoesNotExistInDraftGroupException`: When a
            player does not exist in the draftgroup.
        :raise :class:`lineup.exception.InvalidLineupSalaryException`: When a lineup
            has a salary larger than the maximum allowed for the salary pool
        :raise :class:`lineup.exception.DuplicatePlayerException`: If there are
            duplicate ids in the player_ids list
        :raise :class:`lineup.exception.DuplicatePlayerException`: If there are
            duplicate ids in the player_ids list

        :returns lineup: an instance of :class:`lineup.models.Lineup` model
        """
        self.validate_arguments(player_ids=player_ids, draftgroup=draftgroup)

        #
        # Throw an exception if the draftgroup is expired
        if draftgroup.start < timezone.now():
            raise CreateLineupExpiredDraftgroupException()

        return self.__create_lineup(player_ids, draftgroup, name)

    @staticmethod
    def get_for_contest_by_ids(contest_id, lineup_ids):
        """

        :param contest_id:
        :param lineup_ids:
        :return: list of lineup.models.Lineup objects where the lineup id in the contest is found
        """
        contests = Contest.objects.filter(pk__in=[contest_id])
        distinct_lineup_entries = Entry.objects.filter(contest__in=contests,
                                                       lineup__pk__in=lineup_ids)
        lineups = [entry.lineup for entry in distinct_lineup_entries]
        return lineups

    @staticmethod
    def get_for_contest(contest_id):
        """

        :param contest_id:
        :return: list of lineup.models.Lineup objects in the contest
        """
        contests = Contest.objects.filter(pk__in=[contest_id])
        distinct_lineup_entries = Entry.objects.filter(contest__in=contests).select_related(
            'lineup')
        lineups = [entry.lineup for entry in distinct_lineup_entries]
        return lineups

    @staticmethod
    def get_for_contest_by_search_str(contest_id, search_str):
        """

        :param contest_id:
        :param search_str:
        :return: list of lineup.models.Lineup objects where the owner's username contains 'search_str'
        """
        contests = Contest.objects.filter(pk__in=[contest_id])
        distinct_lineup_entries = Entry.objects.filter(contest__in=contests,
                                                       lineup__user__username__icontains=search_str)
        lineups = [entry.lineup for entry in distinct_lineup_entries]
        return lineups

    def get_players_with_nicknames(self, players, draftgroup):
        players_with_nicknames = list(filter(lambda p: p.lineup_nickname, players))
        user_lineup_nicknames = Lineup.objects.filter(user=self.user, draft_group=draftgroup).values_list(
            'name', flat=True)
        if user_lineup_nicknames:
            # removes players which nickname was already used
            cleaned_players = [player for player in players_with_nicknames if player.lineup_nickname not in user_lineup_nicknames]
            if cleaned_players:
                players_with_nicknames = cleaned_players
        return players_with_nicknames, user_lineup_nicknames

    def set_lineup_nickname(self, lineup, players, draftgroup):
        players_with_nicknames, user_lineup_nicknames = self.get_players_with_nicknames(players, draftgroup)
        lineup_name = ''
        if players_with_nicknames:
            random_player_nickname = random.choice(players_with_nicknames).lineup_nickname
            i = 1
            lineup_name = random_player_nickname
            while user_lineup_nicknames.filter(name__iexact=lineup_name):
                i += 1
                lineup_name = '{} #{}'.format(random_player_nickname, i)
        return lineup_name

    def __create_lineup(self, player_ids, draftgroup, name=''):
        """
        Create Lineup helper

        :param player_ids:
        :param draftgroup:

        :raise :class:`lineup.exception.LineupInvalidRosterSpotException`: When a player
            does not match the corresponding roster spot.
        :raise :class:`lineup.exception.PlayerDoesNotExistInDraftGroupException`: When a
            player does not exist in the draftgroup.
        :raise :class:`lineup.exception.InvalidLineupSalaryException`: When a lineup
            has a salary larger than the maximum allowed for the salary pool
        :raise :class:`lineup.exception.DuplicatePlayerException`: If there are
            duplicate ids in the player_ids list

        :returns lineup: an instance of :class:`lineup.models.Lineup` model
        """
        #
        # get the players and put them into an ordered array
        players = self.get_player_array_from_player_ids_array(player_ids,
                                                              draftgroup.salary_pool.site_sport)

        #
        # validates the lineup based on the players and draftgroup
        roster_manager = RosterManager(draftgroup.salary_pool.site_sport)

        self.__validate_lineup(players, draftgroup, roster_manager)

        #
        # creates a lineup based on the player ids
        lineup = Lineup()
        lineup.user = self.user
        lineup.draft_group = draftgroup
        lineup.name = name
        lineup.save()

        i = 0

        for player in players:
            lineup_player = LineupPlayer()
            lineup_player.player = player
            lineup_player.lineup = lineup
            lineup_player.draft_group_player = self.draft_group_players[player.pk]
            lineup_player.roster_spot = roster_manager.get_roster_spot_for_index(i)
            lineup_player.idx = i
            lineup_player.save()
            i += 1

        if lineup.name == '':
            lineup.name = self.set_lineup_nickname(lineup, players, draftgroup)
            lineup.save()

        self.__merge_lineups(lineup)
        logger.info('action: lineup created | lineup: %s' % lineup)
        return lineup

    @atomic
    def edit_entry(self, player_ids, entry):
        """
        Edits the entry
        :param player_ids:
        :param entry:
        :return:

        :raise :class:`lineup.exception.LineupInvalidRosterSpotException`: When a player
            does not match the corresponding roster spot.
        :raise :class:`lineup.exception.PlayerDoesNotExistInDraftGroupException`: When a
            player does not exist in the draftgroup.
        :raise :class:`lineup.exception.InvalidLineupSalaryException`: When a lineup
            has a salary larger than the maximum allowed for the salary pool
        :raise :class:`lineup.exception.DuplicatePlayerException`: If there are
            duplicate ids in the player_ids list
        :raise :class:`lineup.exception.PlayerSwapGameStartedException`: If trying
            to swap players that are already in games.
        :raise :class:`lineup.exception.InvalidLineupSalaryException`: When a lineup
            is unchanged
        """
        self.validate_arguments(player_ids=player_ids, entry=entry)
        #
        # Throw an exception if the draftgroup is expired
        if entry.lineup.draft_group.start < timezone.now():
            logger.warning('cannot edit entry, draftgroup exired | entry: %s' % entry)
            raise CreateLineupExpiredDraftgroupException()

        self.__validate_lineup_changed(player_ids, entry)
        #
        # Gets the count of entries using the same lineup
        count = Entry.objects.filter(lineup=entry.lineup).count()
        if count == 1:
            self.__edit_lineup(player_ids, entry.lineup)
            logger.info('action: entry edited | entry: %s' % entry)
        else:
            entry.lineup = self.__create_lineup(player_ids, entry.lineup.draft_group)
            entry.save()
            logger.info('action: entry created | entry: %s' % entry)

    @atomic
    def edit_lineup(self, player_ids, lineup):
        """
        This should only be called via a task

        Mass Edits a lineup

        :param player_ids: an ordered list of :class:`sports.models.Player` ids
            for the lineup.
        :param lineup:

        :raise :class:`lineup.exception.LineupInvalidRosterSpotException`: When a player
            does not match the corresponding roster spot.
        :raise :class:`lineup.exception.PlayerDoesNotExistInDraftGroupException`: When a
            player does not exist in the draftgroup.
        :raise :class:`lineup.exception.InvalidLineupSalaryException`: When a lineup
            has a salary larger than the maximum allowed for the salary pool
        :raise :class:`lineup.exception.DuplicatePlayerException`: If there are
            duplicate ids in the player_ids list
        :raise :class:`lineup.exception.PlayerSwapGameStartedException`: If trying
            to swap players that are already in games.

        """
        self.validate_arguments(player_ids=player_ids, lineup=lineup)
        #
        # Throw an exception if the draftgroup is expired
        if lineup.draft_group.start < timezone.now():
            logger.warning('cannot edit lineup, draftgroup exired | lineup: %s' % lineup)
            raise CreateLineupExpiredDraftgroupException()

        self.__edit_lineup(player_ids, lineup)

    def __edit_lineup(self, player_ids, lineup):
        """
        This should only be called via a task

        Mass Edits a lineup helper

        :param player_ids: an ordered list of :class:`sports.models.Player` ids
            for the lineup.
        :param lineup:

        :raise :class:`lineup.exception.LineupInvalidRosterSpotException`: When a player
            does not match the corresponding roster spot.
        :raise :class:`lineup.exception.PlayerDoesNotExistInDraftGroupException`: When a
            player does not exist in the draftgroup.
        :raise :class:`lineup.exception.InvalidLineupSalaryException`: When a lineup
            has a salary larger than the maximum allowed for the salary pool
        :raise :class:`lineup.exception.DuplicatePlayerException`: If there are
            duplicate ids in the player_ids list

        """

        #
        # get the players and put them into an ordered array
        site_sport = lineup.draft_group.salary_pool.site_sport
        players = self.get_player_array_from_player_ids_array(player_ids, site_sport)

        #
        # validates the lineup based on the players and draftgroup
        roster_manager = RosterManager(site_sport)
        self.__validate_lineup(players, lineup.draft_group, roster_manager)

        #
        # adds the player ids to the corresponding spots in the lineup
        lineup_players = LineupPlayer.objects.filter(lineup=lineup).order_by('idx')
        i = 0
        removed_players = []
        for lineup_player in lineup_players:
            player = players[i]
            #
            # replace the player if they are not equal
            if lineup_player.player != player:
                removed_players.append(lineup_player.player)
                lineup_player.player = player
            i += 1
            lineup_player.save()
        for player in removed_players:
            if (player.lineup_nickname != '' and player.lineup_nickname in lineup.name) or lineup.name == '':
                lineup.name = self.set_lineup_nickname(lineup, players, lineup.draft_group)
                lineup.save()

        logger.info('action: lineup edited | lineup: %s' % lineup)
        self.__merge_lineups(lineup)

    def __validate_lineup(self, players, draftgroup, roster_manager):
        """
        Validation that the lineup can be submitted to the contest
        :param players: an ordered list of :class:`sports.models.Player` objects
            for the lineup.
        :param draftgroup: a :class:`draftgroup.models.DraftGroup` object

        :raise :class:`lineup.exception.LineupInvalidRosterSpotException`: When a player
            does not match the corresponding roster spot.
        :raise :class:`lineup.exception.PlayerDoesNotExistInDraftGroupException`: When a
            player does not exist in the draftgroup.
        :raise :class:`lineup.exception.InvalidLineupSalaryException`: When a lineup
            has a salary larger than the maximum allowed for the salary pool
        :raise :class:`lineup.exception.DuplicatePlayerException`: If there are
            duplicate ids in the player_ids list
        """
        #
        # validate the size of the lineup
        if roster_manager.get_roster_spots_count() != len(players):
            print("player size: " + str(len(players)))
            raise InvalidLineupSizeException()
        #
        # ensure that players from at least 3 different team exist
        counter = Counter()
        for player in players:
            counter[player.team.pk] += 1
        if len(counter.items()) < 3:
            raise NotEnoughTeamsException()

        #
        # Logical Validation of the Lineups
        self.__validate_player_positions(players, roster_manager)

        self.__validate_player_salaries(players, draftgroup)

    @staticmethod
    def __validate_player_positions(players, roster_manager):
        """
        Makes sure the players match the corresponding roster spots
        for the sport and that the roster size is correct.

        :param players: an ordered list of :class:`sports.models.Player` objects
            for the lineup.
        :param roster_manager: a :class:`roster.classes.RosterManager` object

        :raise :class:`lineup.exception.LineupInvalidRosterSpotException`: When a player
            does not match the corresponding roster spot.

        """

        #
        # iterate through the players and make sure they all match
        # their corresponding RosterSpots
        i = 0
        for player in players:
            if not roster_manager.player_matches_spot(player, i):
                raise LineupInvalidRosterSpotException()
            i += 1

    def __validate_player_salaries(self, players, draftgroup):
        """
        Makes sure the players salaries do not exceed

        :raise :class:`lineup.exception.PlayerDoesNotExistInDraftGroupException`: When a
            player does not exist in the draftgroup.
        :raise :class:`lineup.exception.InvalidLineupSalaryException`: When a lineup
            has a salary larger than the maximum allowed for the salary pool
        """

        self.draft_group_players = {}

        salary_sum = 0
        #
        # sum all salaries
        for player in players:
            try:
                c_type = ContentType.objects.get_for_model(player)
                draftgroup_player = Player.objects.get(salary_player__player_type=c_type,
                                                       salary_player__player_id=player.pk,
                                                       draft_group=draftgroup)
                #
                self.draft_group_players[
                    draftgroup_player.salary_player.player_id] = draftgroup_player

                salary_sum += draftgroup_player.salary
            except Player.DoesNotExist:
                raise PlayerDoesNotExistInDraftGroupException(player.pk, draftgroup.pk)

        #
        # get the salary_pools largest team salary
        max_team_salary = draftgroup.salary_pool.salary_config.max_team_salary

        #
        # Throw an exception if the salary is larger than the maximum size for
        # a team in a contest.
        if salary_sum > max_team_salary:
            raise InvalidLineupSalaryException(self.user.username, salary_sum, max_team_salary)

    @staticmethod
    def __validate_lineup_changed(player_ids, entry):
        """
        Makes sure the lineup is modified

        :param player_ids: an ordered list of :class:`sports.models.Player` ids
            for the lineup.
        :param entry: a :class:`contest.models.Entry` object

        :raise :class:`lineup.exception.InvalidLineupSalaryException`: When a lineup
            is unchanged
        """
        lineup_players = LineupPlayer.objects.filter(lineup=entry.lineup).order_by('idx')
        i = 0
        same_lineup = True
        for lineup_player in lineup_players:
            if lineup_player.player_id != player_ids[i]:
                same_lineup = False
            i += 1

        if same_lineup:
            raise LineupUnchangedException()

    @staticmethod
    def get_player_array_from_player_ids_array(player_ids, site_sport):
        """
        Creates and returns an array of :class:`sports.models.Player` objects based
        on the player_ids array.

        :param player_ids: an ordered list of :class:`sports.models.Player` ids
            for the lineup.
        :return: an array of :class:`sports.models.Player` objects

        :raise :class:`lineup.exception.DuplicatePlayerException`: If there are
            duplicate ids in the player_ids list
        """
        ssm = SiteSportManager()
        player_class = ssm.get_player_class(site_sport)

        #
        # Check if there are duplicate players
        if len(set(player_ids)) != len(player_ids):
            raise DuplicatePlayerException()

        players = player_class.objects.filter(pk__in=player_ids)
        return sorted(players, key=lambda player: player_ids.index(player.pk))

    def __merge_lineups(self, lineup):
        """
        Merges lineups that have the same lineup players to consolidate to one lineup.
        Delete the duplicate  :class:`lineup.models.Lineup` and  :class:`lineup.models.Player`
        objects.

        :param lineup: a :class:`lineup.models.Lineup` object

        """
        #
        # get the lineups for the draftgroup that are not the lineup passed to
        # the method
        lineups = Lineup.objects.filter(draft_group=lineup.draft_group,
                                        user=self.user).exclude(pk=lineup.pk)
        lineup_players_arr = []
        for l in lineups:
            lineup_players_arr.append(LineupPlayer.objects.filter(lineup=l).order_by('idx'))

        #
        # get the current lineup
        current_lineup_players = LineupPlayer.objects.filter(lineup=lineup).order_by('idx')

        #
        # remove non-matching lineups from the lineup players_arr
        i = 0
        for current_player in current_lineup_players:
            copy_lineup_players_arr = list(lineup_players_arr)
            for lineup_player_arr in copy_lineup_players_arr:
                if current_player.player_id != lineup_player_arr[i].player_id:
                    lineup_players_arr.remove(lineup_player_arr)
            i += 1
        #
        # exit if we have nothing to merge
        if len(lineup_players_arr) == 0:
            return

        logger.info('Identical lineup exist for user - merging | lineup: %s' % lineup)
        #
        # get the list of lineups to delete
        lineups_to_delete = []
        for lineup_player_arr in lineup_players_arr:
            lineups_to_delete.append(lineup_player_arr[0].lineup)

        #
        # get the Entries for the lineups and point them to the new lineup
        Entry.objects.filter(lineup__in=lineups_to_delete).update(lineup=lineup)

        #
        # Delete the lineups and players that have not entries
        LineupPlayer.objects.filter(lineup__in=lineups_to_delete).delete()
        for lineups_to_delete in lineups_to_delete:
            lineups_to_delete.delete()

    def __validate_changed_players_have_not_started(self, player_ids, lineup):
        """
        Makes sure none of the players being swapped have started playing in
        a game.

        :param player_ids:
        :param lineup:
        :return:
        """

        self.draft_group_players = {}

        #
        # adds the player ids to the corresponding spots in the lineup
        lineup_players = LineupPlayer.objects.filter(lineup=lineup).order_by('idx')
        i = 0
        now = timezone.now()
        for lineup_player in lineup_players:
            player_id = player_ids[i]

            if lineup_player.player_id != player_id:

                #
                # Get the draftgroup player for both players to get their start time
                c_type = lineup_player.player_type
                draftgroup_player = Player.objects.get(salary_player__player_type=c_type,
                                                       salary_player__player_id=player_id,
                                                       draft_group=lineup.draft_group)
                # add each draftgroup_player to the table, by their actual player_id (unique to sport!)
                self.draft_group_players[
                    draftgroup_player.salary_player.player_id] = draftgroup_player

                draftgroup_lineup_player = Player.objects.get(
                    salary_player__player_type=lineup_player.player_type,
                    salary_player__player_id=lineup_player.player_id,
                    draft_group=lineup.draft_group)
                #
                # check the player start_time for both players
                # TODO needs update the start time of draftgroup players based on TRADES!!
                if draftgroup_lineup_player.start < now or draftgroup_player.start < now:
                    raise PlayerSwapGameStartedException()
            i += 1

    @staticmethod
    def get_lineup_from_id(lineup_id, contest):
        """
        get lineup data we can show to other users, with masked
        out players if the contest has not started yet.

        :param lineup_id:
        :return:
        """

        data = []
        ssm = SiteSportManager()

        #
        # Get the lineup players for a lineup id
        lineup_players = LineupPlayer.objects.filter(lineup__pk=lineup_id).order_by('idx')
        #
        # sets the started flag to False if draftgroup has not started
        started = True
        if len(lineup_players) > 0 and not lineup_players[0].lineup.draft_group.is_started():
            started = False

        #
        # get the player model(s) for the sport used (multiple for MLB)
        player_stats_models = ssm.get_player_stats_class(contest.site_sport)

        #
        # add all the players to the data array, but if the contest has not started make the
        # specific player information be an empty array.
        for lineup_player in lineup_players:

            #
            # check every stats model type ( ie: baseball has PlayerStatsHitter & PlayerStatsPitcher)
            category_stats = []
            for player_stats_model in player_stats_models:

                player_stats = None
                #
                # if the player is masked out in the starter map, do not display which player it is
                if not started:
                    continue

                #
                # Get the player stats if the model type applies to the player and they have stats
                try:
                    player_stats = player_stats_model.objects.get(player_id=lineup_player.player_id,
                                                                  srid_game=lineup_player.draft_group_player.game_team.game_srid)
                except player_stats_model.DoesNotExist:
                    player_stats = None
                    pass

                #
                # add the stats to the data field for the given player.
                if player_stats is not None:
                    category_stats.append(player_stats.to_json())

            #
            # add the "category_stats" list  -- ie: the stats for each roster idx
            data.append({
                'started': started,
                'i': lineup_player.idx,
                'data': category_stats,
            })

        # this data is safe to return via the API because
        # the players whos games have not yet started have
        # not been shown!
        return data
