"use strict";

module.exports = [
  {
    // regular expression of URL
    pattern: "/live/history",

    // callback that returns the data
    fixtures: function () {
      return [
        {id: 0, "player": "Lebron James", "action": "Rebound", "points": "+1", "x": 300, "y": 400},
        {id: 1, "player": "Demarcus Cousins", "action": "Steal", "points": "+1", "x": 300, "y": 400},
        {id: 2, "player": "Kyle Korver", "action": "3 pointer", "points": "+3", "x": 300, "y": 400},
        {id: 3, "player": "Dwight Howard", "action": "Free throw", "points": "+2"},
        {id: 4, "player": "Giannis Antetokounmpo", "action": "Winning", "points": "+1"}
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
