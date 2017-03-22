from raven.contrib.django.raven_compat.models import client
import time
import hashlib
import json
import requests
import csv
import urllib.parse
import datetime
import pytz
from django.conf import settings
from salary.classes import PlayerProjection
from scoring.models import StatPoint
from .player import get_fantasy_point_projection_from_stats_projection
from .constants import STATPOINT_TO_STATSCOM_NBA
from sports.classes import SiteSportManager
import draftgroup.classes
from statscom.models import (
    PlayerLookup,
)
from util.slack import Webhook
from logging import getLogger

logger = getLogger('statscom.classes')
# For all scheduling purposes, EST is assumed
tz = pytz.timezone('America/New_York')


class ProjectionsWeekWebhook(Webhook):
    # its a piece of the full url from something like this:
    # https://hooks.slack.com/services/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
    identifier = 'T02S3E1FD/B2H8GB97T/gHG66jb3wvGHSJb9Zcr7IwHC'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = 'current-projections-week'


class ApiFailureWebhook(Webhook):
    """
    webhook to send to slack if we get an http status >= 400 from the stats.com api
    """
    identifier = 'T02S3E1FD/B2H8GB97T/gHG66jb3wvGHSJb9Zcr7IwHC'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = 'api-error-response'


class PlayerUpdateManager(draftgroup.classes.PlayerUpdateManager):
    """
    Swish Analytics own class for injecting PlayerUpdate objects into the backend
    particularly so they show up in /api/draft-group/updates/{draft-group-id}/
    """

    # model class for looking up player -> third party id mappings set by admin
    lookup_model_class = PlayerLookup

    # override. update this third party data and enter it as a PlayerUpdate
    def update(self, stats_update):
        # internally calls super().update(player_srid, *args, **kwargs)
        pass


class ResponseDataParser(object):
    """
    most of the response data's outter wrapper is boiler plate.

    this extracts the data we want
    """

    class UnexpectedApiResults(Exception):
        pass

    # boilerplate fields of stats.com api responses
    field_api_results = 'apiResults'
    field_league = 'league'

    # most api calls, result in there being this many items in the "apiResults" list.
    # if we parse an api that has a different number of results, an exception is raised
    default_api_results = 1
    # by default, we will try to get the first item in the "apiResults" list
    default_api_result_index = default_api_results - 1

    # default size of the "eventType" list
    default_event_types = 1
    # by default, try to get the item at this index from "eventType" list
    default_event_type_index = default_event_types - 1

    def __init__(self, data):
        self.data = data

    def get_data(self):
        """
        returns the data objects after stripping off the boiler plate wrapper common to stats.com
        apis.

        note: this method returns inner data from the data, not the data passed in.
        """
        # return self.data
        api_results = self.data.get(self.field_api_results)
        # log error + exit
        if api_results is None:
            err_msg = 'stats.com api error: got %s, expected %s' % (
                self.field_api_results, self.default_api_results)
            logger.error(err_msg)
            raise self.UnexpectedApiResults(err_msg)

        num_results = len(api_results)
        if num_results != self.default_api_results:
            err_msg = 'stats.com api error: got %s %s, expected %s' % (
                num_results, self.field_api_results, self.default_api_results)
            logger.error(err_msg)
            raise self.UnexpectedApiResults(err_msg)
        result = api_results[self.default_api_result_index]
        league = result.get(self.field_league)
        # logger.info('league.keys()', str(league.keys()))
        return league


class Stats(object):
    """
    this class is for calling the STATS.com api and getting back its raw responses as JSON
    """

    class MissingApiKeySettings(Exception):
        pass

    # the amount of seconds to wait to retry if the api rate limited us
    # and gave us an http status 403: "<h1>Developer Over Qps</h1>"
    rate_limit_delay_seconds = 1.0

    # a dictionary, from which we can obtain api credentials
    stats_keys = settings.STATSCOM_KEYS

    # the root url for the api
    url_base = settings.STATSCOM_URL_BASE

    # response format which should be 'json' or 'xml'
    response_format = 'json'

    # field name for credentials in the sport's key data
    field_api_key = 'api_key'
    field_secret = 'secret'

    # response parser class. if this is set, its get_data() method
    # will be used to return the api data.
    # by default, the raw, unmodified JSON is returned.
    parser_class = ResponseDataParser

    # this field of an api response's data can indicate if there is an error
    field_message = 'message'

    def __init__(self, sport):
        self.sport = sport
        self.player_model_class = None
        self.sport_players = None  # set on the first call to self.get_player_model_class()

        # get and validate the api_key and secret token exist for this sport
        self.keys = self.stats_keys.get(self.sport)
        if self.keys is None:
            err_msg = "'%s' missing from settings.STATSCOM_KEYS" % self.sport
            raise self.MissingApiKeySettings(err_msg)

        self.api_key = self.keys.get(self.field_api_key)
        self.secret = self.keys.get(self.field_secret)

        # set up a session object to do the actual http calls
        self.session = requests.Session()
        self.r = None  # we will always save the last response here
        self.data = None

    def get_url_auth_params(self):
        """
        returns a string to concatenate onto the api call for authentication,
        as well as the response format. (format defaults to JSON)
        example: '?api_key=XXXXXXXXXXXX&sig=ALKSJDLKAJSDLKJASDJKLAKSJD&accept=json'
        """
        return '?api_key=%s&sig=%s&accept=%s' % (self.get_api_key(), self.get_sig(), self.response_format)

    def get_api_key(self):
        return self.api_key

    def get_sig(self):
        """
        build and return the 'sig' param which is a sha256 hash
        of the api_key + secret + unix timestamp.
        """
        sig = hashlib.sha256((self.api_key + self.secret +
                              str(int(time.time()))).encode()).hexdigest()
        # logger.info('stats.com api sig=%s' % str(sig))
        return sig

    def get_response_format(self):
        return self.response_format

    def get_url(self, endpoint):
        """
        builds the base of the url, and will append authentication params.

        :param endpoint: string for the api you want to call.
                    example: '/stats/football/nfl/fantasyProjections/weekly/1'
        :return: the complete url you could make the request with
        """
        return self.url_base + endpoint + self.get_url_auth_params()

    def notify_slack_on_http_4xx(self, r):
        """
        sends slack webhook to notify admin that rate limit happened.

        :param r: http response from a requests Session.get() call
        :return:
        """
        # The API 404s for a number of reasons, mainly if there are no games for the day
        # or if the games aren't up yet. It's bad and dumb, but unfortunately we are forced to
        # ignore these.
        if r.status_code == 404:
            logger.warning('404 response from stats.com: %s' % r.url)
        # If we got a a non-404, 400+, log it out and raise an exception.
        # this happens ALL the time, the stats api is really flaky, but it can mostly
        # be safely ignored. A Sumo Logic alert will be setup to make sure that we
        # are getting a succesful update within a certain time period.
        elif r.status_code >= 400:
            w = ApiFailureWebhook()
            err_msg = 'stats.com api gave us an http status code: %s - %s' % (r.status_code, r.text)
            w.send(err_msg)
            logger.warning(err_msg)
            raise Exception(err_msg)

    def api(self, endpoint, format=None, verbose=True, params={}):
        """
        makes the http request and returns the contents as json

        :param endpoint: ie: '/stats/football/nfl/fantasyProjections/weekly/'
        :param format: you can override the format returned. defaults to json.
        :return: the data from the api call
        """
        url = self.get_url(endpoint)
        if params:
            # Add any parameters that were provided.
            url += '&' + urllib.parse.urlencode(params)

        # sleep for a short time before making api request to avoid getting rate limited
        time.sleep(self.rate_limit_delay_seconds)
        self.r = self.session.get(url)
        logger.info('http %s %s' % (str(self.r.status_code), url))

        # check for http >= 400 status code! (bad) and sent note to slack if it happened
        self.notify_slack_on_http_4xx(self.r)

        self.data = json.loads(self.r.text)

        # check if there is an error
        msg = self.data.get(self.field_message)
        if msg:
            logger.error("stats.com api error: %s" % msg)

        # if no self.parser_class is set, return the entire json response
        if self.parser_class is None:
            logger.info('parser_class was None. returning raw response json')
            return self.data

        # use the self.parser_class
        parser = self.parser_class(self.data)
        return parser.get_data()

    def get_player_model_class(self):
        if self.player_model_class is None:
            ssm = SiteSportManager()
            site_sport = ssm.get_site_sport(self.sport)
            self.player_model_class = ssm.get_player_class(site_sport)
        return self.player_model_class

    def get_sport_players(self):
        if self.sport_players is None:
            self.sport_players = self.get_player_model_class().objects.filter()
        return self.sport_players

    def find_player(self, first_name, last_name, pid):
        """
        may return None if a draftboard player with the same First & Last name cant be found
        AND a player with this first name & last name & player id (third party player id -- a 'pid' ) cant be found.

        :param first_name:
        :param last_name:
        :param pid: third-party service player id.
        :return:
        """
        model_class = self.get_player_model_class()
        try:
            return self.get_sport_players().get(first_name=first_name, last_name=last_name)

        except (model_class.MultipleObjectsReturned, model_class.DoesNotExist):
            logger.info('%s.player not found for %s %s' % (self.sport, first_name, last_name))
            # check the lookup table
            return self.find_player_in_lookup_table(first_name, last_name, pid)

            # raise Exception(
            # 'statscom.classes Stats instance - find_player() ERROR - pid[%s] %s %s' % (pid, first_name, last_name))

    def find_player_in_lookup_table(self, first_name, last_name, pid):
        """
        uses the PlayerLookup table to find the named player -- creates an instance if they dont
        exist

        returns None if no player could be looked up in /admin/statscom/playerlookup/
        """
        try:
            logger.debug('find_player_in_lookup_table %s %s' % (first_name, last_name))
            player_lookup = PlayerLookup.objects.get(
                first_name=first_name, last_name=last_name, pid=pid)
            if player_lookup.sport is not self.sport.upper():
                player_lookup.sport = self.sport.upper()
                player_lookup.save()
            return player_lookup.player  # may return None if admin has not set it yet

        except PlayerLookup.DoesNotExist:
            logger.info('creating PlayerLookup for %s %s - pid:%s' % (first_name, last_name, pid))
            # create their entry, but theres nothing to return, because a newly created object wont
            # be linked to an actual SR player yet!
            PlayerLookup.objects.create(
                first_name=first_name,
                last_name=last_name,
                pid=pid,
                sport=self.sport.upper(),
            )

        return None


class DailyGamesNBA(Stats):
    """
    retrieve the information for NBA game events.
    """

    endpoint_daily_games = '/stats/basketball/nba/scores/'

    def __init__(self):
        super().__init__('nba')

    def get_games(self):
        """
        calls the api to get the current day's games.
        """
        logger.info('Fetching NBA games for: Today')
        return self.api(self.endpoint_daily_games)

    def get_tomorrows_games(self):
        """
        Calls the stats api to get tomorrow's games. format: (YYYY-MM-DD)
        """
        now = datetime.datetime.now(tz)
        tomorrow = now + datetime.timedelta(days=1)
        logger.info('Fetching NBA games for: %s' % tomorrow.strftime('%Y-%m-%d'))
        return self.api(self.endpoint_daily_games, params={'date': tomorrow.strftime('%Y-%m-%d')})

    def get_event_ids(self, data=None):
        """
        return a list of the stats.com eventId(s) for all events (ie: games) in the
        data returned by the method: get_games()

        if no 'data' param is supplied, this method will call get_games()

        :param data: the return value of get_games()
        :return: list of integer eventId(s)
        """

        if data is None:
            # Get TOMORROW'S games.
            data = self.get_tomorrows_games()

        season = data.get('season')
        # season.keys()
        event_type_list = season.get('eventType')
        # len(event_type_list)
        event = event_type_list[0]
        # event.keys()
        events = event.get('events')

        # return a list of the eventIds
        return [game.get('eventId') for game in events]


class DailyGamesMLB(Stats):
    endpoint_daily_games = '/stats/baseball/mlb/box/'

    def __init__(self):
        super().__init__('mlb')

    def get_games(self):
        """
        calls the api to get the current days games
        """
        return self.api(self.endpoint_daily_games)


class PlayersParser(ResponseDataParser):
    field_players = 'players'

    def get_data(self):
        data = super().get_data()
        players = data.get(self.field_players, [])
        logger.info('%s players' % (str(len(players))))
        return players


class PlayersNBA(Stats):
    parser_class = PlayersParser
    endpoint = '/stats/basketball/nba/participants/'

    def __init__(self):
        super().__init__('nba')
        self.data = None
        self.players = None

    def get_players(self):
        # calling the api will set the entire response of JSON data to the internal self.data
        return self.api(self.endpoint)

    def get_player_for_id(self, stats_id):
        """
        retrieve player via their stats.com player id

        the data returned is the raw player data from the api. for example:

            {'birth': {'birthDate': {'date': 5,
               'full': '1985-05-05',
               'month': 5,
               'year': 1985},
              'city': 'Raleigh',
              'country': {'abbreviation': 'USA', 'countryId': 1, 'name': 'United States'},
              'state': {'abbreviation': 'NC', 'name': 'North Carolina', 'stateId': 33}},
             'college': {'collegeId': 83,
              'commonName': 'Texas',
              'fullName': 'University of Texas'},
             'displayId': 0,
             'draft': {...},
             'experience': {'experience': 5, 'yearFirst': 2006, 'yearRookie': 2006},
             'firstName': 'P.J.',
             'height': {'centimeters': 198.0, 'inches': 78.0},
             'highSchool': {...},
             'hometown': {'city': 'Raleigh'},
             'isActive': True,
             'isInjured': True,
             'isSuspended': False,
             'lastName': 'Tucker',
             'playerId': 229602,
             'positions': [{'abbreviation': 'SF',
               'name': 'Small Forward',
               'positionId': 5,
               'sequence': 1},
              {'abbreviation': 'SG',
               'name': 'Shooting Guard',
               'positionId': 2,
               'sequence': 2}],
             'team': {'abbreviation': 'Pho',
              'location': 'Phoenix',
              'nickname': 'Suns',
              'teamId': 21},
             'uniform': '17',
             'weight': {'kilograms': 111.13, 'pounds': 245.0}}

        :param stats_id:
        :return:
        """

        self.init_players()

        player_data = self.players.get(stats_id)
        # logger.info('get_player_for_id(%s) returned: %s' % (str(stats_id), str(player_data)))
        return player_data

    def init_players(self):
        """
        builds the internal dict of statsid -> player object mappings

        if it already exists, this has no effect.
        """
        if self.data is None:
            # get the raw data from the api
            self.data = self.get_players()

            # create a dictionary where the players ids index to that players data obj
            self.players = {}
            for player in self.data:
                self.players[player.get('playerId')] = player


class PlayersMLB(Stats):
    parser_class = PlayersParser
    endpoint = '/stats/baseball/mlb/participants/'

    def __init__(self):
        super().__init__('mlb')

    def get_players(self):
        # calling the api will set the entire response of JSON data to the internal self.data
        return self.api(self.endpoint)


class ProjectionsParser(ResponseDataParser):
    class ProjectionsNotFound(Exception):
        pass

    field_season = 'season'
    field_event_type = 'eventType'
    field_fantasy_projections = 'fantasyProjections'
    field_teams = 'teams'

    def get_data(self):
        data = super().get_data()
        season = data.get(self.field_season, {})
        event_type = season.get(self.field_event_type, [])
        num_event_types = len(event_type)
        if num_event_types != self.default_event_types:
            err_msg = 'found %s items in "%s" list. expected %s' % (str(num_event_types),
                                                                    self.field_event_type,
                                                                    str(self.default_event_types))
            raise self.ProjectionsNotFound(err_msg)
        event_type_item = event_type[self.default_event_type_index]
        fantasy_projections = event_type_item.get(self.field_fantasy_projections, {})
        # teams = fantasy_projections.get(self.field_teams) # mlb only !
        return fantasy_projections


class FantasyProjections(Stats):
    player_projection_class = PlayerProjection

    parser_class = ProjectionsParser

    field_fantasy_projections = 'fantasyProjections'

    field_points = 'points'
    field_salary = 'salary'

    field_first_name = 'firstName'
    field_last_name = 'lastName'
    field_player_id = 'playerId'

    field_name = 'name'

    site_dk = 'draftkings'
    site_fd = 'fanduel'

    # the sites projections to use as primary datapoint for draftboard.
    # it should be the site that closest matches our actual scoring.
    default_site = site_dk

    def __init__(self, sport):
        # logger.info(sport)
        super().__init__(sport)

    def build_player_projection(self, player, fantasy_points, sal_dk=None, sal_fd=None):
        return self.player_projection_class(player, fantasy_points, sal_dk=sal_dk, sal_fd=sal_fd)


class PlayerNBA:
    """
    data class for extracting data from the player objects found in the participants api
    """

    class NoPositionFound(Exception):
        pass

    field_positions = 'positions'
    field_abbreviation = 'abbreviation'
    field_first_name = 'firstName'
    field_last_name = 'lastName'
    field_player_id = 'playerId'

    def __init__(self, data):
        self.data = data

    def get_position(self):
        """
        get the first/primary position for the player

        retrieves the field for the positions list, and
        returns the abbreviation of the first one in the list.
        """
        positions = self.data.get(self.field_positions)
        if positions is None or positions == []:
            err_msg = 'the value of field[%s] returned None or empty list. ' \
                      'Here is the raw data: %s' % (str(self.field_positions), str(self.data))
            logger.info(err_msg)
            raise self.NoPositionFound(err_msg)

        # return the first abbreviation found in the list
        position = positions[0]
        return position.get(self.field_abbreviation)

    def get_first_name(self):
        return self.data.get(self.field_first_name)

    def get_last_name(self):
        return self.data.get(self.field_last_name)

    def get_id(self):
        return self.data.get(self.field_player_id)


class FantasyProjectionsNBA(FantasyProjections):
    """
    retrieve the fantasy points projections for an eventId
    """

    endpoint_fantasy_projections = '/stats/basketball/nba/fantasyProjections/'
    field_fantasy_projections = 'fantasyProjections'
    stat_map = STATPOINT_TO_STATSCOM_NBA

    def __init__(self):
        super().__init__('nba')

        # this instance lets us get player data by players' stats.com id
        self.players = PlayersNBA()
        self.scoring_system_stat_points = StatPoint.objects.filter(score_system__sport='nba')
        logger.info('Using scoring system: %s' % self.scoring_system_stat_points)

    def get_projections(self, event_id):
        """
        return the raw data for the fantasy projections of players in the event (the game)

        :param event_id: the game id. for example: 1234
        :return:
        """
        endpoint = self.endpoint_fantasy_projections + str(event_id)
        return self.api(endpoint)

    def get_player_projections(self, event_ids=None):

        if event_ids is None:
            # get the daily event ids
            event_ids = DailyGamesNBA().get_event_ids()
            logger.info('DailyGamesNBA().get_event_ids() -> %s' % event_ids)

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
            logger.info('player_projections count for event.id %s: %s' % (event_id, len(player_projections)))

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
                         'and link [%s] players!' % (str(self.sport), str(num_players_without_lookup)))

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
                # logger.info('    x player_projection:' + str(player_projection)[:50]) # debug the first 50 chars
                # get the player data via their id
                pid = player_projection.get(self.field_player_id)
                # player_data is a big dict of data about the player, all we really need this for is to find their
                # name or PID for matching.
                player_data = self.players.get_player_for_id(pid)
                # logger.info('   player_data: %s', player_data )
                if player_data is None:
                    logger.warn(
                        "(skipping player projection) STATS.com playerId [%s] not found in PlayerNBA data! "
                        "Here's the projection that made us fail: %s" % (str(pid), str(player_projection)))
                    continue

                # try to get the fantasy projection list (of each site projection)
                fantasy_projections = player_projection.get(self.field_fantasy_projections)
                logger.debug('fantasyProjections (site projections): %s' % fantasy_projections)
                if len(fantasy_projections) == 0:
                    msg = 'No site projections found for field[%s]  player[%s]' % (
                        self.field_fantasy_projections, str(player_data))
                    logger.warn(msg)
                    raise Exception(msg)

                # get an instance of this data class to help extract
                # the values we need to look this player up
                p = PlayerNBA(player_data)
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
                    # Figure out what we think their FP will be based on the projected stats from STATS.com.
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
                            sal_dk = self.get_site_player_salary(fantasy_projections_copy, self.site_dk)
                            sal_fd = self.get_site_player_salary(fantasy_projections_copy, self.site_fd)
                            break  # is it possible its never found?

                        else:
                            logger.debug('%s not found in %s' % (
                                self.default_site, site.get(self.field_name, '').lower()))

                    # Extract the player's stat projections and append it to a list of projected stats.
                    # This is the important part - we use these stats to determine the player's salary.
                    player_projections.append(self.build_player_projection(player, our_projected_fp,
                                                                           sal_dk=sal_dk, sal_fd=sal_fd))

        return player_projections, no_lookups

    def get_site_player_salary(self, fantasy_projections, site):
        """
        `FantasyProjectionsNBA`

        this method should be able to retrieve the site specific
        salary from the list of site projections objects if
        the 'site' param is contained within each site items name property.

        :param fantasy_projections: The projections for the player we've found in the stats.com response
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


class FantasyProjectionsMLB(FantasyProjections):
    # the game's eventid must be appended to this endpoint
    endpoint_fantasy_projections = '/stats/baseball/mlb/fantasyProjections/'

    def __init__(self):
        super().__init__('mlb')

    def get_projections(self, eventid):
        """
        returns a list of 2 elements. each element is one of the teams in the game, and has these keys:

            dict_keys(['teamId', 'pitchers', 'batters'])

        caveat: stats.com only gives a projection for the Probable Pitcher (and starting lineup)
        and it might not be nearly enough coverage for us to generate salaries based on this data.

        :param eventid: the game's id. ex: 1600732
        :return:
        """
        endpoint = self.endpoint_fantasy_projections + str(eventid)
        return self.api(endpoint)


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
                         'receptionTouchdowns', 'passYards', 'receptions', 'fieldGoalsMade29', 'fieldGoalsMade49',
                         'chance100RushYards', 'fieldGoalsMade19', 'fumblesLost', 'twoPointConversions',
                         'fieldGoalsMade39', 'interceptions', 'chance100ReceptionYards', 'chance300PassYards',
                         'extraPointsMade', 'fieldGoalsAttempted', 'fieldGoalsMade50', 'receptionYards', 'rushes',
                         'rushYards', 'rushTouchdowns', 'attempts']

    def __init__(self, data):
        self.data = data


class FantasyProjectionsNFL(FantasyProjections):
    endpoint_current_weekly_projections = '/stats/football/nfl/fantasyProjections/weekly/'
    endpoint_weekly_projections = '/stats/football/nfl/fantasyProjections/weekly/'  # append week number

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

    def get_projections(self, week=None):
        """
        get the projections for the current week.

        returns a dict with fields in:

            ['offensiveProjections', 'week', 'defensiveProjections']

        if a week number is specified, this will return the projections for that week (for current season)
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
        offensive_projections = data.get(self.field_offensive_projections)
        player_projections = []
        no_lookups = []
        for proj in offensive_projections:
            # get the players position
            position = proj.get(self.field_position)

            # lookup the player in our database by matching the full name
            player_data = proj.get(self.field_player)
            pid = player_data.get(self.field_player_id)
            first_name = player_data.get(self.field_first_name)
            last_name = player_data.get(self.field_last_name)

            # look up this third party api player in our own db
            player = self.find_player(first_name, last_name, pid)
            if player is None:
                player_string = 'pid[%s] player[%s %s] position[%s]' % (pid, first_name, last_name, position)
                no_lookups.append(player_string)
                logger.warning("Couldn't lookup: %s" % player_string)
                continue

            #
            fantasy_projections = proj.get(self.field_fantasy_projections, [])
            if len(fantasy_projections) == 0:
                raise Exception('field not found: %s' % self.field_fantasy_projections)

            # iterate the list of sites which we have projections for until we find the one we want
            fantasy_projections_copy = fantasy_projections.copy()
            for site in fantasy_projections:
                if self.default_site in site.get(self.field_name, '').lower():
                    # append a new a salary.classes.PlayerProjection to our return list and break
                    fantasy_points = site.get(self.field_points)

                    # try to get the sites own salary for the player for the major sites.
                    sal_dk = self.get_site_player_salary(fantasy_projections_copy, self.site_dk)
                    sal_fd = self.get_site_player_salary(fantasy_projections_copy, self.site_fd)

                    player_projections.append(self.build_player_projection(player, fantasy_points,
                                                                           sal_dk=sal_dk, sal_fd=sal_fd))
                    break

        # send slack webhook with the players we couldnt link
        num_players_without_lookup = len(no_lookups)
        if num_players_without_lookup > 0:
            webhook = ProjectionsWeekWebhook()
            webhook.send('check draftboard.com/admin/statscom/playerlookup/ '
                         'and link [%s] players!' % str(num_players_without_lookup))

        #
        return player_projections

    def get_site_player_salary(self, fantasy_projections, site):
        """
        this method should be able to retrieve the site specific
        salary from the list of site projections objects if
        the 'site' param is contained within each site items name property.

        :param fantasy_projections: The projections for the player we've found in the stats.com response
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
