#
# classes.py

import time
import hashlib
import json
import requests
import csv
from django.conf import settings
from salary.classes import PlayerProjection
from sports.classes import SiteSportManager
from util.utctime import UtcTime
import draftgroup.classes
from statscom.models import (
    PlayerLookup,
)
from util.slack import Webhook

class ProjectionsWeekWebhook(Webhook):

    # its a piece of the full url from something like this:
    # https://hooks.slack.com/services/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
    identifier = 'T02S3E1FD/B2H8GB97T/gHG66jb3wvGHSJb9Zcr7IwHC'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = 'current-projections-week'

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

    class UnexpectedApiResults(Exception): pass

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
        returns the data objects after stripping off the boiler plate wrapper common to stats.com apis.

        note: this method returns inner data from the data, not the data passed in.
        """
        # return self.data
        api_results = self.data.get(self.field_api_results)
        num_results = len(api_results)
        if num_results != self.default_api_results:
            err_msg = 'got %s %s, expected %s' % (str(num_results), self.field_api_results, self.default_api_results)
            raise self.UnexpectedApiResults(err_msg)
        result = api_results[self.default_api_result_index]
        league = result.get(self.field_league)
        print('league.keys()', str(league.keys()))
        return league

class Stats(object):
    """
    this class is for calling the STATS.com api and getting back its raw responses as JSON
    """

    class MissingApiKeySettings(Exception): pass

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
        self.sport_players = None # set on the first call to self.get_player_model_class()

        # get and validate the api_key and secret token exist for this sport
        self.keys = self.stats_keys.get(self.sport)
        if self.keys is None:
            err_msg = "'%s' missing from settings.STATSCOM_KEYS" % self.sport
            raise self.MissingApiKeySettings(err_msg)

        self.api_key = self.keys.get(self.field_api_key)
        self.secret = self.keys.get(self.field_secret)

        # set up a session object to do the actual http calls
        self.session = requests.Session()
        self.r = None # we will always save the last response here
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
        sig = hashlib.sha256((self.api_key + self.secret + str(int(time.time()))).encode()).hexdigest()
        #print('stats.com api sig=%s' % str(sig))
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

    def api(self, endpoint, format=None, verbose=True):
        """
        makes the http request and returns the contents as json

        :param endpoint: ie: '/stats/football/nfl/fantasyProjections/weekly/'
        :param format: you can override the format returned. defaults to json.
        :return: the data from the api call
        """
        url = self.get_url(endpoint)
        self.r = self.session.get(url)
        print('http %s %s' % (str(self.r.status_code), url))
        self.data = json.loads(self.r.text)

        # check if there is an error
        msg = self.data.get(self.field_message)
        print('self.data "%s" -> %s' % (self.field_message, str(msg)))

        # if no self.parser_class is set, return the entire json response
        if self.parser_class is None:
            print('parser_class was None. returning raw response json')
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

        except (model_class.MultipleObjectsReturned, model_class.DoesNotExist) as e:
            # check the lookup table
            return self.find_player_in_lookup_table(first_name, last_name, pid)

        #raise Exception('statscom.classes Stats instance - find_player() ERROR - pid[%s] %s %s' % (pid, first_name, last_name))

    def find_player_in_lookup_table(self, first_name, last_name, pid):
        """
        uses the PlayerLookup table to find the named player -- creates an instance if they dont exist

        returns None if no player could be looked up in /admin/statscom/playerlookup/
        """

        try:
            player_lookup = PlayerLookup.objects.get(first_name=first_name, last_name=last_name, pid=pid)
            return player_lookup.player # may return None if admin has not set it yet

        except PlayerLookup.DoesNotExist:
            # create their entry, but theres nothing to return, because a newly created object wont be linked
            # to an actual SR player yet!
            player_lookup = PlayerLookup.objects.create(first_name=first_name, last_name=last_name, pid=pid)

        #
        return None

class DailyGamesMLB(Stats):

    endpoint_daily_games = '/stats/baseball/mlb/box/'

    def __init__(self):
        super().__init__('mlb')

    def get_games(self):
        """
        calls the api to get the current days games
        """
        return self.api(self.endpoint_daily_games)

    def test(self):
        pass
        # In[3]: data = daily_games_mlb.get_games()

        # In[4]: data.keys()
        # Out[4]: dict_keys(['endTimestamp', 'recordCount', 'startTimestamp', 'apiResults', 'timeTaken', 'status'])

        # In[6]: results = data.get('apiResults')
        #
        # In[7]: len(results)
        # Out[7]: 1
        #
        # In[8]: result = results[0]
        #
        # In[9]: result.keys()
        # Out[9]: dict_keys(['sportId', 'name', 'league'])

        # In[10]: league = result.get('league')
        #
        # In[11]: league.keys()
        # Out[11]: dict_keys(['abbreviation', 'season', 'name', 'leagueId', 'displayName'])

        # In[12]: season = league.get('season')
        #
        # In[13]: season.keys()
        # Out[13]: dict_keys(['season', 'name', 'isActive', 'eventType'])

        # In[14]: event_type_list = season.get('eventType')
        #
        # In[15]: len(event_type_list)
        # Out[15]: 1
        #
        # In[16]: event = event_type_list[0]
        #
        # In[17]: event.keys()
        # Out[17]: dict_keys(['eventTypeId', 'name', 'events'])

        # events = event.get('events')
        # for game in events:
        #     pass
        #     print(game) # will print the game json object
            # In[22]: game.keys()
            # Out[22]: dict_keys(
            #     ['coverageLevel', 'isDataConfirmed', 'startDate', 'seriesId', 'isTba', 'teams', 'tvStations', 'eventId',
            #      'eventConference', 'isDoubleheader', 'venue', 'eventStatus'])

class PlayersParser(ResponseDataParser):

    field_players = 'players'

    def get_data(self):
        data = super().get_data()
        players = data.get(self.field_players, [])
        print('%s players' % (str(len(players)))) # TODO remove debug
        return players

class PlayersMLB(Stats):

    parser_class = PlayersParser
    endpoint = '/stats/baseball/mlb/participants/'

    def __init__(self):
        super().__init__('mlb')

    def get_players(self):
        # calling the api will set the entire response of JSON data to the internal self.data
        return self.api(self.endpoint)

class ProjectionsParser(ResponseDataParser):

    class ProjectionsNotFound(Exception): pass

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

    def __init__(self, sport):
        super().__init__(sport)

    def build_player_projection(self, player, fantasy_points, sal_dk=None, sal_fd=None):
        return self.player_projection_class(player, fantasy_points, sal_dk=sal_dk, sal_fd=sal_fd)

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

        #         #
        #         # In[23]: len(pitchers)
        #         # Out[23]: 1
        #         #
        #         # In[27]: len(batters)
        #         # Out[27]: 8
        #
        #         # In[2]: batter.keys()
        #         # Out[2]: dict_keys(['battingSlot', 'walks', 'runs', 'playerId', 'doubles', 'atBats', 'stolenBases', 'triples',
        #         #                    'caughtStealing', 'homeRuns', 'runsBattedIn', 'singles', 'outs', 'hitByPitch',
        #         #                    'fantasyProjections'])
        #
        #         # In[4]: pitcher.keys()
        #         # Out[4]: dict_keys(
        #         #     ['playerId', 'wins', 'hitBatsmen', 'shutouts', 'fantasyProjections', 'inningsPitched', 'completeGames',
        #         #      'strikeouts', 'noHitters', 'walks', 'earnedRuns', 'hits'])
        #
        # # In[5]: batter
        # # Out[5]:
        # # {'atBats': '4.21127',
        # #  'battingSlot': 1,
        # #  'caughtStealing': '0.00213',
        # #  'doubles': '0.22281',
        # #  'fantasyProjections': [{'name': 'DraftKings (draftkings.com)',
        # #                          'points': '8.28939',
        # #                          'position': '1B',
        # #                          'salary': '4600',
        # #                          'siteId': 1},
        # #                         {'name': 'FanDuel (fanduel.com)',
        # #                          'points': '10.79381',
        # #                          'position': '1B',
        # #                          'salary': '3100',
        # #                          'siteId': 2}],
        # #  'hitByPitch': '0.03242',
        # #  'homeRuns': '0.18517',
        # #  'outs': '3.07268',
        # #  'playerId': 184104,
        # #  'runs': '0.68209',
        # #  'runsBattedIn': '0.42543',
        # #  'singles': '0.73062',
        # #  'stolenBases': '0.0025',
        # #  'triples': '0.0',
        # #  'walks': '0.4197'}
        # #
        # # In[6]: pitcher
        # # Out[6]:
        # # {'completeGames': '0.00482',
        # #  'earnedRuns': '2.46612',
        # #  'fantasyProjections': [{'name': 'DraftKings (draftkings.com)',
        # #                          'points': '13.2881',
        # #                          'position': 'SP',
        # #                          'salary': '5300',
        # #                          'siteId': 1},
        # #                         {'name': 'FanDuel (fanduel.com)',
        # #                          'points': '26.89173',
        # #                          'position': 'P',
        # #                          'salary': '7100',
        # #                          'siteId': 2}],
        # #  'hitBatsmen': '0.1566',
        # #  'hits': '5.99135',
        # #  'inningsPitched': '5.2',
        # #  'noHitters': '0.0',
        # #  'playerId': 598259,
        # #  'shutouts': '0.00212',
        # #  'strikeouts': '4.24619',
        # #  'walks': '1.51576',
        # #  'wins': '0.37096'}

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
    endpoint_weekly_projections = '/stats/football/nfl/fantasyProjections/weekly/' # append week number

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

    field_name = 'name'

    site_dk = 'draftkings'
    site_fd = 'fanduel'

    # the sites projections to use as primary datapoint for draftboard.
    # it should be the site that closest matches our actual scoring.
    default_site = site_dk

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
                player_string = 'pid[%s] player[%s] position[%s]' % (str(pid),
                                                str(first_name + ' ' + last_name), str(position))
                no_lookups.append(player_string)
                err_msg = 'COULDNT LOOKUP -> %s' % player_string
                print(err_msg)
                continue

            #
            fantasy_projections = proj.get(self.field_fantasy_projections, [])
            if len(fantasy_projections) == 0:
                raise Exception('field not found: %s' % self.field_fantasy_projections)

            # iterate the list of sites which we have projections for until we find the one we want
            fantasy_projections_copy = fantasy_projections.copy()
            for site in fantasy_projections:
                if self.default_site in site.get(self.field_name).lower():
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

class NFLPlayerProjectionCsv(PlayerProjectionNFL): # particularly for NFL i might add...
    """ temp helper class to dump out projections and match up with our own players """

    field_fantasy_projections = 'fantasyProjections'
    field_offensive_projections = 'offensiveProjections'

    field_player = 'player'
    field_player_id = 'playerId'
    field_fullname = 'fullname'             # i made this one. it combines the first+last name
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

        # TODO debug
        print('all possible categories seen:', str(self.all_fields.keys()))

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

            #### debug, i want to see all possible projected category names
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
