"use strict";

module.exports = [
  {
    // regular expression of URL
    pattern: "/live/lineup",

    // callback that returns the data
    fixtures: function () {
      return [
        {id: '8ec91366-faea-4196-bbfd-b8fab7434795', "player": "Kyle Korver", "position": "PG", "photo": "", "status": "", "points": 6},
        {id: '4e152a06-673e-4701-b115-aa7e2cd00d2d', "player": "Dwight Howard", "position": "PG", "photo": "", "status": "", "points": 15.5},
        {id: 'cbb8c112-4d7d-11e5-885d-feff819cdc9e', "player": "Giannis Antetokounmpo", "position": "PG", "photo": "", "status": "", "points": "23.5"},
        {id: 'df187a36-4d7d-11e5-885d-feff819cdc9f', "player": "Michael Jordan", "position": "PG", "photo": "", "status": "", "points": 8},
        {id: 'df187cd4-4d7d-11e5-885d-feff819cdc9g', "player": "Kobe Bryant", "position": "PG", "photo": "", "status": "", "points": 12}
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
