from mysite.classes import AbstractSiteUserClass
from django.db.transaction import atomic
from draftgroup.models import DraftGroup, Player
from .models import Lineup, Player as LineupPlayer
from sports.classes import SiteSportManager
from roster.classes import RosterManager
from.exceptions import LineupInvalidRosterSpotException, InvalidLineupSizeException, PlayerDoesNotExistInDraftGroupException, InvalidLineupSalaryException, DuplicatePlayerException, PlayerSwapGameStartedException, LineupUnchangedException, CreateLineupExpiredDraftgroupException
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from contest.models import Entry

class LineupManager(AbstractSiteUserClass):
    """
    Responsible for performing all lineup actions for all active contests for both
    cash and ticket games.
    """

    def __init__(self, user):
        super().__init__(user)

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
        return [ p.pk for p in LineupPlayer.objects.filter( lineup=lineup ).order_by('idx') ]

    @atomic
    def create_lineup(self,  player_ids, draftgroup):
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

        return self.__create_lineup(player_ids, draftgroup)

    def __create_lineup(self,  player_ids, draftgroup):
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
        players = self.get_player_array_from_player_ids_array(player_ids, draftgroup.salary_pool.site_sport)

        #
        # validates the lineup based on the players and draftgroup
        roster_manager = RosterManager(draftgroup.salary_pool.site_sport)

        self.__validate_lineup(players, draftgroup, roster_manager)

        #
        # creates a lineup based on the player ids
        lineup = Lineup()
        lineup.user = self.user
        lineup.draft_group = draftgroup
        lineup.save()

        i = 0
        for player in players:
            lineup_player = LineupPlayer()
            lineup_player.player = player
            lineup_player.lineup = lineup
            lineup_player.roster_spot = roster_manager.get_roster_spot_for_index(i)
            lineup_player.idx = i
            lineup_player.save()
            i += 1

        self.__merge_lineups(lineup)
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

        self.__validate_lineup_changed(player_ids, entry)

        self.__validate_changed_players_have_not_started(player_ids, entry.lineup)
        #
        # Gets the count of entries using the same lineup
        count = Entry.objects.filter(lineup=entry.lineup).count()
        if count == 1:
            self.__edit_lineup(player_ids, entry.lineup)
        else:
            entry.lineup = self.__create_lineup(player_ids, entry.lineup.draft_group)
            entry.save()



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
        self.__validate_changed_players_have_not_started(player_ids, lineup)
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
        for lineup_player in lineup_players:
            player = players[i]
            #
            # replace the player if they are not equal
            if lineup_player.player != player:
                lineup_player.player = player
            i+=1
            lineup_player.save()

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
            print("player size: "+str(len(players)))
            raise InvalidLineupSizeException()

        #
        # Logical Validation of the Lineups
        self.__validate_player_positions(players, roster_manager)

        self.__validate_player_salaries(players, draftgroup)



    def __validate_player_positions(self, players, roster_manager):
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
            i+=1

    def __validate_player_salaries(self, players, draftgroup):
        """
        Makes sure the players salaries do not exceed

        :raise :class:`lineup.exception.PlayerDoesNotExistInDraftGroupException`: When a
            player does not exist in the draftgroup.
        :raise :class:`lineup.exception.InvalidLineupSalaryException`: When a lineup
            has a salary larger than the maximum allowed for the salary pool
        """
        salary_sum = 0
        #
        # sum all salaries
        for player in players:
            try:
                c_type = ContentType.objects.get_for_model(player)
                draftgroup_player = Player.objects.get(salary_player__player_type=c_type,
                                                       salary_player__player_id=player.pk,
                                                       draft_group=draftgroup)
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

    def __validate_lineup_changed(self, player_ids, entry):
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

    def get_player_array_from_player_ids_array(self, player_ids, site_sport):
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
        players = []

        #
        # Check if there are duplicate players
        if len(set(player_ids)) != len(player_ids):
            raise DuplicatePlayerException()

        #
        # create a list of players
        for player_id in player_ids:
            players.append(player_class.objects.get(pk=player_id))

        return players

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