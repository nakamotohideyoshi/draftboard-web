#
# tests.py

import json
from test.classes import (
    AbstractTest,
)
from swish.classes import (
    UpdateData,
    SwishAnalytics,
)
from util.utctime import UtcTime


class UpdateDataTest(AbstractTest):
    def setUp(self):
        super().setUp()

    def test_1(self):
        data_str = """{
      "Id": 260283,
      "DateTime": "2017-03-12T06:40:47-07:00",
      "Priority": 3,
      "Headline": "Double-doubles in Saturday loss",
      "Notes": "Pachulia offered 11 points (4-9 FG, 3-5 FT), 12 rebounds, two assists, one steal and one block over 20 minutes in Saturday's 107-85 loss to the Spurs.",
      "Analysis": "The veteran big man was one of only two current Warriors starters to take the floor Saturday, and he responded with his best scoring and rebound totals in six March contests. The final line also represented Pachulia's first double-double since Dec. 22 and just his third of the season overall. Despite the one-night boost in fantasy production, Pachulia's owners should expect his numbers to see a slight downturn any time the entire first unit is active.",
      "Injury": {
        "Status": null,
        "Type": null,
        "Location": null,
        "Detail": null,
        "Side": null,
        "ReturnDate": null
      },
      "Player": {
        "Id": 2391,
        "SportsDataId": "48a2b27a-87a2-4051-ad03-c95a026ca772",
        "FirstName": "Zaza",
        "LastName": "Pachulia",
        "Position": "C         ",
        "InjuryStatus": null,
        "Link": "http://www.rotowire.com/basketball/player.htm?id=2391"
      },
      "Team": {
        "Id": 22,
        "Code": "GS",
        "SportsDataId": "583ec825-fb46-11e1-82cb-f4ce4684ea4c",
        "Name": "Golden State Warriors",
        "Nickname": "Warriors"
      }
    }"""
        data = json.loads(data_str)
        ud = UpdateData(data)
        updated_at = ud.get_updated_at()
        self.assertEquals(updated_at.tzinfo, UtcTime.TZ_UTC)
        self.assertEquals(ud.get_update_id(), str(data.get('Id')))

        # get a random field and make sure get_field() works
        self.assertIsNotNone(ud.get_player_name())


class SwishTest(AbstractTest):
    def setUp(self):
        super().setUp()

    def test_1(self):
        data = """{
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
        }"""
        data = json.loads(data)
        ud = UpdateData(data)
        self.assertIsNotNone(ud)

    def test_2(self):
        nfl = SwishAnalytics('nfl')
        updates = nfl.get_updates()  # returns a list of UpdateData objects
        self.assertIsNotNone(updates)
