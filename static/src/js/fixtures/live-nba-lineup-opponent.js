"use strict";

module.exports = [
  {
    // regular expression of URL
    pattern: "/live/lineup",

    // callback that returns the data
    fixtures: function () {
      return [
        {id: 'cbb8bb72-4d7d-11e5-885d-feff819cdc9a', "player": "Lebron James", "position": "PG", "photo": "", "status": "playing", "points": 23.5},
        {id: 'cbb8be42-4d7d-11e5-885d-feff819cdc9b', "player": "Demarcus Cousins", "position": "PG", "photo": "", "status": "", "points": 3},
        {id: 'cbb8bf6e-4d7d-11e5-885d-feff819cdc9h', "player": "Kyle Korver", "position": "PG", "photo": "", "status": "", "points": 6}
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
