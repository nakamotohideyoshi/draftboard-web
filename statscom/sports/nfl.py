import csv
from logging import getLogger

import pytz

from scoring.models import StatPoint
from statscom.classes import FantasyProjections, ProjectionsWeekWebhook
from statscom.constants import STATPOINT_TO_STATSCOM_NFL
from statscom.player import get_fantasy_point_projection_from_stats_projection

logger = getLogger('statscom.sports.nfl')
# For all scheduling purposes, EST is assumed
tz = pytz.timezone('America/New_York')


class PlayerProjectionNFL(object):
    """ data parser/wrapper class for offensive nfl player projections """

    # misc fields for this object including player and game information,
    # as well as a list of site specific projected fantasy point totals
    fields_misc = [
        'team',
        'player',
        'position',
        'opponent',
        'eventId',
        'gameDate',

        # list of site specific projections, ie: DK, FD, etc...
        'fantasyProjections',
    ]

    # fantasy scoring categories which that are projected
    # fields_categories = [
    #     'rushYards',
    #     'passYards',
    #     'completions',
    #     'attempts',
    #     'chance100RushYards',
    #     'fumblesLost',
    #     'rushTouchdowns',
    #     'twoPointConversions',
    #     'chance300PassYards',
    #     'rushes',
    #     'passTouchdowns',
    #     'interceptions',
    # ]
    fields_categories = ['completions', 'fieldGoalsMade', 'passTouchdowns', 'extraPointsAttempted',
                         'receptionTouchdowns', 'passYards', 'receptions', 'fieldGoalsMade29',
                         'fieldGoalsMade49',
                         'chance100RushYards', 'fieldGoalsMade19', 'fumblesLost',
                         'twoPointConversions',
                         'fieldGoalsMade39', 'interceptions', 'chance100ReceptionYards',
                         'chance300PassYards',
                         'extraPointsMade', 'fieldGoalsAttempted', 'fieldGoalsMade50',
                         'receptionYards', 'rushes',
                         'rushYards', 'rushTouchdowns', 'attempts']

    def __init__(self, data):
        self.data = data


class FantasyProjectionsNFL(FantasyProjections):
    endpoint_current_weekly_projections = '/stats/football/nfl/fantasyProjections/weekly/'
    # append week number
    endpoint_weekly_projections = '/stats/football/nfl/fantasyProjections/weekly/'
    stat_map = STATPOINT_TO_STATSCOM_NFL

    field_offensive_projections = 'offensiveProjections'
    field_defensive_projections = 'defensiveProjections'
    field_week = 'week'
    field_fantasy_projections = 'fantasyProjections'
    field_position = 'position'

    field_points = 'points'
    field_salary = 'salary'

    field_player = 'player'
    field_first_name = 'firstName'
    field_last_name = 'lastName'
    field_player_id = 'playerId'

    def __init__(self):
        super().__init__('nfl')
        # this instance lets us get player data by players' stats.com id

        self.scoring_system_stat_points = StatPoint.objects.filter(score_system__sport='nfl')
        logger.info('Using scoring system: %s' % self.scoring_system_stat_points)
        logger.info('Using statpoint map: %s' % self.stat_map)

    def get_projections(self, week=None):
        """
        get the projections for the current week.

        returns a dict with fields in:

            ['offensiveProjections', 'week', 'defensiveProjections']

        if a week number is specified, this will return the projections for that
        week (for current season)
        """
        endpoint = self.endpoint_weekly_projections
        if week is not None:
            endpoint += str(week)
        # return the response data
        return self.api(endpoint)

    def get_player_projections(self, week=None):
        """
        return a list of salary.classes.PlayerProjection object
        for all the offensive players found (skip defensive players)
        """

        data = self.get_projections(week=week)
        # grab the offensive player's stat projections.
        fantasy_projections = data.get(self.field_offensive_projections)
        player_projections = []
        no_lookups = []

        # For each player, add prjoected player stats.
        for player_projection in fantasy_projections:
            # get the players position
            position = player_projection.get(self.field_position)

            # lookup the player in our database by matching the full name
            player_data = player_projection.get(self.field_player)
            pid = player_data.get(self.field_player_id)
            first_name = player_data.get(self.field_first_name)
            last_name = player_data.get(self.field_last_name)

            # look up this third party api player in our own db
            player = self.find_player(first_name, last_name, pid)

            # We don't have the player in our local db.
            if player is None:
                player_string = 'pid[%s] player[%s] position[%s]' % (
                    str(pid), str(first_name + ' ' + last_name), str(position))
                no_lookups.append(player_string)
                err_msg = 'COULD NOT LOOKUP -> %s' % player_string
                logger.warning(err_msg)

            else:
                logger.debug('Player found: %s %s' % (first_name, last_name))
                # Figure out what we think their FP will be based on the projected stats from
                # STATS.com.
                sal_dk = None
                sal_fd = None

                our_projected_fp = get_fantasy_point_projection_from_stats_projection(
                    stat_points=self.scoring_system_stat_points,
                    stats_projections=player_projection,
                    stat_map=self.stat_map
                )
                logger.info('player: %s | calculated FP: %s | stats.com projections: %s' % (
                    player, our_projected_fp, player_projection))

                # iterate the list of sites which we have projections for until we find
                # the one we want
                # fantasy_projections_copy = fantasy_projections.copy()
                site_projections = player_projection.get(self.field_fantasy_projections, [])

                # try to get the sites own salary for the player for the major sites.
                sal_dk = self.get_site_player_salary(site_projections, self.site_dk)
                sal_fd = self.get_site_player_salary(site_projections, self.site_fd)

                # Extract the player's stat projections and append it to a list of projected
                # stats. This is the important part - we use these stats to determine the
                # player's salary.
                projection = self.build_player_projection(
                    player, our_projected_fp, sal_dk=sal_dk, sal_fd=sal_fd)

                player_projections.append(projection)

        # # send slack webhook with the players we couldnt link
        num_players_without_lookup = len(no_lookups)
        if num_players_without_lookup > 0:
            webhook = ProjectionsWeekWebhook()
            webhook.send('check draftboard.com/admin/statscom/playerlookup/ '
                         'and link [%s] players!' % str(num_players_without_lookup))

        return player_projections

    def get_site_player_salary(self, fantasy_projections, site):
        """
        this method should be able to retrieve the site specific
        salary from the list of site projections objects if
        the 'site' param is contained within each site items name property.

        :param fantasy_projections: The projections for the player we've found in the stats.com
                                    response
        :param site: a string, ie: 'draftkings'
        :return: float - the projected salary
        """

        projected_player_salary = None

        for site_proj in fantasy_projections:
            site_fullname = site_proj.get(self.field_name, '')

            if site_fullname is None:
                continue

            if site in site_fullname:
                projected_player_salary = site_proj.get(self.field_salary)
                # break out of loop, in order to return first match
                break

        return projected_player_salary


class NFLPlayerProjectionCsv(PlayerProjectionNFL):  # particularly for NFL i might add...
    """ temp helper class to dump out projections and match up with our own players """

    field_fantasy_projections = 'fantasyProjections'
    field_offensive_projections = 'offensiveProjections'

    field_player = 'player'
    field_player_id = 'playerId'
    field_fullname = 'fullname'  # i made this one. it combines the first+last name
    field_first_name = 'firstName'
    field_last_name = 'lastName'
    field_position = 'position'

    columns_player = [
        field_player_id,
        field_fullname,
        field_first_name,
        field_last_name,
        field_position,
    ]

    field_name = 'name'  # its the name of the site the projection is for
    field_points = 'points'  # the projected fantasy point total

    columns_site = [
        field_name,
        field_points,
    ]

    columns_categories = PlayerProjectionNFL.fields_categories

    # all columns for csv header row
    columns = columns_player + columns_categories + columns_site

    def __init__(self, data):
        self.data = data
        self.all_fields = {}

    def generate(self):
        """
        generate the csv file
        :return:
        """
        filename = 'nfl-projections.csv'
        f = open(filename, 'w', newline='')
        writer = csv.writer(f)

        # write the headers on the first line of csv
        writer.writerow(self.columns)

        # write the rows of data into the csv
        offensive_projections = self.data.get(self.field_offensive_projections)
        for proj in offensive_projections:
            self.writerow(writer, proj)

        logger.info('all possible categories seen:', str(self.all_fields.keys()))

        if f is not None:
            # close the file if we used an actual file
            f.close()

    def add_seen_category(self, cat):
        if cat not in self.fields_misc:
            self.all_fields[cat] = ''

    def writerow(self, writer, proj):
        # proj.keys():
        #     ['opponent', 'twoPointConversions', 'chance300PassYards', 'completions', 'rushYards', 'team',
        #      'chance100RushYards', 'interceptions', 'gameDate', 'attempts', 'passYards', 'passTouchdowns', 'player',
        #      'fantasyProjections', 'rushTouchdowns', 'position', 'fumblesLost', 'rushes', 'eventId'])
        player = proj.get(self.field_player)
        position = proj.get(self.field_position)
        pid = player.get(self.field_player_id)
        # {'firstName': 'Andrew', 'lastName': 'Luck', 'playerId': 461175}
        fn = player.get(self.field_first_name)
        ln = player.get(self.field_last_name)
        fullname = fn + ' ' + ln

        # add the columns_site values
        site_projections = proj.get(self.field_fantasy_projections)
        for site_proj in site_projections:
            # manually add the columns_player values
            # TODO warning: if you change the order of self.columns_player
            #    you ALSO have to change the order of the next line of code!!!
            values = [pid, fullname, fn, ln, position]

            # debug, i want to see all possible projected category names
            for cat in proj.keys():
                self.add_seen_category(cat)

            # add the columns_categories values
            for field in self.columns_categories:
                values.append(proj.get(field))

            # add the columns_site values
            for field in self.columns_site:
                values.append(site_proj.get(field))

            # write this row into the csv
            writer.writerow(values)
