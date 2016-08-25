#
# classes.py

import time
import hashlib
import json
import requests
from django.conf import settings

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

    def __init__(self, sport):
        self.sport = sport

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
        return json.loads(self.r.text)

# TODO it looks like most of the response data's outter wrapper is boiler plate

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

class FantasyProjectionData(object): # particularly for NFL i might add...

    def __init__(self, data):
        self.data = data

    def to_csv(self):
        #In[5]: data.keys()
        #Out[5]: dict_keys(['timeTaken', 'endTimestamp', 'apiResults', 'status', 'recordCount', 'startTimestamp'])

        api_results = self.data.get('apiResults')
        # len(api_results)   # 1 thing

        result = api_results[0]

        # In[10]: result.keys()
        # Out[10]: dict_keys(['sportId', 'name', 'league'])

        league = result.get('league')
        # In[13]: league.keys()
        # Out[13]: dict_keys(['season', 'displayName', 'abbreviation', 'leagueId', 'name'])

        season = league.get('season')
        # In[15]: season.keys()
        # Out[15]: dict_keys(['season', 'isActive', 'name', 'eventType'])

        season_year = season.get('season')
        is_active = season.get('isActive')
        event_type_list = season.get('eventType')
        print('%s items in event_type_list' % str(len(event_type_list)))

        event = event_type_list[0]
        # In[23]: event.keys()
        # Out[23]: dict_keys(['fantasyProjections', 'name', 'eventTypeId'])

        fantasy_projections = event.get('fantasyProjections')
        # In[25]: fantasy_projections.keys()
        # Out[25]: dict_keys(['defensiveProjections', 'week', 'offensiveProjections'])

        offensive_projections = fantasy_projections.get('offensiveProjections')
        for proj in offensive_projections:
            # print(str(proj))

            # In[29]: proj.keys()
            # Out[29]: dict_keys(
            #     ['opponent', 'twoPointConversions', 'chance300PassYards', 'completions', 'rushYards', 'team',
            #      'chance100RushYards', 'interceptions', 'gameDate', 'attempts', 'passYards', 'passTouchdowns', 'player',
            #      'fantasyProjections', 'rushTouchdowns', 'position', 'fumblesLost', 'rushes', 'eventId'])

            player = proj.get('player')
            # {'firstName': 'Andrew', 'lastName': 'Luck', 'playerId': 461175}
            fn = player.get('firstName')
            ln = player.get('lastName')
            pid = player.get('playerId')

            site_projections = proj.get('fantasyProjections')
            for site_proj in site_projections:
                # site_proj has keys we care about 'name', 'points'  which are the site name and projection
                name = site_proj.get('name')
                fantasy_points = site_proj.get('points')

                #
                # format the csv row
                print(ln, fn, pid, name, fantasy_points, sep=',')

### snippet will output (in a csv format) the contents for week 1 (change it if you want)
# from statscom.classes import FantasyProjectionsNFL, FantasyProjectionData
# fp = FantasyProjectionsNFL()
# data = fp.get_projections(week=1)
# fpdata = FantasyProjectionData(data)
# fpdata.to_csv()

class FantasyProjections(Stats):

    def __init__(self, sport):
        super().__init__(sport)

class FantasyProjectionsMLB(FantasyProjections):

    # the game's eventid must be appended to this endpoint
    endpoint_fantasy_projections = '/stats/baseball/mlb/fantasyProjections/'

    def __init__(self):
        super().__init__('mlb')

    def get_projections(self, eventid):
        """

        :param eventid: the game's id. ex: 1600732
        :return:
        """
        endpoint = self.endpoint_fantasy_projections + str(eventid)
        return self.api(endpoint)

    def test(self):
        pass

        # In[1]: from statscom.classes import FantasyProjectionsMLB
        #
        # In[2]: api = FantasyProjectionsMLB()
        #
        # In[3]: data = api.get_projections(1600732)
        # http
        # 200
        # http: // api.stats.com / v1 / stats / baseball / mlb / fantasyProjections / 1600732?api_key = vqcfvb8vz9m732hqm5saxv3g & sig = b8871fd729b27cb00c7346d70878d94e34cdbfbcd949f6526458b4e700f860d4 & accept = json
        #
        # In[4]: data.keys()
        # Out[4]: dict_keys(['timeTaken', 'apiResults', 'startTimestamp', 'status', 'endTimestamp', 'recordCount'])
        #
        # In[5]: api_results = data.get('apiResults')
        #
        # In[6]: result = api_results[0]
        #
        # In[7]: result.keys()
        # Out[7]: dict_keys(['league', 'name', 'sportId'])
        #
        # In[8]: league = result.get('league')
        #
        # In[9]: season = league.get('season')
        #
        # In[10]: season.keys()
        # Out[10]: dict_keys(['name', 'eventType', 'season', 'isActive'])
        #
        # In[11]: event_type_list = season.get('eventType')
        #
        # In[12]: events = event_type_list[0]
        #
        # In[13]: len(event_type_list)
        # Out[13]: 1
        #
        # In[14]: events.keys()
        # Out[14]: dict_keys(['eventTypeId', 'fantasyProjections', 'name'])
        #
        # In[15]: fantasy_projections = events.get('fantasyProjections')
        #
        # In[16]: fantasy_projections.keys()
        # Out[16]: dict_keys(['teams', 'eventId'])

        # In[17]: teams = fantasy_projections.get('teams')
        #
        # In[19]: len(teams)
        # Out[19]: 2
        #
        # In[20]: for team in teams:
        #     ....:     print(team.keys())
        #     ....:
        #     dict_keys(['teamId', 'batters', 'pitchers'])
        #     dict_keys(['teamId', 'batters', 'pitchers'])

            # In[21]: pitchers = team.get('pitchers')
            # In[22]: batters = team.get('batters')
            #
            # In[23]: len(pitchers)
            # Out[23]: 1
            #
            # In[27]: len(batters)
            # Out[27]: 8

            # In[2]: batter.keys()
            # Out[2]: dict_keys(['battingSlot', 'walks', 'runs', 'playerId', 'doubles', 'atBats', 'stolenBases', 'triples',
            #                    'caughtStealing', 'homeRuns', 'runsBattedIn', 'singles', 'outs', 'hitByPitch',
            #                    'fantasyProjections'])

            # In[4]: pitcher.keys()
            # Out[4]: dict_keys(
            #     ['playerId', 'wins', 'hitBatsmen', 'shutouts', 'fantasyProjections', 'inningsPitched', 'completeGames',
            #      'strikeouts', 'noHitters', 'walks', 'earnedRuns', 'hits'])

    # In[5]: batter
    # Out[5]:
    # {'atBats': '4.21127',
    #  'battingSlot': 1,
    #  'caughtStealing': '0.00213',
    #  'doubles': '0.22281',
    #  'fantasyProjections': [{'name': 'DraftKings (draftkings.com)',
    #                          'points': '8.28939',
    #                          'position': '1B',
    #                          'salary': '4600',
    #                          'siteId': 1},
    #                         {'name': 'FanDuel (fanduel.com)',
    #                          'points': '10.79381',
    #                          'position': '1B',
    #                          'salary': '3100',
    #                          'siteId': 2}],
    #  'hitByPitch': '0.03242',
    #  'homeRuns': '0.18517',
    #  'outs': '3.07268',
    #  'playerId': 184104,
    #  'runs': '0.68209',
    #  'runsBattedIn': '0.42543',
    #  'singles': '0.73062',
    #  'stolenBases': '0.0025',
    #  'triples': '0.0',
    #  'walks': '0.4197'}
    #
    # In[6]: pitcher
    # Out[6]:
    # {'completeGames': '0.00482',
    #  'earnedRuns': '2.46612',
    #  'fantasyProjections': [{'name': 'DraftKings (draftkings.com)',
    #                          'points': '13.2881',
    #                          'position': 'SP',
    #                          'salary': '5300',
    #                          'siteId': 1},
    #                         {'name': 'FanDuel (fanduel.com)',
    #                          'points': '26.89173',
    #                          'position': 'P',
    #                          'salary': '7100',
    #                          'siteId': 2}],
    #  'hitBatsmen': '0.1566',
    #  'hits': '5.99135',
    #  'inningsPitched': '5.2',
    #  'noHitters': '0.0',
    #  'playerId': 598259,
    #  'shutouts': '0.00212',
    #  'strikeouts': '4.24619',
    #  'walks': '1.51576',
    #  'wins': '0.37096'}

    class FantasyProjectionsNFL(FantasyProjections):

    endpoint_current_weekly_projections = '/stats/football/nfl/fantasyProjections/weekly/'
    endpoint_weekly_projections = '/stats/football/nfl/fantasyProjections/weekly/' # append week number

    def __init__(self):
        super().__init__('nfl')

    def get_projections(self, week=None):
        """
        get the projections for the current week.

        if a week number is specified, this will return the projections for that week (for current season)
        """
        endpoint = self.endpoint_weekly_projections
        if week is not None:
            endpoint += str(week)
        # return the response data
        return self.api(endpoint)
