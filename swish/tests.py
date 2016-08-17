#
# tests.py

from django.test import TestCase
from test.classes import (
    AbstractTest,
)
from swish.classes import (
    SwishAnalytics,
    SwishNFL,
)

class SwishTest(AbstractTest):

    def setUp(self):
        self.data_1 = {
            "status": true,
            "sport": "nfl",
            "endpoint": "/nfl/players/injuries",
            "request": {
            "team": [
              "ne"
            ],
            "sport": [
              "2"
            ],
            "start": [
              "2016-08-15"
            ],
            "end": [
              "2016-08-16"
            ]
            },
            "error": {
            "status": false
            },
            "data": {
            "status": true,
            "count": 2,
            "results": [
                {
                    "id": 295404,
                    "date": "2016-08-16",
                    "time": "14:05:05",
                    "datetime": "2016-08-16 14:05:05",
                    "datetimeUtc": "2016-08-16 18:05:05",
                    "sportId": 2,
                    "sport": "NFL",
                    "teamId": 348,
                    "teamAbbr": "NE",
                    "playerId": 600899,
                    "playerName": "Joe Thuney",
                    "position": "G",
                    "text": "New England Patriots OG Joe Thuney was deemed the best left guard on the roster by Jeff Howe, of the Boston Herald. Thuney is a third-round rookie selection who has been running with the first-team offensive line since organized team activities.",
                    "type": null,
                    "sourceId": 3,
                    "source": "usatoday",
                    "sourceOrigin": "Boston Herald - Jeff Howe",
                    "urlOrigin": "http://www.bostonherald.com/sports/patriots/2016/08/smart_money_s_on_patriots_rookie_guard_joe_thuney",
                    "swishStatusId": 2,
                    "swishStatus": "active",
                    "swishStatusConfidence": 0.661068
                },
                {
                    "id": 295266,
                    "date": "2016-08-16",
                    "time": "11:41:54",
                    "datetime": "2016-08-16 11:41:54",
                    "datetimeUtc": "2016-08-16 15:41:54",
                    "sportId": 2,
                    "sport": "NFL",
                    "teamId": 348,
                    "teamAbbr": "NE",
                    "playerId": 381091,
                    "playerName": "Rob Gronkowski",
                    "position": "TE",
                    "text": "Rob Gronkowski: Gronkowski (unspecified injury) did not practice Tuesday,  ESPN's Mike Reiss reports.",
                    "type": null,
                    "sourceId": 5,
                    "source": "rotowire",
                    "sourceOrigin": "rotowire",
                    "urlOrigin": "https://rotowire.com",
                    "swishStatusId": 8,
                    "swishStatus": "day-to-day",
                    "swishStatusConfidence": 0.485586
                }
            ]
          }
        }

    def test_2(self):
        nfl = SwishNFL()
        data = nfl.get_injuries()
        print(str(data))