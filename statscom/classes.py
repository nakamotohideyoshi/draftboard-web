import datetime
import hashlib
import json
import time
import urllib.parse
from logging import getLogger

import pytz
import requests
from django.conf import settings

import draftgroup.classes
from salary.classes import PlayerProjection
from sports.classes import SiteSportManager
from statscom.models import (
    PlayerLookup,
)
from util.slack import Webhook

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
            err_msg = 'bad stats.com api response: got %s, expected %s' % (
                self.field_api_results, self.default_api_results)
            logger.warning(err_msg)
            raise self.UnexpectedApiResults(err_msg)

        num_results = len(api_results)
        if num_results != self.default_api_results:
            err_msg = 'bad stats.com api response: got %s %s, expected %s' % (
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

        # get and validate the api_key and secret token exist.
        if self.stats_keys is None:
            err_msg = "settings.STATSCOM_KEYS missing"
            raise self.MissingApiKeySettings(err_msg)

        self.api_key = self.stats_keys.get(self.field_api_key)
        self.secret = self.stats_keys.get(self.field_secret)

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
        return '?api_key=%s&sig=%s&accept=%s' % (
        self.get_api_key(), self.get_sig(), self.response_format)

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
            raise Exception("bad stats.com api response: %s" % msg)

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
                pid=pid,
                sport=self.sport.upper()
            )
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


class PlayersParser(ResponseDataParser):
    field_players = 'players'

    def get_data(self):
        data = super().get_data()
        players = data.get(self.field_players, [])
        logger.info('%s players' % (str(len(players))))
        return players


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


class DailyGamesAbstract(Stats):
    """
    retrieve the information for a sport's game events on a specific day. This will give us eventId's
    that we can then use to fetch players, then with players we can fetch projections.
    """

    endpoint_daily_games = None

    def __init__(self, sport):
        super().__init__(sport)

    def get_games(self):
        """
        calls the api to get the current day's games.
        """
        logger.info('Fetching %s games for: Today' % self.sport)
        return self.api(self.endpoint_daily_games)

    def get_tomorrows_games(self):
        """
        Calls the stats api to get tomorrow's games. format: (YYYY-MM-DD)
        """
        now = datetime.datetime.now(tz)
        tomorrow = now + datetime.timedelta(days=1)
        logger.info('Fetching %s games for: %s' % (self.sport, tomorrow.strftime('%Y-%m-%d')))
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

        # if we still have no data, there are no game projections avialable.
        if data is None:
            raise Exception('No events were returned from the stats.com API. %s' % data)

        season = data.get('season', {})
        # season.keys()
        event_type_list = season.get('eventType', [])
        # If there are games, return them in a list.
        if len(event_type_list):
            # len(event_type_list)
            event = event_type_list[0]
            # event.keys()
            events = event.get('events')

            # return a list of the eventIds
            return [game.get('eventId') for game in events]


class PlayersAbstract(Stats):
    """
    Retrieve all the players that will play in a specific game.
    """
    parser_class = PlayersParser
    endpoint = None

    def __init__(self, sport):
        super().__init__(sport)
        self.data = None
        self.players = None

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

    def get_players(self):
        # calling the api will set the entire response of JSON data to the internal self.data
        return self.api(self.endpoint)

    def get_player_for_id(self, stats_id):
        """
        retrieve player via their stats.com player id

        :param stats_id:
        :return:
        """
        self.init_players()

        player_data = self.players.get(stats_id)
        # logger.info('get_player_for_id(%s) returned: %s' % (str(stats_id), str(player_data)))
        return player_data


class StatsPlayer:
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
https://api.gidx-service.in/v3.0/api/CustomerIdentity/Location?ApiKey=k2m9yX4Tl0WXuz8Ahc5muA&MerchantID=Q2wprL4aKEKEj-dzTu44BA&ProductTypeID=iiXXab0LtUCUdZ_6vcdtvQ&DeviceTypeID=2bDPorOkPkepDd8-6Fydtw&ActivityTypeID=login&MerchantSessionID=test_Dan&DeviceIpAddress=24.180.8.163