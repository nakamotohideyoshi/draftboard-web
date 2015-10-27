"use strict";

module.exports = [
  {
    // regular expression of URL
    pattern: "/live/lineup",

    // callback that returns the data
    fixtures: function () {
      return [
        {id: '8ec91366-faea-4196-bbfd-b8fab7434795', "player": "Lebron James", "position": "PG", "photo": "", "status": "playing", "points": 23.5},
        {id: 'ce8d0944-b277-499e-9701-02a5f1828615', "player": "Demarcus Cousins", "position": "PG", "photo": "", "status": "", "points": 3},
        {id: 'df187cd4-4d7d-11e5-885d-feff819cdc9g', "player": "Kyle Korver", "position": "PG", "photo": "", "status": "", "points": 6}
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
