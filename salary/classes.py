import csv
from logging import getLogger
from math import ceil
from random import Random
from statistics import mean

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.transaction import atomic
from django.utils import timezone
from pytz import timezone as pytz_timezone

from contest.classes import RecentPlayerOwnership
from dataden.classes import Season
from mysite.exceptions import IncorrectVariableTypeException, NullModelValuesException
from roster.models import RosterSpot, RosterSpotPosition
from sports.classes import SiteSportManager
from sports.mlb.models import PlayerStatsHitter, PlayerStatsPitcher
from sports.models import PlayerStats
from util.slack import Webhook
from .exceptions import (
    NoPlayersAtRosterSpotException,
    NoPlayerStatsClassesFoundException,
)
from .models import TrailingGameWeight, Pool, Salary

logger = getLogger('salary.classes')


class SalaryProgressWebhook(Webhook):
    # rio slack - channel #stats-projections
    identifier = 'T02S3E1FD/B2H8GB97T/gHG66jb3wvGHSJb9Zcr7IwHC'


class SalaryRounder(object):
    """
    use for anything that sets a final salary to centralize the rounding
    that happens on final salaries.
    """

    ROUND_TO_NEAREST = 100.0

    def round(self, salary_amount):
        return (int)(
            ceil((salary_amount / SalaryRounder.ROUND_TO_NEAREST)) * SalaryRounder.ROUND_TO_NEAREST)


class OwnershipPercentageAdjuster(object):
    def __init__(self, pool):
        self.pool = pool
        self.default_ownership_percentage = self.pool.ownership_threshold_low_cutoff
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
        returns the integer number of how many salaries were updated
        """

        # sets the ownership percentage in the players
        updated_count = self.update_recent_ownership()
        # modifies the salaries based on the ownership percentages
        self.adjust()

        return updated_count

    @atomic
    def update_recent_ownership(self):
        """
        returns the integer number of how many salaries were updated
        """

        rpo = RecentPlayerOwnership(self.pool.site_sport)
        # get a dict of 'player_srid':<ownership percentage float> items
        players = rpo.get_players()

        # reset everyone to the default ownership percentage level
        self.salaries.update(ownership_percentage=self.default_ownership_percentage)

        # update any recent players we have data for
        updated_count = 0
        for player_srid, pct_owned in players.items():
            for player_salary in self.salaries:
                if player_srid == player_salary.player.srid:
                    logger.info('updating %s percent-owned to %s' % (str(player_salary), str(pct_owned)))
                    player_salary.ownership_percentage = (pct_owned * 100)
                    player_salary.save()
                    updated_count += 1
        #
        return updated_count

    def adjust(self):
        """
        adjust the salaries of the players in the pool based on their
        ownership percentages.
        """
        for salary in self.salaries:

            # precedence: do the high ownership first
            if salary.ownership_percentage > self.pool.ownership_threshold_high_cutoff:
                # increase this players salary by pool.high_cutoff_increment
                increments = (salary.ownership_percentage -
                              self.pool.ownership_threshold_high_cutoff)
                high_sal_adjustment = (
                                          (
                                              increments * self.pool.high_cutoff_increment) / 100.0) * salary.amount
                print('high sal adjustment:', high_sal_adjustment, str(salary))
                salary.amount += self.rounder.round(high_sal_adjustment)
                salary.save()

            # low ownership
            elif salary.ownership_percentage < self.pool.ownership_threshold_low_cutoff:
                # decrease this players salary by 'pool.low_cutoff_increment'
                increments = (self.pool.ownership_threshold_low_cutoff -
                              salary.ownership_percentage)
                low_sal_adjustment = (
                                         (
                                             increments * self.pool.low_cutoff_increment) / 100.0) * salary.amount
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


class PlayerProjection(object):
    """
    data class for a sports.<sport>.models.Player and a fantasy_points value.

    use this class to create base data if you want to
    run projections thru the SalaryGeneratorFromProjections.
    """

    def __str__(self):
        return '%s, %s points' % (self.player, self.fantasy_points)

    def __init__(self, player, fantasy_points=0.0, sal_dk=None, sal_fd=None):
        self.player = player
        self.fantasy_points = fantasy_points
        self.sal_dk = sal_dk
        self.sal_fd = sal_fd


class SalaryPlayerStatsObject(object):
    """
    Object that wraps the PlayerStatsObject's important information for
    salary generation.
    """

    type_checking_enabled = True

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
        if self.type_checking_enabled:
            if (not isinstance(player_stats_object, PlayerStats)):
                raise IncorrectVariableTypeException(type(self).__name__, "player_stats_object")

        #
        # Sets the variables of teh PlayerStatsObject to wrap
        # the important data fields of the player_stats_object
        self.player_stats_instance = player_stats_object
        self.first_name = player_stats_object.player.first_name
        self.last_name = player_stats_object.player.last_name
        self.game_id = player_stats_object.game_id
        self.start = player_stats_object.game.start
        self.fantasy_points = player_stats_object.fantasy_points
        self.position = player_stats_object.position
        self.player_id = player_stats_object.player_id
        self.player = player_stats_object.player

        #
        # Throw an exception if any of the important data types
        # are missing data.
        if (self.first_name == None or
                    self.last_name == None or
                    self.game_id == None or
                    self.start == None or
                    self.fantasy_points == None or
                    self.position == None or
                    self.player == None):
            raise NullModelValuesException(type(self).__name__, "player_stats_object")

    def get_player_stats_instance(self):
        return self.player_stats_instance

    def get_trailing_games(self, trailing_games):
        if isinstance(self.get_player_stats_instance(), PlayerStatsPitcher):
            return int(trailing_games / 5)
        #
        return trailing_games

    def __str__(self):
        return str(self.game_id) + "--" + str(self.fantasy_points) + "pts\t " + str(self.start)


class SalaryPlayerStatsProjectionObject(SalaryPlayerStatsObject):
    """
    this class explicitly does not type checking.
    this is especially useful for SalaryGeneratorFromProjections.
    """

    def __init__(self, player, fantasy_points, sal_dk=None, sal_fd=None):
        """
        'projection' needs to allow us to look up the sports.<sport>.models.Player
        as well as get a fantasy_points value.
        """
        self.player_stats_instance = None  # previously set in parent
        self.player = player

        self.first_name = self.player.first_name
        self.last_name = self.player.last_name

        self.game_id = None  # player_stats_object.game_id
        # self.start = None # player_stats_object.game.start
        self.start = timezone.now()
        self.fantasy_points = float(fantasy_points)
        self.position = self.player.position
        self.player_id = self.player.pk

        # save the actual DK and FD salaries for the player
        self.sal_dk = sal_dk
        self.sal_fd = sal_fd

    def __str__(self):
        return "<SalaryPlayerStatsProjectionObject  %s - projected fp (stats.com): %s>" % (
            self.player, self.fantasy_points)


class SalaryPlayerObject(object):
    """
    Object that wraps the the list of SalaryPLayerStatsObjects
    and their derived data
    """

    default_max_games = 99999

    def __init__(self, max_games=None):
        self.max_games = max_games
        if self.max_games is None:
            self.max_games = self.default_max_games
        self.player_stats_list = []
        self.player_id = None
        self.player = None
        self.fantasy_weighted_average = None
        self.fantasy_average = None

        self.flagged = False

    def __str__(self):
        return ("<SalaryPlayerObject: player: %s | w_points: %s | flagged: %s "
                "\ntotal playerstats instances: %s>") % (
                   self.player, self.fantasy_weighted_average, self.flagged,
                   len(self.player_stats_list))

    def get_fantasy_average(self):
        if self.fantasy_average is None:
            self.fantasy_average = 0.0
            count = 0
            for player_stat in self.player_stats_list[:self.max_games]:
                self.fantasy_average += player_stat.fantasy_points
                count += 1

            if count > 0:
                self.fantasy_average /= count
        return self.fantasy_average


class SalaryPositionPointsAverageObject(object):
    def __init__(self, pos):
        self.pos = pos
        self.total_points = 0
        self.count = 0
        self.average = 0

    def update_average(self):
        self.average = self.total_points / self.count

    def __str__(self):
        return "POS:" + self.pos.name + " average_score:" + str(self.average)


class SalaryRosterSpotObject(object):
    def __init__(self, name):
        self.name = name
        self.percentage_of_sum = 0.0
        self.average_cost = 0.0
        self.average_salary = 0.0

    def __str__(self):
        return "Roster_Spot_Name:" + self.name + " average_salary:" + str(self.average_salary) \
               + " percentage_of_sum:" + str(self.percentage_of_sum)


class FppgGenerator(object):
    type_checking_enabled = True

    def __init__(self, player_stats_classes):
        #
        # Makes sure the player_stats_object is an instance
        # of the subclass PlayerStats
        if self.type_checking_enabled:
            for player_stats_class in player_stats_classes:
                if not issubclass(player_stats_class, PlayerStats):
                    raise IncorrectVariableTypeException(type(self).__name__,
                                                         type(player_stats_class).__name__)

        self.player_stats_classes = player_stats_classes

    def get_salary_player_stats_objects(self, player_stats, trailing_games=None):
        """
        build a list where each index is a SalaryPlayerStatsObject object
        from which we can get a list of all their games found in 'player_stats'

        :param player_stats: all the PlayerStats instances to refactor by player
        :return:
        """

        num_trailing_games = trailing_games
        if num_trailing_games is None:
            # default to an arbitrarily large amount of trailing games
            num_trailing_games = 500

        # 1. get the unique player srids
        # TODO

        # 2. loop on the unique player srids, and re-query to get their trailing games
        # TODO

        # TODO fix this code to use 'num_trailing_games'
        logger.info('num_trailing_games: %s' % num_trailing_games)
        salary_player_stats = []
        for player_stat in player_stats:
            #
            # Creates an object for the PlayerStat
            player_stats_object = SalaryPlayerStatsObject(player_stat)

            #
            # checks to see if the player exists in the player_list,
            # if not, create a index for the player and add to the
            # list
            arr = [x for x in salary_player_stats if x.player_id == player_stats_object.player_id]
            player = None
            if len(arr) > 0:
                player = arr[0]
            else:
                player = SalaryPlayerObject(max_games=trailing_games)
                player.player_id = player_stats_object.player_id
                player.player = player_stats_object.player
                salary_player_stats.append(player)

            player.player_stats_list.append(player_stats_object)

        # return the list weve built
        return salary_player_stats

    def helper_get_player_stats(self):
        """
        For each player in the PlayerStats table, get the games
        that are relevant.

        :return a list of SalaryPlayerObjects

        """

        # print( 'self.player_stats_classes', str(self.player_stats_classes))

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
    This is only used if you are doing the OLD way of generating salaries via `salary.admin.OLD_generate_salaries`.
    """

    DEFAULT_SEASON_TYPES = ['reg', 'pst']

    def __init__(self, player_stats_classes, pool, season_types=None, slack_updates=False,
                 debug_srid='1616381c-d6ac-40b1-8c3f-c70d51bda098'):
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

        self.slack = None
        if slack_updates:
            self.slack = SalaryProgressWebhook()

        #
        # sets the variables after being validated
        self.pool = pool
        self.salary_conf = pool.salary_config
        self.site_sport = pool.site_sport
        self.site_sport_manager = SiteSportManager()
        self.season_types = season_types
        if self.season_types is None:
            self.season_types = SalaryGenerator.DEFAULT_SEASON_TYPES
        self.regular_season_games = None
        self.excluded_players = None
        self.excluded_player_stats = None

        self.rounder = SalaryRounder()

        #
        self.debug_srid = debug_srid

    def update_progress(self, msg):
        time_format = '%I:%M %p'
        est_tz = pytz_timezone('America/New_York')
        time_str = timezone.now().astimezone(est_tz).strftime(time_format)
        progress_prefix = '[%s] %s (salary generation)' % (time_str, self.site_sport.name.upper())
        s = '%s: %s' % (progress_prefix, msg)
        logger.info(s)
        if self.slack is not None:
            self.slack.send(s)

    def generate_salaries(self):
        """
        Generates the salaries for the player_stats_players
        :return:
        """

        start = timezone.now()
        self.update_progress('started')

        #
        # get the regular season games, and all the players
        game_class = self.site_sport_manager.get_game_class(self.site_sport)
        self.regular_season_games = game_class.objects.filter(
            season__season_type__in=self.season_types)

        players = self.helper_get_player_stats(trailing_games=self.salary_conf.trailing_games)
        # self.excluded_players = self.get_salary_player_stats_objects(self.excluded_player_stats)

        #
        # Get the average score per position so we know
        # which positions should have more value
        self.update_progress('calculating positional averages for players: %s' % players)
        position_average_list = self.helper_get_average_score_per_position(players)

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
        self.update_progress('updating (%s) players' % len(players))
        self.helper_update_salaries(players, position_average_list, sum_average_points)

        # apply hardcoded minimum salaries.
        # this method must be run AFTER salaries are complete, and the final rounding has been done.
        # it ALSO must be run BEFORE update_unadjusted_salaries() !
        self.update_position_minimum_salaries(self.pool)

        #
        # Save this original salary into the 'amount_unadjusted' field to be able to reset.
        self.update_unadjusted_salaries(self.pool)

        self.update_progress('finished. (%s seconds)' %
                             str((timezone.now() - start).total_seconds()))

    def update_position_minimum_salaries(self, pool):
        """
        overrides to 'min_player_salary' for specific RosterSpot(s)

        this should only be used to raise the minimum for specific positions.
        the salary amount set in the SalaryConfig.min_player_salary should be the lowest for the
        sport and will be used for any specific spots we dont specifically code in this method.

        :param pool:
        :return:
        """

        for salary in Salary.objects.filter(pool=pool):
            # print('pos min override check: %s' % str(salary))
            sport = self.pool.site_sport.name
            if sport == 'nfl':
                qb = 5000.0
                if salary.primary_roster.name == 'QB' and salary.amount < qb:
                    logger.info('Setting QB to minimun salary of %s - %s' % (qb, salary))
                    salary.amount = qb
                    salary.save()
                    #     print('   *changed %s' % str(salary))
                    # else:
                    #     print('    unchanged %s' % str(salary))

            elif sport == 'nba':
                pass
            elif sport == 'nhl':
                pass
            elif sport == 'mlb':
                pass
            else:
                pass

    def helper_get_player_stats(self, trailing_games=None):
        logger.info('helper_get_player_stats() trailing_games: %s | player_stats_classes: %s' % (
            trailing_games, self.player_stats_classes))
        """
        For each player in the PlayerStats table, get the games
        that are relevant.

        :return a list of SalaryPlayerObjects

        """

        logger.info(
            'regular_season_games: %s' % len(self.regular_season_games))

        #
        players = []
        # excluded_players = []
        for player_stats_class in self.player_stats_classes:
            reg_season_game_pks = [g.pk for g in self.regular_season_games]

            # #
            # # iterate through all player_stats ever
            # reg_season_game_pks = []
            # if trailing_days is None:
            #     # get them all
            #     reg_season_game_pks = [ g.pk for g in self.regular_season_games ]
            # else:
            #     # only get the games within the trailing number of days
            #     cutoff = timezone.now() - timedelta(days=trailing_days)
            #     for reg_game in self.regular_season_games:
            #         if reg_game.start >= cutoff:
            #             reg_season_game_pks.append( reg_game.pk )

            # this statement will get the relevant games by ignoring games where
            # the players fantasy_points were 0.0, but for MLB and NHL we
            # do something more specific...
            # print('reg_season_game_pks count: ', len(reg_season_game_pks))
            all_player_stats = player_stats_class.objects.filter(game_id__in=reg_season_game_pks)
            # print('all_player_stats', all_player_stats)
            # excluded_players = []
            if SiteSportManager.MLB in self.site_sport.name:
                class_name = player_stats_class().__class__.__name__.lower()

                if 'hitter' in class_name:
                    # for MLB HITTERS, filter on only player stats where At Bats > 0
                    all_player_stats = all_player_stats.filter(ab__gt=0)
                    # excluded_players.extend(player_stats_class.objects.filter(ab__lte=0))

                elif 'pitcher' in class_name:
                    # for MLB PITCHERS, ...
                    all_player_stats = all_player_stats.filter(ip_1__gt=0)
                    # excluded_players.extend(player_stats_class.objects.filter(ip_1__lte=0))

                    # a special fix for mlb pitchers, who only play about 1 out of every 5 games
                    trailing_games = int(trailing_games / 5)

                else:
                    err_msg = 'SalaryGenerator() - Unknown MLB PlayerStats type: %s' % str(
                        class_name)
                    raise Exception(err_msg)

            elif SiteSportManager.NHL in self.site_sport.name:
                # for NHL, get all of the playersStats objects we have
                # who participated in the game. Not all sports have 'played' property,
                # which is why NHL is a special case.
                all_player_stats = all_player_stats.filter(played=1)

            else:
                # default
                all_player_stats = all_player_stats.filter(fantasy_points__gt=0)
                # excluded_players.extend(player_stats_class.objects.filter(fantasy_points__lte=0))

            # using the PlayerStats objects, build a list of the SalaryPlayerStats objects
            # which have lists of their trailing performances in them and will be useful further on
            players.extend(self.get_salary_player_stats_objects(
                all_player_stats, trailing_games=trailing_games))

        # this will exclude a set of players from receiving a salary in
        # the algorithm -- that being the set of players who have
        # not played, or who have played but have 0.0 fantasy points.
        # lets store those players and give them a minimum salary later on.
        # self.excluded_player_stats = excluded_players

        logger.info("helper_get_player_stats() # of players: %s" % len(players))
        return players

    def update_unadjusted_salaries(self, pool):
        """
        set the Salary objects 'amount' into the amount_unadjusted field
        for all players passed in via 'players' param

        :param pool:
        :return:
        """
        for sal_obj in Salary.objects.filter(pool=pool):
            sal_obj.amount_unadjusted = sal_obj.amount
            sal_obj.save()

    def helper_get_average_score_per_position(self, players):
        logger.info('helper_get_average_score_per_position() - players: %s' % players)
        if len(players) == 0:
            logger.warn('No players were provided to helper_get_average_score_per_position()')

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
                            {player_stats.position: position_points_obj}
                        )
                    else:
                        position_points_obj = position_average_list[player_stats.position]

                    #
                    # adds the points the SalaryPositionPointsAverageObject for
                    # the given position and updates the count to create the
                    # average later
                    position_points_obj.total_points += player_stats.fantasy_points
                    position_points_obj.count += 1

        for key in position_average_list:
            position_average_list[key].update_average()
            # print("\n"+str(position_average_list[key]))
        return position_average_list

    def helper_trim_players_stats(self, players):
        #
        # Sort the lists by newest game first and trim the array to
        # include  self.salary_conf.trailing_games
        for player in players:
            arrToSort = player.player_stats_list
            arrToSort.sort(key=lambda x: x.start, reverse=True)
            # del arrToSort[self.salary_conf.trailing_games : ]
            player_stats_specific_trailing_games = arrToSort[
                0].get_trailing_games(self.salary_conf.trailing_games)
            del arrToSort[player_stats_specific_trailing_games:]

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
                # print('less than the required games: %s for %s' % (str(number_of_games), str(player)))
                # if player has played in 0 thru the min_games_flag,
                # dont use weights, and just average the points they do have and flag them.
                if number_of_games > 0:
                    fp_list = [stat.fantasy_points for stat in player.player_stats_list]
                    player.fantasy_weighted_average = mean(fp_list)
                # flag them regardless
                player.flagged = True

            # else: if more than the min-required-games-played have been played
            else:
                logger.debug('MET required games: %s for %s' % (number_of_games, player))
                # check to makes sure the most recent game played has been less than
                # days_since_last_game_flag days ago
                delta = timezone.now() - player.player_stats_list[0].start
                if delta.days > self.salary_conf.days_since_last_game_flag:
                    logger.debug(
                        'days since last game: %s -- last game %s' % (
                            delta.days, player.player_stats_list[0].start))
                    player.flagged = True

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

        # get all the roster spots for the sport and sum up the average
        # fantasy points for each spot * spot.amount
        roster_spots = RosterSpot.objects.filter(site_sport=self.site_sport)
        sum_average_points = 0.0
        logger.info("roster_spots: %s" % roster_spots)
        logger.info("position_average_list: %s" % position_average_list)
        for roster_spot in roster_spots:
            logger.info(
                'finding the positions that map to the specified roster spot: %s' % roster_spot)
            #
            # find the positions that map to the specified roster spot and average the
            # average fantasy points for the position from the position_average_list
            roster_maps = RosterSpotPosition.objects.filter(roster_spot=roster_spot)
            count = 0
            sum = 0.0
            msg = 'roster_maps: %s for %s' % (str(len(roster_maps)), str(roster_spot))
            logger.info(msg)
            for roster_map in roster_maps:
                position = roster_map.position
                logger.info('position: %s' % position)
                if position in position_average_list:
                    sum += position_average_list[position].average
                    count += 1
            try:
                sum_average_points += ((sum / ((float)(count))) * ((float)(roster_spot.amount)))
            except ZeroDivisionError:
                logger.error('repeated NoPlayersAtRosterSpotExceptions could indicate you '
                      'have set the "Min FPPG Allowed for Avg Calc too high !!!!')
                raise NoPlayersAtRosterSpotException(msg)

        return sum_average_points

    @atomic
    def helper_update_salaries(self, players, position_average_list, sum_average_points):
        """
        calculates the amount of salary that should be spent on each RosterSpot
        that IS primary position.

        :param players:
        :param position_average_list:
        :param sum_average_points:
        :return:
        """

        # We don't want to reset everyone to the minimum, so this is disabled.

        # initialize the salaries by setting everyone to the minimum
        # min_salary = self.salary_conf.min_player_salary
        # Salary.objects.filter(pool=self.pool, amount__lt=min_salary).update(amount=min_salary)
        # count = 0
        # for sal_obj in Salary.objects.filter(pool=self.pool, salary_locked=False):
        #     old_sal = sal_obj.amount
        #     sal_obj.amount = min_salary
        #     sal_obj.save()
        #     sal_obj.refresh_from_db()
        # print('old:', str(old_sal), 'now:', str(sal_obj.amount), 'player:',str(sal_obj.player))

        printed_players = []
        roster_spots = RosterSpot.objects.filter(site_sport=self.site_sport)
        for roster_spot in roster_spots:
            #
            # creates a list of the primary positions for the roster spot
            roster_maps = RosterSpotPosition.objects.filter(
                roster_spot=roster_spot, is_primary=True)
            #
            # If the query returns any roster maps it means that the roster spot
            # is a primary spot for one or more positions.
            if len(roster_maps) > 0:

                #
                # create the average salary for the roster spot based off the
                # the average points percentage of total points for each roster
                # spot multiplied by the max_team_salary
                pos_arr = []
                count = 0
                sum = 0.0
                for roster_map in roster_maps:
                    pos_arr.append(roster_map.position)
                    if roster_map.position in position_average_list:
                        sum += position_average_list[roster_map.position].average
                        count += 1

                average_salary = (((sum / ((float)(count))) / sum_average_points)
                                  * ((float)(self.salary_conf.max_team_salary)))
                average_salary = self.__round_salary(average_salary)
                # print( roster_spot.name+" average salary "+ str(average_salary))

                #
                # Get the average weighted fantasy points for the specific positions
                # in the pos_arr
                count = 0
                sum = 0.0
                average_weighted_fantasy_points_for_pos = 0.0
                for player in players:
                    if player.player_stats_list[0].position in pos_arr:
                        if player.get_fantasy_average() >= self.salary_conf.min_avg_fppg_allowed_for_avg_calc:
                            sum += player.fantasy_weighted_average
                            count += 1
                if count > 0:
                    average_weighted_fantasy_points_for_pos = (sum / ((float)(count)))
                    # print(average_weighted_fantasy_points_for_pos)

                #
                # creates the salary for each player in the specified roster spot
                for player in players:

                    # debug print this player once if their srid is specified by 'debug_srid'
                    if player.player.srid == self.debug_srid and player.player.srid not in printed_players:
                        msg = str(player.player) + '\n'
                        msg += str(player)
                        logger.info(msg)
                        self.update_progress(msg)  # send webhook with the same info
                        # keep track so we dont double-send
                        printed_players.append(player.player.srid)

                    if player.player_stats_list[0].position in pos_arr:
                        salary = self.get_salary_for_player(player.player)

                        # If the player's salary is locked, exit out of this loop iteration and
                        # don't update the salary amount.
                        if salary.salary_locked:
                            logger.info('Player salary is locked, not updating. %s' % player)
                            continue

                        if average_weighted_fantasy_points_for_pos == 0.0:
                            salary.amount = self.salary_conf.min_player_salary
                        else:
                            salary.amount = (
                                (player.fantasy_weighted_average /
                                 average_weighted_fantasy_points_for_pos) * average_salary)

                        salary.amount = self.__round_salary(salary.amount)
                        if salary.amount < self.salary_conf.min_player_salary:
                            salary.amount = self.salary_conf.min_player_salary
                            logger.info(
                                "Player %s's salary is below the minimum of %s" % (
                                    player, self.salary_conf.min_player_salary))
                            # # this if statement can be hardcoded to override
                            # # the 'min_player_salary' per sport&position
                            # sport = self.pool.site_sport.name
                            # if sport == 'nfl':
                            #     if salary.primary_roster.name == 'QB':
                            #         salary.amount = 6000.0
                            #
                            # elif sport == 'nba':
                            #     pass
                            # elif sport == 'nhl':
                            #     pass
                            # elif sport == 'mlb':
                            #     pass
                            # else:
                            #     pass

                        salary.flagged = player.flagged
                        salary.pool = self.pool
                        salary.player = player.player
                        salary.primary_roster = roster_spot

                        salary.fppg = player.get_fantasy_average()

                        salary.fppg_pos_weighted = player.fantasy_weighted_average
                        if salary.fppg_pos_weighted is None:
                            salary.fppg_pos_weighted = 0.0

                        salary.avg_fppg_for_position = average_weighted_fantasy_points_for_pos

                        salary.num_games_included = len(player.player_stats_list)

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
            salary_obj = Salary.objects.get(
                pool=self.pool, player_type=player_type, player_id=player.id)

            return salary_obj
        except Salary.DoesNotExist:
            logger.info('Player has no Salary, creating one. %s' % player)
            # If a player has no Salary, create one.
            player_type = ContentType.objects.get_for_model(player)
            return Salary(pool=self.pool, player_type=player_type, player_id=player.id)

    def __round_salary(self, val):
        # return (int) (ceil((val/SalaryGenerator.ROUND_TO_NEAREST)) *
        # SalaryGenerator.ROUND_TO_NEAREST)
        return self.rounder.round(val)


class SalaryGeneratorFromProjections(SalaryGenerator):
    """
    if you have existing projections, and would like to salary players
    using the same general process, use this class.
    """

    # disable the type checking done against the type() of player_stats_projections
    type_checking_enabled = False

    def __init__(self, player_projections, *args, **kwargs):
        """

        :param player_projections: a list of objects which must have the properties: .player and .fantasy_points
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

        # list of "spoofed" PlayerStats objects, where fantasy_points property is the projection!
        self.player_projections = player_projections

        # set along the way in generate_salaries()
        self.players = None
        self.position_average_list = None
        self.sum_average_points = None

    def generate_salaries(self):
        """
        Generates the salaries for the player_stats_players
        :return:
        """

        start = timezone.now()
        self.update_progress('started')

        # This method creates a SalaryPlayerObject for each player that contains our calculated
        # stats.com FP projections as well as their DK+FD projections.
        self.players = self.helper_get_player_stats()
        logger.info('generate_salaries() for %s players' % len(self.players))

        # Get the average score per position so we know which positions should have more value
        self.update_progress('calculating positional averages')
        self.position_average_data = self.helper_get_average_score_per_position(self.players)

        # # we dont need to trim, because we know we have 1 projected fantasy_points per player
        # self.helper_trim_players_stats(self.players)

        # apply weights to each score to come up with the
        # average weighted score for each player
        self.helper_apply_weight_and_flag(self.players)

        self.sum_average_points = self.helper_sum_average_points_per_roster_spot(
            self.position_average_data)

        # Calculate the salaries for each player based on
        # the mean of weighted score of their position
        self.update_progress('updating (%s) players' % len(self.players))
        self.helper_update_salaries(
            self.players, self.position_average_data, self.sum_average_points)

        # apply hardcoded minimum salaries.
        # this method must be run AFTER salaries are complete, and the final rounding has been done.
        # it ALSO must be run BEFORE update_unadjusted_salaries() !

        # We don't want to do this... we want the previous salary to be sticky, and if we don't get
        # any projections from stats.com, just keep the player's last one
        # self.update_position_minimum_salaries(self.pool)

        # Save this original salary into the 'amount_unadjusted' field to be able to reset
        self.update_unadjusted_salaries(self.pool)

        self.update_progress('finished. (%s seconds)' %
                             str((timezone.now() - start).total_seconds()))

    def helper_get_player_stats(self):
        """
        override method in order to return a custom list,
        where we use the projection instead of the calculated fppg
        but we still return a list of SalaryPlayerObject(s)

        this method updates the players actual DK & FD salary in the salarys player model if
        possible!

        returns a list of SalaryPlayerObject objects

        note: each SalaryPlayerObject has .player_stats_list which is a list of
        SalaryPlayerStatsObject, which is basically a wrapper for a
        sports.<sport>.models.PlayerStats model!
        """
        salary_player_stats = []
        for player_projection in self.player_projections:
            # get the sports.<sport>.models.Player model instance, and the fantasy_points (float)
            player = player_projection.player
            fantasy_points = player_projection.fantasy_points

            # create SalaryPlayerStatsProjectionObject
            sal_dk = player_projection.sal_dk
            sal_fd = player_projection.sal_fd
            player_stats_object = SalaryPlayerStatsProjectionObject(player, fantasy_points,
                                                                    sal_dk=sal_dk, sal_fd=sal_fd)

            # create a SalaryPlayerObject for each player
            player = SalaryPlayerObject(max_games=1)  # 1 because we are going to set the projection
            player.player_id = player_stats_object.player_id
            player.player = player_stats_object.player
            # SalaryPlayerObject has an internal list of 1 SalaryPlayerStatsProjectionObject,
            # and that SalaryPlayerStatsProjectionObject has the actual DK + FD salary.
            player.player_stats_list.append(player_stats_object)

            # add it to the return list
            salary_player_stats.append(player)

        # return the list weve built
        return salary_player_stats

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
            player.get_fantasy_average()
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
                            {player_stats.position: position_points_obj}
                        )
                    else:
                        position_points_obj = position_average_list[player_stats.position]

                    #
                    # adds the points the SalaryPositionPointsAverageObject for
                    # the given position and updates the count to create the
                    # average later
                    position_points_obj.total_points += player_stats.fantasy_points
                    position_points_obj.count += 1

        for key in position_average_list:
            position_average_list[key].update_average()
            logger.info("\n %s" % position_average_list[key])
        return position_average_list

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
                # print('less than the required games: %s for %s' % (str(number_of_games), str(player)))
                # if player has played in 0 thru the min_games_flag,
                # dont use weights, and just average the points they do have and flag them.
                if number_of_games > 0:
                    fp_list = [stat.fantasy_points for stat in player.player_stats_list]
                    player.fantasy_weighted_average = mean(fp_list)
                # flag them regardless
                player.flagged = True

            # else: if more than the min-required-games-played have been played
            else:
                # print('MET required games: %s for %s' % (str(number_of_games), str(player)))
                # check to makes sure the most recent game played has been less than
                # days_since_last_game_flag days ago
                delta = timezone.now() - player.player_stats_list[0].start
                if delta.days > self.salary_conf.days_since_last_game_flag:
                    # print('days since last game: %s -- last game %s' % (str(delta.days), str(player.player_stats_list[0].start)))
                    player.flagged = True

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

        # get all the roster spots for the sport and sum up the average
        # fantasy points for each spot * spot.amount
        roster_spots = RosterSpot.objects.filter(site_sport=self.site_sport)
        sum_average_points = 0.0
        for roster_spot in roster_spots:
            #
            # find the positions that map to the specified roster spot and average the
            # average fantasy points for the position from the position_average_list
            roster_maps = RosterSpotPosition.objects.filter(roster_spot=roster_spot)
            count = 0
            sum = 0.0
            msg = 'roster_maps:%s for %s' % (str(len(roster_maps)), str(roster_spot))
            for roster_map in roster_maps:
                position = roster_map.position
                if position in position_average_list:
                    sum += position_average_list[position].average
                    count += 1
            try:
                sum_average_points += ((sum / ((float)(count))) * ((float)(roster_spot.amount)))
            except ZeroDivisionError:
                logger.error('repeated NoPlayersAtRosterSpotExceptions could indicate you '
                      'have set the "Min FPPG Allowed for Avg Calc too high !!!!')
                raise NoPlayersAtRosterSpotException(msg)

        return sum_average_points

    @atomic
    def helper_update_salaries(self, players, position_average_list, sum_average_points):
        """
        Helper method in charge of creating salary entries for players for the pool
        passed to this class. This method will update existing entries for players
        that already exist. THis method should *not* be called outside of this
        class.

        the 'players' param is a list of SalaryPlayerObjects each of which
        has an internal list of 1 SalaryPlayerStatsProjectionObject which contains
        the projection, and site specific actual salaries (useful for displaying in admin).

        this method also wipes all existing site specific actual salaries (DK, FD, ...) to None
        with the expectation that they are about to be updated (and we dont want stale values lingering).

        :param players:
        :param position_average_list:
        :param sum_average_points:
        :return:
        """

        all_pool_salaries = Salary.objects.filter(pool=self.pool)
        # This used to set ALL players to the minimum before updating them. we don't want this
        # because we want the previous salary to be sticky, this prevents players from getitng reset
        # to minimum just because stats.com thinks they won't play or something like that.
        # Salary.objects.filter(pool=self.pool, amount__lt=min_salary).update(amount=min_salary)
        # count = 0
        logger.info("Resetting %s DK+FD salary projections to None" % len(all_pool_salaries))
        for sal_obj in all_pool_salaries:
            # zero out existing site actual salaries
            sal_obj.sal_dk = None
            sal_obj.sal_fd = None
            sal_obj.save()
            sal_obj.refresh_from_db()

        printed_players = []
        roster_spots = RosterSpot.objects.filter(site_sport=self.site_sport)
        for roster_spot in roster_spots:
            #
            # creates a list of the primary positions for the roster spot
            roster_maps = RosterSpotPosition.objects.filter(roster_spot=roster_spot,
                                                            is_primary=True)
            #
            # If the query returns any roster maps it means that the roster spot
            # is a primary spot for one or more positions.
            if len(roster_maps) > 0:

                #
                # create the average salary for the roster spot based off the
                # the average points percentage of total points for each roster
                # spot multiplied by the max_team_salary
                pos_arr = []
                count = 0
                sum = 0.0
                for roster_map in roster_maps:
                    pos_arr.append(roster_map.position)
                    if roster_map.position in position_average_list:
                        sum += position_average_list[roster_map.position].average
                        count += 1

                average_salary = (((sum / ((float)(count))) / sum_average_points)
                                  * ((float)(self.salary_conf.max_team_salary)))
                average_salary = self.__round_salary(average_salary)
                logger.info(roster_spot.name + " average salary " + str(average_salary))

                #
                # Get the average weighted fantasy points for the specific positions
                # in the pos_arr
                count = 0
                sum = 0.0
                average_weighted_fantasy_points_for_pos = 0.0
                for player in players:
                    if player.player_stats_list[0].position in pos_arr:
                        if player.get_fantasy_average() >= self.salary_conf.min_avg_fppg_allowed_for_avg_calc:
                            sum += player.fantasy_weighted_average
                            count += 1
                if count > 0:
                    average_weighted_fantasy_points_for_pos = (sum / ((float)(count)))
                    # print(average_weighted_fantasy_points_for_pos)

                #
                # creates the salary for each player in the specified roster spot
                for player in players:
                    # debug print this player once if their srid is specified by 'debug_srid'
                    if player.player.srid == self.debug_srid and player.player.srid not in printed_players:
                        msg = str(player.player) + '\n'
                        msg += str(player)
                        # print(msg)
                        self.update_progress(msg)  # send webhook with the same info
                        # keep track so we dont double-send
                        printed_players.append(player.player.srid)

                    # look in each SalaryPlayerObject's list for the only
                    # SalaryPlayerStatsProjectionObject and extract the projection + actual salary
                    # information
                    if player.player_stats_list[0].position in pos_arr:
                        salary = self.get_salary_for_player(player.player)

                        # retrieve the DK + FD actual salaries for this players
                        # SalaryPlayerStatsProjectionObject
                        proj_obj = player.player_stats_list[0]
                        sal_dk = proj_obj.sal_dk
                        sal_fd = proj_obj.sal_fd
                        salary.sal_dk = sal_dk
                        salary.sal_fd = sal_fd
                        salary.save()

                        # If the player's salary is locked, exit out of this loop iteration and
                        # don't update the salary amount - still save dk+fd updates though.
                        if salary.salary_locked:
                            logger.info(
                                'Player salary is locked, not updating (only dk+fd projections '
                                'changed). %s' % player)
                            continue

                        # Update various salary attributes.
                        salary.flagged = player.flagged
                        salary.pool = self.pool
                        salary.player = player.player
                        salary.primary_roster = roster_spot
                        salary.fppg = player.get_fantasy_average()
                        salary.fppg_pos_weighted = player.fantasy_weighted_average

                        if salary.fppg_pos_weighted is None:
                            salary.fppg_pos_weighted = 0.0

                        salary.avg_fppg_for_position = average_weighted_fantasy_points_for_pos
                        salary.num_games_included = len(player.player_stats_list)

                        # Only update the player's salary if we DON'T have a 0 fpp projection
                        # from stats.com. This will make previous salaries 'sticky'. This is done
                        # so that if stats thinks a player isn't starting, their salary doesn't
                        # get set to the minimum.
                        if salary.fppg > 0:
                            # Add random salary adjustments.
                            # We can't divide by 0, so if it is 0, So ignore adjustments if it is.
                            if average_weighted_fantasy_points_for_pos > 0.0:
                                salary.amount = (
                                    (player.fantasy_weighted_average /
                                        average_weighted_fantasy_points_for_pos) * average_salary)

                            salary.amount = self.__round_salary(salary.amount)

                            # DISABLE RANDOM AMOUNT ADJUSTMENT

                            # apply randomization, if pool.random_percent_adjust is non-zero
                            # if self.pool.random_percent_adjust != 0.0:
                            #     r_pct = self.pool.random_percent_adjust
                            #     #
                            #     decimal_places = 1000000
                            #     r = Random()
                            #     # divide by 100, because its entered as 1.75 for 1.75% on the admin
                            #     plus_minus = int(r_pct * decimal_places) / 100
                            #     random_pct = r.randrange(plus_minus * -1,
                            #                              plus_minus) / decimal_places
                            #     # its + or -, but truncate decimals
                            #     random_amount = float(int(salary.amount * random_pct))
                            #     salary.random_adjust_amount = random_amount
                            #     logger.info("Applying random_adjust %s to %s" % (
                            #         random_amount, player))
                            #     salary.amount += salary.random_adjust_amount

                        # If stats says they aren't playing. Leave their salary as-is and exit.
                        else:
                            logger.warning(
                                ('Skipping salary update because stats.com gave us 0 fpp. '
                                 'Salary: %s Projection: %s') % (salary, player)
                            )
                            continue

                        # If the player's salary is less than the minimum, set them to the min.
                        if salary.amount < self.salary_conf.min_player_salary:
                            logger.info(('player was below the min_player_salary'
                                         ', setting to minimum. player: %s  '
                                         'salary: %s') % (player, salary))
                            salary.amount = self.salary_conf.min_player_salary

                        logger.info('setting salary to %s for player: %s' % (salary.amount, player))
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
            logger.info('Player has no Salary, creating one. %s' % player)
            # If a player has no Salary, create one.
            player_type = ContentType.objects.get_for_model(player)
            return Salary(pool=self.pool, player_type=player_type, player_id=player.id)

    def __round_salary(self, val):
        # return (int) (ceil((val/SalaryGenerator.ROUND_TO_NEAREST)) *
        # SalaryGenerator.ROUND_TO_NEAREST)
        return self.rounder.round(val)


class SportSalaryGenerator(SalaryGenerator):
    """
    This class is a wrapper for SalaryGenerator which requires only the sport name to run salaries
    """

    def __init__(self, sport, debug_srid=None):
        """
        given the sport name (ie: 'nfl', 'nba', etc...) run salary generation for the active salary pool

        :param slack_updates: (bool) can be set to enable slack webhooks tracking progress
        """
        ssm = SiteSportManager()
        site_sport = ssm.get_site_sport(sport)
        player_stats_classes = ssm.get_player_stats_classes(site_sport)
        pool = Pool.objects.get(site_sport=site_sport, active=True)
        super().__init__(player_stats_classes, pool, season_types=None, slack_updates=True,
                         debug_srid=debug_srid)


class PlayerFppgGenerator(FppgGenerator):
    """
    Generates regular season "fantasy points per game" for players for a sport.

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
            self.update_sport(sport)

    def update_sport(self, sport):
        """
        update the player fppgs for the sports current season found in SiteSport

        :param sport:
        :return:
        """
        site_sport = self.site_sport_manager.get_site_sport(sport)
        # get the regular season game srids
        season = Season.factory(sport)  # makes a connection to mongolab directly
        game_srids = season.get_game_ids_regular_season(site_sport.current_season)

        # get all the players for the sport
        player_class = self.site_sport_manager.get_player_class(site_sport)
        player_objects = player_class.objects.all()
        # get playerstats classes (there may be multiple)
        player_stats_classes = self.site_sport_manager.get_player_stats_class(site_sport)

        #
        # sports with multiple PlayerStats classes require us to handle
        # the fppg calcs differently, ie: break up pitchers and hitters
        # print('updating season_fppg - sport:', sport)
        # print('... %s player_stats_classses -> %s' % (str(len(player_stats_classes)), str(player_stats_classes)))
        if len(player_stats_classes) == 1:
            #
            # sports like nfl, nhl, nba only have a single PlayerStats model
            self.get_fppg(player_objects, player_stats_classes[0], game_srids)

        #
        # mlb, for example, has 2 stats models, PlayerStatsPitcher, PlayerStatsHitter
        elif len(player_stats_classes) >= 2 and sport == 'mlb':
            #
            # get players that are SP, P, or RP, and the PlayerStatsPitcher class
            q_pitcher_positions = Q(position__name__in=['P', 'SP', 'RP'])
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
        player_ids = [p.id for p in player_objects]
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

    columns = ['id', 'last_name', 'first_name', 'price_draftboard', 'position',
               'fppg', 'avg_fppg_for_position', 'num_games_included', 'sal_dk', 'sal_fd', 'team',
               'alias', 'status', 'is_on_active_roster']

    def __init__(self, salary_pool_id, httpresponse=None):
        self.httpresponse = httpresponse  # set streaming to True when returning this csv in an http response
        self.pool = Pool.objects.get(pk=salary_pool_id)
        self.salaries = Salary.objects.filter(pool=self.pool).order_by('-amount')
        self.csvfile = None

    def __writerow(self, writer, salary):

        # hack to make FBs show up as RBs in the csv for readability.
        position_name = salary.player.position.name
        if position_name == 'FB' and self.pool.site_sport.name == 'nfl':
            position_name = 'RB'

        writer.writerow([
            salary.player.pk,  # 'id'
            salary.player.last_name,  # 'last_name'
            salary.player.first_name,  # 'first_name'
            salary.amount,  # 'price_draftboard'
            position_name,  # 'position'
            salary.fppg,
            salary.avg_fppg_for_position,
            salary.num_games_included,

            # new: include actual site salaries for major sites.
            salary.sal_dk,
            salary.sal_fd,

            salary.player.team.name,
            salary.player.team.alias,

            salary.player.status,
            salary.player.on_active_roster
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
            writer = csv.writer(f)
        else:
            writer = csv.writer(self.httpresponse)

        writer.writerow(self.columns)
        for salary in self.salaries:
            self.__writerow(writer, salary)

        if f is not None:
            # close the file if we used an actual file
            f.close()
