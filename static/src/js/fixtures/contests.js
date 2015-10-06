"use strict";

module.exports = [
  {
    // regular expression of URL
    pattern: "/contest/lobby/",

    // callback that returns the data
    fixtures: function () {
      return {
        "count": 3,
        "next": null,
        "previous": null,
        "results": [
          {
            "id": 1,
            "name": "$1 NBA Head-to-Head",
            "sport": "nba",
            "status": "scheduled",
            "start": "2015-03-20T23:00:00Z",
            "buyin": 1,
            "draft_group": 1,
            "max_entries": 1,
            "prize_structure": 3,
            "prize_pool": 1.8,
            "entries": 2,
            "current_entries": 2,
            "gpp": false,
            "doubleup": false,
            "respawn": true
          },
          {
            "id": 2,
            "name": "$5 NBA Head-to-Head",
            "sport": "nba",
            "status": "scheduled",
            "start": "2015-03-20T23:00:00Z",
            "buyin": 5,
            "draft_group": 1,
            "max_entries": 1,
            "prize_structure": 4,
            "prize_pool": 9,
            "entries": 2,
            "current_entries": 2,
            "gpp": false,
            "doubleup": false,
            "respawn": true
          },
          {
            "id": 3,
            "name": "$100 NBA Head-to-Head",
            "sport": "nba",
            "status": "scheduled",
            "start": "2015-03-20T23:00:00Z",
            "buyin": 100,
            "draft_group": 1,
            "max_entries": 1,
            "prize_structure": 5,
            "prize_pool": 180,
            "entries": 2,
            "current_entries": 2,
            "gpp": false,
            "doubleup": false,
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
