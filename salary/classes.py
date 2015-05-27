from sports.models import PlayerStats, Player, Game
from mysite.exceptions import IncorrectVariableTypeException, NullModelValuesException
from django.contrib.contenttypes.models import ContentType
from .models import SalaryConfig, TrailingGameWeight
from django.utils import timezone

#-------------------------------------------------------------------
#-------------------------------------------------------------------
class SalaryPlayerStatsObject(object):
    """
    Object that wraps the PlayerStatsObject's important information for
    salary generation.
    """

    def __init__(self, player_stats_object):
        """
        Takes in a :class:`sports.models.PlayerStats` object and pulls out
        important information for Salary Generation

        :param player_stats_object: An instance of
            :class:`sports.models.PlayerStats`

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
        self.game_id            = player_stats_object.game_id
        self.start              = player_stats_object.game.start
        self.fantasy_points     = player_stats_object.fantasy_points
        self.position           = player_stats_object.position
        self.primary_position   = player_stats_object.primary_position
        self.player_id          = player_stats_object.player_id


        #
        # Throw an exception if any of the important data types
        # are missing data.
        if( self.first_name         == None or
            self.last_name          == None or
            self.game_id            == None or
            self.start              == None or
            self.fantasy_points     == None or
            self.position           == None or
            self.primary_position   == None):
            raise NullModelValuesException(type(self).__name__,
                                          "player_stats_object")
    def __str__(self):
        return str(self.game_id)+"--" +str(self.fantasy_points)+"pts\t "+str(self.start)
class SalaryPlayerObject(object):
    """
    Object that wraps the the list of SalaryPLayerStatsObjects
    and their derrived data
    """

    def __init__(self):
        self.player_stats_list = []
        self.player_id = None
        self.fantasy_weighted_average = None
        self.flagged = False

    def __str__(self):
        string_ret = str(self.player_id)+ " w_points="+str(self.fantasy_weighted_average)+\
                     " flagged="+str(self.flagged)+": \n"
        for player in self.player_stats_list:
            string_ret += "\t"+str(player)+"\n"
        return string_ret

class SalaryPositionPointsAverageObject(object):
    def __init__(self, pos):
        self.pos = pos
        self.total_points = 0
        self.count = 0
        self.average=  0

    def update_average(self):
        self.average  = self.total_points / self.count

    def __str__(self):
        return "POS:"+self.pos+" average_score:"+str(self.average)

#-------------------------------------------------------------------
#-------------------------------------------------------------------
class SalaryGenerator(object):
    """
    This class is responsible for generating the salaries for a given sport.
    """
    PLAYER_STATS_LIST = 'psl'

    def __init__(self, player_stats_class, salary_conf):
        """

        :return:
        """
        #
        # Makes sure the player_stats_object is an instance
        # of the subclass PlayerStats
        if(not issubclass(player_stats_class, PlayerStats)):
            raise IncorrectVariableTypeException(type(self).__name__,
                                                 type(player_stats_class).__name__)

        #
        # Makes sure the salary_conf is an instance
        # of the subclass SalaryConfig
        if(not isinstance(salary_conf, SalaryConfig)):
            raise IncorrectVariableTypeException(type(self).__name__,
                                                 "salary_conf")
        #
        # sets the variables after being validated
        self.player_stats_class = player_stats_class
        self.salary_conf        = salary_conf




    def generate_salaries(self):
        """
        Generates the salaries for the player_stats_players
        :return:
        """
        #
        # Get all the players
        players = self.__get_relevant_player_stats()

        #
        # Get the average score per position so we know
        # which positions should have more value

        position_average_list =self.__get_average_score_per_position(players)
        #
        # Trim the stats to the games we care about
        self.__trim_players_stats(players)
        #print(players)


        #
        # apply weights to each score to come up with the
        # average weighted score for each player
        self.__apply_weight_and_flag(players)
        self.__print_players_list(players)

        #
        # Calculate the salaries for each player based on
        # the mean of weighted score of their position







    def __get_relevant_player_stats(self):
        """
        For each player in the PlayerStats table, get the games
        that are relevant.
        :return: a list of SalaryPlayerObjects

        """
        #
        #
        players = []
        #
        # iterate through all player_stats ever
        all_player_stats = self.player_stats_class.objects.all()

        for player_stat in all_player_stats:
            #
            # Creates an object for the PlayerStat
            player_stats_object = SalaryPlayerStatsObject(player_stat)

            #
            # checks to see if the player exists in the player_list,
            # if not, create a index for the player and add to the
            # list
            arr =[x for x in players if x.player_id == player_stats_object.player_id]
            player = None
            if(len(arr) >0 ):
                player= arr[0]
            else:
                player = SalaryPlayerObject()
                player.player_id = player_stats_object.player_id
                players.append(player)
            player.player_stats_list.append(player_stats_object)

        return players


    def __get_average_score_per_position(self, players):

        position_average_list = {}
        #
        # Iterate through all of the player stats and store the total
        # fantasy points per position
        for player in players:
            for player_stats in player.player_stats_list:

                #
                # Creates a new SalaryPositionPointsAverageObject if the
                # object is not created for the given position
                position_points_obj = None
                if player_stats.primary_position not in position_average_list:
                    position_points_obj = SalaryPositionPointsAverageObject(
                                                player_stats.primary_position
                                          )

                    position_average_list.update(
                        {player_stats.position:position_points_obj}
                    )

                #
                # adds the points the SalaryPositionPointsAverageObject for
                # the given position and updates the count to create the
                # average later
                position_points_obj.total_points += player_stats.fantasy_points
                position_points_obj.count+= 1

        for key in position_average_list:
            position_average_list[key].update_average()
            print("\n"+str(position_average_list[key]))


        return position_average_list


    def __trim_players_stats(self, players):


        #
        # Sort the lists by newest game first and trim the array to
        # include  self.salary_conf.trailing_games
        for player in players:
            arrToSort = player.player_stats_list
            arrToSort.sort(key=lambda x:x.start, reverse=True)

            del arrToSort[self.salary_conf.trailing_games : ]




    def __print_players_list(self, players):
        for player in players:
            print(player)





    def __apply_weight_and_flag(self, players):
        """
        Updates the flags for the players if they do not meet the requirements for
        salary generation. This method also generates each players weighted salary.
        :param players:
        """
        trailing_game_weights = TrailingGameWeight.objects.filter(salary=self.salary_conf)
        trailing_game_weights.order_by("-through")
        #
        # Iterate through the player objects and weigh their stats and update
        # their flags if applies
        for player in players:
            number_of_games = len(player.player_stats_list)
            player.fantasy_weighted_average = 0

            if(number_of_games > 0 ):
                #
                # check to makes sure the most recent game played has been less than
                # days_since_last_game_flag days ago.
                #  OR
                # check to makes sure the min games are played

                delta = timezone.now() - player.player_stats_list[0].start
                if (delta.days < self.salary_conf.days_since_last_game_flag) or \
                    (number_of_games < self.salary_conf.min_games_flag ):
                    player.flagged= True


                #
                # Iterates through the weights and applies them to the fantasy points
                i = 0
                for tgw in trailing_game_weights:
                    for j in range(i, tgw.through-1):
                        if(j < number_of_games):
                            player.fantasy_weighted_average += \
                                player.player_stats_list[j].fantasy_points * (float)(tgw.weight)

                    i = tgw.through -1
                #
                # takes the sum and divides by the total allowed games
                player.fantasy_weighted_average /= (float)(self.salary_conf.trailing_games)

            else:
                player.flagged= True






















