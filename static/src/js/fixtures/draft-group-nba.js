'use strict';


module.exports = [{
  pattern: '/draft-group/',

  fixtures: function() {
    return {
      "players": [
        {
          "player_id": 190,
          "first_name": "Isaiah",
          "last_name": "Thomas",
          "salary": 11300,
          "start": "2015-03-21T00:30:00Z",
          "position": "PG",
          "team_alias": "BOS"
        },
        {
          "player_id": 477,
          "first_name": "Ray",
          "last_name": "McCallum",
          "salary": 11300,
          "start": "2015-03-21T00:30:00Z",
          "position": "PG",
          "team_alias": "SAS"
        },
        {
          "player_id": 105,
          "first_name": "Kemba",
          "last_name": "Walker",
          "salary": 11000,
          "start": "2015-03-21T02:00:00Z",
          "position": "PG",
          "team_alias": "CHA"
        },
        {
          "player_id": 244,
          "first_name": "Stephen",
          "last_name": "Curry",
          "salary": 19500,
          "start": "2015-03-21T02:30:00Z",
          "position": "PG",
          "team_alias": "GSW"
        },
        {
          "player_id": 315,
          "first_name": "Chris",
          "last_name": "Paul",
          "salary": 16400,
          "start": "2015-03-21T02:30:00Z",
          "position": "PG",
          "team_alias": "LAC"
        },
        {
          "player_id": 118,
          "first_name": "Derrick",
          "last_name": "Rose",
          "salary": 16000,
          "start": "2015-03-21T00:00:00Z",
          "position": "PG",
          "team_alias": "CHI"
        },
        {
          "player_id": 346,
          "first_name": "George",
          "last_name": "Hill",
          "salary": 15600,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "IND"
        },
        {
          "player_id": 137,
          "first_name": "Jeff",
          "last_name": "Teague",
          "salary": 14500,
          "start": "2015-03-21T00:00:00Z",
          "position": "PG",
          "team_alias": "ATL"
        },
        {
          "player_id": 324,
          "first_name": "Damian",
          "last_name": "Lillard",
          "salary": 14000,
          "start": "2015-03-20T23:00:00Z",
          "position": "PG",
          "team_alias": "POR"
        },
        {
          "player_id": 34,
          "first_name": "Russell",
          "last_name": "Westbrook",
          "salary": 24300,
          "start": "2015-03-21T00:00:00Z",
          "position": "PG",
          "team_alias": "OKC"
        },
        {
          "player_id": 219,
          "first_name": "Elfrid",
          "last_name": "Payton",
          "salary": 13900,
          "start": "2015-03-20T23:00:00Z",
          "position": "PG",
          "team_alias": "ORL"
        },
        {
          "player_id": 345,
          "first_name": "John",
          "last_name": "Wall",
          "salary": 12700,
          "start": "2015-03-21T02:30:00Z",
          "position": "PG",
          "team_alias": "WAS"
        },
        {
          "player_id": 408,
          "first_name": "Michael",
          "last_name": "Carter-Williams",
          "salary": 12300,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "MIL"
        },
        {
          "player_id": 394,
          "first_name": "Langston",
          "last_name": "Galloway",
          "salary": 12000,
          "start": "2015-03-20T23:00:00Z",
          "position": "PG",
          "team_alias": "NYK"
        },
        {
          "player_id": 208,
          "first_name": "Kyle",
          "last_name": "Lowry",
          "salary": 11800,
          "start": "2015-03-21T00:00:00Z",
          "position": "PG",
          "team_alias": "TOR"
        },
        {
          "player_id": 297,
          "first_name": "Deron",
          "last_name": "Williams",
          "salary": 11800,
          "start": "2015-03-21T00:30:00Z",
          "position": "PG",
          "team_alias": "DAL"
        }
      ],
      "end": "2015-03-21T04:00:00Z",
      "pk": 1,
      "sport": "nba",
      "start": "2015-03-20T23:00:00Z"
    };
  },

  // `match`: result of the resolution of the regular expression
  // `data`: data returns by `fixtures` attribute
  callback: function (match, data) {
    return {
      body: data
    };
  }

}];
