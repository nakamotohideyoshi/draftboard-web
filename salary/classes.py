#
# salary/classes.py

import csv
from statistics import mean
from django.db.models import Q
from .exceptions import (
    NoPlayersAtRosterSpotException,
    NoPlayerStatsClassesFoundException,
)
from sports.models import PlayerStats, Player, Game, SiteSport, Position
from sports.mlb.models import PlayerStatsHitter, PlayerStatsPitcher
from roster.models import RosterSpot, RosterSpotPosition
from mysite.exceptions import IncorrectVariableTypeException, NullModelValuesException
from django.contrib.contenttypes.models import ContentType
from .models import SalaryConfig, TrailingGameWeight, Pool, Salary
from django.utils import timezone
from datetime import timedelta
from math import ceil
from django.db.transaction import atomic
from sports.classes import SiteSportManager
from dataden.classes import DataDen, Season
from util.dfsdate import DfsDate

class SalaryRounder(object):
    """
    use for anything that sets a final salary to centralize the rounding
    that happens on final salaries.
    """

    ROUND_TO_NEAREST = 100.0

    def round(self, salary_amount):
        return (int) (ceil((salary_amount/SalaryRounder.ROUND_TO_NEAREST)) * SalaryRounder.ROUND_TO_NEAREST)

# class OwnershipPercentageManager(object):
#
#     max_search_days = 10
#
#     def __init__(self, pool): # TODO this should probably take a draft_group , or list of contests
#         self.pool = pool
#         self.occurence_data = None
#         self.dfs_date_range = DfsDate.get_current_dfs_date_range()
#
#     def update(self):
#         """
#         updates the %-owned for all Salary objects based on
#         the players occurence in lineups since the last
#         salary pool for the the same sport.
#         """
#
#         # initialize the dict that will hold player lineup occurence counters.
#         self.occurence_data = {}
#         # get all player srids for this pool - we will go back in time
#         # until we find the last day Entries were submitted with this player
#         player_srids = [ p.srid for p in self.get_sport_players(self.pool) ]
#
#         # get all the lineups with which to calculate ownership percentages
#        #lineups = self.get_recent_lineups()
#
#         # TODO - get the start and end datetimes (get enough draft groups in the recent past
#         #        so as to capture at
#         #        ... a draft group which must be at least a day older than now(?)
#         #      start = start of the previous salary pool run
#         #      end =
#         pass
#
#         #
#         # using the DfsDate range builder
#         dfs_date_range = DfsDate.get_current_dfs_date_range()
#         # TODO iterate this backwards
#
#         # TODO get unique lineups
#         # from Entry, get the unique lineups
#         # >>> entries = Entry.objects.filter(user__username='user8').distinct('lineup')
#         # >>> unique_lineups = [ e.lineup for e in entries ]
#
#         # TODO make sure we get the most recent set of lineups entered in contests for the player for %-owned
#
#     # def get_recent_lineups(self):
#     #     """
#     #     get the Entry objects associated with Contests.
#     #     start with today, and work backwards in time until
#     #     we have the most recent day's worth of lineups for
#     #     a specific player -- or until we give up searching, and give
#     #     a default, typical ownership percentage to players we never found.
#     #     """
#     #
#     #     # initialize the list of Lineups to return
#     #     lineups = {}
#     #
#     #     td_delta = timedelta(days=1)
#     #     dfs_dt_range = DfsDate.get_current_dfs_date_range()
#     #
#     #     i = 0
#     #     while i < self.max_search_days:
#     #         # get the Entry objects with a non-null Contest by unique lineup for the day.
#     #         entries = Entry.objects.filter(contest__start__range=dfs_dt_range).distinct('lineup')
#     #         for e in entries:
#     #
#     #
#     #             lineups[e.lineup.pk] =
#     #
#     #         #
#     #         dfs_dt_range = ((dfs_dt_range[0] - td_delta), (dfs_dt_range[1] - td_delta))
#     #         i += 1
#
#     def remove_from_list(self, remove_vals, remove_from_list):
#         pass # TODO
#
#     def get_sport_players(self, pool):
#         pass # TODO
#
#     def add_player_occurence(self, player):
#         pass # TODO

class OwnershipPercentageAdjuster(object):

    def __init__(self, pool):
        self.pool = pool
        self.max_percent_adjust = self.pool.max_percent_adjust
        self.salaries = Salary.objects.filter(pool=pool)
        self.rounder = SalaryRounder()

    def get_capped_percent_adjustment(self, uncapped_percent_adjustment):
        """
        never add/subtract more than this percentage of salary to a given player from his unadjusted amount
        """
        # if its under the cap
        if uncapped_percent_adjustment < self.max_percent_adjust:
            return uncapped_percent_adjustment

        return self.max_percent_adjust

    def update(self):
        """
        adjust the salaries of the players in the pool based on their
        ownership percentages.
        """
        for salary in self.salaries:

            # precedence: do the high ownership first
            if salary.ownership_percentage > self.pool.ownership_threshold_high_cutoff:
                # increase this players salary by pool.high_cutoff_increment
                increments = (salary.ownership_percentage - self.pool.ownership_threshold_high_cutoff)
                high_sal_adjustment = ((increments * self.pool.high_cutoff_increment) / 100.0) * salary.amount
                print('high sal adjustment:', high_sal_adjustment, str(salary))
                salary.amount += self.rounder.round(high_sal_adjustment)
                salary.save()

            # low ownership
            elif salary.ownership_percentage < self.pool.ownership_threshold_low_cutoff:
                # decrease this players salary by 'pool.low_cutoff_increment'
                increments = (self.pool.ownership_threshold_low_cutoff - salary.ownership_percentage)
                low_sal_adjustment = ((increments * self.pool.low_cutoff_increment) / 100.0) * salary.amount
                print('low sal adjustment:', low_sal_adjustment, str(salary))
                salary.amount -= self.rounder.round(low_sal_adjustment)
                salary.save()

    def reset(self):
        """
        unapplies all ownership adjustments, setting the salaries
        back to their original values
        """
        for salary in self.salaries:
            salary.amount = salary.amount_unadjusted
            salary.save()

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
    and their derived data
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
        if self.fantasy_average == None:
            self.fantasy_average = 0.0
            count = 0
            for player_stat in self.player_stats_list:
                self.fantasy_average += player_stat.fantasy_points
                count+=1

            if count > 0:
                self.fantasy_average /= count
        return self.fantasy_average




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
class FppgGenerator(object):

    def __init__(self, player_stats_classes):
        #
        # Makes sure the player_stats_object is an instance
        # of the subclass PlayerStats
        for player_stats_class in player_stats_classes:
            if not issubclass(player_stats_class, PlayerStats):
                raise IncorrectVariableTypeException(type(self).__name__,
                                                     type(player_stats_class).__name__)

        self.player_stats_classes = player_stats_classes

    def get_salary_player_stats_objects(self, player_stats):
        """
        build a list where each index is a SalaryPlayerStatsObject object
        from which we can get a list of all their games found in 'player_stats'

        :param player_stats: all the PlayerStats instances to refactor by player
        :return:
        """
        salary_player_stats = []
        for player_stat in player_stats:
            #
            # Creates an object for the PlayerStat
            player_stats_object = SalaryPlayerStatsObject(player_stat)

            #
            # checks to see if the player exists in the player_list,
            # if not, create a index for the player and add to the
            # list
            arr = [ x for x in salary_player_stats if x.player_id == player_stats_object.player_id ]
            player = None
            if len(arr) > 0:
                player = arr[0]
            else:
                player              = SalaryPlayerObject()
                player.player_id    = player_stats_object.player_id
                player.player       = player_stats_object.player
                salary_player_stats.append(player)

            player.player_stats_list.append(player_stats_object)

        # return the list weve built
        return salary_player_stats

    def helper_get_player_stats(self):
        """
        For each player in the PlayerStats table, get the games
        that are relevant.

        :param player_stats_objects: default: None. overrides the PlayerStats objects used
        :return a list of SalaryPlayerObjects

        """

        #print( 'self.player_stats_classes', str(self.player_stats_classes))

        #
        #
        players = []
        for player_stats_class in self.player_stats_classes:
            #
            # iterate through all player_stats ever
            all_player_stats = player_stats_class.objects.filter(fantasy_points__gt=0)

            # for player_stat in all_player_stats:
            #     #
            #     # Creates an object for the PlayerStat
            #     player_stats_object = SalaryPlayerStatsObject(player_stat)
            #
            #     #
            #     # checks to see if the player exists in the player_list,
            #     # if not, create a index for the player and add to the
            #     # list
            #     arr =[x for x in players if x.player_id == player_stats_object.player_id]
            #     player = None
            #     if(len(arr) >0 ):
            #         player= arr[0]
            #     else:
            #         player = SalaryPlayerObject()
            #         player.player_id = player_stats_object.player_id
            #         player.player =player_stats_object.player
            #         players.append(player)
            #     player.player_stats_list.append(player_stats_object)
            players.extend(self.get_salary_player_stats_objects(all_player_stats))

        return players

class SalaryGenerator(FppgGenerator):
    """
    This class is responsible for generating the salaries for a given sport.
    """

    DEFAULT_SEASON_TYPES = ['reg','pst']

    def __init__(self, player_stats_classes, pool, season_types=None):
        """

        :return:
        """
        super().__init__(player_stats_classes)

        #
        # Makes sure the pool is an instance
        # of the subclass Pool
        if not isinstance(pool, Pool):
            raise IncorrectVariableTypeException(type(self).__name__,
                                                 type(pool).__name__)


        #
        # sets the variables after being validated
        #self.player_stats_classes = player_stats_classes ### in parent class
        self.pool = pool
        self.salary_conf = pool.salary_config
        self.site_sport = pool.site_sport
        self.site_sport_manager = SiteSportManager()
        self.season_types           = season_types
        if self.season_types is None:
            self.season_types = SalaryGenerator.DEFAULT_SEASON_TYPES
        self.regular_season_games   = None
        self.excluded_players       = None
        self.excluded_player_stats  = None

        self.rounder = SalaryRounder()

    def generate_salaries(self):
        """
        Generates the salaries for the player_stats_players
        :return:
        """

        #
        # get the regular season games, and all the players
        game_class = self.site_sport_manager.get_game_class(self.site_sport)
        self.regular_season_games = game_class.objects.filter(
                                        season__season_type__in=self.season_types )

        players = self.helper_get_player_stats(trailing_days=self.salary_conf.trailing_games)

        self.excluded_players = self.get_salary_player_stats_objects(self.excluded_player_stats)

        #
        # Get the average score per position so we know
        # which positions should have more value
        position_average_list =self.helper_get_average_score_per_position(players)

        #
        # Trim the stats to the games we care about
        self.helper_trim_players_stats(players)

        #
        # apply weights to each score to come up with the
        # average weighted score for each player
        self.helper_apply_weight_and_flag(players)

        sum_average_points = self.helper_sum_average_points_per_roster_spot(position_average_list)

        #
        # Calculate the salaries for each player based on
        # the mean of weighted score of their position
        self.helper_update_salaries(players, position_average_list, sum_average_points)

        #
        # Save this original salary into the 'amount_unadjusted' field to be able to reset
        self.update_unadjusted_salaries(self.pool)

    def helper_get_player_stats(self, trailing_days=None):
        """
        For each player in the PlayerStats table, get the games
        that are relevant.

        :param player_stats_objects: default: None. overrides the PlayerStats objects used
        :return a list of SalaryPlayerObjects

        """

        #
        #
        players = []
        excluded_players = []
        for player_stats_class in self.player_stats_classes:
            #
            # iterate through all player_stats ever
            reg_season_game_pks = []
            if trailing_days is None:
                # get them all
                reg_season_game_pks = [ g.pk for g in self.regular_season_games ]
            else:
                # only get the games within the trailing number of days
                cutoff = timezone.now() - timedelta(days=trailing_days)
                for reg_game in self.regular_season_games:
                    if reg_game.start >= cutoff:
                        reg_season_game_pks.append( reg_game.pk )

            print('%s game pks' % str(len(reg_season_game_pks))) # DEBUG

            all_player_stats = player_stats_class.objects.filter(fantasy_points__gt=0,
                                                        game_id__in=reg_season_game_pks)
            excluded_players.extend(player_stats_class.objects.filter(fantasy_points__lte=0))
            players.extend(self.get_salary_player_stats_objects(all_player_stats))

        # this will exclude a set of players from receiving a salary in
        # the algorithm -- that being the set of players who have
        # not played, or who have played but have 0.0 fantasy points.
        # lets store those players and give them a minimum salary later on.
        self.excluded_player_stats = excluded_players

        return players

    def update_unadjusted_salaries(self, pool):
        """
        set the Salary objects 'amount' into the amount_unadjusted field
        for all players passed in via 'players' param

        :param players:
        :return:
        """
        for sal_obj in Salary.objects.filter(pool=pool):
            sal_obj.amount_unadjusted = sal_obj.amount
            sal_obj.save()

    def helper_get_average_score_per_position(self, players):

        position_average_list = {}
        #
        # Iterate through all of the player stats and store the total
        # fantasy points per position
        for player in players:
            #
            # Make sure the player has an acceptable average FPPG to be included
            # in getting the average points per position
            player_avg = player.get_fantasy_average()
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
            #print("\n"+str(position_average_list[key]))
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

            # if not a lot of games played
            if number_of_games < self.salary_conf.min_games_flag:
                #print('less than the required games: %s for %s' % (str(number_of_games), str(player)))
                # if player has played in 0 thru the min_games_flag,
                # dont use weights, and just average the points they do have
                # and flag them.
                if number_of_games > 0:
                    fp_list = [ stat.fantasy_points for stat in player.player_stats_list ]
                    player.fantasy_weighted_average = mean(fp_list)
                # flag them regardless
                player.flagged = True

            # else: if more than the min-required-games-played have been played
            else:
                #print('MET required games: %s for %s' % (str(number_of_games), str(player)))
                # check to makes sure the most recent game played has been less than
                # days_since_last_game_flag days ago
                delta = timezone.now() - player.player_stats_list[0].start
                if delta.days > self.salary_conf.days_since_last_game_flag:
                    #print('days since last game: %s -- last game %s' % (str(delta.days), str(player.player_stats_list[0].start)))
                    player.flagged= True

                #
                # Iterates through the weights and applies them to the fantasy points
                i = 0
                for tgw in trailing_game_weights:
                    for j in range(i, tgw.through):
                        if i < self.salary_conf.trailing_games:
                            if j < number_of_games:
                                player.fantasy_weighted_average += \
                                    player.player_stats_list[j].fantasy_points * (float)(tgw.weight)
                    #
                    i = tgw.through

                #
                # If the configuration does not account trailing games use a 1x multiplier
                # on the remainder
                while i < self.salary_conf.trailing_games:
                    if i < number_of_games:
                        player.fantasy_weighted_average += \
                            player.player_stats_list[i].fantasy_points * (float)(tgw.weight)
                    i += 1

                #
                # takes the sum and divides by the total allowed games
                player.fantasy_weighted_average /= (float)(self.salary_conf.trailing_games)

    def helper_sum_average_points_per_roster_spot(self, position_average_list):
        """
        Sums up the fppg for each roster spot so we can use it for calculating the
        the salaries
        :param position_average_list:
        :return:
        """
        #print("position_average_list keys:"+str(position_average_list.keys()))
        #print('position_average_list:', str(position_average_list))
        #
        # get all the roster spots for the sport and sum up the average
        # fantasy points for each spot * spot.amount
        roster_spots = RosterSpot.objects.filter(site_sport = self.site_sport)
        #print('site_sport', str(self.site_sport), self.site_sport.name)
        sum_average_points = 0.0
        for roster_spot in roster_spots:
            #
            # find the positions that map to the specified roster spot and average the
            # average fantasy points for the position from the position_average_list
            roster_maps = RosterSpotPosition.objects.filter(roster_spot = roster_spot)
            count = 0
            sum   = 0.0
            #print('roster_maps:', len(roster_maps), 'for %s' % str(roster_spot))
            for roster_map in roster_maps:
                position = roster_map.position
                if position in position_average_list:
                    sum     += position_average_list[position].average
                    count   += 1
                # debug print:
                #print( '    roster_map', str(count), str(roster_map) )
            try:
                sum_average_points += ((sum / ((float)(count))) * ((float)(roster_spot.amount)))
            except ZeroDivisionError:
                print('repeated NoPlayersAtRosterSpotExceptions could indicate you '
                      'have set the "Min FPPG Allowed for Avg Calc too high !!!!')
                raise NoPlayersAtRosterSpotException()

        return sum_average_points

    @atomic
    def helper_update_salaries(self, players, position_average_list, sum_average_points):
        """
        Helper method in charge of creating salary entries for players for the pool
        passed to this class. This method will update existing entries for players
        that already exist. THis method should *not* be called outside of this
        class.
        :param players:
        :param position_average_list:
        :param sum_average_points:
        :return:
        """

        # initialize the salaries by setting everyone to the minimum
        min_salary = self.salary_conf.min_player_salary
        #Salary.objects.filter(pool=self.pool, amount__lt=min_salary).update(amount=min_salary)
        #count = 0
        for sal_obj in Salary.objects.filter(pool=self.pool):
            old_sal = sal_obj.amount
            sal_obj.amount = min_salary
            sal_obj.save()
            sal_obj.refresh_from_db()
            #print('old:', str(old_sal), 'now:', str(sal_obj.amount), 'player:',str(sal_obj.player))

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
                    if roster_map.position in position_average_list:
                        sum     += position_average_list[roster_map.position].average
                        count   += 1

                average_salary = (((sum / ((float)(count))) / sum_average_points)
                                   * ((float)(self.salary_conf.max_team_salary)))
                average_salary = self.__round_salary(average_salary)
                #print( roster_spot.name+" average salary "+ str(average_salary))

                #
                # Get the average weighted fantasy points for the specific positions
                # in the pos_arr
                count = 0
                sum   = 0.0
                average_weighted_fantasy_points_for_pos = 0.0
                for player in players:
                    if(player.player_stats_list[0].position in pos_arr):
                        if player.get_fantasy_average() >= self.salary_conf.min_avg_fppg_allowed_for_avg_calc:
                            sum   += player.fantasy_weighted_average
                            count += 1
                if count > 0:
                    average_weighted_fantasy_points_for_pos = (sum / ((float)(count)))

                #
                # creates the salary for each player in the specified roster spot
                for player in players:
                    if player.player_stats_list[0].position in pos_arr:
                        salary              = self.get_salary_for_player(player.player)
                        if average_weighted_fantasy_points_for_pos == 0.0:
                            salary.amount = self.salary_conf.min_player_salary
                        else:
                            salary.amount = ((player.fantasy_weighted_average /
                                              average_weighted_fantasy_points_for_pos) * average_salary)

                        salary.amount   = self.__round_salary(salary.amount)
                        if(salary.amount < self.salary_conf.min_player_salary):
                            salary.amount = self.salary_conf.min_player_salary
                        salary.flagged  = player.flagged
                        salary.pool     = self.pool
                        salary.player   = player.player
                        salary.primary_roster = roster_spot
                        salary.fppg     = player.fantasy_weighted_average
                        if salary.fppg is None:
                            salary.fppg = 0.0
                        salary.save()

    def get_salary_for_player(self, player):
        """
        Method takes in a :class:`sports.models.Player` model object and
        either gets the Salary object for that player and the pool or returns
        a new Salary Object
        :param player:  a :class:`sports.models.Player` model object
        :return: a :class:`salary.models.Salary` object
        """
        try:
            player_type = ContentType.objects.get_for_model(player)
            salary_obj = Salary.objects.get(pool=self.pool,
                                            player_type=player_type,
                                            player_id=player.id)

            return salary_obj
        except Salary.DoesNotExist:
            return Salary()

    def __round_salary(self, val):
        #return (int) (ceil((val/SalaryGenerator.ROUND_TO_NEAREST)) * SalaryGenerator.ROUND_TO_NEAREST)
        return self.rounder.round(val)

class PlayerFppgGenerator(FppgGenerator):
    """
    Generates regular seasona "fantasy points per game" for players for a sport.

    Utilizes the SalaryGenerator class for its methods which are capable
    of calculating averages on the PlayerStats.fantasy_points field,
    because it does pretty much the same thing.

    While the SalaryGenerator class uses a queryset of PlayerStats objects
    based on the settings of a specific salary pool, this SeasonFppgGenerator's
    primary job is to get the regular season games for the curent season
    and then get those related PlayerStats and pass them off to the methods
    of SalaryGenerator which calculate the average.

    NBA Season Start Month-Day: ~27 October 	    (10th month)
    NHL Season Start Month-Day: ~7 October  	    (10th month)
    MLB Season Start Month-Day: ~3 April 		    (4th month)
    NFL Season Start Month-Day: ~4 September 	    (9th month)
    """

    def __init__(self):
        self.site_sport_manager = SiteSportManager()

    def update(self):
        for sport in self.site_sport_manager.SPORTS:
            #
            # todo, task this off, so if it crashes, it wont other sports
            self.update_sport( sport )

    def update_sport(self, sport):
        """
        update the player fppgs for the sports current season found in SiteSport

        :param sport:
        :return:
        """
        site_sport = self.site_sport_manager.get_site_sport(sport)
        # get the regular season game srids
        season = Season.factory( sport ) # makes a connection to mongolab directly
        game_srids = season.get_game_ids_regular_season(site_sport.current_season)

        # get all the players for the sport
        player_class = self.site_sport_manager.get_player_class(site_sport)
        player_objects = player_class.objects.all()
        # get playerstats classes (there may be multiple)
        player_stats_classes = self.site_sport_manager.get_player_stats_class(site_sport)

        #
        # sports with multiple PlayerStats classes require us to handle
        # the fppg calcs differently, ie: break up pitchers and hitters
        #print('updating season_fppg - sport:', sport)
        #print('... %s player_stats_classses -> %s' % (str(len(player_stats_classes)), str(player_stats_classes)))
        if len(player_stats_classes) == 1:
            #
            # sports like nfl, nhl, nba only have a single PlayerStats model
            self.get_fppg(player_objects, player_stats_classes[0], game_srids)

        #
        # mlb, for example, has 2 stats models, PlayerStatsPitcher, PlayerStatsHitter
        elif len(player_stats_classes) >= 2 and sport == 'mlb':
            #
            # get players that are SP, P, or RP, and the PlayerStatsPitcher class
            q_pitcher_positions = Q(position__name__in=['P','SP','RP'])
            pitcher_players = player_objects.filter(q_pitcher_positions)
            self.get_fppg(pitcher_players, PlayerStatsPitcher, game_srids)

            #
            # get all other players, and the PlayerStatsHitter class.
            # all non-pitchers are hitters, so simply negate the Q expression
            hitter_players = player_objects.filter(~q_pitcher_positions)
            self.get_fppg(hitter_players, PlayerStatsHitter, game_srids)

        # elif len(player_stats_classes) >= 2 and sport == 'xxx': pass

        else:
            raise NoPlayerStatsClassesFoundException('PlayerFppgGenerator: %s' % sport)

    def get_fppg(self, player_objects, player_stats_class, game_srids):
        """
        :param player_objects: list of sport.<sport>.models.Player objects
        :param player_stats_class: the PlayerStats class we want to calc
                                FPPGs with for each player in player_objects
        :return:
        """
        if not issubclass(player_stats_class, PlayerStats):
            raise IncorrectVariableTypeException(type(self).__name__,
                                                 type(player_stats_class).__name__)
        #
        # get the PlayerStats objects for the the players
        # in the 'player_objects' param where the PlayerStats
        # have been filtered to include only PlayerStats from games
        # whose srid is in the param 'game_srids'.

        #
        # we know we have Player objects and PlayerStats objects
        # from the same sport, so we can use the 'player_id' (of
        # the GenericForeignKey) to search for our players...
        player_ids = [ p.id for p in player_objects ]
        player_stats_objects = player_stats_class.objects.filter(player_id__in=player_ids,
                                                                 srid_game__in=game_srids,
                                                                 fantasy_points__gt=0)
        # utilizing the SalaryPlayerStatsObject to amass the fppg
        # from each sublist of individual PlayerStats objects
        salary_player_objects = self.get_salary_player_stats_objects(player_stats_objects)
        # print('... %s players season_fppg calculated' % (str(len(salary_player_objects))))
        # print('printing out a couple of get_fppgs() objects for debug:')
        # for x in salary_player_objects[:3]:
        #     print( str(x) )

        # the get_fantasy_points() should now return the season_fppg.
        # save it into the main player object (which we can get from salary_player_object)
        for salary_player_object in salary_player_objects:
            player = salary_player_object.player
            season_fppg = salary_player_object.get_fantasy_average()

            player.season_fppg = season_fppg
            player.save()

class SalaryPool2Csv(object):

    # class Echo(object):
    #     """
    #     An object that implements just the write method of the file-like interface.
    #     """
    #     def write(self, value):
    #         """
    #         Write the value by returning it, instead of storing in a buffer.
    #         """
    #         return value

    columns = ['id','last_name','first_name','price_draftboard']

    def __init__(self, salary_pool_id, httpresponse=None):
        self.httpresponse = httpresponse # set streaming to True when returning this csv in an http response
        self.pool = Pool.objects.get(pk=salary_pool_id)
        self.salaries = Salary.objects.filter(pool=self.pool).order_by('-amount')
        self.csvfile = None

    def __writerow(self, writer, salary):
        writer.writerow([
            salary.player.pk,           # 'id'
            salary.player.last_name,    # 'last_name'
            salary.player.first_name,   # 'first_name'
            salary.amount,              # 'price_draftboard'
        ])

    def generate(self):
        """
        generate the csv file
        :return:
        """
        f = None
        writer = None
        if self.httpresponse is None:
            filename = 'salary-pool-%s.csv' % str(self.pool.pk)
            f = open(filename, 'w', newline='')
            writer = csv.writer( f )
        else:
            writer = csv.writer( self.httpresponse )

        writer.writerow( self.columns )
        for salary in self.salaries:
            self.__writerow( writer, salary )

        if f is not None:
            # close the file if we used an actual file
            f.close()











