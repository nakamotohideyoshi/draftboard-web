from test.classes import AbstractTest
from statscom.classes import (
    Stats,
    ResponseDataParser,
)
from statscom.player import get_fantasy_point_projection_from_stats_projection


class ResponseDataParserTest(AbstractTest):
    def setUp(self):
        self.parser_class = ResponseDataParser
        self.data = {
            'apiResults': [
                {
                    'league': {'abbreviation': 'MLB',
                               'displayName': 'Major League Baseball',
                               'leagueId': 7,
                               'name': 'Major League Baseball',
                               'season': {'eventType': [{'eventTypeId': 1,
                                                         'fantasyProjections': {'eventId': 1600732, 'teams': []},
                                                         'name': 'Regular Season'}],
                                          'isActive': True,
                                          'name': '2016 MLB Season',
                                          'season': 2016}},
                    'name': 'Baseball',
                    'sportId': 2
                }
            ],
            'endTimestamp': '2016-08-29T19:25:19.3412166Z',
            'recordCount': 1,
            'startTimestamp': '2016-08-29T19:25:18.5130863Z',
            'status': 'OK',
            'timeTaken': 0.8281303
        }

    def test_1(self):
        """ make sure the basic default parser class works and/or throws exception """
        parser = self.parser_class(self.data)
        parser.get_data()


class NFLPlayerProjectionParser(AbstractTest):
    def setUp(self):
        self.data = {
            'attempts': '40',
            'chance100RushYards': '.015928072',
            'chance300PassYards': '.42525303',
            'completions': '24',
            'eventId': 1635716,
            'fantasyProjections': [
                {'name': 'DraftKings (draftkings.com)', 'points': '23.338117938', 'siteId': 1},
                {'name': 'FanDuel (fanduel.com)', 'points': '21.812347455', 'siteId': 2}
            ],
            'fumblesLost': '.202227177',
            'gameDate': {'date': 11, 'dateType': 'utc', 'full': '2016-09-11T20:25:00',
                         'hour': 20, 'minute': 25, 'month': 9, 'year': 2016},
            'interceptions': '1.198161304',
            'opponent': {'abbreviation': 'Det',
                         'location': 'Detroit',
                         'nickname': 'Lions',
                         'teamId': 334},
            'passTouchdowns': '2.224365',
            'passYards': '284',
            'player': {'firstName': 'Andrew', 'lastName': 'Luck', 'playerId': 461175},
            'position': 'QB',
            'rushTouchdowns': '.18559586',
            'rushYards': '18.92635965',
            'rushes': '4',
            'team': {'abbreviation': 'Ind',
                     'location': 'Indianapolis',
                     'nickname': 'Colts',
                     'teamId': 338},
            'twoPointConversions': '.075645994'
        }


class StatsUrlAuthParamTest(AbstractTest):
    def setUp(self):
        self.sport = 'nfl'

    def test_1(self):
        """ ensure some fundamental settings are set - dont validate for correctness here """
        stats = Stats(self.sport)
        self.assertIsNotNone(stats.stats_keys)
        self.assertIsNotNone(stats.url_base)
        self.assertIsNotNone(stats.response_format)

    def test_2(self):
        """ make sure we can build the url authentication params """
        stats = Stats(self.sport)
        url_auth_params = stats.get_url_auth_params()
        print(url_auth_params)
        self.assertIsNotNone(url_auth_params)


class StatsProjectionsWeekTest(AbstractTest):
    def setUp(self):
        self.sport = 'nfl'

    def test_1(self):
        stats = Stats(self.sport)


# TODO:(zach) Test StatsCom.Player
# class StatscomPlayerTest(AbstractTest):
#     def setUp(self):
#         self.scoring_system_stat_points = StatPoint.objects.filter(score_system__sport='nba')
#         print(self.scoring_system_stat_points)
