from mysite.classes import AbstractSiteUserClass
from django.db.transaction import atomic
from draftgroup.models import DraftGroup, Player
from .models import Lineup, Player as LineupPlayer
from sports.classes import SiteSportManager
from roster.classes import RosterManager
from.exceptions import LineupInvalidRosterSpotException, InvalidLineupSizeException, PlayerDoesNotExistInDraftGroupException, InvalidLineupSalaryException, DuplicatePlayerException
from django.contrib.contenttypes.models import ContentType

class LineupManager(AbstractSiteUserClass):
    """
    Responsible for performing all lineup actions for all active contests for both
    cash and ticket games.
    """

    def __init__(self, user):
        super().__init__(user)

    def validate_arguments(self, player_ids, draftgroup=None, lineup=None):
        if player_ids is not None:
            self.validate_variable_array(int, player_ids)
        if draftgroup is not None:
            self.validate_variable(DraftGroup, draftgroup)
        if lineup is not None:
            self.validate_variable(Lineup, lineup)

    @atomic
    def create_lineup(self,  player_ids, draftgroup):
        """

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
        self.validate_arguments(player_ids=player_ids, draftgroup=draftgroup)
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
        lineup.draftgroup = draftgroup
        lineup.save()

        i  = 0
        for player in players:
            lineup_player = LineupPlayer()
            lineup_player.player = player
            lineup_player.lineup = lineup
            lineup_player.roster_spot = roster_manager.get_roster_spot_for_index(i)
            lineup_player.idx = i
            lineup_player.save()
            i +=1

        return lineup


    @atomic
    def edit_lineup(self, player_ids, lineup):
        # TODO this should be a task so users cannot have collisions on edit lineup
        """

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
        self.validate_arguments(player_ids=player_ids, lineup=lineup)

        #
        # get the players and put them into an ordered array
        site_sport = lineup.draftgroup.salary_pool.site_sport
        players = self.get_player_array_from_player_ids_array(player_ids, site_sport)


        #
        # validates the lineup based on the players and draftgroup
        roster_manager = RosterManager(site_sport)
        self.__validate_lineup(players, lineup.draftgroup, roster_manager)

        #
        # TODO check the earliest time for a draftgroup or for each player

        #
        # adds the player ids to the corresponding spots in the lineup
        lineup_players =  LineupPlayer.objects.filter(lineup=lineup).order_by('idx')
        i = 0
        for lineup_player in lineup_players:
            if lineup_player.player != players[i]:
                lineup_player.player = players[i]
            i+=1
            lineup_player.save()


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
