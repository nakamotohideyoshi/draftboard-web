"use strict";

module.exports = [
  {
    // regular expression of URL
    pattern: "/contests",

    // callback that returns the data
    fixtures: function () {
      return [
        {id: 0, "title": "NBA - Anonymous Head-to-Head", "entries_total": "14,231", "entries_filled": "12,014", "prize": "$350,000"},
        {id: 1, "title": "NBA - $150,000 Championship", "entries_total": "10,001", "entries_filled": "2,993", "prize": "$150,000"},
        {id: 2, "title": "NFL - $50,000 Championship", "entries_total": "10,001", "entries_filled": "2,993", "prize": "2150,000"},
        {id: 3, "title": "NBA - $666 Championship", "entries_total": "2,001", "entries_filled": "2,993", "prize": "$666"},
        {id: 4, "title": "NBA - $9 Sunday game", "entries_total": "54,001", "entries_filled": "2,993", "prize": "$150,000"},
        {id: 5, "title": "NBA - Throwback 1999 thing", "entries_total": "10,001", "entries_filled": "2,993", "prize": "$150,000"}
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
