from logging import getLogger

import pytz

from scoring.models import StatPoint
from statscom.classes import (
    FantasyProjections,
    ProjectionsWeekWebhook,
    DailyGamesAbstract,
    StatsPlayer,
    PlayersAbstract)
from statscom.constants import STATPOINT_TO_STATSCOM_MLB
from statscom.player import get_fantasy_point_projection_from_stats_projection

logger = getLogger('statscom.sports.mlb')
# For all scheduling purposes, EST is assumed
tz = pytz.timezone('America/New_York')

"""
TODO: Once Stats.com starts giving us MLB projections, we're going to need to determine the
stats map in `STATPOINT_TO_STATSCOM_MLB`. I think things should work after that, though most of
this code is copied directly from the NBA version, so it may need some tweaking.
"""


class DailyGamesMLB(DailyGamesAbstract):
    endpoint_daily_games = '/stats/baseball/mlb/scores/'

    def __init__(self):
        super().__init__('mlb')


class PlayersMLB(PlayersAbstract):
    endpoint = '/stats/baseball/mlb/participants/'

    def __init__(self):
        super().__init__('mlb')


class FantasyProjectionsMLB(FantasyProjections):
    # the game's eventid must be appended to this endpoint
    endpoint_fantasy_projections = '/stats/baseball/mlb/fantasyProjections/'
    field_fantasy_projections = 'fantasyProjections'
    stat_map = STATPOINT_TO_STATSCOM_MLB

    def __init__(self):
        super().__init__('mlb')

        # this instance lets us get player data by players' stats.com id
        self.players = PlayersMLB()
        self.scoring_system_stat_points = StatPoint.objects.filter(score_system__sport='mlb')
        logger.info('Using scoring system: %s' % self.scoring_system_stat_points)

    def get_projections(self, eventid):
        """
        returns a list of 2 elements. each element is one of the teams in the game, and has these
        keys:

            dict_keys(['teamId', 'pitchers', 'batters'])

        caveat: stats.com only gives a projection for the Probable Pitcher (and starting lineup)
        and it might not be nearly enough coverage for us to generate salaries based on this data.

        :param eventid: the game's id. ex: 1600732
        :return:
        """
        endpoint = self.endpoint_fantasy_projections + str(eventid)
        return self.api(endpoint)

    def get_player_projections(self, event_ids=None):

        if event_ids is None:
            # get the daily event ids
            event_ids = DailyGamesMLB().get_event_ids()
            logger.info('DailyGamesMLB().get_event_ids() -> %s' % event_ids)

        if isinstance(event_ids, int):
            # create a list of the single event id
            event_ids = [event_ids]

        # init the return list
        player_projections = []

        # gets all active players from the api and inits the object
        # so we can call self.players.get_player_for_id(xxx)
        self.players.init_players()

        # initialize the list of players that werent found when we looked them up
        no_lookups = []

        # For each game, get projected player stats. > Based on DK+FD projections.
        for event_id in event_ids:
            player_projection_list, no_lookups_list = self.__get_player_projections(event_id)
            player_projections.extend(player_projection_list)
            no_lookups.extend(no_lookups_list)
            logger.info('player_projections count for event.id %s: %s' % (
                event_id, len(player_projections)))

        log_msg = ''
        for projection in player_projections:
            log_msg += '%s: %s fp points\n' % (projection.player, projection.fantasy_points)

        logger.info(log_msg)

        # send slack webhook with the players we couldnt link
        num_players_without_lookup = len(no_lookups)
        if num_players_without_lookup > 0:
            # just use the NFL webhook to send info to slack
            # comment in/out the next 3 lines back in to enable/disable webhook
            webhook = ProjectionsWeekWebhook()
            webhook.send('[%s] check draftboard.com/admin/statscom/playerlookup/ '
                         'and link [%s] players!' % (
                             self.sport, num_players_without_lookup))

        return player_projections

    def __get_player_projections(self, event_id):
        """
        This will get a player's project FP based on the DK + FD projections.

        returns a tuple of:
            ( <list of salary.classes.PlayerProjection objects>, <list of players not found> )

        :param event_id: a single event_id
        """

        # init the return list
        player_projections = []

        # # gets all active players from the api and inits the object
        # # so we can call self.players.get_player_for_id(xxx)
        # self.players.init_players()

        # initialize the list of players that werent found when we looked them up
        no_lookups = []

        # retrieve the projections for this event
        data = self.get_projections(event_id)
        # data.keys()
        teams = data.get('teams')
        # len(teams)
        # Players are sorted by teams, loop through each team, then loop through each player
        # on that team to extract projections.
        for team in teams:
            team_player_projections = team.get('players')
            for player_projection in team_player_projections:
                logger.debug('===== PLAYER =====')
                # logger.info('   projection: %s' % player_projection)
                # for nba, players do not have names in the projection data!
                # we have to look them up by id using the PlayersNBA instance.

                # get the player data via their id
                pid = player_projection.get(self.field_player_id)
                # player_data is a big dict of data about the player, all we really need this for
                # is to find their name or PID for matching.
                player_data = self.players.get_player_for_id(pid)
                # logger.info('   player_data: %s', player_data )
                if player_data is None:
                    logger.warning(
                        "(skipping player projection) STATS.com playerId [%s] not found in "
                        "Player<SPORT> data! Here's the projection that made us fail: %s" % (
                            pid, player_projection))
                    continue

                # try to get the fantasy projection list (of each site projection)
                fantasy_projections = player_projection.get(self.field_fantasy_projections)
                logger.debug('fantasyProjections (site projections): %s' % fantasy_projections)
                if len(fantasy_projections) == 0:
                    msg = 'No site projections found for field[%s]  player[%s]' % (
                        self.field_fantasy_projections, str(player_data))
                    logger.warning(msg)
                    raise Exception(msg)

                # get an instance of this data class to help extract
                # the values we need to look this player up
                p = StatsPlayer(player_data)
                # get the players position. may raise: NoPositionFound
                position = p.get_position()
                first_name = p.get_first_name()
                last_name = p.get_last_name()

                # look up this third party api player in our own db
                player = self.find_player(first_name, last_name, pid)
                # if player couldn't be found, debug message, and continue loop
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
                    fantasy_projections_copy = fantasy_projections.copy()
                    for site in fantasy_projections:
                        if self.default_site in site.get(self.field_name, '').lower():
                            logger.debug('Site Projection found! %s ' % site)

                            # try to get the sites own salary for the player for the major sites.
                            sal_dk = self.get_site_player_salary(fantasy_projections_copy,
                                                                 self.site_dk)
                            sal_fd = self.get_site_player_salary(fantasy_projections_copy,
                                                                 self.site_fd)
                            break  # is it possible its never found?

                        else:
                            logger.debug('%s not found in %s' % (
                                self.default_site, site.get(self.field_name, '').lower()))

                    # Extract the player's stat projections and append it to a list of projected
                    # stats. This is the important part - we use these stats to determine the
                    # player's salary.
                    player_projections.append(self.build_player_projection(player, our_projected_fp,
                                                                           sal_dk=sal_dk,
                                                                           sal_fd=sal_fd))

        return player_projections, no_lookups
