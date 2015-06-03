from sports.models import PlayerStats, Player, Game, SiteSport, Position
from roster.models import RosterSpot, RosterSpotPosition
from mysite.exceptions import IncorrectVariableTypeException, NullModelValuesException
from django.contrib.contenttypes.models import ContentType
from .models import SalaryConfig, TrailingGameWeight, Pool, Salary
from django.utils import timezone
from math import ceil


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
        self.player_id          = player_stats_object.player_id
        self.player             = player_stats_object.player


        #
        # Throw an exception if any of the important data types
        # are missing data.
        if( self.first_name         == None or
            self.last_name          == None or
            self.game_id            == None or
            self.start              == None or
            self.fantasy_points     == None or
            self.position           == None or
            self.player             == None):
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
        self.player = None
        self.fantasy_weighted_average = None
        self.fantasy_average = None

        self.flagged = False

    def __str__(self):
        string_ret = str(self.player_id)+ " w_points="+str(self.fantasy_weighted_average)+\
                     " flagged="+str(self.flagged)+": \n"
        for player in self.player_stats_list:
            string_ret += "\t"+str(player)+"\n"
        return string_ret

    def get_fantasy_average(self):
        if self.fantasy_weighted_average == None:
            self.fantasy_weighted_average = 0.0
            count = 0
            for player_stat in self.player_stats_list:
                self.fantasy_weighted_average += player_stat.fantasy_points
                count+=1

            if count > 0:
                self.fantasy_weighted_average /= count
        print("\n\nweight:"+str(self.fantasy_weighted_average))
        return self.fantasy_weighted_average




class SalaryPositionPointsAverageObject(object):
    def __init__(self, pos):
        self.pos = pos
        self.total_points = 0
        self.count = 0
        self.average=  0

    def update_average(self):
        self.average  = self.total_points / self.count

    def __str__(self):
        return "POS:"+self.pos.name+" average_score:"+str(self.average)


class SalaryRosterSpotObject(object):
    def __init__(self, name):
        self.name = name
        self.percentage_of_sum = 0.0
        self.average_cost = 0.0
        self.average_salary=  0.0


    def __str__(self):
        return "Roster_Spot_Name:"+self.name+" average_salary:"+str(self.average_salary)\
               +" percentage_of_sum:"+str(self.percentage_of_sum)
#-------------------------------------------------------------------
#-------------------------------------------------------------------
class SalaryGenerator(object):
    """
    This class is responsible for generating the salaries for a given sport.
    """
    PLAYER_STATS_LIST = 'psl'

    def __init__(self, player_stats_class, salary_conf, site_sport):
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
        # Makes sure the site_sport is an instance
        # of the subclass SiteSport
        if(not isinstance(site_sport, SiteSport)):
            raise IncorrectVariableTypeException(type(self).__name__,
                                                 "site_sport")
        #
        # sets the variables after being validated
        self.player_stats_class = player_stats_class
        self.salary_conf        = salary_conf
        self.site_sport         = site_sport



    def generate_salaries(self):
        """
        Generates the salaries for the player_stats_players
        :return:
        """
        #
        # Get all the players
        players = self.helper_get_player_stats()

        #
        # Get the average score per position so we know
        # which positions should have more value

        position_average_list =self.helper_get_average_score_per_position(players)
        #
        # Trim the stats to the games we care about
        self.helper_trim_players_stats(players)
        #print(players)


        #
        # apply weights to each score to come up with the
        # average weighted score for each player
        self.helper_apply_weight_and_flag(players)
        self.__print_players_list(players)

        sum_average_points = self.helper_sum_average_points_per_roster_spot(position_average_list)

        #
        # Calculate the salaries for each player based on
        # the mean of weighted score of their position
        self.helper_update_salaries(players, position_average_list,sum_average_points)






    def helper_get_player_stats(self):
        """
        For each player in the PlayerStats table, get the games
        that are relevant.
        :retun a list of SalaryPlayerObjects

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
                player.player =player_stats_object.player
                players.append(player)
            player.player_stats_list.append(player_stats_object)

        return players


    def helper_get_average_score_per_position(self, players):

        position_average_list = {}
        #
        # Iterate through all of the player stats and store the total
        # fantasy points per position
        for player in players:
            #
            # Make sure the player has an acceptable average FPPG to be included
            # in getting the average points per position
            if player.get_fantasy_average() >= self.salary_conf.min_avg_fppg_allowed_for_avg_calc:
                for player_stats in player.player_stats_list:

                    #
                    # Creates a new SalaryPositionPointsAverageObject if the
                    # object is not created for the given position
                    position_points_obj = None
                    if player_stats.position not in position_average_list:
                        position_points_obj = SalaryPositionPointsAverageObject(
                                                    player_stats.position
                                              )

                        position_average_list.update(
                            {player_stats.position:position_points_obj}
                        )
                    else:
                        position_points_obj = position_average_list[player_stats.position]

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





    def helper_trim_players_stats(self, players):


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





    def helper_apply_weight_and_flag(self, players):
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




    def helper_sum_average_points_per_roster_spot(self, position_average_list):
        #
        # get all the roster spots for the sport and sum up the average
        # fantasy points for each spot * spot.amount
        roster_spots = RosterSpot.objects.filter(site_sport = self.site_sport)
        sum_average_points = 0.0
        for roster_spot in roster_spots:
            #
            # find the positions that map to the specified roster spot and average the
            # average fantasy points for the position from the position_average_list
            roster_maps = RosterSpotPosition.objects.filter(roster_spot = roster_spot)
            count = 0
            sum   = 0.0
            for roster_map in roster_maps:
                position = roster_map.position
                sum     += position_average_list[position].average
                count   += 1
            sum_average_points += ((sum / ((float)(count))) * ((float)(roster_spot.amount)))
        return sum_average_points



    def helper_update_salaries(self, players, position_average_list, sum_average_points):
        #
        # Creates a salary pool
        pool = Pool()
        pool.site_sport = self.site_sport
        pool.salary_config = self.salary_conf
        pool.save()


        roster_spots = RosterSpot.objects.filter(site_sport = self.site_sport)
        for roster_spot in roster_spots:
            #
            # creates a list of the primary positions for the roster spot
            roster_maps = RosterSpotPosition.objects.filter(roster_spot = roster_spot,
                                                            is_primary = True)
            #
            # If the query returns any roster maps it means that the roster spot
            # is a primary spot for one or more positions.
            if len(roster_maps) > 0:

                #
                # create the average salary for the roster spot based off the
                # the average points percentage of total points for each roster
                # spot multiplied by the max_team_salary
                pos_arr= []
                count = 0
                sum   = 0.0
                for roster_map in roster_maps:
                    pos_arr.append(roster_map.position)
                    sum     += position_average_list[roster_map.position].average
                    count   += 1

                average_salary = (((sum / ((float)(count))) / sum_average_points)
                                   * ((float)(self.salary_conf.max_team_salary)))
                average_salary = self.__round_salary(average_salary)


                #
                # Get the average weighted fantasy points for the specific positions
                # in the pos_arr
                count = 0
                sum   = 0.0
                for player in players:
                    if(player.player_stats_list[0].position in pos_arr):
                        sum   += player.fantasy_weighted_average
                        count += 1
                average_weighted_fantasy_points_for_pos = (sum / ((float)(count)))


                #
                # creates the salary for each player in the specified roster spot
                for player in players:
                    if(player.player_stats_list[0].position in pos_arr):

                        salary          = Salary()
                        salary.amount   = ((player.fantasy_weighted_average /
                                          average_weighted_fantasy_points_for_pos) *
                                         average_salary)
                        salary.amount   = self.__round_salary(salary.amount)
                        if(salary.amount < self.salary_conf.min_player_salary):
                            salary.amount = self.salary_conf.min_player_salary
                        salary.flagged  = player.flagged
                        salary.pool     = pool
                        salary.player   = player.player
                        salary.save()
                        print("player: "+salary.player.first_name+" salary: "+str(salary.amount)+ "\n")






    def __round_salary(self, val):
        return (int) (ceil((val/100.0)) *100.0)













