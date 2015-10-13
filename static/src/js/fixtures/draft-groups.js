'use strict';

module.exports = [
  {
    // regular expression of URL
    pattern: "/draft-group/upcoming",

    // callback that returns the data
    fixtures: function () {
      return [
        {
          "count": 3,
          "next": null,
          "previous": null,
          "results": [
            {
              "pk": 1,
              "start": "2016-03-20T20:56:25Z",
              "sport": "nba",
              "num_games": 0,
              "category": null
            },
            {
              "pk": 4,
              "start": "2016-03-20T20:56:25Z",
              "sport": "nba",
              "num_games": 0,
              "category": null
            },
            {
              "pk": 10,
              "start": "2016-03-20T20:56:25Z",
              "sport": "nba",
              "num_games": 0,
              "category": null
            }
          ]
        }

      ];
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
