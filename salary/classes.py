from sports.models import PlayerStats
from mysite.exceptions import IncorrectVariableTypeException, NullModelValuesException

#-------------------------------------------------------------------
#-------------------------------------------------------------------
class PlayerStatsObject(object):
    """
    Object that wraps the PlayerStatsObject's important information for
    salary generation.
    """

    def __init__(self, player_stats_object):
        """
        Takes in a :class:`sports.models.PlayerStats` object and pulls out
        important information for Salary Generation

        :param player_stats_object: An instance of  :class:`sports.models.PlayerStats`

        :raise :class:`mysite.exceptions.IncorrectVariableTypeException`:
        :raise :class:`mysite.exceptions.NullModelValuesException`:

        """
        #
        # Makes sure the player_stats_object is an instance
        # of the subclass PlayerStats
        if(not isinstance(player_stats_object, PlayerStats)):
            raise IncorrectVariableTypeException(type(self).__name__,
                                          "player_stats_object")

        #
        # Sets the variables of teh PlayerStatsObject to wrap
        # the important data fields of the player_stats_object
        self.first_name         = player_stats_object.player.first_name
        self.last_name          = player_stats_object.player.last_name
        self.game_id            = player_stats_object.srid_game
        self.date               = player_stats_object.game.start
        self.fantasy_points     = player_stats_object.fantasy_points
        self.position           = player_stats_object.position
        self.primary_position   = player_stats_object.primary_position

        #
        # Throw an exception if any of the important data types
        # are missing data.
        if( self.first_name         == None or
            self.last_name          == None or
            self.game_id            == None or
            self.date               == None or
            self.fantasy_points     == None or
            self.position           == None or
            self.primary_position   == None):
            raise NullModelValuesException(type(self).__name__,
                                          "player_stats_object")




#-------------------------------------------------------------------
#-------------------------------------------------------------------
class SalaryGenerator(object):
    """
    This class is responsible for generating the salaries for a given sport.
    """

    def __init__(self, player_stats_class, salary_conf):
        """

        :return:
        """
                #
        # Makes sure the player_stats_object is an instance
        # of the subclass PlayerStats
        if(not issubclass(player_stats_class, PlayerStats)):
            raise IncorrectVariableTypeException(type(self).__name__,
                                          "ps_class")


        #
        # sets the variables after being validated
        self.player_stats_class = player_stats_class
        self.salary_conf        = salary_conf



    def generate_salaries(self):
        """
        Generates the salaries for the player_stats_players
        :return:
        """
        players = self.__get_relevant_player_stats()




    def __get_relevant_player_stats(self):
        """
        For each player in the PlayerStats table, get the games
        that are relevant.
        :return:
            [
                [0]:
                [

                    [0]:PlayerStatsObject
                    [1]:...
                ],
                .....
            ]

        """
        #
        # get the Player type from the

        pass

