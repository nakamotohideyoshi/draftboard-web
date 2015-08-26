"use strict";

module.exports = [
  {
    // regular expression of URL
    pattern: "/contest/lobby/",

    // callback that returns the data
    fixtures: function () {
      return {
        "count": 10,
        "next": null,
        "previous": null,
        "results": [
          {
            "name": "ContestThree",
            "sport": "nfl",
            "status": "scheduled",
            "start": "2015-08-20T23:30:00Z",
            "draft_group": null,
            "max_entries": 1,
            "entries": 2,
            "current_entries": 0,
            "gpp": true,
            "respawn": true
          },
          {
            "name": "ContestFour",
            "sport": "nfl",
            "status": "scheduled",
            "start": "2015-08-20T23:00:00Z",
            "draft_group": null,
            "max_entries": 1,
            "entries": 2,
            "current_entries": 0,
            "gpp": true,
            "respawn": false
          },
          {
            "name": "ContestFive",
            "sport": "nfl",
            "status": "scheduled",
            "start": "2015-08-21T23:30:00Z",
            "draft_group": null,
            "max_entries": 1,
            "entries": 2,
            "current_entries": 0,
            "gpp": false,
            "respawn": true
          },
          {
            "name": "ContestSix",
            "sport": "nfl",
            "status": "scheduled",
            "start": "2015-08-22T23:00:00Z",
            "draft_group": null,
            "max_entries": 1,
            "entries": 2,
            "current_entries": 0,
            "gpp": false,
            "respawn": true
          },
          {
            "name": "MLB Head-to-Head",
            "sport": "mlb",
            "status": "reservable",
            "start": "2015-08-19T02:00:00Z",
            "draft_group": null,
            "max_entries": 1,
            "entries": 2,
            "current_entries": 0,
            "gpp": false,
            "respawn": true
          },
          {
            "name": "NFL Test Early Reg",
            "sport": "nfl",
            "status": "scheduled",
            "start": "2015-08-20T23:30:00Z",
            "draft_group": null,
            "max_entries": 1,
            "entries": 2,
            "current_entries": 0,
            "gpp": false,
            "respawn": true
          },
          {
            "name": "NFL NoEarlyReg",
            "sport": "nfl",
            "status": "scheduled",
            "start": "2015-08-20T23:30:00Z",
            "draft_group": null,
            "max_entries": 1,
            "entries": 2,
            "current_entries": 0,
            "gpp": false,
            "respawn": true
          },
          {
            "name": "NFL Test AutoCreateDraftGroup",
            "sport": "nfl",
            "status": "scheduled",
            "start": "2015-08-20T23:30:00Z",
            "draft_group": 5,
            "max_entries": 1,
            "entries": 2,
            "current_entries": 1,
            "gpp": false,
            "respawn": true
          },
          {
            "name": "NFL Test AutoCreateDraftGroup",
            "sport": "nfl",
            "status": "scheduled",
            "start": "2015-08-20T23:30:00Z",
            "draft_group": 5,
            "max_entries": 1,
            "entries": 2,
            "current_entries": 0,
            "gpp": false,
            "respawn": true
          },
          {
            "name": "NFL Test AutoCreateDraftGroup",
            "sport": "nfl",
            "status": "scheduled",
            "start": "2015-08-20T23:30:00Z",
            "draft_group": 5,
            "max_entries": 1,
            "entries": 2,
            "current_entries": 0,
            "gpp": false,
            "respawn": true
          }
        ]
      };
    },

    // `match`: result of the resolution of the regular expression
    // `data`: data returns by `fixtures` attribute
    callback: function (match, data) {
      return {
        body: data
      };
    }
  }
];
