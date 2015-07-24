from mysite.classes import AbstractSiteUserClass
from django.db.transaction import atomic
from draftgroup.models import DraftGroup
from .models import Lineup

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

        """
        self.validate_arguments(player_ids=player_ids, draftgroup=draftgroup)
         #
        # get the players and put them into an ordered array
        players = self.get_player_array_from_player_ids_array(player_ids)

        #
        # validates the lineup based on the players and draftgroup
        self.__validate_lineup(players, draftgroup)

        #
        # creates a lineup based on the player ids


    @atomic
    def edit_lineup(self, player_ids, lineup):
        """

        :param player_ids: an ordered list of :class:`sports.models.Player` ids
            for the lineup.
        :param lineup:

        """
        self.validate_arguments(player_ids=player_ids, lineup=lineup)

        #
        # get the players and put them into an ordered array
        players = self.get_player_array_from_player_ids_array(player_ids)

        #
        # validates the lineup based on the players and draftgroup
        self.__validate_lineup(players, lineup.draftgroup)

        #
        # adds the player ids to the corresponding spots in the lineup


    def __validate_lineup(self, players, draftgroup):
        """
        Validation that the lineup can be submitted to the contest
        :param players: an ordered list of :class:`sports.models.Player` for the lineup.
        :param draftgroup:

        """
        #
        # Logical Validation of the Lineups
        self.__validate_player_positions()
        self.__validate_player_salaries()



    def __validate_player_positions(self):
        """
        Makes sure the players match the corresponding roster spots
        for the sport and that the roster size is correct.

        """

        pass

    def __validate_player_salaries(self):
        """
        Makes sure the players salaries do not exceed
        """
        pass

    def get_player_array_from_player_ids_array(self, player_ids):
        """
        Creates and returns an array of :class:`sports.models.Player` objects based
        on the player_ids array.

        :param player_ids: an ordered list of :class:`sports.models.Player` ids
            for the lineup.
        :return: an array of :class:`sports.models.Player` objects
        """
        return []