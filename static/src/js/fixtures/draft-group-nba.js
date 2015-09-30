'use strict';


module.exports = [{
  pattern: '/draft-group/',

  fixtures: function() {
    return {
      "pk": 1,
      "start": "2015-03-20T23:00:00Z",
      "end": "2015-03-21T04:00:00Z",
      "sport": "nba",
      "players": [
        {
          "player_id": 34,
          "name": "Russell Westbrook",
          "salary": 24300,
          "start": "2015-03-21T00:00:00Z",
          "position": "PG",
          "team_alias": "OKC"
        },
        {
          "player_id": 244,
          "name": "Stephen Curry",
          "salary": 19500,
          "start": "2015-03-21T02:30:00Z",
          "position": "PG",
          "team_alias": "GSW"
        },
        {
          "player_id": 315,
          "name": "Chris Paul",
          "salary": 16400,
          "start": "2015-03-21T02:30:00Z",
          "position": "PG",
          "team_alias": "LAC"
        },
        {
          "player_id": 118,
          "name": "Derrick Rose",
          "salary": 16000,
          "start": "2015-03-21T00:00:00Z",
          "position": "PG",
          "team_alias": "CHI"
        },
        {
          "player_id": 346,
          "name": "George Hill",
          "salary": 15600,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "IND"
        },
        {
          "player_id": 137,
          "name": "Jeff Teague",
          "salary": 14500,
          "start": "2015-03-21T00:00:00Z",
          "position": "PG",
          "team_alias": "ATL"
        },
        {
          "player_id": 324,
          "name": "Damian Lillard",
          "salary": 14000,
          "start": "2015-03-20T23:00:00Z",
          "position": "PG",
          "team_alias": "POR"
        },
        {
          "player_id": 219,
          "name": "Elfrid Payton",
          "salary": 13900,
          "start": "2015-03-20T23:00:00Z",
          "position": "PG",
          "team_alias": "ORL"
        },
        {
          "player_id": 345,
          "name": "John Wall",
          "salary": 12700,
          "start": "2015-03-21T02:30:00Z",
          "position": "PG",
          "team_alias": "WAS"
        },
        {
          "player_id": 408,
          "name": "Michael Carter-Williams",
          "salary": 12300,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "MIL"
        },
        {
          "player_id": 394,
          "name": "Langston Galloway",
          "salary": 12000,
          "start": "2015-03-20T23:00:00Z",
          "position": "PG",
          "team_alias": "NYK"
        },
        {
          "player_id": 208,
          "name": "Kyle Lowry",
          "salary": 11800,
          "start": "2015-03-21T00:00:00Z",
          "position": "PG",
          "team_alias": "TOR"
        },
        {
          "player_id": 297,
          "name": "Deron Williams",
          "salary": 11800,
          "start": "2015-03-21T00:30:00Z",
          "position": "PG",
          "team_alias": "DAL"
        },
        {
          "player_id": 190,
          "name": "Isaiah Thomas",
          "salary": 11300,
          "start": "2015-03-21T00:30:00Z",
          "position": "PG",
          "team_alias": "BOS"
        },
        {
          "player_id": 477,
          "name": "Ray McCallum",
          "salary": 11300,
          "start": "2015-03-21T00:30:00Z",
          "position": "PG",
          "team_alias": "SAS"
        },
        {
          "player_id": 105,
          "name": "Kemba Walker",
          "salary": 11000,
          "start": "2015-03-21T02:00:00Z",
          "position": "PG",
          "team_alias": "CHA"
        },
        {
          "player_id": 301,
          "name": "J.J. Barea",
          "salary": 10600,
          "start": "2015-03-21T00:30:00Z",
          "position": "PG",
          "team_alias": "DAL"
        },
        {
          "player_id": 90,
          "name": "Jarrett Jack",
          "salary": 10300,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "BKN"
        },
        {
          "player_id": 79,
          "name": "Shane Larkin",
          "salary": 8900,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "BKN"
        },
        {
          "player_id": 478,
          "name": "Tony Parker",
          "salary": 8800,
          "start": "2015-03-21T00:30:00Z",
          "position": "PG",
          "team_alias": "SAS"
        },
        {
          "player_id": 357,
          "name": "Rodney Stuckey",
          "salary": 8800,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "IND"
        },
        {
          "player_id": 431,
          "name": "Mike Conley",
          "salary": 8500,
          "start": "2015-03-21T00:30:00Z",
          "position": "PG",
          "team_alias": "MEM"
        },
        {
          "player_id": 187,
          "name": "Marcus Smart",
          "salary": 8200,
          "start": "2015-03-21T00:30:00Z",
          "position": "PG",
          "team_alias": "BOS"
        },
        {
          "player_id": 38,
          "name": "Ish Smith",
          "salary": 8100,
          "start": "2015-03-21T00:00:00Z",
          "position": "PG",
          "team_alias": "OKC"
        },
        {
          "player_id": 188,
          "name": "Avery Bradley",
          "salary": 7800,
          "start": "2015-03-21T00:30:00Z",
          "position": "PG",
          "team_alias": "BOS"
        },
        {
          "player_id": 420,
          "name": "Greivis Vasquez",
          "salary": 7700,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "MIL"
        },
        {
          "player_id": 113,
          "name": "Brian Roberts",
          "salary": 6900,
          "start": "2015-03-21T02:00:00Z",
          "position": "PG",
          "team_alias": "CHA"
        },
        {
          "player_id": 139,
          "name": "Dennis Schroder",
          "salary": 6800,
          "start": "2015-03-21T00:00:00Z",
          "position": "PG",
          "team_alias": "ATL"
        },
        {
          "player_id": 476,
          "name": "Patty Mills",
          "salary": 6500,
          "start": "2015-03-21T00:30:00Z",
          "position": "PG",
          "team_alias": "SAS"
        },
        {
          "player_id": 356,
          "name": "Ramon Sessions",
          "salary": 5900,
          "start": "2015-03-21T02:30:00Z",
          "position": "PG",
          "team_alias": "WAS"
        },
        {
          "player_id": 498,
          "name": "Norris Cole",
          "salary": 5800,
          "start": "2015-03-21T02:30:00Z",
          "position": "PG",
          "team_alias": "NOP"
        },
        {
          "player_id": 422,
          "name": "Jerryd Bayless",
          "salary": 5500,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "MIL"
        },
        {
          "player_id": 243,
          "name": "Shaun Livingston",
          "salary": 5100,
          "start": "2015-03-21T02:30:00Z",
          "position": "PG",
          "team_alias": "GSW"
        },
        {
          "player_id": 55,
          "name": "Erick Green",
          "salary": 5000,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "DEN"
        },
        {
          "player_id": 456,
          "name": "Jrue Holiday",
          "salary": 4700,
          "start": "2015-03-21T02:30:00Z",
          "position": "PG",
          "team_alias": "NOP"
        },
        {
          "player_id": 81,
          "name": "Rajon Rondo",
          "salary": 4600,
          "start": "2015-03-21T02:00:00Z",
          "position": "PG",
          "team_alias": "SAC"
        },
        {
          "player_id": 374,
          "name": "Mo Williams",
          "salary": 4500,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "CLE"
        },
        {
          "player_id": 173,
          "name": "Mario Chalmers",
          "salary": 4400,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "MIA"
        },
        {
          "player_id": 96,
          "name": "D.J. Augustin",
          "salary": 4400,
          "start": "2015-03-21T00:00:00Z",
          "position": "PG",
          "team_alias": "OKC"
        },
        {
          "player_id": 296,
          "name": "Raymond Felton",
          "salary": 4100,
          "start": "2015-03-21T00:30:00Z",
          "position": "PG",
          "team_alias": "DAL"
        },
        {
          "player_id": 441,
          "name": "Beno Udrih",
          "salary": 4000,
          "start": "2015-03-21T00:30:00Z",
          "position": "PG",
          "team_alias": "MEM"
        },
        {
          "player_id": 289,
          "name": "Devin Harris",
          "salary": 3800,
          "start": "2015-03-21T00:30:00Z",
          "position": "PG",
          "team_alias": "DAL"
        },
        {
          "player_id": 372,
          "name": "Kyrie Irving",
          "salary": 3700,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "CLE"
        },
        {
          "player_id": 144,
          "name": "Shelvin Mack",
          "salary": 3700,
          "start": "2015-03-21T00:00:00Z",
          "position": "PG",
          "team_alias": "ATL"
        },
        {
          "player_id": 91,
          "name": "Darren Collison",
          "salary": 3000,
          "start": "2015-03-21T02:00:00Z",
          "position": "PG",
          "team_alias": "SAC"
        },
        {
          "player_id": 500,
          "name": "Luke Ridnour",
          "salary": 3000,
          "start": "2015-03-21T00:00:00Z",
          "position": "PG",
          "team_alias": "TOR"
        },
        {
          "player_id": 11,
          "name": "Jeremy Lin",
          "salary": 3000,
          "start": "2015-03-21T02:00:00Z",
          "position": "PG",
          "team_alias": "CHA"
        },
        {
          "player_id": 411,
          "name": "Jorge Gutierrez",
          "salary": 3000,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "MIL"
        },
        {
          "player_id": 215,
          "name": "Shabazz Napier",
          "salary": 3000,
          "start": "2015-03-20T23:00:00Z",
          "position": "PG",
          "team_alias": "ORL"
        },
        {
          "player_id": 75,
          "name": "David Stockton",
          "salary": 3000,
          "start": "2015-03-21T02:00:00Z",
          "position": "PG",
          "team_alias": "SAC"
        },
        {
          "player_id": 313,
          "name": "Pablo Prigioni",
          "salary": 3000,
          "start": "2015-03-21T02:30:00Z",
          "position": "PG",
          "team_alias": "LAC"
        },
        {
          "player_id": 428,
          "name": "Russ Smith",
          "salary": 3000,
          "start": "2015-03-21T00:30:00Z",
          "position": "PG",
          "team_alias": "MEM"
        },
        {
          "player_id": 126,
          "name": "Aaron Brooks",
          "salary": 3000,
          "start": "2015-03-21T00:00:00Z",
          "position": "PG",
          "team_alias": "CHI"
        },
        {
          "player_id": 409,
          "name": "Tyler Ennis",
          "salary": 3000,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "MIL"
        },
        {
          "player_id": 200,
          "name": "Cory Joseph",
          "salary": 3000,
          "start": "2015-03-21T00:00:00Z",
          "position": "PG",
          "team_alias": "TOR"
        },
        {
          "player_id": 423,
          "name": "Jameer Nelson",
          "salary": 3000,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "DEN"
        },
        {
          "player_id": 344,
          "name": "Toney Douglas",
          "salary": 3000,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "IND"
        },
        {
          "player_id": 473,
          "name": "Jimmer Fredette",
          "salary": 3000,
          "start": "2015-03-21T00:30:00Z",
          "position": "PG",
          "team_alias": "SAS"
        },
        {
          "player_id": 509,
          "name": "Alexey Shved",
          "salary": 3000,
          "start": "2015-03-20T23:00:00Z",
          "position": "PG",
          "team_alias": "NYK"
        },
        {
          "player_id": 21,
          "name": "Isaiah Canaan",
          "salary": 3000,
          "start": "2015-03-20T23:00:00Z",
          "position": "PG",
          "team_alias": "PHI"
        },
        {
          "player_id": 221,
          "name": "C.J. Watson",
          "salary": 3000,
          "start": "2015-03-20T23:00:00Z",
          "position": "PG",
          "team_alias": "ORL"
        },
        {
          "player_id": 62,
          "name": "Donald Sloan",
          "salary": 3000,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "BKN"
        },
        {
          "player_id": 398,
          "name": "Jose Calderon",
          "salary": 3000,
          "start": "2015-03-20T23:00:00Z",
          "position": "PG",
          "team_alias": "NYK"
        },
        {
          "player_id": 333,
          "name": "Phil Pressey",
          "salary": 3000,
          "start": "2015-03-20T23:00:00Z",
          "position": "PG",
          "team_alias": "POR"
        },
        {
          "player_id": 49,
          "name": "Nate Robinson",
          "salary": 3000,
          "start": "2015-03-20T23:30:00Z",
          "position": "PG",
          "team_alias": "DEN"
        },
        {
          "player_id": 65,
          "name": "Seth Curry",
          "salary": 3000,
          "start": "2015-03-21T02:00:00Z",
          "position": "PG",
          "team_alias": "SAC"
        },
        {
          "player_id": 43,
          "name": "Sebastian Telfair",
          "salary": 3000,
          "start": "2015-03-21T00:00:00Z",
          "position": "PG",
          "team_alias": "OKC"
        },
        {
          "player_id": 319,
          "name": "Tim Frazier",
          "salary": 3000,
          "start": "2015-03-20T23:00:00Z",
          "position": "PG",
          "team_alias": "POR"
        },
        {
          "player_id": 363,
          "name": "Bradley Beal",
          "salary": 14100,
          "start": "2015-03-21T02:30:00Z",
          "position": "SG",
          "team_alias": "WAS"
        },
        {
          "player_id": 114,
          "name": "Jimmy Butler",
          "salary": 13200,
          "start": "2015-03-21T00:00:00Z",
          "position": "SG",
          "team_alias": "CHI"
        },
        {
          "player_id": 228,
          "name": "Victor Oladipo",
          "salary": 11800,
          "start": "2015-03-20T23:00:00Z",
          "position": "SG",
          "team_alias": "ORL"
        },
        {
          "player_id": 335,
          "name": "Monta Ellis",
          "salary": 11600,
          "start": "2015-03-20T23:30:00Z",
          "position": "SG",
          "team_alias": "IND"
        },
        {
          "player_id": 203,
          "name": "DeMar DeRozan",
          "salary": 11400,
          "start": "2015-03-21T00:00:00Z",
          "position": "SG",
          "team_alias": "TOR"
        },
        {
          "player_id": 245,
          "name": "Andre Iguodala",
          "salary": 10900,
          "start": "2015-03-21T02:30:00Z",
          "position": "SG",
          "team_alias": "GSW"
        },
        {
          "player_id": 349,
          "name": "C.J. Miles",
          "salary": 10600,
          "start": "2015-03-20T23:30:00Z",
          "position": "SG",
          "team_alias": "IND"
        },
        {
          "player_id": 463,
          "name": "Tyreke Evans",
          "salary": 10500,
          "start": "2015-03-21T02:30:00Z",
          "position": "SG",
          "team_alias": "NOP"
        },
        {
          "player_id": 93,
          "name": "Dion Waiters",
          "salary": 10000,
          "start": "2015-03-21T00:00:00Z",
          "position": "SG",
          "team_alias": "OKC"
        },
        {
          "player_id": 191,
          "name": "Evan Turner",
          "salary": 9400,
          "start": "2015-03-21T00:30:00Z",
          "position": "SG",
          "team_alias": "BOS"
        },
        {
          "player_id": 71,
          "name": "Ben McLemore",
          "salary": 9300,
          "start": "2015-03-21T02:00:00Z",
          "position": "SG",
          "team_alias": "SAC"
        },
        {
          "player_id": 464,
          "name": "Eric Gordon",
          "salary": 9000,
          "start": "2015-03-21T02:30:00Z",
          "position": "SG",
          "team_alias": "NOP"
        },
        {
          "player_id": 241,
          "name": "Klay Thompson",
          "salary": 8900,
          "start": "2015-03-21T02:30:00Z",
          "position": "SG",
          "team_alias": "GSW"
        },
        {
          "player_id": 163,
          "name": "Dwyane Wade",
          "salary": 8800,
          "start": "2015-03-20T23:30:00Z",
          "position": "SG",
          "team_alias": "MIA"
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

}];
