module.exports = {
  "createLineup": {
    "errorMessage": null,
    "lineupTitle": null,
    "lineup": [],
    "remainingSalary": 0,
    "avgRemainingPlayerSalary": 0,
    "contestSalaryLimit": 0,
    "availablePositions": [],
    "lineupCanBeSaved": false
  },
  "currentDraftGroups": {
    "items": []
  },
  "currentLineups": {
    "updatedAt": 1461560812066,
    "items": {
      "194": {
        "id": 194,
        "draft_group": 127,
        "name": "My Lineup",
        "start": 1458255600000,
        "contests": [
          743,
          742
        ]
      }
    }
  },
  "draftGroupPlayers": {
    "sport": null,
    "id": null,
    "isFetching": false,
    "allPlayers": {},
    "focusedPlayer": null,
    "filters": {
      "orderBy": {
        "property": "salary",
        "direction": "asc"
      },
      "playerSearchFilter": {
        "property": "player.name",
        "match": ""
      },
      "positionFilter": {},
      "teamFilter": {
        "match": [],
        "count": 0
      }
    }
  },
  "entries": {
    "isFetching": false,
    "hasRelatedInfo": false,
    "items": {
      "622": {
        "id": 622,
        "contest": 743,
        "lineup": 194,
        "draft_group": 127,
        "start": "2016-03-17T23:00:00Z",
        "lineup_name": "My Lineup",
        "sport": "nba"
      },
      "623": {
        "id": 623,
        "contest": 742,
        "lineup": 194,
        "draft_group": 127,
        "start": "2016-03-17T23:00:00Z",
        "lineup_name": "My Lineup",
        "sport": "nba"
      }
    },
    "expiresAt": 1458241178527
  },
  "entryRequests": {
    "history": {}
  },
  "fantasyHistory": {},
  "featuredContests": {
    "isFetching": false,
    "banners": []
  },
  "injuries": {},
  "lineupEditRequests": {},
  "live": {
    "watching": {
      "myLineupId": 194,
      "sport": "nba",
      "contestId": null,
      "opponentLineupId": null,
      "draftGroupId": 127
    }
  },
  "liveContests": {
    "742": {
      "id": 742,
      "isFetchingInfo": false,
      "hasRelatedInfo": true,
      "isFetchingLineups": false,
      "info": {
        "id": 742,
        "name": "$2 H2H",
        "sport": "nba",
        "status": "scheduled",
        "start": "2016-03-17T23:00:00Z",
        "buyin": 2,
        "draft_group": 127,
        "max_entries": 1,
        "prize_structure": 2,
        "prize_pool": 3.6,
        "entries": 2,
        "current_entries": 2,
        "gpp": false,
        "doubleup": false,
        "respawn": true
      },
      "expiresAt": 1458327279009,
      "lineupBytes": "",
      "lineups": {}
    },
    "743": {
      "id": 743,
      "isFetchingInfo": false,
      "hasRelatedInfo": true,
      "isFetchingLineups": false,
      "info": {
        "id": 743,
        "name": "$1 H2H",
        "sport": "nba",
        "status": "scheduled",
        "start": "2016-03-17T23:00:00Z",
        "buyin": 1,
        "draft_group": 127,
        "max_entries": 1,
        "prize_structure": 1,
        "prize_pool": 1.8,
        "entries": 2,
        "current_entries": 2,
        "gpp": false,
        "doubleup": false,
        "respawn": true
      },
      "expiresAt": 1458327278970,
      "lineupBytes": "",
      "lineups": {}
    }
  },
  "liveDraftGroups": {
    "127": {
      "boxScores": {},
      "playersInfo": {
        "1": {
          "player_id": 1,
          "name": "Monta Ellis",
          "salary": 6400,
          "start": "2016-03-17T23:00:00Z",
          "position": "SG",
          "fppg": 31.0625,
          "team_alias": "IND",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "0c144557-df20-492c-bf75-be53adf92699"
        },
        "2": {
          "player_id": 2,
          "name": "P.J. Hairston",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 11.375,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "2733be7a-cfc6-4787-8405-371db5af0399"
        },
        "3": {
          "player_id": 3,
          "name": "Jeremy Lin",
          "salary": 4300,
          "start": "2016-03-17T23:30:00Z",
          "position": "PG",
          "fppg": 18.0875,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "287c389a-0499-4f80-ac4f-1a72366af999"
        },
        "4": {
          "player_id": 4,
          "name": "Shayne Whittington",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 4.91666666666667,
          "team_alias": "IND",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "15fc95b7-5f6d-4d71-beda-7d9605a0187b"
        },
        "5": {
          "player_id": 5,
          "name": "Jason Maxiell",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "PF",
          "fppg": 0,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "3919daa3-0cc4-4c44-a3cc-10f5f9c31fe5"
        },
        "6": {
          "player_id": 6,
          "name": "Chase Budinger",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "SF",
          "fppg": 9.4,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "22f65f0b-5ccb-4f72-9bbe-ab383c86fa6b"
        },
        "7": {
          "player_id": 7,
          "name": "Troy Daniels",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "SG",
          "fppg": 11.6,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "562677c1-2a13-4934-a801-a6c88c619e83"
        },
        "8": {
          "player_id": 8,
          "name": "Myles Turner",
          "salary": 5100,
          "start": "2016-03-17T23:00:00Z",
          "position": "C",
          "fppg": 25.125,
          "team_alias": "IND",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "323f9ef8-ecdd-41a7-859e-dd3db48ba913"
        },
        "9": {
          "player_id": 9,
          "name": "Lavoy Allen",
          "salary": 3600,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 15.3625,
          "team_alias": "IND",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "37ad80b2-c9f4-4fde-b462-e1109f249b56"
        },
        "10": {
          "player_id": 10,
          "name": "Elliot Williams",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 4.2,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "6255b242-0bbd-4f05-9c61-f44750061410"
        },
        "11": {
          "player_id": 11,
          "name": "Tyler Hansbrough",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "PF",
          "fppg": 7.7,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "705c7422-c87f-4ab5-85ff-274339193138"
        },
        "13": {
          "player_id": 13,
          "name": "George Hill",
          "salary": 5300,
          "start": "2016-03-17T23:00:00Z",
          "position": "PG",
          "fppg": 25.4625,
          "team_alias": "IND",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "6e566165-6674-4306-9994-470f60720a2c"
        },
        "14": {
          "player_id": 14,
          "name": "Al Jefferson",
          "salary": 4300,
          "start": "2016-03-17T23:30:00Z",
          "position": "C",
          "fppg": 21.8875,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "8bf57b59-a618-4bfa-ae2e-4308b9108606"
        },
        "15": {
          "player_id": 15,
          "name": "Jeremy Lamb",
          "salary": 3600,
          "start": "2016-03-17T23:30:00Z",
          "position": "SG",
          "fppg": 15.125,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "8d80f6fc-a7ac-48cf-bcd8-516d57acbbfe"
        },
        "16": {
          "player_id": 16,
          "name": "C.J. Miles",
          "salary": 3400,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 14.7875,
          "team_alias": "IND",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "732b1bd6-d99a-4971-bc2c-4de4842b4a9a"
        },
        "17": {
          "player_id": 17,
          "name": "Rakeem Christmas",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 1.8125,
          "team_alias": "IND",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "74a7e6ac-58ee-424c-b341-69a69451d481"
        },
        "18": {
          "player_id": 18,
          "name": "Kemba Walker",
          "salary": 8600,
          "start": "2016-03-17T23:30:00Z",
          "position": "PG",
          "fppg": 41.6375,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "a35ee8ed-f1db-4f7e-bb17-f823e8ee0b38"
        },
        "19": {
          "player_id": 19,
          "name": "Glenn Robinson",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 8.95,
          "team_alias": "IND",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "7f462af0-2ac8-4ca5-aa5a-17b37dc5001b"
        },
        "20": {
          "player_id": 20,
          "name": "Nicolas Batum",
          "salary": 6800,
          "start": "2016-03-17T23:30:00Z",
          "position": "SF",
          "fppg": 34.1875,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "a89ac040-715d-4057-8fc0-9d71ad06fa0a"
        },
        "21": {
          "player_id": 21,
          "name": "Joseph Young",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PG",
          "fppg": 10.7875,
          "team_alias": "IND",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "8f8d93e9-c9b4-4820-a546-2de60a00ecad"
        },
        "22": {
          "player_id": 22,
          "name": "Aaron Harrison",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "SF",
          "fppg": 1.90384615384615,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "bff3d21b-880f-43f4-93a2-9fd9a8408716"
        },
        "23": {
          "player_id": 23,
          "name": "Frank Kaminsky",
          "salary": 3200,
          "start": "2016-03-17T23:30:00Z",
          "position": "C",
          "fppg": 15.7625,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "c9b1c381-e0ac-4618-9887-ce3e8993b265"
        },
        "24": {
          "player_id": 24,
          "name": "Jordan Hill",
          "salary": 4100,
          "start": "2016-03-17T23:00:00Z",
          "position": "C",
          "fppg": 20.1625,
          "team_alias": "IND",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "91ec3171-9b9c-48ee-bb52-d075dc41bacb"
        },
        "25": {
          "player_id": 25,
          "name": "Spencer Hawes",
          "salary": 4200,
          "start": "2016-03-17T23:30:00Z",
          "position": "PF",
          "fppg": 19.0375,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ddb5d888-09e5-435a-9009-a2549d8c8382"
        },
        "26": {
          "player_id": 26,
          "name": "Rodney Stuckey",
          "salary": 3300,
          "start": "2016-03-17T23:00:00Z",
          "position": "PG",
          "fppg": 15.225,
          "team_alias": "IND",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "b4a94a3a-8563-49bd-97d2-98161cfb6c8d"
        },
        "27": {
          "player_id": 27,
          "name": "Marvin Williams",
          "salary": 6400,
          "start": "2016-03-17T23:30:00Z",
          "position": "PF",
          "fppg": 30.125,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "e17a3191-b05c-4878-8be6-21028b8ec007"
        },
        "28": {
          "player_id": 28,
          "name": "Ian Mahinmi",
          "salary": 4800,
          "start": "2016-03-17T23:00:00Z",
          "position": "C",
          "fppg": 23.2375,
          "team_alias": "IND",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "d2abbbb8-0d36-49d4-9785-d8664021eb78"
        },
        "30": {
          "player_id": 30,
          "name": "Cody Zeller",
          "salary": 4500,
          "start": "2016-03-17T23:30:00Z",
          "position": "C",
          "fppg": 21.0875,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "e1ce75b8-44ce-4086-b2e1-d2e22efc86ff"
        },
        "31": {
          "player_id": 31,
          "name": "Paul George",
          "salary": 9300,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 42.65,
          "team_alias": "IND",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "db09f372-9a17-4889-add7-bf8a75ab6da6"
        },
        "33": {
          "player_id": 33,
          "name": "Solomon Hill",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 10.625,
          "team_alias": "IND",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "e68c7b19-7c0e-49a6-920c-48668f7ddbcf"
        },
        "35": {
          "player_id": 35,
          "name": "Michael Kidd-Gilchrist",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "SF",
          "fppg": 24.1071428571429,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ea8a18e4-1341-48f1-b75d-5bbac8d789d4"
        },
        "36": {
          "player_id": 36,
          "name": "C.J. Fair",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 1.7125,
          "team_alias": "IND",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ecafe060-0a4f-4740-9e21-03715d653327"
        },
        "38": {
          "player_id": 38,
          "name": "Brian Roberts",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "PG",
          "fppg": 9.325,
          "team_alias": "POR",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "eb1f731e-653d-435f-8ccb-3a7f15f84116"
        },
        "54": {
          "player_id": 54,
          "name": "Rasual Butler",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "SF",
          "fppg": 9.2875,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "007a5e3c-978e-49e3-af38-7a4d9354cf21"
        },
        "55": {
          "player_id": 55,
          "name": "Tim Duncan",
          "salary": 4700,
          "start": "2016-03-18T00:30:00Z",
          "position": "C",
          "fppg": 23.1375,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "1f9d116b-7c1b-4d1a-bf02-59ba4b22092e"
        },
        "56": {
          "player_id": 56,
          "name": "David West",
          "salary": 3800,
          "start": "2016-03-18T00:30:00Z",
          "position": "PF",
          "fppg": 17.4,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "2365e884-e0d9-43a4-8efe-a4bd9a14329a"
        },
        "57": {
          "player_id": 57,
          "name": "Boban Marjanovic",
          "salary": 3300,
          "start": "2016-03-18T00:30:00Z",
          "position": "C",
          "fppg": 15.7625,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "24c17409-ac10-4859-be6c-59d6cc6b5810"
        },
        "58": {
          "player_id": 58,
          "name": "Kyle Anderson",
          "salary": 3600,
          "start": "2016-03-18T00:30:00Z",
          "position": "SF",
          "fppg": 16.5,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "2e49c27a-06c5-4c4a-87fd-69840b783947"
        },
        "59": {
          "player_id": 59,
          "name": "LaMarcus Aldridge",
          "salary": 7400,
          "start": "2016-03-18T00:30:00Z",
          "position": "PF",
          "fppg": 38.05,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "3157a0b5-1b4c-46d1-934c-ac2df3810950"
        },
        "60": {
          "player_id": 60,
          "name": "Keifer Sykes",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "PG",
          "fppg": 0.125,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "4173ac8e-175c-4ea2-b531-f9e5fe8aa37e"
        },
        "61": {
          "player_id": 61,
          "name": "Youssou Ndoye",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "C",
          "fppg": 1.225,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "41857ce7-febe-4a63-9835-6f3461336945"
        },
        "62": {
          "player_id": 62,
          "name": "Deshaun Thomas",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "SF",
          "fppg": 0.775,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "4237e763-c872-4db0-8744-024e695a666e"
        },
        "63": {
          "player_id": 63,
          "name": "Jonathon Simmons",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "SG",
          "fppg": 10.3125,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "44733f78-d10e-4668-ae99-8de54b69b32a"
        },
        "64": {
          "player_id": 64,
          "name": "Bryce Cotton",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "PG",
          "fppg": 6,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "02259413-3191-4057-9473-caa3268fb189"
        },
        "65": {
          "player_id": 65,
          "name": "Danny Green",
          "salary": 4700,
          "start": "2016-03-18T00:30:00Z",
          "position": "SG",
          "fppg": 22.0375,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "478e5e20-5d59-402f-a901-b8e78f3e9508"
        },
        "66": {
          "player_id": 66,
          "name": "Boris Diaw",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "PF",
          "fppg": 12.4625,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "52eba610-a87e-4c05-bb2d-dfb71bb32d03"
        },
        "67": {
          "player_id": 67,
          "name": "Dante Exum",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "PG",
          "fppg": 0,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "0d187d04-4cd9-44b3-9a29-408fac5b011e"
        },
        "69": {
          "player_id": 69,
          "name": "J.J. O'Brien",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "SF",
          "fppg": 3.25,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "2ec0dd5b-2bd3-47f8-936c-bc23859a2686"
        },
        "70": {
          "player_id": 70,
          "name": "Matt Bonner",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "C",
          "fppg": 7.30357142857143,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "8da88be3-bc4a-406a-9e16-147bdac064eb"
        },
        "72": {
          "player_id": 72,
          "name": "Manu Ginobili",
          "salary": 4600,
          "start": "2016-03-18T00:30:00Z",
          "position": "SG",
          "fppg": 20.2875,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "95ca0a9b-4fd0-4ae8-8714-247b57fb84ea"
        },
        "73": {
          "player_id": 73,
          "name": "Rudy Gobert",
          "salary": 7100,
          "start": "2016-03-18T01:00:00Z",
          "position": "C",
          "fppg": 31.9125,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "37fbc3a5-0d10-4e22-803b-baa2ea0cdb12"
        },
        "74": {
          "player_id": 74,
          "name": "Patty Mills",
          "salary": 4400,
          "start": "2016-03-18T00:30:00Z",
          "position": "PG",
          "fppg": 21.6625,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "9e917c97-5227-4581-9ab5-2dd07a7187ef"
        },
        "75": {
          "player_id": 75,
          "name": "Treveon Graham",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "SG",
          "fppg": 0.25,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "3f170fb8-2633-481f-bc63-0bce20b37557"
        },
        "76": {
          "player_id": 76,
          "name": "Ray McCallum",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 10.0972222222222,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "a90a5752-ae6b-491a-8ff6-43acd5b12aa9"
        },
        "77": {
          "player_id": 77,
          "name": "Elijah Millsap",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "SF",
          "fppg": 6.95,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "46bb99cd-123f-4d42-bfcb-ad2891df2e0e"
        },
        "78": {
          "player_id": 78,
          "name": "Tony Parker",
          "salary": 4600,
          "start": "2016-03-18T00:30:00Z",
          "position": "PG",
          "fppg": 21.7625,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "b1b2d578-44df-4e05-9884-31dd89e82cf0"
        },
        "79": {
          "player_id": 79,
          "name": "Trey Lyles",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "PF",
          "fppg": 9.85,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "55f10af0-4b71-4693-aa82-435e958ab560"
        },
        "80": {
          "player_id": 80,
          "name": "Reggie Williams",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "SF",
          "fppg": 2.5375,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "b1d48323-0ef7-478e-a10c-cbd9f2e3f1df"
        },
        "81": {
          "player_id": 81,
          "name": "Trey Burke",
          "salary": 3200,
          "start": "2016-03-18T01:00:00Z",
          "position": "PG",
          "fppg": 14.425,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "572261e2-8ad9-4198-969d-16cad41fdef3"
        },
        "82": {
          "player_id": 82,
          "name": "Kawhi Leonard",
          "salary": 8100,
          "start": "2016-03-18T00:30:00Z",
          "position": "SF",
          "fppg": 39.15,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "c12fb587-fc86-471c-8a84-19caf31325ce"
        },
        "83": {
          "player_id": 83,
          "name": "Joe Ingles",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "SF",
          "fppg": 8.5125,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "5b297372-b2af-445e-a4bc-777982dbc1e3"
        },
        "85": {
          "player_id": 85,
          "name": "Jeff Withey",
          "salary": 3100,
          "start": "2016-03-18T01:00:00Z",
          "position": "C",
          "fppg": 13.2,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "6c2124da-2ab9-4cad-bd88-224c87e6e6f3"
        },
        "87": {
          "player_id": 87,
          "name": "Alec Burks",
          "salary": 4600,
          "start": "2016-03-18T01:00:00Z",
          "position": "SG",
          "fppg": 22.8125,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "73fcf334-2088-4862-b83b-66eae415cf87"
        },
        "89": {
          "player_id": 89,
          "name": "Trevor Booker",
          "salary": 3600,
          "start": "2016-03-18T01:00:00Z",
          "position": "PF",
          "fppg": 15.8875,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "86da224d-e103-412a-8406-1ca8976726e7"
        },
        "91": {
          "player_id": 91,
          "name": "Raulzinho Neto",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "PG",
          "fppg": 13.7125,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "8e7ffd66-f779-418c-bf18-b9f746a1c5fe"
        },
        "93": {
          "player_id": 93,
          "name": "Gordon Hayward",
          "salary": 7900,
          "start": "2016-03-18T01:00:00Z",
          "position": "SF",
          "fppg": 35.2,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "a1ddebee-950c-497d-9acd-b5061360b464"
        },
        "95": {
          "player_id": 95,
          "name": "Derrick Favors",
          "salary": 7500,
          "start": "2016-03-18T01:00:00Z",
          "position": "PF",
          "fppg": 36.6,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ad354ebb-88e5-46e4-ad79-f7188ee1f6c2"
        },
        "97": {
          "player_id": 97,
          "name": "Olivier Hanlan",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "SG",
          "fppg": 0,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "cc35d329-4c26-44d9-bced-460b008f816e"
        },
        "98": {
          "player_id": 98,
          "name": "Rodney Hood",
          "salary": 5700,
          "start": "2016-03-18T01:00:00Z",
          "position": "SG",
          "fppg": 27.125,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "d38f8754-7ecb-4791-a350-f67e5c4c785a"
        },
        "101": {
          "player_id": 101,
          "name": "Chris Johnson",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "SF",
          "fppg": 9.1375,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "e3848f10-1f5a-4feb-b2ad-0b4dce9b1209"
        },
        "102": {
          "player_id": 102,
          "name": "Mirza Teletovic",
          "salary": 4200,
          "start": "2016-03-18T01:00:00Z",
          "position": "PF",
          "fppg": 21.2125,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "0abf221a-5fea-4c98-9547-f19e917210be"
        },
        "103": {
          "player_id": 103,
          "name": "Grant Jerrett",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "PF",
          "fppg": 0,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ef0cf1e1-e3e1-48e6-aace-fdfd3c0fb719"
        },
        "105": {
          "player_id": 105,
          "name": "Ronnie Price",
          "salary": 3500,
          "start": "2016-03-18T01:00:00Z",
          "position": "PG",
          "fppg": 18.25,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "1981e577-063e-426a-af2c-adf666403911"
        },
        "107": {
          "player_id": 107,
          "name": "Tibor Pleiss",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "C",
          "fppg": 6.89285714285714,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "f80c054f-53ba-4ca5-9873-6ece55552600"
        },
        "108": {
          "player_id": 108,
          "name": "Markieff Morris",
          "salary": 5900,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 27.2125,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "25c4a949-c310-4bd3-af3f-10441215b323"
        },
        "109": {
          "player_id": 109,
          "name": "D.J. Augustin",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 17.1125,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "a18805c2-d746-4d4b-be83-5b96c3bdf6af"
        },
        "110": {
          "player_id": 110,
          "name": "T.J. Warren",
          "salary": 4300,
          "start": "2016-03-18T01:00:00Z",
          "position": "SF",
          "fppg": 19.6875,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "2ec7092d-e988-4576-ab8b-e3197448fa5d"
        },
        "112": {
          "player_id": 112,
          "name": "Alex Len",
          "salary": 6300,
          "start": "2016-03-18T01:00:00Z",
          "position": "C",
          "fppg": 30.7375,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "2facd6c5-10c6-4481-a20f-a885b3f84460"
        },
        "114": {
          "player_id": 114,
          "name": "Henry Sims",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "C",
          "fppg": 0.9,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "2fcb797b-0f24-4862-9c6f-7dea69720f7a"
        },
        "115": {
          "player_id": 115,
          "name": "Steve Novak",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 4.75,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "bfe054d7-7f26-4445-aa1e-c1cc175f854c"
        },
        "116": {
          "player_id": 116,
          "name": "Devin Booker",
          "salary": 5700,
          "start": "2016-03-18T01:00:00Z",
          "position": "SG",
          "fppg": 29.5875,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "31baa84f-c759-4f92-8e1f-a92305ade3d6"
        },
        "118": {
          "player_id": 118,
          "name": "Tyson Chandler",
          "salary": 4800,
          "start": "2016-03-18T01:00:00Z",
          "position": "C",
          "fppg": 23.6625,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "3cd2d1c1-d575-45fd-b069-3f0adf57796d"
        },
        "120": {
          "player_id": 120,
          "name": "Sonny Weems",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SG",
          "fppg": 7.325,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "4262a004-5ad9-446f-9f5f-b464f4d8bb6b"
        },
        "122": {
          "player_id": 122,
          "name": "Terrico White",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "SG",
          "fppg": 0.325,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "475cbd01-c335-4941-937e-37220b6e99cb"
        },
        "124": {
          "player_id": 124,
          "name": "Archie Goodwin",
          "salary": 5000,
          "start": "2016-03-18T01:00:00Z",
          "position": "SG",
          "fppg": 19.5625,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "55a8550a-3b5d-437a-b3fc-a4b6937c3e71"
        },
        "125": {
          "player_id": 125,
          "name": "Cory Jefferson",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "PF",
          "fppg": 7.75,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "7f9a1243-6571-40cb-b80b-882cde378c70"
        },
        "126": {
          "player_id": 126,
          "name": "Eric Bledsoe",
          "salary": 7600,
          "start": "2016-03-18T01:00:00Z",
          "position": "PG",
          "fppg": 37.075,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "8cee3c73-f765-4000-882d-0c6d0b8acbe3"
        },
        "128": {
          "player_id": 128,
          "name": "Kyle Casey",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "SF",
          "fppg": 0,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "a6f5375d-b7be-4ca7-bb96-60e99538eb5e"
        },
        "129": {
          "player_id": 129,
          "name": "P.J. Tucker",
          "salary": 4900,
          "start": "2016-03-18T01:00:00Z",
          "position": "SF",
          "fppg": 22.375,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "da7d17aa-f245-4710-820c-99d29a7458b4"
        },
        "130": {
          "player_id": 130,
          "name": "Jon Leuer",
          "salary": 3500,
          "start": "2016-03-18T01:00:00Z",
          "position": "PF",
          "fppg": 14.6875,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ee9ddf70-f50d-49b0-846c-f83719b095d8"
        },
        "131": {
          "player_id": 131,
          "name": "Brandon Knight",
          "salary": 6000,
          "start": "2016-03-18T01:00:00Z",
          "position": "PG",
          "fppg": 29.925,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "f58a9803-0ede-4c0b-acbd-08bc0da229af"
        },
        "132": {
          "player_id": 132,
          "name": "O.J. Mayo",
          "salary": 3200,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 15.15,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "1919675f-32c1-4efd-b1ff-3512538bc015"
        },
        "133": {
          "player_id": 133,
          "name": "Charlie Westbrook",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 0.5625,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "193aaf99-08bf-4cde-b11d-1fc36b302afd"
        },
        "134": {
          "player_id": 134,
          "name": "Marcus Landry",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 1.3125,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "196177fb-6444-48d9-95ff-c738cf70776f"
        },
        "135": {
          "player_id": 135,
          "name": "Michael Carter-Williams",
          "salary": 5400,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 26.65,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "1f5e7dfc-225d-4a25-8857-e6f8192b4c44"
        },
        "136": {
          "player_id": 136,
          "name": "Tyler Ennis",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 6.325,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "228a967c-1b1a-407e-adc6-c1432bb50e6a"
        },
        "137": {
          "player_id": 137,
          "name": "Josh Powell",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 0.2875,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "3d386f0a-05bb-4f9b-b1d1-17f6f80b3b71"
        },
        "138": {
          "player_id": 138,
          "name": "Johnny O'Bryant",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 5.8625,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "44ec1037-795f-4a4a-92c2-004d5bd4f3e6"
        },
        "139": {
          "player_id": 139,
          "name": "Jorge Gutierrez",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "PG",
          "fppg": 4.875,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "469db920-ec47-4b41-bbca-5c956d0de0cc"
        },
        "140": {
          "player_id": 140,
          "name": "Khris Middleton",
          "salary": 7800,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 38.7875,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "4c362eee-6474-40ea-b1b4-d8f917f95175"
        },
        "141": {
          "player_id": 141,
          "name": "Giannis Antetokounmpo",
          "salary": 9000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 45.225,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "6c60282d-165a-4cba-8e5a-4f2d9d4c5905"
        },
        "143": {
          "player_id": 143,
          "name": "Rashad Vaughn",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 6.0625,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "6efad0c0-447b-4a48-b5c3-6786b207b8d8"
        },
        "144": {
          "player_id": 144,
          "name": "Miles Plumlee",
          "salary": 3200,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 17.2875,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "73e55440-d981-48e6-9639-d2ed7276f22d"
        },
        "145": {
          "player_id": 145,
          "name": "Greg Monroe",
          "salary": 6900,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 32.5,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "762d218c-cdbd-4886-9252-10cd99284c7a"
        },
        "146": {
          "player_id": 146,
          "name": "Damien Inglis",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 4.25,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "83594c82-2829-44c8-b2bf-3ff1c19fa4b1"
        },
        "147": {
          "player_id": 147,
          "name": "Jon Horford",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 0,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ac552028-1157-4139-85c4-5bc94ee54a56"
        },
        "148": {
          "player_id": 148,
          "name": "John Henson",
          "salary": 4000,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 19.4625,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "c555e067-c4d5-43f6-99af-716b6005cbba"
        },
        "149": {
          "player_id": 149,
          "name": "Greivis Vasquez",
          "salary": 3400,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 16.1428571428571,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "cbe8d33e-a92a-473c-942f-90d8b76ed77c"
        },
        "150": {
          "player_id": 150,
          "name": "Jabari Parker",
          "salary": 6300,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 30.1875,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "e58c5e0e-f1f5-4685-9ff2-7197f9330bea"
        },
        "151": {
          "player_id": 151,
          "name": "Donald Sloan",
          "salary": 4300,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 21.3,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "0b131b69-ffc9-4739-9aa0-0d54c1078200"
        },
        "152": {
          "player_id": 152,
          "name": "Jerryd Bayless",
          "salary": 3900,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 20.6625,
          "team_alias": "MIL",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "f444ee53-e3b3-4899-923e-a27369ce7e59"
        },
        "153": {
          "player_id": 153,
          "name": "Thomas Robinson",
          "salary": 3400,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 15.2,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "1ec23c3b-649c-492f-97af-9ef1199f21a7"
        },
        "154": {
          "player_id": 154,
          "name": "Joe Johnson",
          "salary": 5600,
          "start": "2016-03-17T23:30:00Z",
          "position": "SF",
          "fppg": 26.725,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "2c14656f-1be0-4bd5-9a1f-e9684a89a489"
        },
        "155": {
          "player_id": 155,
          "name": "Thaddeus Young",
          "salary": 6900,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 33.15,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "31a50d54-ef46-47a8-863c-6f4d4e5aa184"
        },
        "156": {
          "player_id": 156,
          "name": "Andrea Bargnani",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 9.275,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "339879bc-5749-44cb-81b0-83449911f13d"
        },
        "157": {
          "player_id": 157,
          "name": "Markel Brown",
          "salary": 3100,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 14.675,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "3d43f259-7c1b-47ed-9dfd-d9478751d4ff"
        },
        "160": {
          "player_id": 160,
          "name": "Sergey Karasev",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 4.875,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "462416b4-840b-4c4a-a9bf-7d9e0b594e20"
        },
        "162": {
          "player_id": 162,
          "name": "Wayne Ellington",
          "salary": 3600,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 17.8,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "47e00cc4-53ca-453b-993a-0f58279e2a94"
        },
        "163": {
          "player_id": 163,
          "name": "Jason Thompson",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "C",
          "fppg": 8.0875,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "3360c00c-4737-4b6e-b683-46f4092cfb0a"
        },
        "166": {
          "player_id": 166,
          "name": "Shane Larkin",
          "salary": 3700,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 16.5375,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "76c71fde-f27f-4a50-8f7f-421898aacc72"
        },
        "167": {
          "player_id": 167,
          "name": "Sean Kilpatrick",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 10.8076923076923,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "238e8363-aa63-4f01-b47c-5405e78b16e6"
        },
        "169": {
          "player_id": 169,
          "name": "Bojan Bogdanovic",
          "salary": 3600,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 17.7125,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "7ff02e19-e829-4e56-9a34-233a71fce76c"
        },
        "172": {
          "player_id": 172,
          "name": "Chris Daniels",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 3.575,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "81d36b4b-3713-4180-ac34-c033e019f639"
        },
        "178": {
          "player_id": 178,
          "name": "Dahntay Jones",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 2.475,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "90c64141-1d4d-4935-9387-fe236313c3f5"
        },
        "179": {
          "player_id": 179,
          "name": "Jarell Eddie",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 7.45,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "6e6545d7-7d40-4a3f-b962-5e17a9860fce"
        },
        "180": {
          "player_id": 180,
          "name": "Chris McCullough",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 6.5,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "a012493e-ebc1-4f5a-9894-e9363958b4d7"
        },
        "183": {
          "player_id": 183,
          "name": "Willie Reed",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 10.9625,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ab55b5eb-f998-4480-a69b-eacaa7325ff3"
        },
        "186": {
          "player_id": 186,
          "name": "Rondae Hollis-Jefferson",
          "salary": 3800,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 19.4166666666667,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "b0d9c043-32b9-4c79-a692-564e93f62bd3"
        },
        "189": {
          "player_id": 189,
          "name": "Brook Lopez",
          "salary": 8200,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 42.325,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "c179fb5c-9845-4e37-aef7-6e00d97548eb"
        },
        "192": {
          "player_id": 192,
          "name": "Jarrett Jack",
          "salary": 6100,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 30.275,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "c3a3881d-92e9-4352-979b-d8465a5a3605"
        },
        "197": {
          "player_id": 197,
          "name": "Quincy Miller",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 0.5625,
          "team_alias": "BKN",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "f0ba938e-d631-48d3-9618-e0090a68a02d"
        },
        "210": {
          "player_id": 210,
          "name": "Jared Dudley",
          "salary": 4500,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 18.3125,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "04856926-1edc-4375-a147-246c4d66b6bb"
        },
        "211": {
          "player_id": 211,
          "name": "Ish Smith",
          "salary": 6500,
          "start": "2016-03-17T23:00:00Z",
          "position": "PG",
          "fppg": 31.7625,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "05a90cd6-73de-43d5-9d30-bc2588d03262"
        },
        "212": {
          "player_id": 212,
          "name": "Kris Humphries",
          "salary": 3300,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 16.4125,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "1a072572-763d-4839-b920-82b48d8e296a"
        },
        "213": {
          "player_id": 213,
          "name": "Alan Anderson",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SG",
          "fppg": 13.5,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "1b260e56-45ff-4a14-9b4e-744553ef15bf"
        },
        "214": {
          "player_id": 214,
          "name": "Drew Gooden",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 8.3,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "23dfb4c0-f7ff-4372-b379-09fd61ce2616"
        },
        "215": {
          "player_id": 215,
          "name": "John Wall",
          "salary": 10000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PG",
          "fppg": 48.6875,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "6769d1ca-0581-48b0-b487-b5c87b8f696e"
        },
        "216": {
          "player_id": 216,
          "name": "Otto Porter",
          "salary": 4300,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 21.375,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "792fdc1e-e833-4777-a372-11e93e457480"
        },
        "217": {
          "player_id": 217,
          "name": "Gary Neal",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SG",
          "fppg": 14.5875,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "79b65432-3224-4da9-a1dc-2a08d089c917"
        },
        "218": {
          "player_id": 218,
          "name": "DeJuan Blair",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "C",
          "fppg": 6.9,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "7a76d222-962a-4776-90e4-8683af6477bb"
        },
        "219": {
          "player_id": 219,
          "name": "Kelly Oubre",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 6.525,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "7dfa0971-96be-4705-9811-f9f54758145f"
        },
        "220": {
          "player_id": 220,
          "name": "Toure' Murry",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 0.3625,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "8a226084-2a76-4ff3-84b8-7dcc263aacc5"
        },
        "221": {
          "player_id": 221,
          "name": "Jaleel Roberts",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "C",
          "fppg": 0.75,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "8af481b0-90f8-4ddb-8f2d-5a2529030f80"
        },
        "222": {
          "player_id": 222,
          "name": "Martell Webster",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 0,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "8b93c7f5-bb43-4a72-98fe-312cd08fc957"
        },
        "223": {
          "player_id": 223,
          "name": "Ramon Sessions",
          "salary": 3200,
          "start": "2016-03-17T23:00:00Z",
          "position": "PG",
          "fppg": 16.1625,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "91ac13f8-e8d3-4902-b451-83ff32d2cf28"
        },
        "224": {
          "player_id": 224,
          "name": "Jaron Johnson",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SG",
          "fppg": 0.5,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "dd27a652-cb3d-484c-8a1b-731e0e1be32e"
        },
        "225": {
          "player_id": 225,
          "name": "Josh Harrellson",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 1.7375,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "e8a19123-81c1-49b4-ac6d-6862e63427c8"
        },
        "226": {
          "player_id": 226,
          "name": "Garrett Temple",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SG",
          "fppg": 12.25,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ee2644c1-1260-4bf4-9c70-7c5b0cee4770"
        },
        "227": {
          "player_id": 227,
          "name": "Marcin Gortat",
          "salary": 6900,
          "start": "2016-03-17T23:00:00Z",
          "position": "C",
          "fppg": 31.7875,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "f0deff5f-c269-4389-9713-b8a7e70207cb"
        },
        "228": {
          "player_id": 228,
          "name": "Nene Hilario",
          "salary": 4100,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 18.9625,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "f1b776e4-b59e-48c7-9e8a-272de4946b37"
        },
        "229": {
          "player_id": 229,
          "name": "Bradley Beal",
          "salary": 5300,
          "start": "2016-03-17T23:00:00Z",
          "position": "SG",
          "fppg": 25.75,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ff461754-ad20-4eeb-af02-2b46cc980b24"
        },
        "257": {
          "player_id": 257,
          "name": "Jimmy Butler",
          "salary": 8800,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 42.55,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "0e163d44-67a7-4107-9421-5333600166bb"
        },
        "259": {
          "player_id": 259,
          "name": "Tony Snell",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 9.9375,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "26414d70-d298-4999-a391-2eee2dd7067d"
        },
        "261": {
          "player_id": 261,
          "name": "Jordan Crawford",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 1.7625,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "264a1d66-7f41-465a-b64c-c0f20ab31ad3"
        },
        "263": {
          "player_id": 263,
          "name": "Kirk Hinrich",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 8.525,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "2ef5faba-5362-4111-98ed-22f7c639521e"
        },
        "265": {
          "player_id": 265,
          "name": "Cristiano Felicio",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 4.53125,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "3f64e9a6-6e1e-499b-aec8-764c99f634b2"
        },
        "267": {
          "player_id": 267,
          "name": "Derrick Rose",
          "salary": 6700,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 32.9625,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "48341095-ae5a-4d61-bcc8-1b0ceed870b2"
        },
        "269": {
          "player_id": 269,
          "name": "Pau Gasol",
          "salary": 9200,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 46.4375,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "4aafa7e4-d271-42d2-8979-bdefcd221d30"
        },
        "272": {
          "player_id": 272,
          "name": "Mike Dunleavy",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 16.9333333333333,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "4ec1bff7-ec1b-488b-8a24-aed83e62b4ce"
        },
        "274": {
          "player_id": 274,
          "name": "E'Twaun Moore",
          "salary": 4100,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 23.675,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "5a854508-5f41-4009-8986-a162224c511d"
        },
        "276": {
          "player_id": 276,
          "name": "Doug McDermott",
          "salary": 3700,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 17.6375,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "66156be8-6202-40bd-bdc2-014a46bee28f"
        },
        "278": {
          "player_id": 278,
          "name": "Bobby Portis",
          "salary": 4200,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 18.6875,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "68b7aac9-02fd-4bd8-b10c-6702d2c5eb98"
        },
        "279": {
          "player_id": 279,
          "name": "Taj Gibson",
          "salary": 5200,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 24.975,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "9c8dc8ee-6207-48d5-81ee-f362f5e17f9b"
        },
        "280": {
          "player_id": 280,
          "name": "Joakim Noah",
          "salary": 5100,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 23.975,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "b6eee153-eac4-41e5-afcb-ab46cf7a8ba8"
        },
        "281": {
          "player_id": 281,
          "name": "Aaron Brooks",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 13.675,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "b838cbad-0877-4189-ba3d-039962da7ebd"
        },
        "282": {
          "player_id": 282,
          "name": "Marcus Simmons",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 0.0375,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "b9c5cdbd-98e7-4921-8e49-6c192326d8eb"
        },
        "283": {
          "player_id": 283,
          "name": "Nikola Mirotic",
          "salary": 5100,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 23.5625,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ca6e9e9a-3d47-422d-bc1e-2dcf6deba5ca"
        },
        "284": {
          "player_id": 284,
          "name": "Jake Anderson",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 0,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "d72a7bb4-146a-465e-85fc-dd54aee148eb"
        },
        "285": {
          "player_id": 285,
          "name": "Cameron Bairstow",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 5.08823529411765,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "d98a598a-5ef5-4194-9fb2-c400370151be"
        },
        "298": {
          "player_id": 298,
          "name": "Ty Lawson",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PG",
          "fppg": 11.325,
          "team_alias": "IND",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "95fd2469-00cc-481c-a42d-5ec9eaa80868"
        },
        "302": {
          "player_id": 302,
          "name": "Marcus Thornton",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SG",
          "fppg": 13.8375,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "d5ef3cfe-2ab9-4b77-823a-62678c13058f"
        },
        "324": {
          "player_id": 324,
          "name": "Justin Holiday",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 9.075,
          "team_alias": "CHI",
          "game_srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
          "team_srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "05dea31d-f1ff-491b-9f17-8be88b26f413"
        },
        "326": {
          "player_id": 326,
          "name": "Kent Bazemore",
          "salary": 5300,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 23.2375,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "2c157857-fffd-4eb5-8e2a-b28ebea8da77"
        },
        "327": {
          "player_id": 327,
          "name": "Tim Hardaway Jr.",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 11.025,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "35cd1338-c56b-4247-b53c-264585c59883"
        },
        "328": {
          "player_id": 328,
          "name": "Lamar Patterson",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 7.65,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "4970099b-0a37-44f6-9b71-304040992efc"
        },
        "329": {
          "player_id": 329,
          "name": "Paul Millsap",
          "salary": 8100,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 36.125,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "59f6f688-7000-4cf5-a27f-a1980dd86d93"
        },
        "330": {
          "player_id": 330,
          "name": "Earl Barron",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 0.875,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "5b59ce10-becf-4ab4-be21-a33fe998a90c"
        },
        "331": {
          "player_id": 331,
          "name": "Edgar Sosa",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 0.05,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "75df82d5-1156-42e1-877c-5964562d7e69"
        },
        "332": {
          "player_id": 332,
          "name": "Delon Wright",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PG",
          "fppg": 4.69642857142857,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "1db0df17-b3d5-4ddb-98d0-8f86239347bf"
        },
        "333": {
          "player_id": 333,
          "name": "James Johnson",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 11.1875,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "1f0687ca-c8f2-4c71-8306-8a18cbf6cc60"
        },
        "334": {
          "player_id": 334,
          "name": "Mike Muscala",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 8.6,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "7c636961-816a-4b44-8991-671df9d91d9c"
        },
        "335": {
          "player_id": 335,
          "name": "Shannon Scott",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PG",
          "fppg": 0.65,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "2f617d47-8839-40db-8286-40bd5cd95a71"
        },
        "336": {
          "player_id": 336,
          "name": "Walter Tavares",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 7.13888888888889,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "7fb15c57-6024-4b0c-9493-8d52d3ef3c24"
        },
        "337": {
          "player_id": 337,
          "name": "Cory Joseph",
          "salary": 4100,
          "start": "2016-03-17T23:00:00Z",
          "position": "PG",
          "fppg": 19.3375,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "5769354c-0661-4ac7-86e5-3fd51506df36"
        },
        "338": {
          "player_id": 338,
          "name": "Tiago Splitter",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 12.45,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "8c81dcdb-fec1-4186-98ce-310f9f55bb0a"
        },
        "339": {
          "player_id": 339,
          "name": "Patrick Patterson",
          "salary": 3300,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 16.3375,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "5a25d084-9ef7-4e81-8da8-737b5a9d6ed9"
        },
        "340": {
          "player_id": 340,
          "name": "Jeff Teague",
          "salary": 6400,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 32.275,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "9cf99a61-6b51-4aed-8940-0480dc512b36"
        },
        "341": {
          "player_id": 341,
          "name": "Luis Scola",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 13.275,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "5be304d2-f98b-4f1b-a040-8cb402644ef7"
        },
        "342": {
          "player_id": 342,
          "name": "Dennis Schroder",
          "salary": 4900,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 22.3875,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "a2c6a907-282f-4172-9d60-42d03987da0e"
        },
        "343": {
          "player_id": 343,
          "name": "DeMar DeRozan",
          "salary": 7500,
          "start": "2016-03-17T23:00:00Z",
          "position": "SG",
          "fppg": 38.3625,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "5e86a9c3-b4d0-4fe1-a551-acd83e5d60eb"
        },
        "344": {
          "player_id": 344,
          "name": "Lucas Nogueira",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "C",
          "fppg": 5.90277777777778,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "62ae945c-5c43-4063-84b3-4a83b2fa4843"
        },
        "345": {
          "player_id": 345,
          "name": "Thabo Sefolosha",
          "salary": 3200,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 15.575,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ad0aa3eb-81c3-4688-b769-e0375cdb5c13"
        },
        "346": {
          "player_id": 346,
          "name": "Ronald Roberts",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 0.975,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "62bc2f36-5cb9-449d-a5c4-b9f0f7863a37"
        },
        "347": {
          "player_id": 347,
          "name": "DeMarre Carroll",
          "salary": 4800,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 22.4875,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "664afb4f-3fc1-4e25-bcb8-bab2c0c3c33b"
        },
        "348": {
          "player_id": 348,
          "name": "Kyle Korver",
          "salary": 4100,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 19.4375,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ba1b12c1-ee81-47d2-9f02-56110ff2a318"
        },
        "349": {
          "player_id": 349,
          "name": "Bruno Caboclo",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 2.75,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "664f0884-717b-4f4a-a1a6-79f08acb41bd"
        },
        "350": {
          "player_id": 350,
          "name": "Al Horford",
          "salary": 7200,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 34.625,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "cf3a87ec-c2f7-42e8-9698-6f8b2ba916a9"
        },
        "351": {
          "player_id": 351,
          "name": "Kyle Lowry",
          "salary": 8400,
          "start": "2016-03-17T23:00:00Z",
          "position": "PG",
          "fppg": 42.1375,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "8c090758-6baa-468d-82fd-d47e17d5091b"
        },
        "352": {
          "player_id": 352,
          "name": "Mike Scott",
          "salary": 3100,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 11.9875,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "e3c8bfbe-086f-4bbf-be9b-38accc5d5037"
        },
        "353": {
          "player_id": 353,
          "name": "Bismack Biyombo",
          "salary": 3600,
          "start": "2016-03-17T23:00:00Z",
          "position": "C",
          "fppg": 18.1625,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "8e3cbaa3-e30a-4cf8-aa7a-1b57f15f0f98"
        },
        "354": {
          "player_id": 354,
          "name": "DeQuan Jones",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 0.5875,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "e77345ce-8cb5-4727-a875-5332900b0309"
        },
        "355": {
          "player_id": 355,
          "name": "Anthony Bennett",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 4.82692307692308,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "b634fb27-1562-4d4a-b340-066c46e62d25"
        },
        "356": {
          "player_id": 356,
          "name": "Terrence Ross",
          "salary": 4100,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 16.9375,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "b7d0fa52-b5ca-4465-9bbb-3ec9b6b7b536"
        },
        "357": {
          "player_id": 357,
          "name": "Shelvin Mack",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "PG",
          "fppg": 19.025,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ee6b8f67-08cc-4d6f-ac8a-9f7c2432cb80"
        },
        "358": {
          "player_id": 358,
          "name": "Jonas Valanciunas",
          "salary": 5900,
          "start": "2016-03-17T23:00:00Z",
          "position": "C",
          "fppg": 27.1875,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "c8788ad2-89f7-4ec9-a22b-dcaf6190889b"
        },
        "359": {
          "player_id": 359,
          "name": "Terran Petteway",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 0.6875,
          "team_alias": "ATL",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "f58ca913-fc54-4e8c-9e69-e0cd8bc22a1b"
        },
        "360": {
          "player_id": 360,
          "name": "Norman Powell",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SG",
          "fppg": 5.7,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "e1e4c26d-ab5c-4bd7-886a-812854466bb8"
        },
        "361": {
          "player_id": 361,
          "name": "Michale Kyser",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 0.125,
          "team_alias": "TOR",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "e7e7dc21-c48f-4c33-a9df-7b0027cc21d4"
        },
        "362": {
          "player_id": 362,
          "name": "Axel Toupane",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 9.45833333333333,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "f3fd7679-312f-42a1-b78d-326da1492c03"
        },
        "363": {
          "player_id": 363,
          "name": "Russ Smith",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 5.125,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "02bdc54a-4db6-45d0-966e-d7659dd4ce13"
        },
        "364": {
          "player_id": 364,
          "name": "Oleksiy Pecherov",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 0.3625,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "0cf7e66d-14d3-463c-a825-e6fc62a0a6c6"
        },
        "365": {
          "player_id": 365,
          "name": "Jarell Martin",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 13.4166666666667,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "162412a2-d4ff-46f0-8e08-53acc1ab838d"
        },
        "366": {
          "player_id": 366,
          "name": "Danilo Gallinari",
          "salary": 7000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 31.4625,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "47cd6421-0ce1-431e-9b9c-a8d9bfd0eb04"
        },
        "367": {
          "player_id": 367,
          "name": "Yakhouba Diawara",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 1.275,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "20b06e01-26cb-4bc1-b5ff-c760a9ece0e4"
        },
        "368": {
          "player_id": 368,
          "name": "Jameer Nelson",
          "salary": 4800,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 22.95,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "5d3681c6-9c73-4895-9b59-b4851069469f"
        },
        "369": {
          "player_id": 369,
          "name": "Ryan Hollins",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 9.4,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "224fd5f2-02de-48c9-8c39-b2a5f6ed5486"
        },
        "370": {
          "player_id": 370,
          "name": "Matt Janning",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 0.275,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "5f3bd1f4-072b-4f32-9787-37670954cf3b"
        },
        "371": {
          "player_id": 371,
          "name": "JaMychal Green",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 19.15,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "2bd97a34-ced9-4413-bfaa-94dbafaa0fdd"
        },
        "372": {
          "player_id": 372,
          "name": "Gary Harris",
          "salary": 4800,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 24.7,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "6b5d0264-fa2d-4956-919b-61abfc6bb8d7"
        },
        "373": {
          "player_id": 373,
          "name": "Mike Conley",
          "salary": 6600,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 32.125,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "460b7264-b98f-483e-b841-59a18c2e4d67"
        },
        "374": {
          "player_id": 374,
          "name": "Kenneth Faried",
          "salary": 6300,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 29.3375,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "6ee485e1-534f-4d07-9492-c30b1ae9d607"
        },
        "375": {
          "player_id": 375,
          "name": "Courtney Lee",
          "salary": 3400,
          "start": "2016-03-17T23:30:00Z",
          "position": "SG",
          "fppg": 17.25,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "5247355c-121e-4053-8627-54d99e61d518"
        },
        "377": {
          "player_id": 377,
          "name": "Michael Holyfield",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": -0.5,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "61795760-96af-4588-82ad-5e40e79f2a73"
        },
        "378": {
          "player_id": 378,
          "name": "J.J. Hickson",
          "salary": 3200,
          "start": "2016-03-17T23:00:00Z",
          "position": "C",
          "fppg": 16.1375,
          "team_alias": "WAS",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "7ea5ebcb-e825-4b6e-bd46-13a45c88c09c"
        },
        "379": {
          "player_id": 379,
          "name": "Erick Green",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "PG",
          "fppg": 4.14285714285714,
          "team_alias": "UTA",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "81f26bbb-c9a8-488a-8f3e-dbede7757677"
        },
        "380": {
          "player_id": 380,
          "name": "Jordan Adams",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 9.5,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "703719b2-2db0-4590-90f7-0be1041c1f81"
        },
        "381": {
          "player_id": 381,
          "name": "Will Barton",
          "salary": 5800,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 26.9,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "85e1279a-77c4-49a7-bfa0-7699e64b581f"
        },
        "383": {
          "player_id": 383,
          "name": "Emmanuel Mudiay",
          "salary": 5900,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 29.9375,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "8f7caaba-426f-4bee-be51-9625718d51f3"
        },
        "384": {
          "player_id": 384,
          "name": "Matt Barnes",
          "salary": 4900,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 24.075,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "a0d07bb9-3935-4d53-bdbb-6cb27c1a46b1"
        },
        "385": {
          "player_id": 385,
          "name": "Nick Johnson",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 1.25,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "98ec8372-22fd-4ab4-88f2-94b47df7cb58"
        },
        "387": {
          "player_id": 387,
          "name": "Marc Gasol",
          "salary": 7100,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 34.8375,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "b73a8508-23a1-49ee-a466-aa9ea8add09e"
        },
        "388": {
          "player_id": 388,
          "name": "Jusuf Nurkic",
          "salary": 3300,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 17.15,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "a8b48aa9-cf98-4a87-8bba-e88eead8cdaa"
        },
        "390": {
          "player_id": 390,
          "name": "Darrell Arthur",
          "salary": 3600,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 16.05,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "c25afa99-b041-46db-9725-8d92492df50b"
        },
        "391": {
          "player_id": 391,
          "name": "Brandan Wright",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 15.0625,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "c1189e9c-3b45-4552-b731-e0ff544bc1bd"
        },
        "393": {
          "player_id": 393,
          "name": "Devin Sweetney",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 0.2375,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "d386c6c9-7bd1-4a56-a0ca-3476c7b57fd6"
        },
        "395": {
          "player_id": 395,
          "name": "Zach Randolph",
          "salary": 6400,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 29.025,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "f5987aa7-b7fd-4bd6-855d-fd6407324950"
        },
        "396": {
          "player_id": 396,
          "name": "Wilson Chandler",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 4.875,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "db90c8f4-5d2a-4ff9-8f57-1fc44a253dcf"
        },
        "398": {
          "player_id": 398,
          "name": "Joffrey Lauvergne",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 13.75,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "f05628db-779b-41e8-9527-cf3b204b5bac"
        },
        "399": {
          "player_id": 399,
          "name": "Beno Udrih",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "PG",
          "fppg": 12.5,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "f77263f9-a97c-45b9-91f0-0f0da4156b9f"
        },
        "401": {
          "player_id": 401,
          "name": "Nikola Jokic",
          "salary": 6100,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 30.3,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "f2625432-3903-4f90-9b0b-2e4f63856bb0"
        },
        "403": {
          "player_id": 403,
          "name": "Vince Carter",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 16.3,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "fa1c4130-38de-4ea1-b93a-4c3c962473e6"
        },
        "404": {
          "player_id": 404,
          "name": "Lazeric Jones",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 2.5375,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "fa431c70-d091-4548-9330-484321788b1d"
        },
        "406": {
          "player_id": 406,
          "name": "Tony Allen",
          "salary": 4500,
          "start": "2016-03-18T00:00:00Z",
          "position": "SG",
          "fppg": 22.8625,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ff76cdb2-9e72-4ba9-956f-9d99033cbe13"
        },
        "420": {
          "player_id": 420,
          "name": "John Jenkins",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "SG",
          "fppg": 7.5875,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "f4c21698-8e9b-4720-ac1e-5e07bd7c2e92"
        },
        "424": {
          "player_id": 424,
          "name": "Kevin Martin",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "SG",
          "fppg": 10.275,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "767837db-62fa-4fc6-b118-1d56a8b23415"
        },
        "430": {
          "player_id": 430,
          "name": "Lorenzo Brown",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "PG",
          "fppg": 6.15625,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "a2a15cb3-9a7d-4e24-b3ce-62cb4e1c3c68"
        },
        "443": {
          "player_id": 443,
          "name": "Andre Miller",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "PG",
          "fppg": 7.5,
          "team_alias": "SAS",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "d5381ecd-6a70-401e-a019-817f51ac5aa2"
        },
        "461": {
          "player_id": 461,
          "name": "Justise Winslow",
          "salary": 4600,
          "start": "2016-03-17T23:30:00Z",
          "position": "SF",
          "fppg": 21.1625,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "0e6ddc9f-4a7b-4d48-8033-998103edfb32"
        },
        "463": {
          "player_id": 463,
          "name": "Gerald Green",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "SG",
          "fppg": 11.7375,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "11da94f7-02c0-4bc9-9da3-8e8994f46fb6"
        },
        "465": {
          "player_id": 465,
          "name": "John Lucas III",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "PG",
          "fppg": 0.15,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "17d7d84a-1d9c-48e4-b13c-3c365ea16f13"
        },
        "467": {
          "player_id": 467,
          "name": "Dwyane Wade",
          "salary": 7400,
          "start": "2016-03-17T23:30:00Z",
          "position": "SG",
          "fppg": 36.9,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "2038ebc0-a35b-4979-9fd6-15c72c435101"
        },
        "469": {
          "player_id": 469,
          "name": "Tre Kelley",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "PG",
          "fppg": 0.9375,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "3a3268ca-7e0d-4e26-81ac-8a51f1bcfde1"
        },
        "471": {
          "player_id": 471,
          "name": "Hassan Whiteside",
          "salary": 8500,
          "start": "2016-03-17T23:30:00Z",
          "position": "C",
          "fppg": 41.0375,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "3b8024e6-5872-4ceb-b675-415715527776"
        },
        "473": {
          "player_id": 473,
          "name": "Corey Hawkins",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "SG",
          "fppg": 0.6,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "44658d86-ae85-4ea9-80e5-0df9eab45cf0"
        },
        "474": {
          "player_id": 474,
          "name": "James Ennis",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 4.58333333333333,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "4cbe58e4-5e4b-46b0-9f7b-6cf18ad002c6"
        },
        "476": {
          "player_id": 476,
          "name": "Chris Andersen",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "C",
          "fppg": 9.81666666666667,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "510c6cdf-1a1a-450e-8d38-eed8d9b55df9"
        },
        "479": {
          "player_id": 479,
          "name": "Luol Deng",
          "salary": 6600,
          "start": "2016-03-17T23:30:00Z",
          "position": "SF",
          "fppg": 32.725,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "5176c4c0-b451-4122-81e9-7d5dc9502de5"
        },
        "480": {
          "player_id": 480,
          "name": "Josh McRoberts",
          "salary": 3100,
          "start": "2016-03-17T23:30:00Z",
          "position": "PF",
          "fppg": 13.1625,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "54723896-1f7b-4150-95d6-0392596a328f"
        },
        "482": {
          "player_id": 482,
          "name": "Keith Benson",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "C",
          "fppg": 3.525,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "6f004551-2fd3-4c66-b1c4-a13fbd5ead5a"
        },
        "484": {
          "player_id": 484,
          "name": "Amar'e Stoudemire",
          "salary": 3900,
          "start": "2016-03-17T23:30:00Z",
          "position": "C",
          "fppg": 16.5,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "76b89403-aaea-4730-bb7e-e60f38c56c3e"
        },
        "487": {
          "player_id": 487,
          "name": "Tyler Johnson",
          "salary": 3700,
          "start": "2016-03-17T23:30:00Z",
          "position": "SG",
          "fppg": 18.1125,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "895fa449-c569-44d1-ac1b-de05db7d2589"
        },
        "489": {
          "player_id": 489,
          "name": "Mario Chalmers",
          "salary": 4600,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 23.6125,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "b60c920c-b42e-4896-9f6d-7f3031fc6492"
        },
        "491": {
          "player_id": 491,
          "name": "Greg Whittington",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "SF",
          "fppg": 2.1125,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "d0cb08b3-51b4-4700-9311-4e111df81d49"
        },
        "493": {
          "player_id": 493,
          "name": "Udonis Haslem",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "PF",
          "fppg": 5.425,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ed343fa6-397c-4456-9f3f-63efee6706b5"
        },
        "495": {
          "player_id": 495,
          "name": "Josh Richardson",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "SG",
          "fppg": 17.0375,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ef11cca9-6605-44e8-943e-193c7b821465"
        },
        "496": {
          "player_id": 496,
          "name": "Chris Bosh",
          "salary": 7000,
          "start": "2016-03-17T23:30:00Z",
          "position": "PF",
          "fppg": 33.2875,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "f5163a3f-f880-4c2c-ac9b-00db844246b2"
        },
        "497": {
          "player_id": 497,
          "name": "Goran Dragic",
          "salary": 6700,
          "start": "2016-03-17T23:30:00Z",
          "position": "PG",
          "fppg": 33.8125,
          "team_alias": "MIA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "fea7b92a-0124-4775-8747-e4828f0dab8b"
        },
        "498": {
          "player_id": 498,
          "name": "Tony Wroten",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SG",
          "fppg": 14.0357142857143,
          "team_alias": "NYK",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "1647115a-1607-4250-889e-8ae1af98fc92"
        },
        "499": {
          "player_id": 499,
          "name": "Nerlens Noel",
          "salary": 6600,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 30.625,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "2012f4fd-98e0-4080-98a7-0cfb9de87067"
        },
        "500": {
          "player_id": 500,
          "name": "Nik Stauskas",
          "salary": 3200,
          "start": "2016-03-17T23:00:00Z",
          "position": "SG",
          "fppg": 16.075,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "2ccaaefc-917d-4e2a-b7c6-947836c38c6f"
        },
        "501": {
          "player_id": 501,
          "name": "Robert Covington",
          "salary": 5900,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 27.075,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "3e512d9e-ff9c-4f23-a4fd-a88128ee3af2"
        },
        "502": {
          "player_id": 502,
          "name": "Scottie Wilbekin",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PG",
          "fppg": 2.4125,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "4d6d7a45-3144-472a-bd4f-a477e855011f"
        },
        "503": {
          "player_id": 503,
          "name": "Pierre Jackson",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PG",
          "fppg": 0.9625,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "55e9d1e5-6ea3-4475-9877-d9d1f5f1910d"
        },
        "504": {
          "player_id": 504,
          "name": "Jerami Grant",
          "salary": 5200,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 23.95,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "5b315e15-6633-4ce2-8200-71b821553314"
        },
        "505": {
          "player_id": 505,
          "name": "JaKarr Sampson",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 8.7625,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "7a3749f6-b03a-49eb-9e1d-07b897bd0b2d"
        },
        "507": {
          "player_id": 507,
          "name": "Christian Wood",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 9.125,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "98100660-988b-4e71-a89e-f35839964483"
        },
        "508": {
          "player_id": 508,
          "name": "Isaiah Canaan",
          "salary": 3700,
          "start": "2016-03-17T23:00:00Z",
          "position": "PG",
          "fppg": 18.95,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "98a43535-8643-45ff-a954-2afecb418a9d"
        },
        "509": {
          "player_id": 509,
          "name": "Kendall Marshall",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PG",
          "fppg": 10.25,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "9fd789bc-0aa4-4028-b114-5014deacfbe2"
        },
        "510": {
          "player_id": 510,
          "name": "Jahlil Okafor",
          "salary": 6100,
          "start": "2016-03-17T23:00:00Z",
          "position": "C",
          "fppg": 30.225,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "a47ac0db-084a-4620-95e8-812c6168cf8d"
        },
        "511": {
          "player_id": 511,
          "name": "Furkan Aldemir",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 3.1125,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "aa9dc37e-bd55-48d7-b5ed-adc1b31d1143"
        },
        "512": {
          "player_id": 512,
          "name": "Carl Landry",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 13.125,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ba16b6ef-0c63-4580-8119-2a2d5600b160"
        },
        "513": {
          "player_id": 513,
          "name": "Joel Embiid",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "C",
          "fppg": 0,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "bf9ad0fd-0cb8-4360-8970-5f1b5cf3fa8d"
        },
        "514": {
          "player_id": 514,
          "name": "J.P. Tokoto",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 0.4625,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "c5ab83b1-9e16-46d2-b983-d75a8ed883d7"
        },
        "515": {
          "player_id": 515,
          "name": "Hollis Thompson",
          "salary": 3800,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 17.9125,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "dbf62639-cf0d-43ea-b470-c116128b76ec"
        },
        "516": {
          "player_id": 516,
          "name": "T.J. McConnell",
          "salary": 3400,
          "start": "2016-03-17T23:00:00Z",
          "position": "PG",
          "fppg": 16.475,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "e3dfa2a2-6272-4f3f-adf0-dd5dadea9481"
        },
        "517": {
          "player_id": 517,
          "name": "Richaun Holmes",
          "salary": 3200,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 13.2125,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "e96ef8d2-192f-47a3-a6ad-876603de1907"
        },
        "518": {
          "player_id": 518,
          "name": "Tim Frazier",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "PG",
          "fppg": 8.05,
          "team_alias": "NOP",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "005948cb-f744-4928-bf7f-d26076717c99"
        },
        "519": {
          "player_id": 519,
          "name": "Pat Connaughton",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "SG",
          "fppg": 4.60294117647059,
          "team_alias": "POR",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "298852ca-299d-4cb9-a9e5-6ac909582f78"
        },
        "520": {
          "player_id": 520,
          "name": "Gerald Henderson",
          "salary": 4000,
          "start": "2016-03-18T00:30:00Z",
          "position": "SG",
          "fppg": 19.4875,
          "team_alias": "POR",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "390c3ce6-7e5b-4aba-bd54-4dfb6add4767"
        },
        "521": {
          "player_id": 521,
          "name": "Meyers Leonard",
          "salary": 3400,
          "start": "2016-03-18T00:30:00Z",
          "position": "C",
          "fppg": 17.5125,
          "team_alias": "POR",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "51d0a386-20a8-4e68-a8ec-face10febaff"
        },
        "522": {
          "player_id": 522,
          "name": "Damian Lillard",
          "salary": 9400,
          "start": "2016-03-18T00:30:00Z",
          "position": "PG",
          "fppg": 46.275,
          "team_alias": "POR",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "5382cf43-3a79-4a5a-a7fd-153906fe65dd"
        },
        "523": {
          "player_id": 523,
          "name": "Al-Farouq Aminu",
          "salary": 4300,
          "start": "2016-03-18T00:30:00Z",
          "position": "SF",
          "fppg": 19.65,
          "team_alias": "POR",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "56ff7cb8-4828-4aaa-8f95-0bf569a0786d"
        },
        "524": {
          "player_id": 524,
          "name": "Allen Crabbe",
          "salary": 3500,
          "start": "2016-03-18T00:30:00Z",
          "position": "SG",
          "fppg": 16.8625,
          "team_alias": "POR",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "5ac1fb0f-24fe-4dce-aba5-6fc0dc9c27e7"
        },
        "525": {
          "player_id": 525,
          "name": "Noah Vonleh",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "PF",
          "fppg": 12.2125,
          "team_alias": "POR",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "84215e01-6108-4fd0-9a11-19e9518ab378"
        },
        "526": {
          "player_id": 526,
          "name": "Chris Kaman",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "C",
          "fppg": 6.05555555555556,
          "team_alias": "POR",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "859f0120-c1e1-4b75-ba10-3dca7020312b"
        },
        "527": {
          "player_id": 527,
          "name": "Luis Montero",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "SG",
          "fppg": 2.75,
          "team_alias": "POR",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "9304e1de-0d5a-4ccb-9409-100342405041"
        },
        "528": {
          "player_id": 528,
          "name": "Mason Plumlee",
          "salary": 4900,
          "start": "2016-03-18T00:30:00Z",
          "position": "C",
          "fppg": 22.5875,
          "team_alias": "POR",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "9570a938-324f-40e8-92dd-8a4fcf4a953b"
        },
        "531": {
          "player_id": 531,
          "name": "Ed Davis",
          "salary": 4200,
          "start": "2016-03-18T00:30:00Z",
          "position": "PF",
          "fppg": 17.725,
          "team_alias": "POR",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "9dbc15ee-deec-4c8c-86e9-71396ff80ef8"
        },
        "533": {
          "player_id": 533,
          "name": "Omari Johnson",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "SF",
          "fppg": 0.7,
          "team_alias": "POR",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "a34e015a-193c-4d57-b4b4-720eb5e1eef2"
        },
        "535": {
          "player_id": 535,
          "name": "C.J. McCollum",
          "salary": 7100,
          "start": "2016-03-18T00:30:00Z",
          "position": "SG",
          "fppg": 32.4875,
          "team_alias": "POR",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "bc70a55a-cee0-478f-9a13-cf51c4a4187c"
        },
        "538": {
          "player_id": 538,
          "name": "Moe Harkless",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "SF",
          "fppg": 12.4875,
          "team_alias": "POR",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "df6f21d3-5221-42e2-945b-8fe7cebdf03e"
        },
        "540": {
          "player_id": 540,
          "name": "Phil Pressey",
          "salary": 3000,
          "start": "2016-03-18T01:00:00Z",
          "position": "PG",
          "fppg": 10.2236842105263,
          "team_alias": "PHX",
          "game_srid": "2b9028c3-c482-4300-89fe-64e133aad607",
          "team_srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "e5b54fa6-88e0-4702-9677-282f204a43e1"
        },
        "542": {
          "player_id": 542,
          "name": "Cliff Alexander",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "PF",
          "fppg": 4.25,
          "team_alias": "POR",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "f3233c73-bb6b-44a4-8a16-20e772dbf69a"
        },
        "547": {
          "player_id": 547,
          "name": "Lance Stephenson",
          "salary": 3500,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 21.05,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "01e8f44f-f1ee-4d3a-86bd-c29d597ba9bd"
        },
        "573": {
          "player_id": 573,
          "name": "Alex Stepheson",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PF",
          "fppg": 12.25,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "765919dd-9d63-40a4-81fd-905ef04e4fc5"
        },
        "576": {
          "player_id": 576,
          "name": "Mike Miller",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 4.875,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "440251c0-601a-471a-9bdf-a8c7cd7efda8"
        },
        "580": {
          "player_id": 580,
          "name": "Kadeem Jack",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "SF",
          "fppg": 0.1,
          "team_alias": "IND",
          "game_srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
          "team_srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "d211740f-b91f-4ebd-8a4c-42db96770ae8"
        },
        "581": {
          "player_id": 581,
          "name": "Daniel Diez ",
          "salary": 3000,
          "start": "2016-03-18T00:30:00Z",
          "position": "SF",
          "fppg": 0,
          "team_alias": "POR",
          "game_srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
          "team_srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "dbbb8ac3-ea3a-4271-99c5-95f7f99bb927"
        },
        "582": {
          "player_id": 582,
          "name": "Sam Thompson",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "SF",
          "fppg": 0.3625,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "71663a1e-77a8-452e-b121-d4d06ed5c7db"
        },
        "583": {
          "player_id": 583,
          "name": "Jason Washburn",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "C",
          "fppg": 0.3375,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "d8e0340f-918d-4820-aa51-91e450721c9c"
        },
        "584": {
          "player_id": 584,
          "name": "Damien Wilkins",
          "salary": 3000,
          "start": "2016-03-17T23:30:00Z",
          "position": "SF",
          "fppg": 0.4625,
          "team_alias": "CHA",
          "game_srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
          "team_srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "ff482131-2cfa-41e1-ba23-6e8503b55ed2"
        },
        "585": {
          "player_id": 585,
          "name": "Briante Weber",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "PG",
          "fppg": 22.3333333333333,
          "team_alias": "MEM",
          "game_srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
          "team_srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "a1d0ec05-0d36-42fe-add4-170f7fc08692"
        },
        "588": {
          "player_id": 588,
          "name": "Kostas Papanikolaou",
          "salary": 3000,
          "start": "2016-03-18T00:00:00Z",
          "position": "SF",
          "fppg": 7.45,
          "team_alias": "DEN",
          "game_srid": "440a04df-0caa-4e99-a032-911ddb602576",
          "team_srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "a764ea7a-2209-4ff3-af9c-f97d9ac00333"
        },
        "589": {
          "player_id": 589,
          "name": "Elton Brand",
          "salary": 3000,
          "start": "2016-03-17T23:00:00Z",
          "position": "PF",
          "fppg": 12.4375,
          "team_alias": "PHI",
          "game_srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
          "team_srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "player_srid": "28512bba-0a6b-4ec2-816a-72f2b43036e1"
        }
      },
      "playersStats": {},
      "infoExpiresAt": 1458284081237,
      "fpExpiresAt": 1458241481187,
      "boxscoresExpiresAt": 1458240880794,
      "id": 127,
      "isFetchingInfo": false,
      "hasAllInfo": true,
      "isFetchingFP": false,
      "playersBySRID": {
        "0c144557-df20-492c-bf75-be53adf92699": 1,
        "2733be7a-cfc6-4787-8405-371db5af0399": 2,
        "287c389a-0499-4f80-ac4f-1a72366af999": 3,
        "15fc95b7-5f6d-4d71-beda-7d9605a0187b": 4,
        "3919daa3-0cc4-4c44-a3cc-10f5f9c31fe5": 5,
        "22f65f0b-5ccb-4f72-9bbe-ab383c86fa6b": 6,
        "562677c1-2a13-4934-a801-a6c88c619e83": 7,
        "323f9ef8-ecdd-41a7-859e-dd3db48ba913": 8,
        "37ad80b2-c9f4-4fde-b462-e1109f249b56": 9,
        "6255b242-0bbd-4f05-9c61-f44750061410": 10,
        "705c7422-c87f-4ab5-85ff-274339193138": 11,
        "6e566165-6674-4306-9994-470f60720a2c": 13,
        "8bf57b59-a618-4bfa-ae2e-4308b9108606": 14,
        "8d80f6fc-a7ac-48cf-bcd8-516d57acbbfe": 15,
        "732b1bd6-d99a-4971-bc2c-4de4842b4a9a": 16,
        "74a7e6ac-58ee-424c-b341-69a69451d481": 17,
        "a35ee8ed-f1db-4f7e-bb17-f823e8ee0b38": 18,
        "7f462af0-2ac8-4ca5-aa5a-17b37dc5001b": 19,
        "a89ac040-715d-4057-8fc0-9d71ad06fa0a": 20,
        "8f8d93e9-c9b4-4820-a546-2de60a00ecad": 21,
        "bff3d21b-880f-43f4-93a2-9fd9a8408716": 22,
        "c9b1c381-e0ac-4618-9887-ce3e8993b265": 23,
        "91ec3171-9b9c-48ee-bb52-d075dc41bacb": 24,
        "ddb5d888-09e5-435a-9009-a2549d8c8382": 25,
        "b4a94a3a-8563-49bd-97d2-98161cfb6c8d": 26,
        "e17a3191-b05c-4878-8be6-21028b8ec007": 27,
        "d2abbbb8-0d36-49d4-9785-d8664021eb78": 28,
        "e1ce75b8-44ce-4086-b2e1-d2e22efc86ff": 30,
        "db09f372-9a17-4889-add7-bf8a75ab6da6": 31,
        "e68c7b19-7c0e-49a6-920c-48668f7ddbcf": 33,
        "ea8a18e4-1341-48f1-b75d-5bbac8d789d4": 35,
        "ecafe060-0a4f-4740-9e21-03715d653327": 36,
        "eb1f731e-653d-435f-8ccb-3a7f15f84116": 38,
        "007a5e3c-978e-49e3-af38-7a4d9354cf21": 54,
        "1f9d116b-7c1b-4d1a-bf02-59ba4b22092e": 55,
        "2365e884-e0d9-43a4-8efe-a4bd9a14329a": 56,
        "24c17409-ac10-4859-be6c-59d6cc6b5810": 57,
        "2e49c27a-06c5-4c4a-87fd-69840b783947": 58,
        "3157a0b5-1b4c-46d1-934c-ac2df3810950": 59,
        "4173ac8e-175c-4ea2-b531-f9e5fe8aa37e": 60,
        "41857ce7-febe-4a63-9835-6f3461336945": 61,
        "4237e763-c872-4db0-8744-024e695a666e": 62,
        "44733f78-d10e-4668-ae99-8de54b69b32a": 63,
        "02259413-3191-4057-9473-caa3268fb189": 64,
        "478e5e20-5d59-402f-a901-b8e78f3e9508": 65,
        "52eba610-a87e-4c05-bb2d-dfb71bb32d03": 66,
        "0d187d04-4cd9-44b3-9a29-408fac5b011e": 67,
        "2ec0dd5b-2bd3-47f8-936c-bc23859a2686": 69,
        "8da88be3-bc4a-406a-9e16-147bdac064eb": 70,
        "95ca0a9b-4fd0-4ae8-8714-247b57fb84ea": 72,
        "37fbc3a5-0d10-4e22-803b-baa2ea0cdb12": 73,
        "9e917c97-5227-4581-9ab5-2dd07a7187ef": 74,
        "3f170fb8-2633-481f-bc63-0bce20b37557": 75,
        "a90a5752-ae6b-491a-8ff6-43acd5b12aa9": 76,
        "46bb99cd-123f-4d42-bfcb-ad2891df2e0e": 77,
        "b1b2d578-44df-4e05-9884-31dd89e82cf0": 78,
        "55f10af0-4b71-4693-aa82-435e958ab560": 79,
        "b1d48323-0ef7-478e-a10c-cbd9f2e3f1df": 80,
        "572261e2-8ad9-4198-969d-16cad41fdef3": 81,
        "c12fb587-fc86-471c-8a84-19caf31325ce": 82,
        "5b297372-b2af-445e-a4bc-777982dbc1e3": 83,
        "6c2124da-2ab9-4cad-bd88-224c87e6e6f3": 85,
        "73fcf334-2088-4862-b83b-66eae415cf87": 87,
        "86da224d-e103-412a-8406-1ca8976726e7": 89,
        "8e7ffd66-f779-418c-bf18-b9f746a1c5fe": 91,
        "a1ddebee-950c-497d-9acd-b5061360b464": 93,
        "ad354ebb-88e5-46e4-ad79-f7188ee1f6c2": 95,
        "cc35d329-4c26-44d9-bced-460b008f816e": 97,
        "d38f8754-7ecb-4791-a350-f67e5c4c785a": 98,
        "e3848f10-1f5a-4feb-b2ad-0b4dce9b1209": 101,
        "0abf221a-5fea-4c98-9547-f19e917210be": 102,
        "ef0cf1e1-e3e1-48e6-aace-fdfd3c0fb719": 103,
        "1981e577-063e-426a-af2c-adf666403911": 105,
        "f80c054f-53ba-4ca5-9873-6ece55552600": 107,
        "25c4a949-c310-4bd3-af3f-10441215b323": 108,
        "a18805c2-d746-4d4b-be83-5b96c3bdf6af": 109,
        "2ec7092d-e988-4576-ab8b-e3197448fa5d": 110,
        "2facd6c5-10c6-4481-a20f-a885b3f84460": 112,
        "2fcb797b-0f24-4862-9c6f-7dea69720f7a": 114,
        "bfe054d7-7f26-4445-aa1e-c1cc175f854c": 115,
        "31baa84f-c759-4f92-8e1f-a92305ade3d6": 116,
        "3cd2d1c1-d575-45fd-b069-3f0adf57796d": 118,
        "4262a004-5ad9-446f-9f5f-b464f4d8bb6b": 120,
        "475cbd01-c335-4941-937e-37220b6e99cb": 122,
        "55a8550a-3b5d-437a-b3fc-a4b6937c3e71": 124,
        "7f9a1243-6571-40cb-b80b-882cde378c70": 125,
        "8cee3c73-f765-4000-882d-0c6d0b8acbe3": 126,
        "a6f5375d-b7be-4ca7-bb96-60e99538eb5e": 128,
        "da7d17aa-f245-4710-820c-99d29a7458b4": 129,
        "ee9ddf70-f50d-49b0-846c-f83719b095d8": 130,
        "f58a9803-0ede-4c0b-acbd-08bc0da229af": 131,
        "1919675f-32c1-4efd-b1ff-3512538bc015": 132,
        "193aaf99-08bf-4cde-b11d-1fc36b302afd": 133,
        "196177fb-6444-48d9-95ff-c738cf70776f": 134,
        "1f5e7dfc-225d-4a25-8857-e6f8192b4c44": 135,
        "228a967c-1b1a-407e-adc6-c1432bb50e6a": 136,
        "3d386f0a-05bb-4f9b-b1d1-17f6f80b3b71": 137,
        "44ec1037-795f-4a4a-92c2-004d5bd4f3e6": 138,
        "469db920-ec47-4b41-bbca-5c956d0de0cc": 139,
        "4c362eee-6474-40ea-b1b4-d8f917f95175": 140,
        "6c60282d-165a-4cba-8e5a-4f2d9d4c5905": 141,
        "6efad0c0-447b-4a48-b5c3-6786b207b8d8": 143,
        "73e55440-d981-48e6-9639-d2ed7276f22d": 144,
        "762d218c-cdbd-4886-9252-10cd99284c7a": 145,
        "83594c82-2829-44c8-b2bf-3ff1c19fa4b1": 146,
        "ac552028-1157-4139-85c4-5bc94ee54a56": 147,
        "c555e067-c4d5-43f6-99af-716b6005cbba": 148,
        "cbe8d33e-a92a-473c-942f-90d8b76ed77c": 149,
        "e58c5e0e-f1f5-4685-9ff2-7197f9330bea": 150,
        "0b131b69-ffc9-4739-9aa0-0d54c1078200": 151,
        "f444ee53-e3b3-4899-923e-a27369ce7e59": 152,
        "1ec23c3b-649c-492f-97af-9ef1199f21a7": 153,
        "2c14656f-1be0-4bd5-9a1f-e9684a89a489": 154,
        "31a50d54-ef46-47a8-863c-6f4d4e5aa184": 155,
        "339879bc-5749-44cb-81b0-83449911f13d": 156,
        "3d43f259-7c1b-47ed-9dfd-d9478751d4ff": 157,
        "462416b4-840b-4c4a-a9bf-7d9e0b594e20": 160,
        "47e00cc4-53ca-453b-993a-0f58279e2a94": 162,
        "3360c00c-4737-4b6e-b683-46f4092cfb0a": 163,
        "76c71fde-f27f-4a50-8f7f-421898aacc72": 166,
        "238e8363-aa63-4f01-b47c-5405e78b16e6": 167,
        "7ff02e19-e829-4e56-9a34-233a71fce76c": 169,
        "81d36b4b-3713-4180-ac34-c033e019f639": 172,
        "90c64141-1d4d-4935-9387-fe236313c3f5": 178,
        "6e6545d7-7d40-4a3f-b962-5e17a9860fce": 179,
        "a012493e-ebc1-4f5a-9894-e9363958b4d7": 180,
        "ab55b5eb-f998-4480-a69b-eacaa7325ff3": 183,
        "b0d9c043-32b9-4c79-a692-564e93f62bd3": 186,
        "c179fb5c-9845-4e37-aef7-6e00d97548eb": 189,
        "c3a3881d-92e9-4352-979b-d8465a5a3605": 192,
        "f0ba938e-d631-48d3-9618-e0090a68a02d": 197,
        "04856926-1edc-4375-a147-246c4d66b6bb": 210,
        "05a90cd6-73de-43d5-9d30-bc2588d03262": 211,
        "1a072572-763d-4839-b920-82b48d8e296a": 212,
        "1b260e56-45ff-4a14-9b4e-744553ef15bf": 213,
        "23dfb4c0-f7ff-4372-b379-09fd61ce2616": 214,
        "6769d1ca-0581-48b0-b487-b5c87b8f696e": 215,
        "792fdc1e-e833-4777-a372-11e93e457480": 216,
        "79b65432-3224-4da9-a1dc-2a08d089c917": 217,
        "7a76d222-962a-4776-90e4-8683af6477bb": 218,
        "7dfa0971-96be-4705-9811-f9f54758145f": 219,
        "8a226084-2a76-4ff3-84b8-7dcc263aacc5": 220,
        "8af481b0-90f8-4ddb-8f2d-5a2529030f80": 221,
        "8b93c7f5-bb43-4a72-98fe-312cd08fc957": 222,
        "91ac13f8-e8d3-4902-b451-83ff32d2cf28": 223,
        "dd27a652-cb3d-484c-8a1b-731e0e1be32e": 224,
        "e8a19123-81c1-49b4-ac6d-6862e63427c8": 225,
        "ee2644c1-1260-4bf4-9c70-7c5b0cee4770": 226,
        "f0deff5f-c269-4389-9713-b8a7e70207cb": 227,
        "f1b776e4-b59e-48c7-9e8a-272de4946b37": 228,
        "ff461754-ad20-4eeb-af02-2b46cc980b24": 229,
        "0e163d44-67a7-4107-9421-5333600166bb": 257,
        "26414d70-d298-4999-a391-2eee2dd7067d": 259,
        "264a1d66-7f41-465a-b64c-c0f20ab31ad3": 261,
        "2ef5faba-5362-4111-98ed-22f7c639521e": 263,
        "3f64e9a6-6e1e-499b-aec8-764c99f634b2": 265,
        "48341095-ae5a-4d61-bcc8-1b0ceed870b2": 267,
        "4aafa7e4-d271-42d2-8979-bdefcd221d30": 269,
        "4ec1bff7-ec1b-488b-8a24-aed83e62b4ce": 272,
        "5a854508-5f41-4009-8986-a162224c511d": 274,
        "66156be8-6202-40bd-bdc2-014a46bee28f": 276,
        "68b7aac9-02fd-4bd8-b10c-6702d2c5eb98": 278,
        "9c8dc8ee-6207-48d5-81ee-f362f5e17f9b": 279,
        "b6eee153-eac4-41e5-afcb-ab46cf7a8ba8": 280,
        "b838cbad-0877-4189-ba3d-039962da7ebd": 281,
        "b9c5cdbd-98e7-4921-8e49-6c192326d8eb": 282,
        "ca6e9e9a-3d47-422d-bc1e-2dcf6deba5ca": 283,
        "d72a7bb4-146a-465e-85fc-dd54aee148eb": 284,
        "d98a598a-5ef5-4194-9fb2-c400370151be": 285,
        "95fd2469-00cc-481c-a42d-5ec9eaa80868": 298,
        "d5ef3cfe-2ab9-4b77-823a-62678c13058f": 302,
        "05dea31d-f1ff-491b-9f17-8be88b26f413": 324,
        "2c157857-fffd-4eb5-8e2a-b28ebea8da77": 326,
        "35cd1338-c56b-4247-b53c-264585c59883": 327,
        "4970099b-0a37-44f6-9b71-304040992efc": 328,
        "59f6f688-7000-4cf5-a27f-a1980dd86d93": 329,
        "5b59ce10-becf-4ab4-be21-a33fe998a90c": 330,
        "75df82d5-1156-42e1-877c-5964562d7e69": 331,
        "1db0df17-b3d5-4ddb-98d0-8f86239347bf": 332,
        "1f0687ca-c8f2-4c71-8306-8a18cbf6cc60": 333,
        "7c636961-816a-4b44-8991-671df9d91d9c": 334,
        "2f617d47-8839-40db-8286-40bd5cd95a71": 335,
        "7fb15c57-6024-4b0c-9493-8d52d3ef3c24": 336,
        "5769354c-0661-4ac7-86e5-3fd51506df36": 337,
        "8c81dcdb-fec1-4186-98ce-310f9f55bb0a": 338,
        "5a25d084-9ef7-4e81-8da8-737b5a9d6ed9": 339,
        "9cf99a61-6b51-4aed-8940-0480dc512b36": 340,
        "5be304d2-f98b-4f1b-a040-8cb402644ef7": 341,
        "a2c6a907-282f-4172-9d60-42d03987da0e": 342,
        "5e86a9c3-b4d0-4fe1-a551-acd83e5d60eb": 343,
        "62ae945c-5c43-4063-84b3-4a83b2fa4843": 344,
        "ad0aa3eb-81c3-4688-b769-e0375cdb5c13": 345,
        "62bc2f36-5cb9-449d-a5c4-b9f0f7863a37": 346,
        "664afb4f-3fc1-4e25-bcb8-bab2c0c3c33b": 347,
        "ba1b12c1-ee81-47d2-9f02-56110ff2a318": 348,
        "664f0884-717b-4f4a-a1a6-79f08acb41bd": 349,
        "cf3a87ec-c2f7-42e8-9698-6f8b2ba916a9": 350,
        "8c090758-6baa-468d-82fd-d47e17d5091b": 351,
        "e3c8bfbe-086f-4bbf-be9b-38accc5d5037": 352,
        "8e3cbaa3-e30a-4cf8-aa7a-1b57f15f0f98": 353,
        "e77345ce-8cb5-4727-a875-5332900b0309": 354,
        "b634fb27-1562-4d4a-b340-066c46e62d25": 355,
        "b7d0fa52-b5ca-4465-9bbb-3ec9b6b7b536": 356,
        "ee6b8f67-08cc-4d6f-ac8a-9f7c2432cb80": 357,
        "c8788ad2-89f7-4ec9-a22b-dcaf6190889b": 358,
        "f58ca913-fc54-4e8c-9e69-e0cd8bc22a1b": 359,
        "e1e4c26d-ab5c-4bd7-886a-812854466bb8": 360,
        "e7e7dc21-c48f-4c33-a9df-7b0027cc21d4": 361,
        "f3fd7679-312f-42a1-b78d-326da1492c03": 362,
        "02bdc54a-4db6-45d0-966e-d7659dd4ce13": 363,
        "0cf7e66d-14d3-463c-a825-e6fc62a0a6c6": 364,
        "162412a2-d4ff-46f0-8e08-53acc1ab838d": 365,
        "47cd6421-0ce1-431e-9b9c-a8d9bfd0eb04": 366,
        "20b06e01-26cb-4bc1-b5ff-c760a9ece0e4": 367,
        "5d3681c6-9c73-4895-9b59-b4851069469f": 368,
        "224fd5f2-02de-48c9-8c39-b2a5f6ed5486": 369,
        "5f3bd1f4-072b-4f32-9787-37670954cf3b": 370,
        "2bd97a34-ced9-4413-bfaa-94dbafaa0fdd": 371,
        "6b5d0264-fa2d-4956-919b-61abfc6bb8d7": 372,
        "460b7264-b98f-483e-b841-59a18c2e4d67": 373,
        "6ee485e1-534f-4d07-9492-c30b1ae9d607": 374,
        "5247355c-121e-4053-8627-54d99e61d518": 375,
        "61795760-96af-4588-82ad-5e40e79f2a73": 377,
        "7ea5ebcb-e825-4b6e-bd46-13a45c88c09c": 378,
        "81f26bbb-c9a8-488a-8f3e-dbede7757677": 379,
        "703719b2-2db0-4590-90f7-0be1041c1f81": 380,
        "85e1279a-77c4-49a7-bfa0-7699e64b581f": 381,
        "8f7caaba-426f-4bee-be51-9625718d51f3": 383,
        "a0d07bb9-3935-4d53-bdbb-6cb27c1a46b1": 384,
        "98ec8372-22fd-4ab4-88f2-94b47df7cb58": 385,
        "b73a8508-23a1-49ee-a466-aa9ea8add09e": 387,
        "a8b48aa9-cf98-4a87-8bba-e88eead8cdaa": 388,
        "c25afa99-b041-46db-9725-8d92492df50b": 390,
        "c1189e9c-3b45-4552-b731-e0ff544bc1bd": 391,
        "d386c6c9-7bd1-4a56-a0ca-3476c7b57fd6": 393,
        "f5987aa7-b7fd-4bd6-855d-fd6407324950": 395,
        "db90c8f4-5d2a-4ff9-8f57-1fc44a253dcf": 396,
        "f05628db-779b-41e8-9527-cf3b204b5bac": 398,
        "f77263f9-a97c-45b9-91f0-0f0da4156b9f": 399,
        "f2625432-3903-4f90-9b0b-2e4f63856bb0": 401,
        "fa1c4130-38de-4ea1-b93a-4c3c962473e6": 403,
        "fa431c70-d091-4548-9330-484321788b1d": 404,
        "ff76cdb2-9e72-4ba9-956f-9d99033cbe13": 406,
        "f4c21698-8e9b-4720-ac1e-5e07bd7c2e92": 420,
        "767837db-62fa-4fc6-b118-1d56a8b23415": 424,
        "a2a15cb3-9a7d-4e24-b3ce-62cb4e1c3c68": 430,
        "d5381ecd-6a70-401e-a019-817f51ac5aa2": 443,
        "0e6ddc9f-4a7b-4d48-8033-998103edfb32": 461,
        "11da94f7-02c0-4bc9-9da3-8e8994f46fb6": 463,
        "17d7d84a-1d9c-48e4-b13c-3c365ea16f13": 465,
        "2038ebc0-a35b-4979-9fd6-15c72c435101": 467,
        "3a3268ca-7e0d-4e26-81ac-8a51f1bcfde1": 469,
        "3b8024e6-5872-4ceb-b675-415715527776": 471,
        "44658d86-ae85-4ea9-80e5-0df9eab45cf0": 473,
        "4cbe58e4-5e4b-46b0-9f7b-6cf18ad002c6": 474,
        "510c6cdf-1a1a-450e-8d38-eed8d9b55df9": 476,
        "5176c4c0-b451-4122-81e9-7d5dc9502de5": 479,
        "54723896-1f7b-4150-95d6-0392596a328f": 480,
        "6f004551-2fd3-4c66-b1c4-a13fbd5ead5a": 482,
        "76b89403-aaea-4730-bb7e-e60f38c56c3e": 484,
        "895fa449-c569-44d1-ac1b-de05db7d2589": 487,
        "b60c920c-b42e-4896-9f6d-7f3031fc6492": 489,
        "d0cb08b3-51b4-4700-9311-4e111df81d49": 491,
        "ed343fa6-397c-4456-9f3f-63efee6706b5": 493,
        "ef11cca9-6605-44e8-943e-193c7b821465": 495,
        "f5163a3f-f880-4c2c-ac9b-00db844246b2": 496,
        "fea7b92a-0124-4775-8747-e4828f0dab8b": 497,
        "1647115a-1607-4250-889e-8ae1af98fc92": 498,
        "2012f4fd-98e0-4080-98a7-0cfb9de87067": 499,
        "2ccaaefc-917d-4e2a-b7c6-947836c38c6f": 500,
        "3e512d9e-ff9c-4f23-a4fd-a88128ee3af2": 501,
        "4d6d7a45-3144-472a-bd4f-a477e855011f": 502,
        "55e9d1e5-6ea3-4475-9877-d9d1f5f1910d": 503,
        "5b315e15-6633-4ce2-8200-71b821553314": 504,
        "7a3749f6-b03a-49eb-9e1d-07b897bd0b2d": 505,
        "98100660-988b-4e71-a89e-f35839964483": 507,
        "98a43535-8643-45ff-a954-2afecb418a9d": 508,
        "9fd789bc-0aa4-4028-b114-5014deacfbe2": 509,
        "a47ac0db-084a-4620-95e8-812c6168cf8d": 510,
        "aa9dc37e-bd55-48d7-b5ed-adc1b31d1143": 511,
        "ba16b6ef-0c63-4580-8119-2a2d5600b160": 512,
        "bf9ad0fd-0cb8-4360-8970-5f1b5cf3fa8d": 513,
        "c5ab83b1-9e16-46d2-b983-d75a8ed883d7": 514,
        "dbf62639-cf0d-43ea-b470-c116128b76ec": 515,
        "e3dfa2a2-6272-4f3f-adf0-dd5dadea9481": 516,
        "e96ef8d2-192f-47a3-a6ad-876603de1907": 517,
        "005948cb-f744-4928-bf7f-d26076717c99": 518,
        "298852ca-299d-4cb9-a9e5-6ac909582f78": 519,
        "390c3ce6-7e5b-4aba-bd54-4dfb6add4767": 520,
        "51d0a386-20a8-4e68-a8ec-face10febaff": 521,
        "5382cf43-3a79-4a5a-a7fd-153906fe65dd": 522,
        "56ff7cb8-4828-4aaa-8f95-0bf569a0786d": 523,
        "5ac1fb0f-24fe-4dce-aba5-6fc0dc9c27e7": 524,
        "84215e01-6108-4fd0-9a11-19e9518ab378": 525,
        "859f0120-c1e1-4b75-ba10-3dca7020312b": 526,
        "9304e1de-0d5a-4ccb-9409-100342405041": 527,
        "9570a938-324f-40e8-92dd-8a4fcf4a953b": 528,
        "9dbc15ee-deec-4c8c-86e9-71396ff80ef8": 531,
        "a34e015a-193c-4d57-b4b4-720eb5e1eef2": 533,
        "bc70a55a-cee0-478f-9a13-cf51c4a4187c": 535,
        "df6f21d3-5221-42e2-945b-8fe7cebdf03e": 538,
        "e5b54fa6-88e0-4702-9677-282f204a43e1": 540,
        "f3233c73-bb6b-44a4-8a16-20e772dbf69a": 542,
        "01e8f44f-f1ee-4d3a-86bd-c29d597ba9bd": 547,
        "765919dd-9d63-40a4-81fd-905ef04e4fc5": 573,
        "440251c0-601a-471a-9bdf-a8c7cd7efda8": 576,
        "d211740f-b91f-4ebd-8a4c-42db96770ae8": 580,
        "dbbb8ac3-ea3a-4271-99c5-95f7f99bb927": 581,
        "71663a1e-77a8-452e-b121-d4d06ed5c7db": 582,
        "d8e0340f-918d-4820-aa51-91e450721c9c": 583,
        "ff482131-2cfa-41e1-ba23-6e8503b55ed2": 584,
        "a1d0ec05-0d36-42fe-add4-170f7fc08692": 585,
        "a764ea7a-2209-4ff3-af9c-f97d9ac00333": 588,
        "28512bba-0a6b-4ec2-816a-72f2b43036e1": 589
      },
      "start": 1458255600000,
      "end": 1458273600000,
      "sport": "nba"
    }
  },
  "eventsMultipart": {
    "events": {},
    "watchablePlayers": []
  },
  "livePlayers": {
    "isFetching": [],
    "relevantPlayers": {},
    "fetched": [
      194
    ],
    "expiresAt": 1458241480616
  },
  "messages": {},
  "payments": {
    "payments": [],
    "depositFormErrors": {},
    "withdrawalFormErrors": {}
  },
  "playerNews": {
    "isFetching": false
  },
  "playerBoxScoreHistory": {
    "isFetching": false,
    "nba": {
      "1": {
        "id": 1,
        "fp": 30.0875,
        "points": 14.8,
        "rebounds": 4.05,
        "assists": 4.05,
        "steals": 1.9,
        "blocks": 0.45,
        "turnovers": 2.4
      },
      "2": {
        "id": 2,
        "fp": 9.325,
        "points": 5.35,
        "rebounds": 1.9,
        "assists": 0.45,
        "steals": 0.3,
        "blocks": 0.2,
        "turnovers": 0.85
      },
      "3": {
        "id": 3,
        "fp": 18.1875,
        "points": 9.2,
        "rebounds": 2.75,
        "assists": 2.4,
        "steals": 0.65,
        "blocks": 0.55,
        "turnovers": 1.55
      },
      "4": {
        "id": 4,
        "fp": 0.0625,
        "points": 0,
        "rebounds": 0.05,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "5": {
        "id": 5,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "6": {
        "id": 6,
        "fp": 5.475,
        "points": 2.3,
        "rebounds": 1.4,
        "assists": 0.4,
        "steals": 0.35,
        "blocks": 0.1,
        "turnovers": 0.3
      },
      "7": {
        "id": 7,
        "fp": 3.95,
        "points": 2.05,
        "rebounds": 0.7,
        "assists": 0.3,
        "steals": 0.1,
        "blocks": 0.1,
        "turnovers": 0.05
      },
      "8": {
        "id": 8,
        "fp": 24.3,
        "points": 12.15,
        "rebounds": 6.1,
        "assists": 0.6,
        "steals": 0.45,
        "blocks": 1.55,
        "turnovers": 1.2
      },
      "9": {
        "id": 9,
        "fp": 14.0125,
        "points": 4.85,
        "rebounds": 5.05,
        "assists": 0.9,
        "steals": 0.15,
        "blocks": 0.7,
        "turnovers": 0.55
      },
      "10": {
        "id": 10,
        "fp": 1.77631578947368,
        "points": 0.894736842105263,
        "rebounds": 0.263157894736842,
        "assists": 0.210526315789474,
        "steals": 0.105263157894737,
        "blocks": 0,
        "turnovers": 0.105263157894737
      },
      "11": {
        "id": 11,
        "fp": 1.8375,
        "points": 0.75,
        "rebounds": 0.55,
        "assists": 0,
        "steals": 0.15,
        "blocks": 0.05,
        "turnovers": 0
      },
      "12": {
        "id": 12,
        "fp": 15.75,
        "points": 6.75,
        "rebounds": 2.2,
        "assists": 2.1,
        "steals": 1.25,
        "blocks": 0.2,
        "turnovers": 0.95
      },
      "13": {
        "id": 13,
        "fp": 25.5125,
        "points": 11,
        "rebounds": 4.65,
        "assists": 4.2,
        "steals": 0.95,
        "blocks": 0.2,
        "turnovers": 1.2
      },
      "14": {
        "id": 14,
        "fp": 15.25,
        "points": 7.5,
        "rebounds": 4,
        "assists": 0.8,
        "steals": 0.3,
        "blocks": 0.55,
        "turnovers": 0.45
      },
      "15": {
        "id": 15,
        "fp": 10.725,
        "points": 5.3,
        "rebounds": 1.9,
        "assists": 0.9,
        "steals": 0.6,
        "blocks": 0.2,
        "turnovers": 0.4
      },
      "16": {
        "id": 16,
        "fp": 6.5875,
        "points": 4.4,
        "rebounds": 0.85,
        "assists": 0.35,
        "steals": 0.15,
        "blocks": 0.15,
        "turnovers": 0.65
      },
      "17": {
        "id": 17,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "18": {
        "id": 18,
        "fp": 40.4125,
        "points": 22.75,
        "rebounds": 4.85,
        "assists": 5.7,
        "steals": 1.1,
        "blocks": 0.15,
        "turnovers": 2
      },
      "19": {
        "id": 19,
        "fp": 3.375,
        "points": 1.5,
        "rebounds": 0.7,
        "assists": 0.25,
        "steals": 0.15,
        "blocks": 0.15,
        "turnovers": 0.05
      },
      "20": {
        "id": 20,
        "fp": 34.575,
        "points": 14.4,
        "rebounds": 5.9,
        "assists": 5.85,
        "steals": 1.05,
        "blocks": 1.05,
        "turnovers": 2.75
      },
      "21": {
        "id": 21,
        "fp": 5.4875,
        "points": 2.7,
        "rebounds": 0.95,
        "assists": 0.95,
        "steals": 0.15,
        "blocks": 0,
        "turnovers": 0.5
      },
      "22": {
        "id": 22,
        "fp": 0.625,
        "points": 0.25,
        "rebounds": 0.1,
        "assists": 0.05,
        "steals": 0.1,
        "blocks": 0,
        "turnovers": 0.1
      },
      "23": {
        "id": 23,
        "fp": 16.5875,
        "points": 6.7,
        "rebounds": 4.65,
        "assists": 1.2,
        "steals": 0.55,
        "blocks": 0.6,
        "turnovers": 0.85
      },
      "24": {
        "id": 24,
        "fp": 18.9125,
        "points": 9.05,
        "rebounds": 5.45,
        "assists": 1.35,
        "steals": 0.35,
        "blocks": 0.45,
        "turnovers": 1.3
      },
      "25": {
        "id": 25,
        "fp": 6.25,
        "points": 2.25,
        "rebounds": 1.6,
        "assists": 0.6,
        "steals": 0.2,
        "blocks": 0.45,
        "turnovers": 0.55
      },
      "26": {
        "id": 26,
        "fp": 6.6125,
        "points": 3.55,
        "rebounds": 0.85,
        "assists": 0.9,
        "steals": 0.35,
        "blocks": 0.05,
        "turnovers": 0.5
      },
      "27": {
        "id": 27,
        "fp": 30.7,
        "points": 15.6,
        "rebounds": 7.1,
        "assists": 1.15,
        "steals": 0.9,
        "blocks": 0.9,
        "turnovers": 0.85
      },
      "28": {
        "id": 28,
        "fp": 20.8875,
        "points": 8,
        "rebounds": 5.95,
        "assists": 1.45,
        "steals": 0.8,
        "blocks": 1.1,
        "turnovers": 1.35
      },
      "29": {
        "id": 29,
        "fp": 26.825,
        "points": 15.75,
        "rebounds": 3.9,
        "assists": 2.6,
        "steals": 1.05,
        "blocks": 0,
        "turnovers": 1.45
      },
      "30": {
        "id": 30,
        "fp": 21.125,
        "points": 8.7,
        "rebounds": 6.8,
        "assists": 1.2,
        "steals": 0.5,
        "blocks": 0.8,
        "turnovers": 1.3
      },
      "31": {
        "id": 31,
        "fp": 43.55,
        "points": 23.05,
        "rebounds": 6.7,
        "assists": 5.05,
        "steals": 1.8,
        "blocks": 0.45,
        "turnovers": 2.85
      },
      "32": {
        "id": 32,
        "fp": 9.7625,
        "points": 3.95,
        "rebounds": 1.45,
        "assists": 2.25,
        "steals": 0.25,
        "blocks": 0.25,
        "turnovers": 1
      },
      "33": {
        "id": 33,
        "fp": 9.3625,
        "points": 3.5,
        "rebounds": 2.65,
        "assists": 0.95,
        "steals": 0.5,
        "blocks": 0.1,
        "turnovers": 0.5
      },
      "34": {
        "id": 34,
        "fp": 1.7875,
        "points": 0.8,
        "rebounds": 0.55,
        "assists": 0.1,
        "steals": 0,
        "blocks": 0.1,
        "turnovers": 0.1
      },
      "35": {
        "id": 35,
        "fp": 7.325,
        "points": 3.8,
        "rebounds": 1.9,
        "assists": 0.4,
        "steals": 0.15,
        "blocks": 0.15,
        "turnovers": 0.3
      },
      "36": {
        "id": 36,
        "fp": 5.70833333333333,
        "points": 1.33333333333333,
        "rebounds": 2.16666666666667,
        "assists": 0.5,
        "steals": 0.166666666666667,
        "blocks": 0.333333333333333,
        "turnovers": 0.166666666666667
      },
      "37": {
        "id": 37,
        "fp": 11.8,
        "points": 4.7,
        "rebounds": 3.2,
        "assists": 0.75,
        "steals": 0.4,
        "blocks": 0.75,
        "turnovers": 0.65
      },
      "38": {
        "id": 38,
        "fp": 5.6375,
        "points": 3.8,
        "rebounds": 0.55,
        "assists": 0.7,
        "steals": 0.05,
        "blocks": 0,
        "turnovers": 0.2
      },
      "39": {
        "id": 39,
        "fp": 31.4625,
        "points": 14,
        "rebounds": 11.35,
        "assists": 1.4,
        "steals": 0.6,
        "blocks": 0.05,
        "turnovers": 2.05
      },
      "40": {
        "id": 40,
        "fp": 17.7625,
        "points": 11.2,
        "rebounds": 1.85,
        "assists": 1.75,
        "steals": 0.65,
        "blocks": 0.2,
        "turnovers": 1.3
      },
      "41": {
        "id": 41,
        "fp": 2.2875,
        "points": 0.8,
        "rebounds": 0.65,
        "assists": 0.15,
        "steals": 0.2,
        "blocks": 0.05,
        "turnovers": 0.1
      },
      "42": {
        "id": 42,
        "fp": 4.16666666666667,
        "points": 2.5,
        "rebounds": 0.666666666666667,
        "assists": 0,
        "steals": 0.5,
        "blocks": 0,
        "turnovers": 0.666666666666667
      },
      "43": {
        "id": 43,
        "fp": 2.95,
        "points": 0.9,
        "rebounds": 1,
        "assists": 0.3,
        "steals": 0.15,
        "blocks": 0.05,
        "turnovers": 0.15
      },
      "44": {
        "id": 44,
        "fp": 6.6625,
        "points": 1.7,
        "rebounds": 2.55,
        "assists": 0.3,
        "steals": 0.3,
        "blocks": 0.45,
        "turnovers": 0.35
      },
      "45": {
        "id": 45,
        "fp": 8.675,
        "points": 3.15,
        "rebounds": 3.1,
        "assists": 0.45,
        "steals": 0.4,
        "blocks": 0.2,
        "turnovers": 0.45
      },
      "46": {
        "id": 46,
        "fp": 3.79166666666667,
        "points": 1.33333333333333,
        "rebounds": 1.16666666666667,
        "assists": 0.5,
        "steals": 0.166666666666667,
        "blocks": 0,
        "turnovers": 0.333333333333333
      },
      "47": {
        "id": 47,
        "fp": 17.5,
        "points": 8.15,
        "rebounds": 4.4,
        "assists": 1,
        "steals": 0.55,
        "blocks": 0.8,
        "turnovers": 0.7
      },
      "48": {
        "id": 48,
        "fp": 8.8875,
        "points": 5,
        "rebounds": 1.65,
        "assists": 0.7,
        "steals": 0.2,
        "blocks": 0.1,
        "turnovers": 0.4
      },
      "49": {
        "id": 49,
        "fp": 28.7875,
        "points": 16.4,
        "rebounds": 3.05,
        "assists": 3.9,
        "steals": 1.25,
        "blocks": 0.15,
        "turnovers": 2.2
      },
      "50": {
        "id": 50,
        "fp": 3.975,
        "points": 1.4,
        "rebounds": 1,
        "assists": 0.5,
        "steals": 0.2,
        "blocks": 0.05,
        "turnovers": 0.05
      },
      "51": {
        "id": 51,
        "fp": 3.54166666666667,
        "points": 1.33333333333333,
        "rebounds": 0.833333333333333,
        "assists": 0.166666666666667,
        "steals": 0,
        "blocks": 0.5,
        "turnovers": 0.166666666666667
      },
      "52": {
        "id": 52,
        "fp": 2.58333333333333,
        "points": 0.666666666666667,
        "rebounds": 1,
        "assists": 0,
        "steals": 0.166666666666667,
        "blocks": 0.166666666666667,
        "turnovers": 0
      },
      "53": {
        "id": 53,
        "fp": 22.075,
        "points": 14.05,
        "rebounds": 3.1,
        "assists": 1.55,
        "steals": 0.6,
        "blocks": 0.1,
        "turnovers": 0.9
      },
      "54": {
        "id": 54,
        "fp": 6.5,
        "points": 2.65,
        "rebounds": 1.1,
        "assists": 0.55,
        "steals": 0.3,
        "blocks": 0.5,
        "turnovers": 0.15
      },
      "55": {
        "id": 55,
        "fp": 13.125,
        "points": 4.15,
        "rebounds": 4,
        "assists": 1.45,
        "steals": 0.4,
        "blocks": 0.6,
        "turnovers": 0.55
      },
      "56": {
        "id": 56,
        "fp": 18.025,
        "points": 7.85,
        "rebounds": 4,
        "assists": 1.85,
        "steals": 0.6,
        "blocks": 0.85,
        "turnovers": 1.05
      },
      "57": {
        "id": 57,
        "fp": 5.7125,
        "points": 2.2,
        "rebounds": 2.15,
        "assists": 0.3,
        "steals": 0.1,
        "blocks": 0.15,
        "turnovers": 0.25
      },
      "58": {
        "id": 58,
        "fp": 15.7375,
        "points": 5.65,
        "rebounds": 3.75,
        "assists": 1.8,
        "steals": 1.15,
        "blocks": 0.45,
        "turnovers": 1.15
      },
      "59": {
        "id": 59,
        "fp": 36.7875,
        "points": 20.7,
        "rebounds": 7.55,
        "assists": 1.65,
        "steals": 0.55,
        "blocks": 1.55,
        "turnovers": 0.95
      },
      "60": {
        "id": 60,
        "fp": 0.5,
        "points": 0,
        "rebounds": 0.4,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "61": {
        "id": 61,
        "fp": 4.9,
        "points": 2,
        "rebounds": 1.2,
        "assists": 0.2,
        "steals": 0.6,
        "blocks": 0,
        "turnovers": 0.2
      },
      "62": {
        "id": 62,
        "fp": 3.1,
        "points": 1.8,
        "rebounds": 0.4,
        "assists": 0.2,
        "steals": 0.2,
        "blocks": 0.2,
        "turnovers": 0.6
      },
      "63": {
        "id": 63,
        "fp": 6.95,
        "points": 3.55,
        "rebounds": 1.3,
        "assists": 0.8,
        "steals": 0.25,
        "blocks": 0.15,
        "turnovers": 0.6
      },
      "64": {
        "id": 64,
        "fp": 0.6,
        "points": 0.2,
        "rebounds": 0,
        "assists": 0.15,
        "steals": 0.15,
        "blocks": 0,
        "turnovers": 0.25
      },
      "65": {
        "id": 65,
        "fp": 20.1375,
        "points": 8.05,
        "rebounds": 4.15,
        "assists": 1.8,
        "steals": 1.2,
        "blocks": 0.75,
        "turnovers": 0.85
      },
      "66": {
        "id": 66,
        "fp": 12.1125,
        "points": 4.7,
        "rebounds": 2.55,
        "assists": 2.25,
        "steals": 0.3,
        "blocks": 0.3,
        "turnovers": 1.05
      },
      "67": {
        "id": 67,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "68": {
        "id": 68,
        "fp": 1.84615384615385,
        "points": 1,
        "rebounds": 0.461538461538462,
        "assists": 0.153846153846154,
        "steals": 0.0769230769230769,
        "blocks": 0,
        "turnovers": 0.307692307692308
      },
      "69": {
        "id": 69,
        "fp": 0.361111111111111,
        "points": 0,
        "rebounds": 0.111111111111111,
        "assists": 0,
        "steals": 0.111111111111111,
        "blocks": 0,
        "turnovers": 0
      },
      "70": {
        "id": 70,
        "fp": 1.4625,
        "points": 0.9,
        "rebounds": 0.25,
        "assists": 0.1,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "71": {
        "id": 71,
        "fp": 6.79166666666667,
        "points": 1.83333333333333,
        "rebounds": 3.16666666666667,
        "assists": 0.166666666666667,
        "steals": 0.333333333333333,
        "blocks": 0.166666666666667,
        "turnovers": 0.5
      },
      "72": {
        "id": 72,
        "fp": 5.8375,
        "points": 3.4,
        "rebounds": 0.55,
        "assists": 0.65,
        "steals": 0.45,
        "blocks": 0,
        "turnovers": 0.55
      },
      "73": {
        "id": 73,
        "fp": 31.9125,
        "points": 9.8,
        "rebounds": 11.75,
        "assists": 1.6,
        "steals": 0.85,
        "blocks": 1.8,
        "turnovers": 1.9
      },
      "74": {
        "id": 74,
        "fp": 22.3375,
        "points": 10.75,
        "rebounds": 2.85,
        "assists": 3.95,
        "steals": 0.65,
        "blocks": 0.1,
        "turnovers": 0.75
      },
      "75": {
        "id": 75,
        "fp": 1,
        "points": 0.2,
        "rebounds": 0.4,
        "assists": 0.2,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "76": {
        "id": 76,
        "fp": 6.2625,
        "points": 2.85,
        "rebounds": 1.05,
        "assists": 0.95,
        "steals": 0.25,
        "blocks": 0.1,
        "turnovers": 0.45
      },
      "77": {
        "id": 77,
        "fp": 3.8125,
        "points": 1.05,
        "rebounds": 0.95,
        "assists": 0.7,
        "steals": 0.25,
        "blocks": 0.1,
        "turnovers": 0.35
      },
      "78": {
        "id": 78,
        "fp": 19.475,
        "points": 9.65,
        "rebounds": 2,
        "assists": 4.85,
        "steals": 0.35,
        "blocks": 0.05,
        "turnovers": 1.95
      },
      "79": {
        "id": 79,
        "fp": 9.775,
        "points": 5.45,
        "rebounds": 2.5,
        "assists": 0.3,
        "steals": 0.15,
        "blocks": 0.25,
        "turnovers": 0.65
      },
      "80": {
        "id": 80,
        "fp": 8.45833333333333,
        "points": 3.83333333333333,
        "rebounds": 1.83333333333333,
        "assists": 0.5,
        "steals": 0.5,
        "blocks": 0.166666666666667,
        "turnovers": 0.333333333333333
      },
      "81": {
        "id": 81,
        "fp": 7.275,
        "points": 4.2,
        "rebounds": 0.8,
        "assists": 1.05,
        "steals": 0.25,
        "blocks": 0.05,
        "turnovers": 0.85
      },
      "82": {
        "id": 82,
        "fp": 35.05,
        "points": 19.75,
        "rebounds": 6.1,
        "assists": 2.2,
        "steals": 1.35,
        "blocks": 0.75,
        "turnovers": 1.5
      },
      "83": {
        "id": 83,
        "fp": 7.9125,
        "points": 2.85,
        "rebounds": 1.65,
        "assists": 1.3,
        "steals": 0.6,
        "blocks": 0,
        "turnovers": 0.8
      },
      "84": {
        "id": 84,
        "fp": 0.7,
        "points": 0.3,
        "rebounds": 0.2,
        "assists": 0.05,
        "steals": 0.05,
        "blocks": 0,
        "turnovers": 0.05
      },
      "85": {
        "id": 85,
        "fp": 0.6625,
        "points": 0.45,
        "rebounds": 0.05,
        "assists": 0.05,
        "steals": 0,
        "blocks": 0.05,
        "turnovers": 0.05
      },
      "86": {
        "id": 86,
        "fp": 25.1125,
        "points": 11.45,
        "rebounds": 6.75,
        "assists": 0.8,
        "steals": 0.6,
        "blocks": 1.4,
        "turnovers": 1.15
      },
      "87": {
        "id": 87,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "88": {
        "id": 88,
        "fp": 12.7125,
        "points": 6.95,
        "rebounds": 1.65,
        "assists": 1.2,
        "steals": 0.85,
        "blocks": 0.15,
        "turnovers": 0.9
      },
      "89": {
        "id": 89,
        "fp": 14.3875,
        "points": 5.5,
        "rebounds": 4.95,
        "assists": 0.85,
        "steals": 0.55,
        "blocks": 0.35,
        "turnovers": 0.8
      },
      "90": {
        "id": 90,
        "fp": 4.6375,
        "points": 3.3,
        "rebounds": 0.45,
        "assists": 0.2,
        "steals": 0.15,
        "blocks": 0,
        "turnovers": 0.1
      },
      "91": {
        "id": 91,
        "fp": 13.7125,
        "points": 7.25,
        "rebounds": 1.55,
        "assists": 2.3,
        "steals": 0.7,
        "blocks": 0,
        "turnovers": 1.5
      },
      "92": {
        "id": 92,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "93": {
        "id": 93,
        "fp": 34.1875,
        "points": 20.4,
        "rebounds": 4.65,
        "assists": 3.65,
        "steals": 1.15,
        "blocks": 0.25,
        "turnovers": 2.45
      },
      "94": {
        "id": 94,
        "fp": 52.575,
        "points": 29.65,
        "rebounds": 8.4,
        "assists": 5.4,
        "steals": 0.8,
        "blocks": 1.45,
        "turnovers": 4.15
      },
      "95": {
        "id": 95,
        "fp": 36.6,
        "points": 17,
        "rebounds": 8.9,
        "assists": 1.7,
        "steals": 0.95,
        "blocks": 2.25,
        "turnovers": 2.15
      },
      "96": {
        "id": 96,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "97": {
        "id": 97,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "98": {
        "id": 98,
        "fp": 25.6125,
        "points": 15.1,
        "rebounds": 3.25,
        "assists": 2.75,
        "steals": 0.95,
        "blocks": 0.1,
        "turnovers": 1.5
      },
      "99": {
        "id": 99,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "100": {
        "id": 100,
        "fp": 27.65,
        "points": 14.55,
        "rebounds": 8.9,
        "assists": 0.3,
        "steals": 0.5,
        "blocks": 0.35,
        "turnovers": 1.55
      },
      "101": {
        "id": 101,
        "fp": 9.1375,
        "points": 3.45,
        "rebounds": 2.45,
        "assists": 0.6,
        "steals": 0.4,
        "blocks": 0.5,
        "turnovers": 0.65
      },
      "102": {
        "id": 102,
        "fp": 20.525,
        "points": 13,
        "rebounds": 3.4,
        "assists": 0.75,
        "steals": 0.35,
        "blocks": 0.35,
        "turnovers": 0.8
      },
      "103": {
        "id": 103,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "104": {
        "id": 104,
        "fp": 6.7625,
        "points": 2.65,
        "rebounds": 2.35,
        "assists": 0.15,
        "steals": 0.15,
        "blocks": 0.25,
        "turnovers": 0.05
      },
      "105": {
        "id": 105,
        "fp": 10.3,
        "points": 4.25,
        "rebounds": 1.2,
        "assists": 1.7,
        "steals": 0.75,
        "blocks": 0.25,
        "turnovers": 0.8
      },
      "106": {
        "id": 106,
        "fp": 54.4875,
        "points": 22.75,
        "rebounds": 8.35,
        "assists": 12,
        "steals": 1.4,
        "blocks": 0.3,
        "turnovers": 4.25
      },
      "107": {
        "id": 107,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "108": {
        "id": 108,
        "fp": 23.825,
        "points": 11.05,
        "rebounds": 5.7,
        "assists": 2,
        "steals": 0.9,
        "blocks": 0.7,
        "turnovers": 1.75
      },
      "109": {
        "id": 109,
        "fp": 17.4625,
        "points": 8.7,
        "rebounds": 1.75,
        "assists": 3.5,
        "steals": 0.65,
        "blocks": 0,
        "turnovers": 1.35
      },
      "110": {
        "id": 110,
        "fp": 1.7875,
        "points": 1.15,
        "rebounds": 0.25,
        "assists": 0.15,
        "steals": 0.05,
        "blocks": 0,
        "turnovers": 0
      },
      "111": {
        "id": 111,
        "fp": 20.1625,
        "points": 8.4,
        "rebounds": 6.75,
        "assists": 0.75,
        "steals": 0.45,
        "blocks": 0.95,
        "turnovers": 1.2
      },
      "112": {
        "id": 112,
        "fp": 28.9125,
        "points": 12.3,
        "rebounds": 9.95,
        "assists": 1.4,
        "steals": 0.5,
        "blocks": 0.75,
        "turnovers": 2.2
      },
      "113": {
        "id": 113,
        "fp": 0.625,
        "points": 0,
        "rebounds": 0.5,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "114": {
        "id": 114,
        "fp": 4.5,
        "points": 2,
        "rebounds": 1.5,
        "assists": 0.25,
        "steals": 0.25,
        "blocks": 0,
        "turnovers": 0.5
      },
      "115": {
        "id": 115,
        "fp": 0.6125,
        "points": 0.5,
        "rebounds": 0.05,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.05
      },
      "116": {
        "id": 116,
        "fp": 29.5875,
        "points": 18.4,
        "rebounds": 3.05,
        "assists": 4.2,
        "steals": 0.5,
        "blocks": 0.3,
        "turnovers": 2.85
      },
      "117": {
        "id": 117,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "118": {
        "id": 118,
        "fp": 19.9375,
        "points": 7.25,
        "rebounds": 8.25,
        "assists": 0.75,
        "steals": 0.3,
        "blocks": 0.45,
        "turnovers": 1.4
      },
      "119": {
        "id": 119,
        "fp": 9.5375,
        "points": 4.2,
        "rebounds": 2.65,
        "assists": 0.55,
        "steals": 0.5,
        "blocks": 0.1,
        "turnovers": 0.45
      },
      "120": {
        "id": 120,
        "fp": 4.675,
        "points": 2.35,
        "rebounds": 0.9,
        "assists": 0.85,
        "steals": 0.15,
        "blocks": 0,
        "turnovers": 0.75
      },
      "121": {
        "id": 121,
        "fp": 7.2875,
        "points": 3.05,
        "rebounds": 1.15,
        "assists": 1.4,
        "steals": 0.35,
        "blocks": 0.1,
        "turnovers": 0.65
      },
      "122": {
        "id": 122,
        "fp": 1.625,
        "points": 0,
        "rebounds": 0.5,
        "assists": 0,
        "steals": 0.25,
        "blocks": 0.25,
        "turnovers": 0
      },
      "123": {
        "id": 123,
        "fp": 4,
        "points": 1.15,
        "rebounds": 1.6,
        "assists": 0.4,
        "steals": 0.1,
        "blocks": 0.2,
        "turnovers": 0.7
      },
      "124": {
        "id": 124,
        "fp": 19.5625,
        "points": 11.6,
        "rebounds": 3.05,
        "assists": 2.75,
        "steals": 0.3,
        "blocks": 0.15,
        "turnovers": 2.35
      },
      "125": {
        "id": 125,
        "fp": 1.325,
        "points": 0.7,
        "rebounds": 0.5,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "126": {
        "id": 126,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "128": {
        "id": 128,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "129": {
        "id": 129,
        "fp": 22.375,
        "points": 8.3,
        "rebounds": 6.2,
        "assists": 2.35,
        "steals": 1.35,
        "blocks": 0.2,
        "turnovers": 1.6
      },
      "130": {
        "id": 130,
        "fp": 9.8375,
        "points": 4.6,
        "rebounds": 2.85,
        "assists": 0.55,
        "steals": 0.3,
        "blocks": 0.2,
        "turnovers": 0.5
      },
      "131": {
        "id": 131,
        "fp": 5.05,
        "points": 2.4,
        "rebounds": 0.6,
        "assists": 0.95,
        "steals": 0.15,
        "blocks": 0.1,
        "turnovers": 0.6
      },
      "132": {
        "id": 132,
        "fp": 7.975,
        "points": 2.75,
        "rebounds": 1.5,
        "assists": 1.3,
        "steals": 0.65,
        "blocks": 0.15,
        "turnovers": 1.2
      },
      "133": {
        "id": 133,
        "fp": 5.625,
        "points": 2,
        "rebounds": 1.5,
        "assists": 0.5,
        "steals": 0.5,
        "blocks": 0,
        "turnovers": 0
      },
      "134": {
        "id": 134,
        "fp": 5.25,
        "points": 2,
        "rebounds": 1.4,
        "assists": 0.4,
        "steals": 0,
        "blocks": 0.4,
        "turnovers": 0.2
      },
      "135": {
        "id": 135,
        "fp": 14.2875,
        "points": 5.45,
        "rebounds": 3.05,
        "assists": 2.15,
        "steals": 0.6,
        "blocks": 0.55,
        "turnovers": 1.3
      },
      "136": {
        "id": 136,
        "fp": 4.2125,
        "points": 1.8,
        "rebounds": 0.65,
        "assists": 0.85,
        "steals": 0.2,
        "blocks": 0,
        "turnovers": 0.3
      },
      "137": {
        "id": 137,
        "fp": 1.05,
        "points": 0,
        "rebounds": 0.6,
        "assists": 0.4,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.6
      },
      "138": {
        "id": 138,
        "fp": 1.675,
        "points": 0.55,
        "rebounds": 0.6,
        "assists": 0.15,
        "steals": 0.1,
        "blocks": 0,
        "turnovers": 0.1
      },
      "139": {
        "id": 139,
        "fp": 2.90277777777778,
        "points": 1.16666666666667,
        "rebounds": 0.277777777777778,
        "assists": 0.888888888888889,
        "steals": 0.111111111111111,
        "blocks": 0,
        "turnovers": 0.333333333333333
      },
      "140": {
        "id": 140,
        "fp": 36.025,
        "points": 18.9,
        "rebounds": 4.5,
        "assists": 4.1,
        "steals": 2.65,
        "blocks": 0.3,
        "turnovers": 2.9
      },
      "141": {
        "id": 141,
        "fp": 44.725,
        "points": 18.7,
        "rebounds": 8.5,
        "assists": 6,
        "steals": 1.7,
        "blocks": 1.6,
        "turnovers": 2.65
      },
      "142": {
        "id": 142,
        "fp": 0.7375,
        "points": 0.55,
        "rebounds": 0.05,
        "assists": 0.05,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.05
      },
      "143": {
        "id": 143,
        "fp": 4.9,
        "points": 2.4,
        "rebounds": 0.7,
        "assists": 0.6,
        "steals": 0.25,
        "blocks": 0.1,
        "turnovers": 0.3
      },
      "144": {
        "id": 144,
        "fp": 16.6,
        "points": 7.1,
        "rebounds": 5.2,
        "assists": 0.35,
        "steals": 0.4,
        "blocks": 1.05,
        "turnovers": 0.85
      },
      "145": {
        "id": 145,
        "fp": 30.1125,
        "points": 13.9,
        "rebounds": 8.35,
        "assists": 2,
        "steals": 0.75,
        "blocks": 0.8,
        "turnovers": 1.4
      },
      "146": {
        "id": 146,
        "fp": 0.3,
        "points": 0.1,
        "rebounds": 0.1,
        "assists": 0,
        "steals": 0.05,
        "blocks": 0,
        "turnovers": 0.05
      },
      "147": {
        "id": 147,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "148": {
        "id": 148,
        "fp": 0.3375,
        "points": 0.2,
        "rebounds": 0.05,
        "assists": 0,
        "steals": 0.05,
        "blocks": 0,
        "turnovers": 0.05
      },
      "149": {
        "id": 149,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "150": {
        "id": 150,
        "fp": 29.275,
        "points": 17,
        "rebounds": 5.7,
        "assists": 1.95,
        "steals": 1.15,
        "blocks": 0.35,
        "turnovers": 2.2
      },
      "151": {
        "id": 151,
        "fp": 21.475,
        "points": 9,
        "rebounds": 3.4,
        "assists": 4.35,
        "steals": 0.9,
        "blocks": 0.1,
        "turnovers": 1.5
      },
      "152": {
        "id": 152,
        "fp": 16.275,
        "points": 8.4,
        "rebounds": 2.1,
        "assists": 2.15,
        "steals": 0.6,
        "blocks": 0.15,
        "turnovers": 0.65
      },
      "153": {
        "id": 153,
        "fp": 15.05,
        "points": 3.35,
        "rebounds": 5.9,
        "assists": 1.3,
        "steals": 0.85,
        "blocks": 0.55,
        "turnovers": 1
      },
      "154": {
        "id": 154,
        "fp": 26.725,
        "points": 14.2,
        "rebounds": 3.6,
        "assists": 4.35,
        "steals": 0.8,
        "blocks": 0.1,
        "turnovers": 2.35
      },
      "155": {
        "id": 155,
        "fp": 32.6875,
        "points": 14.15,
        "rebounds": 9.15,
        "assists": 2.55,
        "steals": 1.35,
        "blocks": 0.5,
        "turnovers": 1.85
      },
      "156": {
        "id": 156,
        "fp": 7.0625,
        "points": 4.65,
        "rebounds": 1.15,
        "assists": 0.45,
        "steals": 0.05,
        "blocks": 0.15,
        "turnovers": 0.25
      },
      "157": {
        "id": 157,
        "fp": 14.2625,
        "points": 7.95,
        "rebounds": 1.75,
        "assists": 1.9,
        "steals": 0.6,
        "blocks": 0.05,
        "turnovers": 1
      },
      "158": {
        "id": 158,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "159": {
        "id": 159,
        "fp": 21.8875,
        "points": 4.85,
        "rebounds": 6.45,
        "assists": 2.75,
        "steals": 0.8,
        "blocks": 1.85,
        "turnovers": 1.1
      },
      "160": {
        "id": 160,
        "fp": 2.275,
        "points": 0.8,
        "rebounds": 0.5,
        "assists": 0.25,
        "steals": 0.15,
        "blocks": 0.1,
        "turnovers": 0.25
      },
      "161": {
        "id": 161,
        "fp": 3.29166666666667,
        "points": 1.33333333333333,
        "rebounds": 0.5,
        "assists": 0.666666666666667,
        "steals": 0,
        "blocks": 0.166666666666667,
        "turnovers": 0.333333333333333
      },
      "162": {
        "id": 162,
        "fp": 16.925,
        "points": 10.45,
        "rebounds": 2.5,
        "assists": 1.15,
        "steals": 0.55,
        "blocks": 0,
        "turnovers": 0.5
      },
      "163": {
        "id": 163,
        "fp": 4.55,
        "points": 1.7,
        "rebounds": 1.2,
        "assists": 0.3,
        "steals": 0.25,
        "blocks": 0.25,
        "turnovers": 0.25
      },
      "164": {
        "id": 164,
        "fp": 10.8,
        "points": 3,
        "rebounds": 1.2,
        "assists": 2.8,
        "steals": 1,
        "blocks": 0.2,
        "turnovers": 0.8
      },
      "165": {
        "id": 165,
        "fp": 10.9125,
        "points": 6.3,
        "rebounds": 1.65,
        "assists": 1.05,
        "steals": 0.4,
        "blocks": 0.1,
        "turnovers": 0.35
      },
      "166": {
        "id": 166,
        "fp": 16.35,
        "points": 6.25,
        "rebounds": 2,
        "assists": 4.3,
        "steals": 0.95,
        "blocks": 0.05,
        "turnovers": 2
      },
      "167": {
        "id": 167,
        "fp": 8.3625,
        "points": 6.1,
        "rebounds": 0.95,
        "assists": 0.35,
        "steals": 0.15,
        "blocks": 0,
        "turnovers": 0.45
      },
      "168": {
        "id": 168,
        "fp": 8.175,
        "points": 3.25,
        "rebounds": 2.1,
        "assists": 0.75,
        "steals": 0.25,
        "blocks": 0.3,
        "turnovers": 0.3
      },
      "169": {
        "id": 169,
        "fp": 18.475,
        "points": 11.8,
        "rebounds": 2.9,
        "assists": 1.6,
        "steals": 0.2,
        "blocks": 0.05,
        "turnovers": 1.55
      },
      "170": {
        "id": 170,
        "fp": 25.55,
        "points": 14.8,
        "rebounds": 5.7,
        "assists": 1.05,
        "steals": 0.55,
        "blocks": 0.25,
        "turnovers": 1.1
      },
      "171": {
        "id": 171,
        "fp": 34.2625,
        "points": 23.55,
        "rebounds": 3.65,
        "assists": 1.4,
        "steals": 1.4,
        "blocks": 0.15,
        "turnovers": 1.35
      },
      "172": {
        "id": 172,
        "fp": 14.1,
        "points": 7.4,
        "rebounds": 2.8,
        "assists": 1,
        "steals": 0.4,
        "blocks": 0.6,
        "turnovers": 2
      },
      "173": {
        "id": 173,
        "fp": 5.08333333333333,
        "points": 1.33333333333333,
        "rebounds": 0.333333333333333,
        "assists": 2,
        "steals": 0.333333333333333,
        "blocks": 0,
        "turnovers": 0.666666666666667
      },
      "174": {
        "id": 174,
        "fp": 39.3375,
        "points": 11.1,
        "rebounds": 10.05,
        "assists": 7.35,
        "steals": 1.3,
        "blocks": 1.35,
        "turnovers": 3.5
      },
      "175": {
        "id": 175,
        "fp": 7.33333333333333,
        "points": 4.13333333333333,
        "rebounds": 1.6,
        "assists": 0.4,
        "steals": 0.2,
        "blocks": 0,
        "turnovers": 0.4
      },
      "176": {
        "id": 176,
        "fp": 13.1375,
        "points": 6.35,
        "rebounds": 2.35,
        "assists": 1.1,
        "steals": 0.5,
        "blocks": 0.6,
        "turnovers": 0.7
      },
      "177": {
        "id": 177,
        "fp": 1.5625,
        "points": 0.5,
        "rebounds": 0.25,
        "assists": 0.25,
        "steals": 0.25,
        "blocks": 0,
        "turnovers": 0.25
      },
      "178": {
        "id": 178,
        "fp": 9.9,
        "points": 6,
        "rebounds": 1.6,
        "assists": 1,
        "steals": 0.2,
        "blocks": 0.2,
        "turnovers": 1.2
      },
      "179": {
        "id": 179,
        "fp": 0.0625,
        "points": 0,
        "rebounds": 0.05,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "180": {
        "id": 180,
        "fp": 3.1375,
        "points": 1.2,
        "rebounds": 0.65,
        "assists": 0.05,
        "steals": 0.25,
        "blocks": 0.3,
        "turnovers": 0.2
      },
      "181": {
        "id": 181,
        "fp": 37.525,
        "points": 19.4,
        "rebounds": 3.5,
        "assists": 7.05,
        "steals": 1.65,
        "blocks": 0.4,
        "turnovers": 3.45
      },
      "182": {
        "id": 182,
        "fp": 14.4375,
        "points": 5.65,
        "rebounds": 2.05,
        "assists": 2.9,
        "steals": 0.8,
        "blocks": 0.4,
        "turnovers": 1.05
      },
      "183": {
        "id": 183,
        "fp": 5.2625,
        "points": 2.15,
        "rebounds": 1.25,
        "assists": 0.25,
        "steals": 0.15,
        "blocks": 0.45,
        "turnovers": 0.05
      },
      "184": {
        "id": 184,
        "fp": 6.4125,
        "points": 2.7,
        "rebounds": 1.65,
        "assists": 0.6,
        "steals": 0.35,
        "blocks": 0.05,
        "turnovers": 0.45
      },
      "185": {
        "id": 185,
        "fp": 48.45,
        "points": 28.65,
        "rebounds": 4.9,
        "assists": 5.6,
        "steals": 1.75,
        "blocks": 0.2,
        "turnovers": 2.75
      },
      "186": {
        "id": 186,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "187": {
        "id": 187,
        "fp": 4.85,
        "points": 0.9,
        "rebounds": 2.2,
        "assists": 0.35,
        "steals": 0.35,
        "blocks": 0.15,
        "turnovers": 0.65
      },
      "188": {
        "id": 188,
        "fp": 3.8125,
        "points": 1.95,
        "rebounds": 0.65,
        "assists": 0.55,
        "steals": 0.15,
        "blocks": 0,
        "turnovers": 0.3
      },
      "189": {
        "id": 189,
        "fp": 40.25,
        "points": 22.85,
        "rebounds": 7,
        "assists": 2.5,
        "steals": 1.1,
        "blocks": 1.75,
        "turnovers": 2.45
      },
      "190": {
        "id": 190,
        "fp": 5.45,
        "points": 2.05,
        "rebounds": 2,
        "assists": 0.15,
        "steals": 0.1,
        "blocks": 0.3,
        "turnovers": 0.25
      },
      "191": {
        "id": 191,
        "fp": 11.1875,
        "points": 4.55,
        "rebounds": 2.15,
        "assists": 1.9,
        "steals": 0.55,
        "blocks": 0.1,
        "turnovers": 0.8
      },
      "192": {
        "id": 192,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "193": {
        "id": 193,
        "fp": 12.3,
        "points": 7,
        "rebounds": 0.8,
        "assists": 1,
        "steals": 1.4,
        "blocks": 0.2,
        "turnovers": 1
      },
      "195": {
        "id": 195,
        "fp": 9.5,
        "points": 3.66666666666667,
        "rebounds": 4,
        "assists": 0.166666666666667,
        "steals": 0.333333333333333,
        "blocks": 0.166666666666667,
        "turnovers": 0.833333333333333
      },
      "196": {
        "id": 196,
        "fp": 19.0875,
        "points": 9.6,
        "rebounds": 4.65,
        "assists": 1.7,
        "steals": 0.35,
        "blocks": 0.2,
        "turnovers": 0.85
      },
      "197": {
        "id": 197,
        "fp": 2.25,
        "points": 0.8,
        "rebounds": 1,
        "assists": 0,
        "steals": 0.2,
        "blocks": 0,
        "turnovers": 0.4
      },
      "198": {
        "id": 198,
        "fp": 9.35,
        "points": 2.55,
        "rebounds": 4.8,
        "assists": 0.3,
        "steals": 0.2,
        "blocks": 0.05,
        "turnovers": 0.3
      },
      "199": {
        "id": 199,
        "fp": 0.791666666666667,
        "points": 0.333333333333333,
        "rebounds": 0.166666666666667,
        "assists": 0.333333333333333,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.5
      },
      "200": {
        "id": 200,
        "fp": 5.6875,
        "points": 2.75,
        "rebounds": 1.25,
        "assists": 0.4,
        "steals": 0.2,
        "blocks": 0.1,
        "turnovers": 0.05
      },
      "201": {
        "id": 201,
        "fp": 15.175,
        "points": 8.55,
        "rebounds": 3.2,
        "assists": 0.95,
        "steals": 0.25,
        "blocks": 0.4,
        "turnovers": 0.75
      },
      "202": {
        "id": 202,
        "fp": 3,
        "points": 1.75,
        "rebounds": 0.7,
        "assists": 0.25,
        "steals": 0.05,
        "blocks": 0,
        "turnovers": 0.25
      },
      "203": {
        "id": 203,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "204": {
        "id": 204,
        "fp": 47.6,
        "points": 25.85,
        "rebounds": 10.4,
        "assists": 2.1,
        "steals": 1.35,
        "blocks": 1.25,
        "turnovers": 1.65
      },
      "205": {
        "id": 205,
        "fp": 0.775,
        "points": 0.25,
        "rebounds": 0.4,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "206": {
        "id": 206,
        "fp": 20.0875,
        "points": 9.85,
        "rebounds": 2.35,
        "assists": 3.95,
        "steals": 0.8,
        "blocks": 0.05,
        "turnovers": 1.3
      },
      "207": {
        "id": 207,
        "fp": 10.95,
        "points": 3.85,
        "rebounds": 3,
        "assists": 0.95,
        "steals": 0.85,
        "blocks": 0.2,
        "turnovers": 0.55
      },
      "208": {
        "id": 208,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "209": {
        "id": 209,
        "fp": 5.9625,
        "points": 3.75,
        "rebounds": 0.55,
        "assists": 0.55,
        "steals": 0.2,
        "blocks": 0.1,
        "turnovers": 0.4
      },
      "210": {
        "id": 210,
        "fp": 17.65,
        "points": 7.8,
        "rebounds": 3.3,
        "assists": 2,
        "steals": 0.85,
        "blocks": 0.5,
        "turnovers": 1.25
      },
      "211": {
        "id": 211,
        "fp": 30.1,
        "points": 14.15,
        "rebounds": 4,
        "assists": 5.8,
        "steals": 1.3,
        "blocks": 0.15,
        "turnovers": 2.25
      },
      "212": {
        "id": 212,
        "fp": 9.6375,
        "points": 4.15,
        "rebounds": 2.75,
        "assists": 0.5,
        "steals": 0.35,
        "blocks": 0.25,
        "turnovers": 0.3
      },
      "213": {
        "id": 213,
        "fp": 4.725,
        "points": 2.6,
        "rebounds": 0.8,
        "assists": 0.4,
        "steals": 0.1,
        "blocks": 0.05,
        "turnovers": 0.1
      },
      "214": {
        "id": 214,
        "fp": 2.3625,
        "points": 0.85,
        "rebounds": 0.95,
        "assists": 0.1,
        "steals": 0,
        "blocks": 0.1,
        "turnovers": 0.05
      },
      "215": {
        "id": 215,
        "fp": 48.875,
        "points": 20.55,
        "rebounds": 6.4,
        "assists": 10.25,
        "steals": 1.6,
        "blocks": 0.65,
        "turnovers": 3.3
      },
      "216": {
        "id": 216,
        "fp": 21.75,
        "points": 10.15,
        "rebounds": 4.5,
        "assists": 1.25,
        "steals": 1.3,
        "blocks": 0.65,
        "turnovers": 0.95
      },
      "217": {
        "id": 217,
        "fp": 2.5875,
        "points": 1.6,
        "rebounds": 0.45,
        "assists": 0.15,
        "steals": 0.1,
        "blocks": 0,
        "turnovers": 0.05
      },
      "218": {
        "id": 218,
        "fp": 2.5875,
        "points": 1.2,
        "rebounds": 0.75,
        "assists": 0.2,
        "steals": 0.1,
        "blocks": 0,
        "turnovers": 0.1
      },
      "219": {
        "id": 219,
        "fp": 3.15,
        "points": 1.45,
        "rebounds": 1.1,
        "assists": 0,
        "steals": 0.25,
        "blocks": 0,
        "turnovers": 0.4
      },
      "220": {
        "id": 220,
        "fp": 1.8125,
        "points": 1,
        "rebounds": 0.75,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.25
      },
      "221": {
        "id": 221,
        "fp": 3.75,
        "points": 1.5,
        "rebounds": 1,
        "assists": 0,
        "steals": 0,
        "blocks": 0.5,
        "turnovers": 0
      },
      "222": {
        "id": 222,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "223": {
        "id": 223,
        "fp": 15.1625,
        "points": 9.15,
        "rebounds": 2.35,
        "assists": 1.95,
        "steals": 0.2,
        "blocks": 0.1,
        "turnovers": 1.15
      },
      "224": {
        "id": 224,
        "fp": 2.5,
        "points": 2,
        "rebounds": 0.5,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.25
      },
      "225": {
        "id": 225,
        "fp": 8.6875,
        "points": 2.75,
        "rebounds": 2.25,
        "assists": 0.75,
        "steals": 0.25,
        "blocks": 0.75,
        "turnovers": 0.5
      },
      "226": {
        "id": 226,
        "fp": 12.7875,
        "points": 5.75,
        "rebounds": 2.55,
        "assists": 1.4,
        "steals": 0.8,
        "blocks": 0.05,
        "turnovers": 0.95
      },
      "227": {
        "id": 227,
        "fp": 31.6375,
        "points": 13.35,
        "rebounds": 9.75,
        "assists": 1.3,
        "steals": 0.45,
        "blocks": 1.5,
        "turnovers": 1
      },
      "228": {
        "id": 228,
        "fp": 16.1625,
        "points": 7.65,
        "rebounds": 3.55,
        "assists": 1.5,
        "steals": 0.8,
        "blocks": 0.35,
        "turnovers": 0.95
      },
      "229": {
        "id": 229,
        "fp": 22.9125,
        "points": 14.6,
        "rebounds": 2.35,
        "assists": 2.15,
        "steals": 0.9,
        "blocks": 0.15,
        "turnovers": 1.4
      },
      "230": {
        "id": 230,
        "fp": 4.2375,
        "points": 2.25,
        "rebounds": 0.55,
        "assists": 0.35,
        "steals": 0.25,
        "blocks": 0.1,
        "turnovers": 0.2
      },
      "231": {
        "id": 231,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "232": {
        "id": 232,
        "fp": 15.0625,
        "points": 7.1,
        "rebounds": 4.35,
        "assists": 0.35,
        "steals": 0.45,
        "blocks": 0.7,
        "turnovers": 0.6
      },
      "233": {
        "id": 233,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "234": {
        "id": 234,
        "fp": 4.2875,
        "points": 1.7,
        "rebounds": 1.05,
        "assists": 0.2,
        "steals": 0.3,
        "blocks": 0.25,
        "turnovers": 0.45
      },
      "235": {
        "id": 235,
        "fp": 6.0875,
        "points": 3.3,
        "rebounds": 0.95,
        "assists": 0.65,
        "steals": 0.25,
        "blocks": 0.1,
        "turnovers": 0.6
      },
      "236": {
        "id": 236,
        "fp": 13.375,
        "points": 8.65,
        "rebounds": 1.4,
        "assists": 1.2,
        "steals": 0.55,
        "blocks": 0,
        "turnovers": 0.95
      },
      "237": {
        "id": 237,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "238": {
        "id": 238,
        "fp": 2.45833333333333,
        "points": 0.666666666666667,
        "rebounds": 0.833333333333333,
        "assists": 0.666666666666667,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.5
      },
      "239": {
        "id": 239,
        "fp": 25.3625,
        "points": 13.15,
        "rebounds": 4.95,
        "assists": 1.5,
        "steals": 1.5,
        "blocks": 0.55,
        "turnovers": 1.9
      },
      "240": {
        "id": 240,
        "fp": 11.1125,
        "points": 4.05,
        "rebounds": 3.45,
        "assists": 0.45,
        "steals": 0.45,
        "blocks": 0.65,
        "turnovers": 0.25
      },
      "241": {
        "id": 241,
        "fp": 0.5,
        "points": 0.285714285714286,
        "rebounds": 0,
        "assists": 0.142857142857143,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "242": {
        "id": 242,
        "fp": 36.6125,
        "points": 10.75,
        "rebounds": 4.55,
        "assists": 10.8,
        "steals": 2.25,
        "blocks": 0.05,
        "turnovers": 3.5
      },
      "243": {
        "id": 243,
        "fp": 6.0875,
        "points": 2.5,
        "rebounds": 1.75,
        "assists": 0.25,
        "steals": 0.35,
        "blocks": 0.05,
        "turnovers": 0.25
      },
      "244": {
        "id": 244,
        "fp": 1.0875,
        "points": 0.55,
        "rebounds": 0.15,
        "assists": 0.15,
        "steals": 0.05,
        "blocks": 0,
        "turnovers": 0
      },
      "245": {
        "id": 245,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "246": {
        "id": 246,
        "fp": 10.5,
        "points": 4.7,
        "rebounds": 2.9,
        "assists": 0.4,
        "steals": 0.45,
        "blocks": 0.4,
        "turnovers": 0.4
      },
      "247": {
        "id": 247,
        "fp": 7.775,
        "points": 3.85,
        "rebounds": 1.8,
        "assists": 0.55,
        "steals": 0.3,
        "blocks": 0,
        "turnovers": 0.2
      },
      "248": {
        "id": 248,
        "fp": 49.3875,
        "points": 24.95,
        "rebounds": 10.45,
        "assists": 3.95,
        "steals": 1.7,
        "blocks": 1.2,
        "turnovers": 3.85
      },
      "249": {
        "id": 249,
        "fp": 40.3125,
        "points": 14.95,
        "rebounds": 15.05,
        "assists": 0.95,
        "steals": 1.2,
        "blocks": 1.2,
        "turnovers": 1.95
      },
      "250": {
        "id": 250,
        "fp": 20.1125,
        "points": 10.4,
        "rebounds": 4.65,
        "assists": 0.85,
        "steals": 1.05,
        "blocks": 0.2,
        "turnovers": 0.9
      },
      "251": {
        "id": 251,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "252": {
        "id": 252,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "253": {
        "id": 253,
        "fp": 25.6125,
        "points": 13.8,
        "rebounds": 4.45,
        "assists": 3.25,
        "steals": 0.6,
        "blocks": 0.1,
        "turnovers": 1.5
      },
      "254": {
        "id": 254,
        "fp": 26.6125,
        "points": 15.55,
        "rebounds": 2.25,
        "assists": 4.05,
        "steals": 1.1,
        "blocks": 0.1,
        "turnovers": 1.7
      },
      "255": {
        "id": 255,
        "fp": 12.8,
        "points": 5.55,
        "rebounds": 3.4,
        "assists": 1.55,
        "steals": 0.3,
        "blocks": 0.15,
        "turnovers": 1.25
      },
      "256": {
        "id": 256,
        "fp": 30.4375,
        "points": 17.8,
        "rebounds": 2.05,
        "assists": 5.6,
        "steals": 0.7,
        "blocks": 0.25,
        "turnovers": 2.5
      },
      "257": {
        "id": 257,
        "fp": 9.5375,
        "points": 4.95,
        "rebounds": 1.55,
        "assists": 1.3,
        "steals": 0.3,
        "blocks": 0.1,
        "turnovers": 0.5
      },
      "258": {
        "id": 258,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "259": {
        "id": 259,
        "fp": 7.65,
        "points": 3.2,
        "rebounds": 2.1,
        "assists": 0.9,
        "steals": 0.1,
        "blocks": 0.15,
        "turnovers": 0.5
      },
      "260": {
        "id": 260,
        "fp": 7.125,
        "points": 4.35,
        "rebounds": 0.9,
        "assists": 0.75,
        "steals": 0.25,
        "blocks": 0,
        "turnovers": 0.45
      },
      "261": {
        "id": 261,
        "fp": 5.03571428571429,
        "points": 2.28571428571429,
        "rebounds": 1.28571428571429,
        "assists": 0.714285714285714,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.285714285714286
      },
      "262": {
        "id": 262,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "263": {
        "id": 263,
        "fp": 4.3,
        "points": 1,
        "rebounds": 1.1,
        "assists": 1.15,
        "steals": 0.15,
        "blocks": 0,
        "turnovers": 0.4
      },
      "264": {
        "id": 264,
        "fp": 15.2125,
        "points": 7.8,
        "rebounds": 4.35,
        "assists": 0.4,
        "steals": 0.5,
        "blocks": 0.1,
        "turnovers": 0.7
      },
      "265": {
        "id": 265,
        "fp": 3.9125,
        "points": 0.8,
        "rebounds": 1.55,
        "assists": 0.5,
        "steals": 0.15,
        "blocks": 0.1,
        "turnovers": 0.15
      },
      "266": {
        "id": 266,
        "fp": 8.3625,
        "points": 3.7,
        "rebounds": 0.95,
        "assists": 2.25,
        "steals": 0.2,
        "blocks": 0,
        "turnovers": 1.35
      },
      "267": {
        "id": 267,
        "fp": 24.6625,
        "points": 14.2,
        "rebounds": 2.95,
        "assists": 4.15,
        "steals": 0.6,
        "blocks": 0.1,
        "turnovers": 2.45
      },
      "268": {
        "id": 268,
        "fp": 15.55,
        "points": 7.3,
        "rebounds": 1.9,
        "assists": 3.1,
        "steals": 0.45,
        "blocks": 0.2,
        "turnovers": 1.35
      },
      "269": {
        "id": 269,
        "fp": 39.7,
        "points": 15.4,
        "rebounds": 9.8,
        "assists": 5.25,
        "steals": 0.55,
        "blocks": 1.5,
        "turnovers": 2.4
      },
      "270": {
        "id": 270,
        "fp": 14.8,
        "points": 5.7,
        "rebounds": 4.7,
        "assists": 0.6,
        "steals": 0.35,
        "blocks": 1,
        "turnovers": 0.75
      },
      "271": {
        "id": 271,
        "fp": 18.925,
        "points": 11.35,
        "rebounds": 2.7,
        "assists": 1.1,
        "steals": 1.1,
        "blocks": 0.15,
        "turnovers": 0.8
      },
      "272": {
        "id": 272,
        "fp": 12.9,
        "points": 6.9,
        "rebounds": 2.5,
        "assists": 1.15,
        "steals": 0.25,
        "blocks": 0.2,
        "turnovers": 0.7
      },
      "273": {
        "id": 273,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "274": {
        "id": 274,
        "fp": 23.0625,
        "points": 12.2,
        "rebounds": 3.25,
        "assists": 2.95,
        "steals": 0.75,
        "blocks": 0.45,
        "turnovers": 1.45
      },
      "275": {
        "id": 275,
        "fp": 0.1375,
        "points": 0.1,
        "rebounds": 0.05,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.05
      },
      "276": {
        "id": 276,
        "fp": 18.6875,
        "points": 13.45,
        "rebounds": 2.45,
        "assists": 0.6,
        "steals": 0.3,
        "blocks": 0.1,
        "turnovers": 0.6
      },
      "277": {
        "id": 277,
        "fp": 0.964285714285714,
        "points": 0.857142857142857,
        "rebounds": 0.142857142857143,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.142857142857143
      },
      "278": {
        "id": 278,
        "fp": 18.975,
        "points": 7.85,
        "rebounds": 6.1,
        "assists": 1.2,
        "steals": 0.55,
        "blocks": 0.3,
        "turnovers": 0.75
      },
      "279": {
        "id": 279,
        "fp": 22.6625,
        "points": 9.05,
        "rebounds": 6.35,
        "assists": 1.9,
        "steals": 0.65,
        "blocks": 1,
        "turnovers": 1.25
      },
      "280": {
        "id": 280,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "281": {
        "id": 281,
        "fp": 11.4125,
        "points": 5.6,
        "rebounds": 1.05,
        "assists": 2.4,
        "steals": 0.45,
        "blocks": 0.15,
        "turnovers": 1.25
      },
      "282": {
        "id": 282,
        "fp": 0.09375,
        "points": 0,
        "rebounds": 0.125,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.125
      },
      "283": {
        "id": 283,
        "fp": 6.3375,
        "points": 2.95,
        "rebounds": 1.35,
        "assists": 0.5,
        "steals": 0.3,
        "blocks": 0.2,
        "turnovers": 0.6
      },
      "284": {
        "id": 284,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "285": {
        "id": 285,
        "fp": 2.6,
        "points": 1.2,
        "rebounds": 0.6,
        "assists": 0.25,
        "steals": 0.05,
        "blocks": 0.1,
        "turnovers": 0.1
      },
      "286": {
        "id": 286,
        "fp": 5.85714285714286,
        "points": 2.42857142857143,
        "rebounds": 2.28571428571429,
        "assists": 0,
        "steals": 0.142857142857143,
        "blocks": 0.285714285714286,
        "turnovers": 0.571428571428571
      },
      "287": {
        "id": 287,
        "fp": 2.71428571428571,
        "points": 1.14285714285714,
        "rebounds": 1.14285714285714,
        "assists": 0,
        "steals": 0.142857142857143,
        "blocks": 0,
        "turnovers": 0.285714285714286
      },
      "288": {
        "id": 288,
        "fp": 3.2,
        "points": 1.85,
        "rebounds": 0.8,
        "assists": 0.05,
        "steals": 0.15,
        "blocks": 0,
        "turnovers": 0.05
      },
      "289": {
        "id": 289,
        "fp": 7.3125,
        "points": 3.75,
        "rebounds": 1,
        "assists": 0.75,
        "steals": 0.5,
        "blocks": 0,
        "turnovers": 0.125
      },
      "290": {
        "id": 290,
        "fp": 17.825,
        "points": 9.7,
        "rebounds": 2.4,
        "assists": 1.45,
        "steals": 1.15,
        "blocks": 0.35,
        "turnovers": 1
      },
      "291": {
        "id": 291,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "292": {
        "id": 292,
        "fp": 9.46428571428571,
        "points": 3.57142857142857,
        "rebounds": 1.57142857142857,
        "assists": 2.14285714285714,
        "steals": 0.571428571428571,
        "blocks": 0,
        "turnovers": 1.14285714285714
      },
      "293": {
        "id": 293,
        "fp": 10.4375,
        "points": 5.6,
        "rebounds": 1.25,
        "assists": 1.25,
        "steals": 0.55,
        "blocks": 0.05,
        "turnovers": 0.65
      },
      "294": {
        "id": 294,
        "fp": 4.45,
        "points": 2.15,
        "rebounds": 0.9,
        "assists": 0.3,
        "steals": 0.2,
        "blocks": 0.2,
        "turnovers": 0.15
      },
      "295": {
        "id": 295,
        "fp": 5.1875,
        "points": 2.45,
        "rebounds": 1.45,
        "assists": 0.55,
        "steals": 0.1,
        "blocks": 0,
        "turnovers": 0.3
      },
      "296": {
        "id": 296,
        "fp": 24.575,
        "points": 9.85,
        "rebounds": 4.2,
        "assists": 3.3,
        "steals": 1.8,
        "blocks": 0.5,
        "turnovers": 1.35
      },
      "297": {
        "id": 297,
        "fp": 29.5875,
        "points": 13.15,
        "rebounds": 4.25,
        "assists": 3.05,
        "steals": 2.6,
        "blocks": 0.45,
        "turnovers": 1.35
      },
      "298": {
        "id": 298,
        "fp": 8.7,
        "points": 4.1,
        "rebounds": 1.3,
        "assists": 1.6,
        "steals": 0.35,
        "blocks": 0.1,
        "turnovers": 1
      },
      "299": {
        "id": 299,
        "fp": 53.15,
        "points": 29.9,
        "rebounds": 6.3,
        "assists": 7.4,
        "steals": 1.9,
        "blocks": 0.65,
        "turnovers": 4.7
      },
      "300": {
        "id": 300,
        "fp": 33.9625,
        "points": 14.15,
        "rebounds": 11.25,
        "assists": 1.25,
        "steals": 1,
        "blocks": 1.15,
        "turnovers": 2.35
      },
      "301": {
        "id": 301,
        "fp": 11.9375,
        "points": 4.6,
        "rebounds": 3.85,
        "assists": 0.3,
        "steals": 0.15,
        "blocks": 1,
        "turnovers": 0.45
      },
      "302": {
        "id": 302,
        "fp": 11.15,
        "points": 6.15,
        "rebounds": 1.5,
        "assists": 1.15,
        "steals": 0.4,
        "blocks": 0.15,
        "turnovers": 0.5
      },
      "303": {
        "id": 303,
        "fp": 13.53125,
        "points": 5.625,
        "rebounds": 5.125,
        "assists": 0.875,
        "steals": 0.25,
        "blocks": 0.25,
        "turnovers": 1.625
      },
      "304": {
        "id": 304,
        "fp": 3.0625,
        "points": 1.9,
        "rebounds": 0.55,
        "assists": 0.25,
        "steals": 0.05,
        "blocks": 0.05,
        "turnovers": 0.3
      },
      "305": {
        "id": 305,
        "fp": 3.41666666666667,
        "points": 2.33333333333333,
        "rebounds": 1,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.333333333333333
      },
      "306": {
        "id": 306,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "307": {
        "id": 307,
        "fp": 17.7875,
        "points": 7,
        "rebounds": 3.95,
        "assists": 2.5,
        "steals": 0.85,
        "blocks": 0.2,
        "turnovers": 0.9
      },
      "308": {
        "id": 308,
        "fp": 2.58333333333333,
        "points": 1.33333333333333,
        "rebounds": 0.333333333333333,
        "assists": 0.666666666666667,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.333333333333333
      },
      "309": {
        "id": 309,
        "fp": 41.6125,
        "points": 22,
        "rebounds": 8.65,
        "assists": 4.2,
        "steals": 0.65,
        "blocks": 0.55,
        "turnovers": 2.3
      },
      "310": {
        "id": 310,
        "fp": 8.2625,
        "points": 4,
        "rebounds": 1.65,
        "assists": 0.9,
        "steals": 0.35,
        "blocks": 0,
        "turnovers": 0.35
      },
      "311": {
        "id": 311,
        "fp": 24.65,
        "points": 12.35,
        "rebounds": 5.2,
        "assists": 1.2,
        "steals": 0.55,
        "blocks": 1.5,
        "turnovers": 1.35
      },
      "312": {
        "id": 312,
        "fp": 19.7125,
        "points": 11.15,
        "rebounds": 3.55,
        "assists": 2.05,
        "steals": 0.45,
        "blocks": 0.05,
        "turnovers": 1.15
      },
      "313": {
        "id": 313,
        "fp": 17.45,
        "points": 7,
        "rebounds": 3,
        "assists": 3.65,
        "steals": 0.55,
        "blocks": 0.1,
        "turnovers": 1.3
      },
      "314": {
        "id": 314,
        "fp": 2.13888888888889,
        "points": 0.666666666666667,
        "rebounds": 0.555555555555556,
        "assists": 0.222222222222222,
        "steals": 0.111111111111111,
        "blocks": 0.111111111111111,
        "turnovers": 0
      },
      "315": {
        "id": 315,
        "fp": 0.666666666666667,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0.333333333333333,
        "turnovers": 0
      },
      "316": {
        "id": 316,
        "fp": 12.4875,
        "points": 7.2,
        "rebounds": 2.75,
        "assists": 0.7,
        "steals": 0.3,
        "blocks": 0.1,
        "turnovers": 0.45
      },
      "317": {
        "id": 317,
        "fp": 0.416666666666667,
        "points": 0,
        "rebounds": 0.333333333333333,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "318": {
        "id": 318,
        "fp": 9.175,
        "points": 3.8,
        "rebounds": 1.5,
        "assists": 1.6,
        "steals": 0.6,
        "blocks": 0.1,
        "turnovers": 0.75
      },
      "319": {
        "id": 319,
        "fp": 0.925,
        "points": 0.3,
        "rebounds": 0.2,
        "assists": 0.15,
        "steals": 0,
        "blocks": 0.1,
        "turnovers": 0.1
      },
      "320": {
        "id": 320,
        "fp": 2.875,
        "points": 1.5,
        "rebounds": 0.6,
        "assists": 0.35,
        "steals": 0,
        "blocks": 0.15,
        "turnovers": 0.4
      },
      "321": {
        "id": 321,
        "fp": 29.5375,
        "points": 13,
        "rebounds": 9.35,
        "assists": 1.05,
        "steals": 0.25,
        "blocks": 1.55,
        "turnovers": 1.7
      },
      "322": {
        "id": 322,
        "fp": 9.4,
        "points": 3.75,
        "rebounds": 2.5,
        "assists": 0.75,
        "steals": 0.15,
        "blocks": 0.65,
        "turnovers": 0.6
      },
      "323": {
        "id": 323,
        "fp": 7.075,
        "points": 3.9,
        "rebounds": 1.6,
        "assists": 0.6,
        "steals": 0.15,
        "blocks": 0,
        "turnovers": 0.5
      },
      "324": {
        "id": 324,
        "fp": 7.6125,
        "points": 3.35,
        "rebounds": 1.35,
        "assists": 0.75,
        "steals": 0.45,
        "blocks": 0.35,
        "turnovers": 0.75
      },
      "325": {
        "id": 325,
        "fp": 1.82142857142857,
        "points": 0.285714285714286,
        "rebounds": 1,
        "assists": 0,
        "steals": 0.142857142857143,
        "blocks": 0,
        "turnovers": 0
      },
      "326": {
        "id": 326,
        "fp": 23.65,
        "points": 9.85,
        "rebounds": 6.2,
        "assists": 2,
        "steals": 1.2,
        "blocks": 0.5,
        "turnovers": 2
      },
      "327": {
        "id": 327,
        "fp": 10.9625,
        "points": 6.1,
        "rebounds": 1.85,
        "assists": 0.8,
        "steals": 0.45,
        "blocks": 0.15,
        "turnovers": 0.45
      },
      "328": {
        "id": 328,
        "fp": 0.7125,
        "points": 0.35,
        "rebounds": 0.05,
        "assists": 0.1,
        "steals": 0.1,
        "blocks": 0,
        "turnovers": 0.15
      },
      "329": {
        "id": 329,
        "fp": 37.3625,
        "points": 15.85,
        "rebounds": 8.35,
        "assists": 2.85,
        "steals": 1.85,
        "blocks": 1.65,
        "turnovers": 2.3
      },
      "330": {
        "id": 330,
        "fp": 3.5,
        "points": 1.8,
        "rebounds": 1.2,
        "assists": 0.2,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.4
      },
      "331": {
        "id": 331,
        "fp": 0.2,
        "points": 0,
        "rebounds": 0,
        "assists": 0.2,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.2
      },
      "332": {
        "id": 332,
        "fp": 2.475,
        "points": 1.15,
        "rebounds": 0.3,
        "assists": 0.4,
        "steals": 0.15,
        "blocks": 0,
        "turnovers": 0.1
      },
      "333": {
        "id": 333,
        "fp": 7.775,
        "points": 3.45,
        "rebounds": 1.4,
        "assists": 0.85,
        "steals": 0.25,
        "blocks": 0.45,
        "turnovers": 0.5
      },
      "334": {
        "id": 334,
        "fp": 7.5,
        "points": 3.15,
        "rebounds": 2,
        "assists": 0.6,
        "steals": 0.25,
        "blocks": 0.3,
        "turnovers": 0.35
      },
      "335": {
        "id": 335,
        "fp": 1.85714285714286,
        "points": 0.285714285714286,
        "rebounds": 0.571428571428571,
        "assists": 0.285714285714286,
        "steals": 0.285714285714286,
        "blocks": 0,
        "turnovers": 0.285714285714286
      },
      "336": {
        "id": 336,
        "fp": 0.825,
        "points": 0.3,
        "rebounds": 0.3,
        "assists": 0.05,
        "steals": 0,
        "blocks": 0.05,
        "turnovers": 0.05
      },
      "337": {
        "id": 337,
        "fp": 18.9875,
        "points": 9.5,
        "rebounds": 2.55,
        "assists": 3.25,
        "steals": 0.7,
        "blocks": 0.2,
        "turnovers": 1.2
      },
      "338": {
        "id": 338,
        "fp": 0.6625,
        "points": 0.25,
        "rebounds": 0.25,
        "assists": 0,
        "steals": 0.05,
        "blocks": 0,
        "turnovers": 0
      },
      "339": {
        "id": 339,
        "fp": 17.125,
        "points": 7.55,
        "rebounds": 4.6,
        "assists": 1.05,
        "steals": 0.55,
        "blocks": 0.4,
        "turnovers": 0.8
      },
      "340": {
        "id": 340,
        "fp": 32.7625,
        "points": 16.45,
        "rebounds": 2.85,
        "assists": 6.7,
        "steals": 1.3,
        "blocks": 0.25,
        "turnovers": 2.65
      },
      "341": {
        "id": 341,
        "fp": 12.4375,
        "points": 5.55,
        "rebounds": 3.15,
        "assists": 0.95,
        "steals": 0.55,
        "blocks": 0.25,
        "turnovers": 0.8
      },
      "342": {
        "id": 342,
        "fp": 22.7875,
        "points": 12.15,
        "rebounds": 2.45,
        "assists": 4.4,
        "steals": 0.65,
        "blocks": 0.15,
        "turnovers": 2.3
      },
      "343": {
        "id": 343,
        "fp": 36.475,
        "points": 24.3,
        "rebounds": 4.2,
        "assists": 3.3,
        "steals": 1.2,
        "blocks": 0.2,
        "turnovers": 2.3
      },
      "344": {
        "id": 344,
        "fp": 1.1875,
        "points": 0.4,
        "rebounds": 0.45,
        "assists": 0,
        "steals": 0.1,
        "blocks": 0.05,
        "turnovers": 0.15
      },
      "345": {
        "id": 345,
        "fp": 15.3125,
        "points": 5.7,
        "rebounds": 4.65,
        "assists": 1,
        "steals": 0.7,
        "blocks": 0.5,
        "turnovers": 1
      },
      "346": {
        "id": 346,
        "fp": 2.78571428571429,
        "points": 1.42857142857143,
        "rebounds": 1.14285714285714,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.142857142857143
      },
      "347": {
        "id": 347,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "348": {
        "id": 348,
        "fp": 19.175,
        "points": 9.3,
        "rebounds": 3,
        "assists": 1.8,
        "steals": 1.1,
        "blocks": 0.4,
        "turnovers": 1.25
      },
      "349": {
        "id": 349,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "350": {
        "id": 350,
        "fp": 35.2625,
        "points": 15.95,
        "rebounds": 7.45,
        "assists": 3.3,
        "steals": 0.65,
        "blocks": 1.75,
        "turnovers": 1.3
      },
      "351": {
        "id": 351,
        "fp": 41.9375,
        "points": 22.35,
        "rebounds": 4.65,
        "assists": 6.25,
        "steals": 1.8,
        "blocks": 0.25,
        "turnovers": 2.5
      },
      "352": {
        "id": 352,
        "fp": 11.075,
        "points": 4.45,
        "rebounds": 3.1,
        "assists": 1.05,
        "steals": 0.4,
        "blocks": 0.2,
        "turnovers": 0.65
      },
      "353": {
        "id": 353,
        "fp": 19.45,
        "points": 5.25,
        "rebounds": 7.5,
        "assists": 0.45,
        "steals": 0.35,
        "blocks": 1.9,
        "turnovers": 0.85
      },
      "354": {
        "id": 354,
        "fp": 2.35,
        "points": 1.8,
        "rebounds": 0.2,
        "assists": 0,
        "steals": 0.2,
        "blocks": 0,
        "turnovers": 0.2
      },
      "355": {
        "id": 355,
        "fp": 1.05,
        "points": 0.45,
        "rebounds": 0.3,
        "assists": 0,
        "steals": 0.1,
        "blocks": 0,
        "turnovers": 0
      },
      "356": {
        "id": 356,
        "fp": 16.9125,
        "points": 10.7,
        "rebounds": 2.45,
        "assists": 0.75,
        "steals": 0.45,
        "blocks": 0.15,
        "turnovers": 0.3
      },
      "357": {
        "id": 357,
        "fp": 16.925,
        "points": 8.25,
        "rebounds": 2.4,
        "assists": 3.2,
        "steals": 0.6,
        "blocks": 0.05,
        "turnovers": 1.9
      },
      "358": {
        "id": 358,
        "fp": 25.4125,
        "points": 12.55,
        "rebounds": 7.65,
        "assists": 0.6,
        "steals": 0.35,
        "blocks": 0.85,
        "turnovers": 1.05
      },
      "359": {
        "id": 359,
        "fp": 3.4375,
        "points": 1.25,
        "rebounds": 0.25,
        "assists": 1,
        "steals": 0.25,
        "blocks": 0,
        "turnovers": 0.5
      },
      "360": {
        "id": 360,
        "fp": 6.7375,
        "points": 2.65,
        "rebounds": 1.35,
        "assists": 0.65,
        "steals": 0.45,
        "blocks": 0.25,
        "turnovers": 0.25
      },
      "361": {
        "id": 361,
        "fp": 0.357142857142857,
        "points": 0,
        "rebounds": 0.285714285714286,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "362": {
        "id": 362,
        "fp": 4.67857142857143,
        "points": 2.14285714285714,
        "rebounds": 0.571428571428571,
        "assists": 0.5,
        "steals": 0.285714285714286,
        "blocks": 0.142857142857143,
        "turnovers": 0
      },
      "363": {
        "id": 363,
        "fp": 1.675,
        "points": 0.55,
        "rebounds": 0.3,
        "assists": 0.3,
        "steals": 0.15,
        "blocks": 0.05,
        "turnovers": 0.2
      },
      "364": {
        "id": 364,
        "fp": 1.45,
        "points": 1.2,
        "rebounds": 0.2,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "365": {
        "id": 365,
        "fp": 7.2125,
        "points": 3.35,
        "rebounds": 2.25,
        "assists": 0.35,
        "steals": 0.15,
        "blocks": 0.2,
        "turnovers": 0.35
      },
      "366": {
        "id": 366,
        "fp": 17.3125,
        "points": 10.85,
        "rebounds": 2.25,
        "assists": 1.4,
        "steals": 0.7,
        "blocks": 0.1,
        "turnovers": 0.95
      },
      "367": {
        "id": 367,
        "fp": 6.375,
        "points": 2.5,
        "rebounds": 1,
        "assists": 0.5,
        "steals": 1,
        "blocks": 0,
        "turnovers": 0.75
      },
      "368": {
        "id": 368,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "369": {
        "id": 369,
        "fp": 9.225,
        "points": 4.1,
        "rebounds": 2.8,
        "assists": 0.35,
        "steals": 0.1,
        "blocks": 0.65,
        "turnovers": 0.8
      },
      "370": {
        "id": 370,
        "fp": 1.1,
        "points": 0.4,
        "rebounds": 0,
        "assists": 0.2,
        "steals": 0.2,
        "blocks": 0,
        "turnovers": 0
      },
      "371": {
        "id": 371,
        "fp": 19.8375,
        "points": 9.15,
        "rebounds": 5.15,
        "assists": 1.15,
        "steals": 0.85,
        "blocks": 0.5,
        "turnovers": 1.2
      },
      "372": {
        "id": 372,
        "fp": 24.95,
        "points": 13.65,
        "rebounds": 3.4,
        "assists": 2.15,
        "steals": 1.7,
        "blocks": 0.2,
        "turnovers": 1.25
      },
      "373": {
        "id": 373,
        "fp": 23.275,
        "points": 12.3,
        "rebounds": 2,
        "assists": 4.5,
        "steals": 0.7,
        "blocks": 0.15,
        "turnovers": 1.15
      },
      "374": {
        "id": 374,
        "fp": 28.45,
        "points": 14.15,
        "rebounds": 8.4,
        "assists": 1.15,
        "steals": 0.4,
        "blocks": 0.6,
        "turnovers": 1.2
      },
      "375": {
        "id": 375,
        "fp": 16.1375,
        "points": 8.3,
        "rebounds": 2.25,
        "assists": 1.75,
        "steals": 0.85,
        "blocks": 0.35,
        "turnovers": 1
      },
      "376": {
        "id": 376,
        "fp": 12.375,
        "points": 5.3,
        "rebounds": 2.3,
        "assists": 1.7,
        "steals": 0.4,
        "blocks": 0.35,
        "turnovers": 0.85
      },
      "377": {
        "id": 377,
        "fp": -0.5,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 1
      },
      "378": {
        "id": 378,
        "fp": 2.55,
        "points": 1.25,
        "rebounds": 0.7,
        "assists": 0.15,
        "steals": 0.15,
        "blocks": 0,
        "turnovers": 0.2
      },
      "379": {
        "id": 379,
        "fp": 3.51470588235294,
        "points": 1.82352941176471,
        "rebounds": 0.529411764705882,
        "assists": 0.470588235294118,
        "steals": 0.117647058823529,
        "blocks": 0,
        "turnovers": 0.0588235294117647
      },
      "380": {
        "id": 380,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "381": {
        "id": 381,
        "fp": 27.425,
        "points": 13.4,
        "rebounds": 6.5,
        "assists": 2.35,
        "steals": 0.75,
        "blocks": 0.6,
        "turnovers": 1.85
      },
      "383": {
        "id": 383,
        "fp": 29.675,
        "points": 13.95,
        "rebounds": 3.1,
        "assists": 6,
        "steals": 1.15,
        "blocks": 0.6,
        "turnovers": 2.65
      },
      "384": {
        "id": 384,
        "fp": 23.475,
        "points": 9.95,
        "rebounds": 5.1,
        "assists": 2.4,
        "steals": 0.75,
        "blocks": 0.85,
        "turnovers": 1.55
      },
      "385": {
        "id": 385,
        "fp": 4.9,
        "points": 1.4,
        "rebounds": 1.6,
        "assists": 1.2,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.8
      },
      "386": {
        "id": 386,
        "fp": 0.65,
        "points": 0.35,
        "rebounds": 0.1,
        "assists": 0.05,
        "steals": 0.05,
        "blocks": 0,
        "turnovers": 0
      },
      "387": {
        "id": 387,
        "fp": 5.2625,
        "points": 2.85,
        "rebounds": 0.95,
        "assists": 0.6,
        "steals": 0.05,
        "blocks": 0.2,
        "turnovers": 0.35
      },
      "388": {
        "id": 388,
        "fp": 8.5,
        "points": 3.25,
        "rebounds": 2.5,
        "assists": 0.45,
        "steals": 0.45,
        "blocks": 0.45,
        "turnovers": 0.85
      },
      "389": {
        "id": 389,
        "fp": 23.3625,
        "points": 13.15,
        "rebounds": 4.05,
        "assists": 1.6,
        "steals": 0.55,
        "blocks": 0.75,
        "turnovers": 0.85
      },
      "390": {
        "id": 390,
        "fp": 12.875,
        "points": 5.45,
        "rebounds": 2.8,
        "assists": 1.25,
        "steals": 0.55,
        "blocks": 0.4,
        "turnovers": 0.5
      },
      "391": {
        "id": 391,
        "fp": 3.9375,
        "points": 1.85,
        "rebounds": 0.95,
        "assists": 0.1,
        "steals": 0.2,
        "blocks": 0.25,
        "turnovers": 0.3
      },
      "392": {
        "id": 392,
        "fp": 3.975,
        "points": 1.25,
        "rebounds": 1.5,
        "assists": 0,
        "steals": 0.1,
        "blocks": 0.35,
        "turnovers": 0.1
      },
      "393": {
        "id": 393,
        "fp": 0.95,
        "points": 0.2,
        "rebounds": 0.6,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "394": {
        "id": 394,
        "fp": 0.3375,
        "points": 0.25,
        "rebounds": 0.05,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "395": {
        "id": 395,
        "fp": 22.5375,
        "points": 12.4,
        "rebounds": 5.35,
        "assists": 1.9,
        "steals": 0.3,
        "blocks": 0.1,
        "turnovers": 1
      },
      "396": {
        "id": 396,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "397": {
        "id": 397,
        "fp": 6.425,
        "points": 2.95,
        "rebounds": 1.6,
        "assists": 0.15,
        "steals": 0.25,
        "blocks": 0.35,
        "turnovers": 0.3
      },
      "398": {
        "id": 398,
        "fp": 13.725,
        "points": 6.85,
        "rebounds": 4.4,
        "assists": 0.65,
        "steals": 0.2,
        "blocks": 0.15,
        "turnovers": 0.8
      },
      "399": {
        "id": 399,
        "fp": 8.8875,
        "points": 3.95,
        "rebounds": 1.35,
        "assists": 1.95,
        "steals": 0.35,
        "blocks": 0,
        "turnovers": 1.05
      },
      "400": {
        "id": 400,
        "fp": 7.425,
        "points": 3.7,
        "rebounds": 1.1,
        "assists": 0.85,
        "steals": 0.45,
        "blocks": 0.15,
        "turnovers": 0.6
      },
      "401": {
        "id": 401,
        "fp": 29.7875,
        "points": 11.65,
        "rebounds": 8.15,
        "assists": 2.95,
        "steals": 1,
        "blocks": 0.75,
        "turnovers": 1.6
      },
      "402": {
        "id": 402,
        "fp": 5.875,
        "points": 2.5,
        "rebounds": 2,
        "assists": 0.5,
        "steals": 0,
        "blocks": 0.25,
        "turnovers": 0.75
      },
      "403": {
        "id": 403,
        "fp": 15.3125,
        "points": 7.8,
        "rebounds": 2.75,
        "assists": 0.9,
        "steals": 0.95,
        "blocks": 0.3,
        "turnovers": 0.8
      },
      "404": {
        "id": 404,
        "fp": 12.6875,
        "points": 7,
        "rebounds": 1.75,
        "assists": 1.75,
        "steals": 0.25,
        "blocks": 0,
        "turnovers": 0.5
      },
      "405": {
        "id": 405,
        "fp": 2.275,
        "points": 1.1,
        "rebounds": 0.7,
        "assists": 0.05,
        "steals": 0.05,
        "blocks": 0.1,
        "turnovers": 0.15
      },
      "406": {
        "id": 406,
        "fp": 12.0875,
        "points": 5.4,
        "rebounds": 2.85,
        "assists": 0.7,
        "steals": 1.05,
        "blocks": 0.15,
        "turnovers": 0.85
      },
      "407": {
        "id": 407,
        "fp": 33.275,
        "points": 17.7,
        "rebounds": 5.8,
        "assists": 3.55,
        "steals": 1.05,
        "blocks": 0.35,
        "turnovers": 2
      },
      "408": {
        "id": 408,
        "fp": 4.75,
        "points": 0.6,
        "rebounds": 1.8,
        "assists": 0.8,
        "steals": 0.4,
        "blocks": 0.2,
        "turnovers": 1
      },
      "409": {
        "id": 409,
        "fp": 21.8125,
        "points": 7.1,
        "rebounds": 8.75,
        "assists": 1.6,
        "steals": 0.7,
        "blocks": 0.15,
        "turnovers": 1.25
      },
      "410": {
        "id": 410,
        "fp": 4.0625,
        "points": 2.05,
        "rebounds": 1.15,
        "assists": 0.2,
        "steals": 0.1,
        "blocks": 0.05,
        "turnovers": 0.25
      },
      "411": {
        "id": 411,
        "fp": 19.275,
        "points": 10.2,
        "rebounds": 2.9,
        "assists": 2.2,
        "steals": 0.75,
        "blocks": 0.1,
        "turnovers": 0.7
      },
      "412": {
        "id": 412,
        "fp": 20.1125,
        "points": 8.75,
        "rebounds": 3.15,
        "assists": 3.7,
        "steals": 1.05,
        "blocks": 0.1,
        "turnovers": 1.2
      },
      "413": {
        "id": 413,
        "fp": 25.7625,
        "points": 12.6,
        "rebounds": 2.45,
        "assists": 5.5,
        "steals": 0.8,
        "blocks": 0.2,
        "turnovers": 1.8
      },
      "414": {
        "id": 414,
        "fp": 4.3875,
        "points": 2.15,
        "rebounds": 1.15,
        "assists": 0.15,
        "steals": 0.35,
        "blocks": 0,
        "turnovers": 0.25
      },
      "415": {
        "id": 415,
        "fp": 6.25,
        "points": 2.4,
        "rebounds": 0.6,
        "assists": 0.2,
        "steals": 1,
        "blocks": 0.6,
        "turnovers": 1.2
      },
      "416": {
        "id": 416,
        "fp": 32.5875,
        "points": 19,
        "rebounds": 6.15,
        "assists": 1.45,
        "steals": 0.7,
        "blocks": 1,
        "turnovers": 1.2
      },
      "417": {
        "id": 417,
        "fp": 17.5375,
        "points": 10,
        "rebounds": 1.55,
        "assists": 3.5,
        "steals": 0.15,
        "blocks": 0,
        "turnovers": 1
      },
      "418": {
        "id": 418,
        "fp": 7.1,
        "points": 1.4,
        "rebounds": 1.6,
        "assists": 1.6,
        "steals": 0.6,
        "blocks": 0,
        "turnovers": 0
      },
      "419": {
        "id": 419,
        "fp": 8.35,
        "points": 3.2,
        "rebounds": 2.6,
        "assists": 0,
        "steals": 0.4,
        "blocks": 0.8,
        "turnovers": 1
      },
      "420": {
        "id": 420,
        "fp": 2.85,
        "points": 1.8,
        "rebounds": 0.5,
        "assists": 0.3,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.15
      },
      "421": {
        "id": 421,
        "fp": 4.9,
        "points": 1.85,
        "rebounds": 1.7,
        "assists": 0.4,
        "steals": 0.2,
        "blocks": 0.1,
        "turnovers": 0.6
      },
      "422": {
        "id": 422,
        "fp": 2.6125,
        "points": 1.25,
        "rebounds": 0.55,
        "assists": 0.2,
        "steals": 0.15,
        "blocks": 0.05,
        "turnovers": 0.3
      },
      "423": {
        "id": 423,
        "fp": 5.925,
        "points": 2,
        "rebounds": 1.5,
        "assists": 0.6,
        "steals": 0.4,
        "blocks": 0.2,
        "turnovers": 0.15
      },
      "424": {
        "id": 424,
        "fp": 3.925,
        "points": 2.5,
        "rebounds": 0.8,
        "assists": 0.2,
        "steals": 0.1,
        "blocks": 0,
        "turnovers": 0.45
      },
      "425": {
        "id": 425,
        "fp": 31.4625,
        "points": 20.95,
        "rebounds": 3.55,
        "assists": 2.25,
        "steals": 1,
        "blocks": 0.75,
        "turnovers": 2.45
      },
      "426": {
        "id": 426,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "427": {
        "id": 427,
        "fp": 0.107142857142857,
        "points": 0,
        "rebounds": 0.142857142857143,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.142857142857143
      },
      "428": {
        "id": 428,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "429": {
        "id": 429,
        "fp": 1.175,
        "points": 0.75,
        "rebounds": 0.2,
        "assists": 0,
        "steals": 0,
        "blocks": 0.05,
        "turnovers": 0
      },
      "430": {
        "id": 430,
        "fp": 3.675,
        "points": 1.3,
        "rebounds": 0.4,
        "assists": 0.8,
        "steals": 0.35,
        "blocks": 0.1,
        "turnovers": 0.5
      },
      "431": {
        "id": 431,
        "fp": 43.65,
        "points": 22.35,
        "rebounds": 7.2,
        "assists": 6.15,
        "steals": 1.3,
        "blocks": 0.4,
        "turnovers": 3.1
      },
      "432": {
        "id": 432,
        "fp": 34.6,
        "points": 11.9,
        "rebounds": 4.3,
        "assists": 9.25,
        "steals": 1.7,
        "blocks": 0.15,
        "turnovers": 2.45
      },
      "433": {
        "id": 433,
        "fp": 1.825,
        "points": 0.6,
        "rebounds": 0.6,
        "assists": 0.25,
        "steals": 0.1,
        "blocks": 0,
        "turnovers": 0.2
      },
      "434": {
        "id": 434,
        "fp": 14.475,
        "points": 4,
        "rebounds": 4.4,
        "assists": 1.7,
        "steals": 1.05,
        "blocks": 0.25,
        "turnovers": 1
      },
      "435": {
        "id": 435,
        "fp": 43.2625,
        "points": 20.75,
        "rebounds": 11.25,
        "assists": 2.5,
        "steals": 0.75,
        "blocks": 1.65,
        "turnovers": 2.4
      },
      "436": {
        "id": 436,
        "fp": 9.175,
        "points": 4.75,
        "rebounds": 2.2,
        "assists": 0.6,
        "steals": 0.25,
        "blocks": 0.05,
        "turnovers": 0.5
      },
      "437": {
        "id": 437,
        "fp": 17.2125,
        "points": 10.5,
        "rebounds": 3.75,
        "assists": 0.65,
        "steals": 0.45,
        "blocks": 0.15,
        "turnovers": 0.8
      },
      "438": {
        "id": 438,
        "fp": 9.3875,
        "points": 3.8,
        "rebounds": 0.95,
        "assists": 2.2,
        "steals": 0.45,
        "blocks": 0.1,
        "turnovers": 0.6
      },
      "439": {
        "id": 439,
        "fp": 6.8625,
        "points": 2.6,
        "rebounds": 2.15,
        "assists": 0.55,
        "steals": 0.25,
        "blocks": 0.2,
        "turnovers": 0.3
      },
      "440": {
        "id": 440,
        "fp": 0.7625,
        "points": 0.45,
        "rebounds": 0.15,
        "assists": 0.05,
        "steals": 0.05,
        "blocks": 0,
        "turnovers": 0.1
      },
      "441": {
        "id": 441,
        "fp": 0.1875,
        "points": 0,
        "rebounds": 0.15,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "442": {
        "id": 442,
        "fp": 22.6125,
        "points": 12.75,
        "rebounds": 3.05,
        "assists": 1.55,
        "steals": 1.05,
        "blocks": 0.2,
        "turnovers": 0.55
      },
      "443": {
        "id": 443,
        "fp": 3.8125,
        "points": 1.7,
        "rebounds": 0.65,
        "assists": 0.95,
        "steals": 0.05,
        "blocks": 0,
        "turnovers": 0.5
      },
      "444": {
        "id": 444,
        "fp": 12.8625,
        "points": 5.5,
        "rebounds": 4.35,
        "assists": 0.3,
        "steals": 0.25,
        "blocks": 0.65,
        "turnovers": 0.8
      },
      "445": {
        "id": 445,
        "fp": 27.5,
        "points": 16.9,
        "rebounds": 3,
        "assists": 2.8,
        "steals": 0.95,
        "blocks": 0.35,
        "turnovers": 1.85
      },
      "446": {
        "id": 446,
        "fp": 2.57142857142857,
        "points": 1.14285714285714,
        "rebounds": 0.571428571428571,
        "assists": 0.285714285714286,
        "steals": 0.142857142857143,
        "blocks": 0,
        "turnovers": 0
      },
      "447": {
        "id": 447,
        "fp": 32.4125,
        "points": 13.1,
        "rebounds": 8.25,
        "assists": 2.65,
        "steals": 1.15,
        "blocks": 1.55,
        "turnovers": 1.75
      },
      "448": {
        "id": 448,
        "fp": 0.1,
        "points": 0.1,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "449": {
        "id": 449,
        "fp": 1,
        "points": 1,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "450": {
        "id": 450,
        "fp": 27.1875,
        "points": 12.5,
        "rebounds": 7.35,
        "assists": 2.2,
        "steals": 0.45,
        "blocks": 0.45,
        "turnovers": 1.2
      },
      "451": {
        "id": 451,
        "fp": 10.3214285714286,
        "points": 4.28571428571429,
        "rebounds": 3,
        "assists": 0.714285714285714,
        "steals": 0.142857142857143,
        "blocks": 0.428571428571429,
        "turnovers": 0.714285714285714
      },
      "452": {
        "id": 452,
        "fp": 7,
        "points": 2.85714285714286,
        "rebounds": 1.14285714285714,
        "assists": 1.85714285714286,
        "steals": 0.142857142857143,
        "blocks": 0,
        "turnovers": 1
      },
      "453": {
        "id": 453,
        "fp": 36.8875,
        "points": 23.2,
        "rebounds": 2.55,
        "assists": 5,
        "steals": 1.1,
        "blocks": 0.4,
        "turnovers": 2.25
      },
      "454": {
        "id": 454,
        "fp": 0.75,
        "points": 0.3,
        "rebounds": 0.3,
        "assists": 0,
        "steals": 0,
        "blocks": 0.05,
        "turnovers": 0.05
      },
      "455": {
        "id": 455,
        "fp": 1.425,
        "points": 1.2,
        "rebounds": 0.1,
        "assists": 0.1,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.2
      },
      "456": {
        "id": 456,
        "fp": 4.17857142857143,
        "points": 1.28571428571429,
        "rebounds": 1,
        "assists": 0.428571428571429,
        "steals": 0.142857142857143,
        "blocks": 0.428571428571429,
        "turnovers": 0.285714285714286
      },
      "457": {
        "id": 457,
        "fp": 11.4875,
        "points": 5.55,
        "rebounds": 0.75,
        "assists": 2.8,
        "steals": 0.4,
        "blocks": 0.05,
        "turnovers": 1.25
      },
      "458": {
        "id": 458,
        "fp": 2.53571428571429,
        "points": 1.85714285714286,
        "rebounds": 0.428571428571429,
        "assists": 0.142857142857143,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.285714285714286
      },
      "459": {
        "id": 459,
        "fp": 2.2125,
        "points": 0.5,
        "rebounds": 0.35,
        "assists": 0.75,
        "steals": 0.1,
        "blocks": 0,
        "turnovers": 0.2
      },
      "460": {
        "id": 460,
        "fp": 27.5375,
        "points": 10.45,
        "rebounds": 7.85,
        "assists": 1.95,
        "steals": 1.2,
        "blocks": 0.8,
        "turnovers": 0.9
      },
      "461": {
        "id": 461,
        "fp": 21.1625,
        "points": 8.15,
        "rebounds": 6.35,
        "assists": 1.5,
        "steals": 1.3,
        "blocks": 0.4,
        "turnovers": 1.35
      },
      "462": {
        "id": 462,
        "fp": 10.8625,
        "points": 4.95,
        "rebounds": 2.95,
        "assists": 0.65,
        "steals": 0.2,
        "blocks": 0.2,
        "turnovers": 0.25
      },
      "463": {
        "id": 463,
        "fp": 8.925,
        "points": 4.45,
        "rebounds": 2.2,
        "assists": 0.6,
        "steals": 0.25,
        "blocks": 0.2,
        "turnovers": 0.55
      },
      "464": {
        "id": 464,
        "fp": 15.175,
        "points": 7.6,
        "rebounds": 3,
        "assists": 1.7,
        "steals": 0.5,
        "blocks": 0.2,
        "turnovers": 1.35
      },
      "465": {
        "id": 465,
        "fp": 0.428571428571429,
        "points": 0,
        "rebounds": 0.285714285714286,
        "assists": 0.142857142857143,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.285714285714286
      },
      "466": {
        "id": 466,
        "fp": 20.4,
        "points": 7.4,
        "rebounds": 2.4,
        "assists": 5.3,
        "steals": 0.95,
        "blocks": 0.25,
        "turnovers": 1.7
      },
      "467": {
        "id": 467,
        "fp": 29.5125,
        "points": 16.9,
        "rebounds": 3.55,
        "assists": 4.25,
        "steals": 1.15,
        "blocks": 0.45,
        "turnovers": 2.8
      },
      "468": {
        "id": 468,
        "fp": 0.986111111111111,
        "points": 0.555555555555556,
        "rebounds": 0.166666666666667,
        "assists": 0.0555555555555556,
        "steals": 0.111111111111111,
        "blocks": 0.0555555555555556,
        "turnovers": 0.388888888888889
      },
      "469": {
        "id": 469,
        "fp": 2.67857142857143,
        "points": 1,
        "rebounds": 0.142857142857143,
        "assists": 1.14285714285714,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.428571428571429
      },
      "470": {
        "id": 470,
        "fp": 5.66666666666667,
        "points": 1,
        "rebounds": 2.66666666666667,
        "assists": 0.333333333333333,
        "steals": 0.166666666666667,
        "blocks": 0.333333333333333,
        "turnovers": 0.333333333333333
      },
      "471": {
        "id": 471,
        "fp": 36.1,
        "points": 13.65,
        "rebounds": 11.1,
        "assists": 0.45,
        "steals": 0.45,
        "blocks": 3.25,
        "turnovers": 1.25
      },
      "472": {
        "id": 472,
        "fp": 26.6375,
        "points": 14.1,
        "rebounds": 6.15,
        "assists": 1.85,
        "steals": 0.6,
        "blocks": 0.65,
        "turnovers": 1.65
      },
      "473": {
        "id": 473,
        "fp": 2,
        "points": 1,
        "rebounds": 0.333333333333333,
        "assists": 0.166666666666667,
        "steals": 0,
        "blocks": 0.166666666666667,
        "turnovers": 0.333333333333333
      },
      "474": {
        "id": 474,
        "fp": 0.475,
        "points": 0.25,
        "rebounds": 0.1,
        "assists": 0,
        "steals": 0.05,
        "blocks": 0,
        "turnovers": 0
      },
      "475": {
        "id": 475,
        "fp": 8.5125,
        "points": 2.7,
        "rebounds": 1.55,
        "assists": 2,
        "steals": 0.35,
        "blocks": 0.2,
        "turnovers": 0.65
      },
      "476": {
        "id": 476,
        "fp": 5.525,
        "points": 1.8,
        "rebounds": 2.1,
        "assists": 0.15,
        "steals": 0.2,
        "blocks": 0.3,
        "turnovers": 0.25
      },
      "477": {
        "id": 477,
        "fp": 1.4,
        "points": 0.6,
        "rebounds": 0,
        "assists": 0.2,
        "steals": 0.2,
        "blocks": 0,
        "turnovers": 0
      },
      "478": {
        "id": 478,
        "fp": 15.9375,
        "points": 8.85,
        "rebounds": 2.95,
        "assists": 0.5,
        "steals": 0.55,
        "blocks": 0.95,
        "turnovers": 0.95
      },
      "479": {
        "id": 479,
        "fp": 32.725,
        "points": 16.4,
        "rebounds": 7.8,
        "assists": 1.95,
        "steals": 1.35,
        "blocks": 0.25,
        "turnovers": 1.2
      },
      "480": {
        "id": 480,
        "fp": 7.0875,
        "points": 2.55,
        "rebounds": 1.45,
        "assists": 1.3,
        "steals": 0.2,
        "blocks": 0.15,
        "turnovers": 0.25
      },
      "481": {
        "id": 481,
        "fp": 24.5625,
        "points": 13.9,
        "rebounds": 5.15,
        "assists": 1.95,
        "steals": 0.55,
        "blocks": 0.1,
        "turnovers": 1.25
      },
      "482": {
        "id": 482,
        "fp": 10.0714285714286,
        "points": 4.14285714285714,
        "rebounds": 4,
        "assists": 0.428571428571429,
        "steals": 0,
        "blocks": 0.142857142857143,
        "turnovers": 0.428571428571429
      },
      "483": {
        "id": 483,
        "fp": 2.8125,
        "points": 1,
        "rebounds": 0.85,
        "assists": 0.2,
        "steals": 0.05,
        "blocks": 0.2,
        "turnovers": 0.2
      },
      "484": {
        "id": 484,
        "fp": 16.5,
        "points": 6.05,
        "rebounds": 5.4,
        "assists": 0.7,
        "steals": 0.25,
        "blocks": 1.3,
        "turnovers": 1.05
      },
      "485": {
        "id": 485,
        "fp": 4.16666666666667,
        "points": 2.33333333333333,
        "rebounds": 1.33333333333333,
        "assists": 0.166666666666667,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.333333333333333
      },
      "486": {
        "id": 486,
        "fp": 3.1,
        "points": 1.1,
        "rebounds": 0.8,
        "assists": 0.25,
        "steals": 0.25,
        "blocks": 0.05,
        "turnovers": 0.2
      },
      "487": {
        "id": 487,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "488": {
        "id": 488,
        "fp": 33.1375,
        "points": 17.7,
        "rebounds": 4.65,
        "assists": 3.45,
        "steals": 1.6,
        "blocks": 0.75,
        "turnovers": 1.85
      },
      "489": {
        "id": 489,
        "fp": 23.6125,
        "points": 10.8,
        "rebounds": 2.75,
        "assists": 3.95,
        "steals": 1.65,
        "blocks": 0.35,
        "turnovers": 1.7
      },
      "490": {
        "id": 490,
        "fp": 22.975,
        "points": 13.95,
        "rebounds": 2.7,
        "assists": 2.45,
        "steals": 0.9,
        "blocks": 0,
        "turnovers": 1.4
      },
      "491": {
        "id": 491,
        "fp": 5.96428571428571,
        "points": 1.57142857142857,
        "rebounds": 2.71428571428571,
        "assists": 0.285714285714286,
        "steals": 0.285714285714286,
        "blocks": 0.285714285714286,
        "turnovers": 1.28571428571429
      },
      "492": {
        "id": 492,
        "fp": 7.5,
        "points": 2.6,
        "rebounds": 2.9,
        "assists": 0.15,
        "steals": 0.25,
        "blocks": 0.35,
        "turnovers": 0.3
      },
      "493": {
        "id": 493,
        "fp": 0.85,
        "points": 0.3,
        "rebounds": 0.3,
        "assists": 0.05,
        "steals": 0.05,
        "blocks": 0,
        "turnovers": 0
      },
      "494": {
        "id": 494,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "495": {
        "id": 495,
        "fp": 13.9375,
        "points": 6.75,
        "rebounds": 1.85,
        "assists": 1.15,
        "steals": 0.85,
        "blocks": 0.55,
        "turnovers": 0.4
      },
      "496": {
        "id": 496,
        "fp": 8.2,
        "points": 5.3,
        "rebounds": 1.7,
        "assists": 0.5,
        "steals": 0.05,
        "blocks": 0.05,
        "turnovers": 0.55
      },
      "497": {
        "id": 497,
        "fp": 33.8125,
        "points": 16.05,
        "rebounds": 4.65,
        "assists": 7.05,
        "steals": 0.75,
        "blocks": 0.15,
        "turnovers": 2.2
      },
      "498": {
        "id": 498,
        "fp": 4.9125,
        "points": 2.9,
        "rebounds": 0.85,
        "assists": 0.9,
        "steals": 0.1,
        "blocks": 0,
        "turnovers": 1.35
      },
      "499": {
        "id": 499,
        "fp": 26.0125,
        "points": 10.4,
        "rebounds": 5.85,
        "assists": 2.3,
        "steals": 1.65,
        "blocks": 1.25,
        "turnovers": 2.25
      },
      "500": {
        "id": 500,
        "fp": 14.275,
        "points": 8.3,
        "rebounds": 2,
        "assists": 1.5,
        "steals": 0.55,
        "blocks": 0.05,
        "turnovers": 1.2
      },
      "501": {
        "id": 501,
        "fp": 24.5375,
        "points": 11.55,
        "rebounds": 5.75,
        "assists": 1.1,
        "steals": 1.4,
        "blocks": 0.6,
        "turnovers": 1.9
      },
      "502": {
        "id": 502,
        "fp": 8.04166666666667,
        "points": 4.83333333333333,
        "rebounds": 0.5,
        "assists": 1,
        "steals": 0.5,
        "blocks": 0,
        "turnovers": 0.833333333333333
      },
      "503": {
        "id": 503,
        "fp": 3.20833333333333,
        "points": 0.666666666666667,
        "rebounds": 1.16666666666667,
        "assists": 0.666666666666667,
        "steals": 0.166666666666667,
        "blocks": 0,
        "turnovers": 0.5
      },
      "504": {
        "id": 504,
        "fp": 20.7125,
        "points": 7.85,
        "rebounds": 4.65,
        "assists": 2.2,
        "steals": 0.5,
        "blocks": 1.65,
        "turnovers": 1.5
      },
      "505": {
        "id": 505,
        "fp": 5.725,
        "points": 2.55,
        "rebounds": 1.3,
        "assists": 0.45,
        "steals": 0.3,
        "blocks": 0.25,
        "turnovers": 0.65
      },
      "506": {
        "id": 506,
        "fp": 4.9625,
        "points": 3,
        "rebounds": 0.65,
        "assists": 0.6,
        "steals": 0.15,
        "blocks": 0.05,
        "turnovers": 0.5
      },
      "507": {
        "id": 507,
        "fp": 0.775,
        "points": 0.4,
        "rebounds": 0.2,
        "assists": 0,
        "steals": 0.05,
        "blocks": 0,
        "turnovers": 0
      },
      "508": {
        "id": 508,
        "fp": 19.55,
        "points": 12.1,
        "rebounds": 2.3,
        "assists": 1.55,
        "steals": 0.75,
        "blocks": 0,
        "turnovers": 0.9
      },
      "509": {
        "id": 509,
        "fp": 3.925,
        "points": 1.95,
        "rebounds": 0.2,
        "assists": 1,
        "steals": 0.15,
        "blocks": 0.05,
        "turnovers": 0.6
      },
      "510": {
        "id": 510,
        "fp": 17.675,
        "points": 10.8,
        "rebounds": 3.6,
        "assists": 0.8,
        "steals": 0.2,
        "blocks": 0.7,
        "turnovers": 1.6
      },
      "511": {
        "id": 511,
        "fp": 10.375,
        "points": 2.83333333333333,
        "rebounds": 3.5,
        "assists": 1.16666666666667,
        "steals": 0.666666666666667,
        "blocks": 0.333333333333333,
        "turnovers": 1.16666666666667
      },
      "512": {
        "id": 512,
        "fp": 10.8875,
        "points": 5.8,
        "rebounds": 2.75,
        "assists": 0.65,
        "steals": 0.2,
        "blocks": 0.2,
        "turnovers": 0.3
      },
      "513": {
        "id": 513,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "514": {
        "id": 514,
        "fp": 1.54166666666667,
        "points": 1.33333333333333,
        "rebounds": 0.166666666666667,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "515": {
        "id": 515,
        "fp": 16.6375,
        "points": 9.3,
        "rebounds": 3.35,
        "assists": 1.05,
        "steals": 0.4,
        "blocks": 0.15,
        "turnovers": 0.65
      },
      "516": {
        "id": 516,
        "fp": 15.5125,
        "points": 5.9,
        "rebounds": 2.15,
        "assists": 3.6,
        "steals": 1,
        "blocks": 0,
        "turnovers": 1.2
      },
      "517": {
        "id": 517,
        "fp": 8.125,
        "points": 3.15,
        "rebounds": 2,
        "assists": 0.5,
        "steals": 0.35,
        "blocks": 0.65,
        "turnovers": 0.65
      },
      "518": {
        "id": 518,
        "fp": 4.125,
        "points": 1.45,
        "rebounds": 0.7,
        "assists": 1.05,
        "steals": 0.15,
        "blocks": 0,
        "turnovers": 0.2
      },
      "519": {
        "id": 519,
        "fp": 2.1375,
        "points": 1.05,
        "rebounds": 0.45,
        "assists": 0.35,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.1
      },
      "520": {
        "id": 520,
        "fp": 19.4875,
        "points": 10.25,
        "rebounds": 3.75,
        "assists": 1.2,
        "steals": 0.9,
        "blocks": 0.45,
        "turnovers": 0.55
      },
      "521": {
        "id": 521,
        "fp": 17.5125,
        "points": 7.65,
        "rebounds": 5.45,
        "assists": 1.45,
        "steals": 0.1,
        "blocks": 0.3,
        "turnovers": 1.4
      },
      "522": {
        "id": 522,
        "fp": 46.275,
        "points": 28.6,
        "rebounds": 3.7,
        "assists": 6.55,
        "steals": 1.05,
        "blocks": 0.35,
        "turnovers": 3.1
      },
      "523": {
        "id": 523,
        "fp": 19.65,
        "points": 8.05,
        "rebounds": 5,
        "assists": 1.75,
        "steals": 0.9,
        "blocks": 0.45,
        "turnovers": 1
      },
      "524": {
        "id": 524,
        "fp": 15.85,
        "points": 8.6,
        "rebounds": 2.6,
        "assists": 1.15,
        "steals": 0.8,
        "blocks": 0.3,
        "turnovers": 0.65
      },
      "525": {
        "id": 525,
        "fp": 8.3625,
        "points": 3.2,
        "rebounds": 3.55,
        "assists": 0.15,
        "steals": 0.05,
        "blocks": 0.3,
        "turnovers": 0.65
      },
      "526": {
        "id": 526,
        "fp": 1.3375,
        "points": 0.5,
        "rebounds": 0.35,
        "assists": 0.2,
        "steals": 0.05,
        "blocks": 0,
        "turnovers": 0.05
      },
      "527": {
        "id": 527,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "528": {
        "id": 528,
        "fp": 22.5875,
        "points": 7.45,
        "rebounds": 7.05,
        "assists": 2.5,
        "steals": 0.6,
        "blocks": 1.1,
        "turnovers": 1.65
      },
      "529": {
        "id": 529,
        "fp": 0.675,
        "points": 0,
        "rebounds": 0.3,
        "assists": 0.1,
        "steals": 0.1,
        "blocks": 0,
        "turnovers": 0.1
      },
      "530": {
        "id": 530,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "531": {
        "id": 531,
        "fp": 17.725,
        "points": 5.2,
        "rebounds": 6.7,
        "assists": 0.85,
        "steals": 0.6,
        "blocks": 1,
        "turnovers": 0.65
      },
      "532": {
        "id": 532,
        "fp": 0.708333333333333,
        "points": 0.5,
        "rebounds": 0.166666666666667,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.166666666666667
      },
      "533": {
        "id": 533,
        "fp": 2.33333333333333,
        "points": 1.16666666666667,
        "rebounds": 0.666666666666667,
        "assists": 0,
        "steals": 0.166666666666667,
        "blocks": 0,
        "turnovers": 0.166666666666667
      },
      "534": {
        "id": 534,
        "fp": 5.5,
        "points": 2.66666666666667,
        "rebounds": 1.33333333333333,
        "assists": 0.333333333333333,
        "steals": 0,
        "blocks": 0.333333333333333,
        "turnovers": 0.666666666666667
      },
      "535": {
        "id": 535,
        "fp": 32.4875,
        "points": 20.4,
        "rebounds": 2.95,
        "assists": 3.6,
        "steals": 1.15,
        "blocks": 0.45,
        "turnovers": 2.65
      },
      "536": {
        "id": 536,
        "fp": 12.0375,
        "points": 5.35,
        "rebounds": 3.65,
        "assists": 0.65,
        "steals": 0.15,
        "blocks": 0.45,
        "turnovers": 0.65
      },
      "537": {
        "id": 537,
        "fp": 1.85,
        "points": 0.6,
        "rebounds": 0.3,
        "assists": 0,
        "steals": 0,
        "blocks": 0.45,
        "turnovers": 0.05
      },
      "538": {
        "id": 538,
        "fp": 12.1375,
        "points": 5.75,
        "rebounds": 2.95,
        "assists": 0.65,
        "steals": 0.5,
        "blocks": 0.3,
        "turnovers": 0.4
      },
      "539": {
        "id": 539,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "540": {
        "id": 540,
        "fp": 7.775,
        "points": 1.65,
        "rebounds": 1,
        "assists": 2.45,
        "steals": 0.65,
        "blocks": 0.2,
        "turnovers": 1
      },
      "541": {
        "id": 541,
        "fp": 6.125,
        "points": 3.5,
        "rebounds": 1.4,
        "assists": 0.4,
        "steals": 0.1,
        "blocks": 0.05,
        "turnovers": 0.3
      },
      "542": {
        "id": 542,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "543": {
        "id": 543,
        "fp": 14.25,
        "points": 6.35,
        "rebounds": 4.2,
        "assists": 0.7,
        "steals": 0.3,
        "blocks": 0.55,
        "turnovers": 0.65
      },
      "544": {
        "id": 544,
        "fp": 2.08333333333333,
        "points": 0.666666666666667,
        "rebounds": 1,
        "assists": 0.333333333333333,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.666666666666667
      },
      "545": {
        "id": 545,
        "fp": 42.7375,
        "points": 14.7,
        "rebounds": 14.95,
        "assists": 1.4,
        "steals": 1,
        "blocks": 2.55,
        "turnovers": 1.8
      },
      "546": {
        "id": 546,
        "fp": 21.475,
        "points": 9.65,
        "rebounds": 4.1,
        "assists": 2.35,
        "steals": 1.45,
        "blocks": 0.15,
        "turnovers": 1.25
      },
      "547": {
        "id": 547,
        "fp": 20.65,
        "points": 11.5,
        "rebounds": 3.9,
        "assists": 2.25,
        "steals": 0.55,
        "blocks": 0.1,
        "turnovers": 1.25
      },
      "548": {
        "id": 548,
        "fp": 23.35,
        "points": 14.6,
        "rebounds": 2.5,
        "assists": 1.95,
        "steals": 1.1,
        "blocks": 0.15,
        "turnovers": 1.45
      },
      "549": {
        "id": 549,
        "fp": 14.3,
        "points": 4.3,
        "rebounds": 4.8,
        "assists": 0.7,
        "steals": 0.6,
        "blocks": 1.15,
        "turnovers": 1.1
      },
      "550": {
        "id": 550,
        "fp": 14.2625,
        "points": 4.6,
        "rebounds": 4.85,
        "assists": 1.35,
        "steals": 0.4,
        "blocks": 0.6,
        "turnovers": 1
      },
      "551": {
        "id": 551,
        "fp": 1.55,
        "points": 0.75,
        "rebounds": 0.1,
        "assists": 0.15,
        "steals": 0.15,
        "blocks": 0.05,
        "turnovers": 0.05
      },
      "552": {
        "id": 552,
        "fp": 36.95,
        "points": 22.05,
        "rebounds": 3,
        "assists": 5.75,
        "steals": 1.1,
        "blocks": 0.15,
        "turnovers": 2.1
      },
      "553": {
        "id": 553,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "554": {
        "id": 554,
        "fp": 26.8625,
        "points": 10.45,
        "rebounds": 5.45,
        "assists": 5.1,
        "steals": 0.9,
        "blocks": 0.4,
        "turnovers": 1.75
      },
      "555": {
        "id": 555,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "556": {
        "id": 556,
        "fp": 29.7875,
        "points": 12,
        "rebounds": 8.05,
        "assists": 2.8,
        "steals": 1.1,
        "blocks": 0.65,
        "turnovers": 1.2
      },
      "557": {
        "id": 557,
        "fp": 19.1,
        "points": 7.2,
        "rebounds": 4.7,
        "assists": 0.9,
        "steals": 1.35,
        "blocks": 0.9,
        "turnovers": 0.85
      },
      "558": {
        "id": 558,
        "fp": 2.5125,
        "points": 0.6,
        "rebounds": 0.65,
        "assists": 0.55,
        "steals": 0.1,
        "blocks": 0.05,
        "turnovers": 0.15
      },
      "559": {
        "id": 559,
        "fp": 6.7125,
        "points": 4.35,
        "rebounds": 0.75,
        "assists": 0.65,
        "steals": 0.25,
        "blocks": 0,
        "turnovers": 0.55
      },
      "560": {
        "id": 560,
        "fp": 0.725,
        "points": 0.3,
        "rebounds": 0.1,
        "assists": 0.1,
        "steals": 0.05,
        "blocks": 0,
        "turnovers": 0
      },
      "561": {
        "id": 561,
        "fp": 9.225,
        "points": 4.55,
        "rebounds": 1.9,
        "assists": 1,
        "steals": 0.2,
        "blocks": 0.2,
        "turnovers": 0.8
      },
      "562": {
        "id": 562,
        "fp": 23.4,
        "points": 11.75,
        "rebounds": 4.3,
        "assists": 1.55,
        "steals": 1.55,
        "blocks": 0.25,
        "turnovers": 0.55
      },
      "563": {
        "id": 563,
        "fp": 9.7625,
        "points": 4.45,
        "rebounds": 2.15,
        "assists": 1.1,
        "steals": 0.3,
        "blocks": 0.35,
        "turnovers": 1.1
      },
      "564": {
        "id": 564,
        "fp": 15.5625,
        "points": 8.25,
        "rebounds": 4.15,
        "assists": 0.6,
        "steals": 0.2,
        "blocks": 0.6,
        "turnovers": 0.9
      },
      "565": {
        "id": 565,
        "fp": 6.9125,
        "points": 1.9,
        "rebounds": 1.45,
        "assists": 1.55,
        "steals": 0.45,
        "blocks": 0.05,
        "turnovers": 0.65
      },
      "566": {
        "id": 566,
        "fp": 24.6125,
        "points": 16.35,
        "rebounds": 2.15,
        "assists": 2.4,
        "steals": 0.85,
        "blocks": 0.15,
        "turnovers": 1.45
      },
      "567": {
        "id": 567,
        "fp": 49.225,
        "points": 22.05,
        "rebounds": 4.5,
        "assists": 10.55,
        "steals": 2.35,
        "blocks": 0.2,
        "turnovers": 2.5
      },
      "568": {
        "id": 568,
        "fp": 6.525,
        "points": 2.55,
        "rebounds": 1.7,
        "assists": 0.3,
        "steals": 0.7,
        "blocks": 0.1,
        "turnovers": 0.5
      },
      "569": {
        "id": 569,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "570": {
        "id": 570,
        "fp": 24.8875,
        "points": 18.4,
        "rebounds": 1.95,
        "assists": 1.3,
        "steals": 0.7,
        "blocks": 0,
        "turnovers": 1.3
      },
      "571": {
        "id": 571,
        "fp": 3.6,
        "points": 0.6,
        "rebounds": 1.8,
        "assists": 0.5,
        "steals": 0.1,
        "blocks": 0,
        "turnovers": 0.4
      },
      "572": {
        "id": 572,
        "fp": 2.625,
        "points": 1,
        "rebounds": 0.5,
        "assists": 0.25,
        "steals": 0.25,
        "blocks": 0.25,
        "turnovers": 0.75
      },
      "573": {
        "id": 573,
        "fp": 5.28125,
        "points": 1.5,
        "rebounds": 2.375,
        "assists": 0.125,
        "steals": 0.0625,
        "blocks": 0.25,
        "turnovers": 0.1875
      },
      "574": {
        "id": 574,
        "fp": 10.3,
        "points": 5.4,
        "rebounds": 2,
        "assists": 1,
        "steals": 0.8,
        "blocks": 0,
        "turnovers": 1.8
      },
      "575": {
        "id": 575,
        "fp": 23.2,
        "points": 7.75,
        "rebounds": 9.2,
        "assists": 0.85,
        "steals": 0.45,
        "blocks": 0.8,
        "turnovers": 0.7
      },
      "576": {
        "id": 576,
        "fp": 0.9125,
        "points": 0.3,
        "rebounds": 0.15,
        "assists": 0.15,
        "steals": 0.05,
        "blocks": 0.05,
        "turnovers": 0.1
      },
      "577": {
        "id": 577,
        "fp": 8.95,
        "points": 3.4,
        "rebounds": 0.6,
        "assists": 2.8,
        "steals": 0.4,
        "blocks": 0,
        "turnovers": 0.8
      },
      "578": {
        "id": 578,
        "fp": 4.15909090909091,
        "points": 1.90909090909091,
        "rebounds": 1.36363636363636,
        "assists": 0.272727272727273,
        "steals": 0,
        "blocks": 0.0909090909090909,
        "turnovers": 0.0909090909090909
      },
      "579": {
        "id": 579,
        "fp": 8.08333333333333,
        "points": 3,
        "rebounds": 1,
        "assists": 2.66666666666667,
        "steals": 0.333333333333333,
        "blocks": 0,
        "turnovers": 1.66666666666667
      },
      "580": {
        "id": 580,
        "fp": 0.5,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0.25,
        "turnovers": 0
      },
      "581": {
        "id": 581,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "582": {
        "id": 582,
        "fp": 1.45,
        "points": 0.8,
        "rebounds": 0.2,
        "assists": 0,
        "steals": 0.2,
        "blocks": 0,
        "turnovers": 0
      },
      "583": {
        "id": 583,
        "fp": 1.25,
        "points": 0,
        "rebounds": 0.6,
        "assists": 0,
        "steals": 0,
        "blocks": 0.4,
        "turnovers": 0.6
      },
      "584": {
        "id": 584,
        "fp": 3.08333333333333,
        "points": 1.66666666666667,
        "rebounds": 0.333333333333333,
        "assists": 0.666666666666667,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "585": {
        "id": 585,
        "fp": 18.35,
        "points": 5.4,
        "rebounds": 3.8,
        "assists": 3.4,
        "steals": 1.4,
        "blocks": 0.6,
        "turnovers": 1.8
      },
      "588": {
        "id": 588,
        "fp": 6.25,
        "points": 2.3,
        "rebounds": 1.4,
        "assists": 0.7,
        "steals": 0.5,
        "blocks": 0.2,
        "turnovers": 0.9
      },
      "589": {
        "id": 589,
        "fp": 2.9125,
        "points": 1.1,
        "rebounds": 0.55,
        "assists": 0.4,
        "steals": 0.2,
        "blocks": 0.1,
        "turnovers": 0.15
      },
      "590": {
        "id": 590,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "591": {
        "id": 591,
        "fp": 1.52083333333333,
        "points": 0.5,
        "rebounds": 0.25,
        "assists": 0.166666666666667,
        "steals": 0,
        "blocks": 0.25,
        "turnovers": 0.0833333333333333
      },
      "592": {
        "id": 592,
        "fp": 7.34375,
        "points": 3.25,
        "rebounds": 1.875,
        "assists": 0.25,
        "steals": 0.375,
        "blocks": 0.375,
        "turnovers": 0.5
      },
      "593": {
        "id": 593,
        "fp": 2.8125,
        "points": 1.625,
        "rebounds": 0,
        "assists": 0.25,
        "steals": 0.25,
        "blocks": 0.125,
        "turnovers": 0
      },
      "594": {
        "id": 594,
        "fp": 18.0714285714286,
        "points": 10,
        "rebounds": 4,
        "assists": 0.571428571428571,
        "steals": 0.857142857142857,
        "blocks": 0.428571428571429,
        "turnovers": 0.857142857142857
      },
      "595": {
        "id": 595,
        "fp": 0.916666666666667,
        "points": 0.666666666666667,
        "rebounds": 0.333333333333333,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0.333333333333333
      },
      "596": {
        "id": 596,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      },
      "597": {
        "id": 597,
        "fp": 0,
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "steals": 0,
        "blocks": 0,
        "turnovers": 0
      }
    },
    "mlb": {},
    "updatedAt": 1458240882011
  },
  "prizes": {
    "1": {
      "info": {
        "pk": 1,
        "name": "$1 H2H",
        "prize_pool": 1.8,
        "payout_spots": 1,
        "buyin": 1,
        "ranks": [
          {
            "rank": 1,
            "value": 1.8,
            "category": "cash"
          }
        ]
      },
      "isFetching": false
    },
    "2": {
      "info": {
        "pk": 2,
        "name": "$2 H2H",
        "prize_pool": 3.6,
        "payout_spots": 1,
        "buyin": 2,
        "ranks": [
          {
            "rank": 1,
            "value": 3.6,
            "category": "cash"
          }
        ]
      },
      "isFetching": false
    }
  },
  "events": {
    "currentEvent": {},
    "gamesQueue": {},
    "playerEventDescriptions": {},
    "playerHistories": {},
    "playersPlaying": []
  },
  "results": {},
  "routing": {
    "locationBeforeTransitions": {
      "pathname": "/live/nba/lineups/194/",
      "search": "",
      "hash": "",
      "state": null,
      "action": "PUSH",
      "key": "nhz7rm",
      "query": {},
      "$searchBase": {
        "search": "",
        "searchBase": ""
      }
    }
  },
  "sports": {
    "games": {
      "e2c33042-9ac9-4462-bbe1-71db18fde051": {
        "srid_away": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
        "status": "scheduled",
        "title": "",
        "srid_home": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
        "start": "2016-03-17T23:00:00Z",
        "srid": "e2c33042-9ac9-4462-bbe1-71db18fde051",
        "updated": "2016-03-17T06:38:48.857731Z",
        "sport": "nba",
        "timeRemaining": {
          "duration": 48,
          "decimal": 0.9999
        }
      },
      "9a98eb05-477f-436e-99c7-3c60674055ff": {
        "srid_away": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
        "status": "scheduled",
        "title": "",
        "srid_home": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
        "start": "2016-03-17T23:30:00Z",
        "srid": "9a98eb05-477f-436e-99c7-3c60674055ff",
        "updated": "2016-03-17T06:38:48.920769Z",
        "sport": "nba",
        "timeRemaining": {
          "duration": 48,
          "decimal": 0.9999
        }
      },
      "47dcf0e0-f141-458e-8ef2-31d8f5f4a357": {
        "srid_away": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
        "status": "scheduled",
        "title": "",
        "srid_home": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
        "start": "2016-03-18T00:00:00Z",
        "srid": "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
        "updated": "2016-03-17T06:38:49.006080Z",
        "sport": "nba",
        "timeRemaining": {
          "duration": 48,
          "decimal": 0.9999
        }
      },
      "2b9028c3-c482-4300-89fe-64e133aad607": {
        "srid_away": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
        "status": "scheduled",
        "title": "",
        "srid_home": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
        "start": "2016-03-18T01:00:00Z",
        "srid": "2b9028c3-c482-4300-89fe-64e133aad607",
        "updated": "2016-03-17T06:38:49.093280Z",
        "sport": "nba",
        "timeRemaining": {
          "duration": 48,
          "decimal": 0.9999
        }
      },
      "654a55e1-004a-4d3c-916c-b48eabaab840": {
        "srid_away": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
        "status": "scheduled",
        "title": "",
        "srid_home": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
        "start": "2016-03-18T00:00:00Z",
        "srid": "654a55e1-004a-4d3c-916c-b48eabaab840",
        "updated": "2016-03-17T06:38:49.044755Z",
        "sport": "nba",
        "timeRemaining": {
          "duration": 48,
          "decimal": 0.9999
        }
      },
      "82a6f3e1-3b5a-420f-9288-85b99f781507": {
        "srid_away": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
        "status": "scheduled",
        "title": "",
        "srid_home": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
        "start": "2016-03-18T00:30:00Z",
        "srid": "82a6f3e1-3b5a-420f-9288-85b99f781507",
        "updated": "2016-03-17T06:38:49.071390Z",
        "sport": "nba",
        "timeRemaining": {
          "duration": 48,
          "decimal": 0.9999
        }
      },
      "73e40c5f-c690-4936-8853-339ed43dcc76": {
        "srid_away": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
        "status": "scheduled",
        "title": "",
        "srid_home": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
        "start": "2016-03-17T23:00:00Z",
        "srid": "73e40c5f-c690-4936-8853-339ed43dcc76",
        "updated": "2016-03-17T06:38:48.813992Z",
        "sport": "nba",
        "timeRemaining": {
          "duration": 48,
          "decimal": 0.9999
        }
      },
      "440a04df-0caa-4e99-a032-911ddb602576": {
        "srid_away": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
        "status": "scheduled",
        "title": "",
        "srid_home": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
        "start": "2016-03-18T00:00:00Z",
        "srid": "440a04df-0caa-4e99-a032-911ddb602576",
        "updated": "2016-03-17T06:38:48.948230Z",
        "sport": "nba",
        "timeRemaining": {
          "duration": 48,
          "decimal": 0.9999
        }
      },
      "395ec023-b416-419c-8368-70e57720f99d": {
        "srid_away": "441781b9-0f24-11e2-8525-18a905767e44",
        "status": "scheduled",
        "title": "",
        "srid_home": "44151f7a-0f24-11e2-8525-18a905767e44",
        "start": "2016-03-18T02:30:00Z",
        "srid": "395ec023-b416-419c-8368-70e57720f99d",
        "sport": "nhl",
        "timeRemaining": {
          "duration": 60,
          "decimal": 0.9999
        }
      },
      "b5a2dab9-98b3-4eeb-a779-0c1c62f8cb6c": {
        "srid_away": "44169bb9-0f24-11e2-8525-18a905767e44",
        "status": "scheduled",
        "title": "",
        "srid_home": "44167db4-0f24-11e2-8525-18a905767e44",
        "start": "2016-03-17T23:00:00Z",
        "srid": "b5a2dab9-98b3-4eeb-a779-0c1c62f8cb6c",
        "sport": "nhl",
        "timeRemaining": {
          "duration": 60,
          "decimal": 0.9999
        }
      },
      "93113aa7-5afd-46d1-9c9a-683e13c121f6": {
        "srid_away": "441766b9-0f24-11e2-8525-18a905767e44",
        "status": "scheduled",
        "title": "",
        "srid_home": "441643b7-0f24-11e2-8525-18a905767e44",
        "start": "2016-03-18T00:00:00Z",
        "srid": "93113aa7-5afd-46d1-9c9a-683e13c121f6",
        "sport": "nhl",
        "timeRemaining": {
          "duration": 60,
          "decimal": 0.9999
        }
      },
      "27c230bc-30b3-40f3-be66-b6aa10c63f8b": {
        "srid_away": "44155909-0f24-11e2-8525-18a905767e44",
        "status": "scheduled",
        "title": "",
        "srid_home": "44153da1-0f24-11e2-8525-18a905767e44",
        "start": "2016-03-18T02:00:00Z",
        "srid": "27c230bc-30b3-40f3-be66-b6aa10c63f8b",
        "sport": "nhl",
        "timeRemaining": {
          "duration": 60,
          "decimal": 0.9999
        }
      },
      "5f9175c7-83f8-477a-8fb0-e42a63e6206e": {
        "srid_away": "4416091c-0f24-11e2-8525-18a905767e44",
        "status": "scheduled",
        "title": "",
        "srid_home": "44174b0c-0f24-11e2-8525-18a905767e44",
        "start": "2016-03-17T23:00:00Z",
        "srid": "5f9175c7-83f8-477a-8fb0-e42a63e6206e",
        "sport": "nhl",
        "timeRemaining": {
          "duration": 60,
          "decimal": 0.9999
        }
      },
      "633df866-11a6-4801-9090-4c2a1a79d8d5": {
        "srid_away": "4417d3cb-0f24-11e2-8525-18a905767e44",
        "status": "scheduled",
        "title": "",
        "srid_home": "44157522-0f24-11e2-8525-18a905767e44",
        "start": "2016-03-18T00:30:00Z",
        "srid": "633df866-11a6-4801-9090-4c2a1a79d8d5",
        "sport": "nhl",
        "timeRemaining": {
          "duration": 60,
          "decimal": 0.9999
        }
      },
      "e496cc84-14bb-4eee-bbae-09d12d253795": {
        "srid_away": "4418464d-0f24-11e2-8525-18a905767e44",
        "status": "scheduled",
        "title": "",
        "srid_home": "441730a9-0f24-11e2-8525-18a905767e44",
        "start": "2016-03-17T23:30:00Z",
        "srid": "e496cc84-14bb-4eee-bbae-09d12d253795",
        "sport": "nhl",
        "timeRemaining": {
          "duration": 60,
          "decimal": 0.9999
        }
      },
      "76f98202-6c63-42c5-8d2e-270c20948dac": {
        "srid_away": "44182a9d-0f24-11e2-8525-18a905767e44",
        "status": "scheduled",
        "title": "",
        "srid_home": "4417b7d7-0f24-11e2-8525-18a905767e44",
        "start": "2016-03-17T23:00:00Z",
        "srid": "76f98202-6c63-42c5-8d2e-270c20948dac",
        "sport": "nhl",
        "timeRemaining": {
          "duration": 60,
          "decimal": 0.9999
        }
      },
      "a5ecca24-c461-4292-8f93-a6c7e6ca34d5": {
        "srid_away": "dcfd5266-00ce-442c-bc09-264cd20cf455",
        "status": "scheduled",
        "title": "",
        "srid_home": "d99f919b-1534-4516-8e8a-9cd106c6d8cd",
        "start": "2016-03-18T01:05:00Z",
        "srid": "a5ecca24-c461-4292-8f93-a6c7e6ca34d5",
        "day_night": "N",
        "game_number": 1,
        "sport": "mlb",
        "timeRemaining": {
          "duration": 18,
          "decimal": 0.9999
        }
      },
      "15ab1217-2fc5-4829-a54e-fa979167f851": {
        "srid_away": "75729d34-bca7-4a0f-b3df-6f26c6ad3719",
        "status": "scheduled",
        "title": "",
        "srid_home": "93941372-eb4c-4c40-aced-fe3267174393",
        "start": "2016-03-17T17:05:00Z",
        "srid": "15ab1217-2fc5-4829-a54e-fa979167f851",
        "day_night": "D",
        "game_number": 1,
        "sport": "mlb",
        "timeRemaining": {
          "duration": 18,
          "decimal": 0.9999
        }
      },
      "a15a9d61-2c05-4e20-ac9f-7f8005b98175": {
        "srid_away": "12079497-e414-450a-8bf2-29f91de646bf",
        "status": "scheduled",
        "boxscore": {
          "srid_game": "a15a9d61-2c05-4e20-ac9f-7f8005b98175",
          "srid_home": "d89bed32-3aee-4407-99e3-4103641b999a",
          "srid_away": "12079497-e414-450a-8bf2-29f91de646bf",
          "home_score": 0,
          "away_score": 0,
          "status": "inprogress",
          "attendance": 0,
          "coverage": "boxscore",
          "home_scoring_data": null,
          "away_scoring_data": null,
          "day_night": "D",
          "game_number": 1,
          "inning": "9.0",
          "inning_half": "T",
          "srid_home_pp": null,
          "srid_home_sp": null,
          "srid_away_pp": null,
          "srid_away_sp": null,
          "srid_win": null,
          "srid_loss": null,
          "home_errors": 0,
          "home_hits": 0,
          "away_errors": 0,
          "away_hits": 0
        },
        "title": "",
        "srid_home": "d89bed32-3aee-4407-99e3-4103641b999a",
        "start": "2016-03-17T17:05:00Z",
        "srid": "a15a9d61-2c05-4e20-ac9f-7f8005b98175",
        "day_night": "D",
        "game_number": 1,
        "sport": "mlb",
        "timeRemaining": {
          "duration": 0,
          "decimal": 0
        }
      },
      "a13273ad-dc00-4b91-a3d0-1ee7533989ed": {
        "srid_away": "4f735188-37c8-473d-ae32-1f7e34ccf892",
        "status": "scheduled",
        "boxscore": {
          "srid_game": "a13273ad-dc00-4b91-a3d0-1ee7533989ed",
          "srid_home": "29dd9a87-5bcc-4774-80c3-7f50d985068b",
          "srid_away": "4f735188-37c8-473d-ae32-1f7e34ccf892",
          "home_score": 1,
          "away_score": 4,
          "status": "inprogress",
          "attendance": 0,
          "coverage": "full",
          "home_scoring_data": [
            {
              "inning": {
                "number": 1,
                "sequence": 1,
                "runs": 0
              }
            },
            {
              "inning": {
                "number": 2,
                "sequence": 2,
                "runs": 0
              }
            },
            {
              "inning": {
                "number": 3,
                "sequence": 3,
                "runs": 1
              }
            },
            {
              "inning": {
                "number": 4,
                "sequence": 4,
                "runs": 0
              }
            },
            {
              "inning": {
                "number": 5,
                "sequence": 5,
                "runs": 0
              }
            }
          ],
          "away_scoring_data": [
            {
              "inning": {
                "number": 1,
                "sequence": 1,
                "runs": 2
              }
            },
            {
              "inning": {
                "number": 2,
                "sequence": 2,
                "runs": 1
              }
            },
            {
              "inning": {
                "number": 3,
                "sequence": 3,
                "runs": 1
              }
            },
            {
              "inning": {
                "number": 4,
                "sequence": 4,
                "runs": 0
              }
            },
            {
              "inning": {
                "number": 5,
                "sequence": 5,
                "runs": 0
              }
            }
          ],
          "day_night": "D",
          "game_number": 1,
          "inning": "5.0",
          "inning_half": "B",
          "srid_home_pp": "d2b49c9d-1c9f-44b4-b9b9-c4222dc0c089",
          "srid_home_sp": "d2b49c9d-1c9f-44b4-b9b9-c4222dc0c089",
          "srid_away_pp": "3c0813bf-0d4b-4ec7-9ecb-4a3db0936de4",
          "srid_away_sp": "3c0813bf-0d4b-4ec7-9ecb-4a3db0936de4",
          "srid_win": null,
          "srid_loss": null,
          "home_errors": 1,
          "home_hits": 4,
          "away_errors": 1,
          "away_hits": 10
        },
        "title": "",
        "srid_home": "29dd9a87-5bcc-4774-80c3-7f50d985068b",
        "start": "2016-03-17T20:10:00Z",
        "srid": "a13273ad-dc00-4b91-a3d0-1ee7533989ed",
        "day_night": "D",
        "game_number": 1,
        "sport": "mlb",
        "timeRemaining": {
          "duration": 7,
          "decimal": 0.3889
        }
      },
      "930ba2a6-a528-4bbd-a454-0c3a0127a076": {
        "srid_away": "aa34e0ed-f342-4ec6-b774-c79b47b60e2d",
        "status": "scheduled",
        "title": "",
        "srid_home": "75729d34-bca7-4a0f-b3df-6f26c6ad3719",
        "start": "2016-03-17T23:05:00Z",
        "srid": "930ba2a6-a528-4bbd-a454-0c3a0127a076",
        "day_night": "N",
        "game_number": 1,
        "sport": "mlb",
        "timeRemaining": {
          "duration": 18,
          "decimal": 0.9999
        }
      },
      "43de6de9-9b26-4ba0-ac98-dcff50a5cc51": {
        "srid_away": "bdc11650-6f74-49c4-875e-778aeb7632d9",
        "status": "scheduled",
        "boxscore": {
          "srid_game": "43de6de9-9b26-4ba0-ac98-dcff50a5cc51",
          "srid_home": "2142e1ba-3b40-445c-b8bb-f1f8b1054220",
          "srid_away": "bdc11650-6f74-49c4-875e-778aeb7632d9",
          "home_score": 0,
          "away_score": 0,
          "status": "inprogress",
          "attendance": 0,
          "coverage": "boxscore",
          "home_scoring_data": null,
          "away_scoring_data": null,
          "day_night": "D",
          "game_number": 1,
          "inning": "9.0",
          "inning_half": "T",
          "srid_home_pp": null,
          "srid_home_sp": null,
          "srid_away_pp": null,
          "srid_away_sp": null,
          "srid_win": null,
          "srid_loss": null,
          "home_errors": 0,
          "home_hits": 0,
          "away_errors": 0,
          "away_hits": 0
        },
        "title": "",
        "srid_home": "2142e1ba-3b40-445c-b8bb-f1f8b1054220",
        "start": "2016-03-17T17:05:00Z",
        "srid": "43de6de9-9b26-4ba0-ac98-dcff50a5cc51",
        "day_night": "D",
        "game_number": 1,
        "sport": "mlb",
        "timeRemaining": {
          "duration": 0,
          "decimal": 0
        }
      },
      "fcd1a636-2e3a-4224-8a48-494a4d29ffd1": {
        "srid_away": "833a51a9-0d84-410f-bd77-da08c3e5e26e",
        "status": "scheduled",
        "boxscore": {
          "srid_game": "fcd1a636-2e3a-4224-8a48-494a4d29ffd1",
          "srid_home": "ef64da7f-cfaf-4300-87b0-9313386b977c",
          "srid_away": "833a51a9-0d84-410f-bd77-da08c3e5e26e",
          "home_score": 0,
          "away_score": 0,
          "status": "inprogress",
          "attendance": 0,
          "coverage": "boxscore",
          "home_scoring_data": null,
          "away_scoring_data": {},
          "day_night": "D",
          "game_number": 1,
          "inning": "",
          "inning_half": "",
          "srid_home_pp": null,
          "srid_home_sp": null,
          "srid_away_pp": "7570d0a2-7246-4078-bf8c-d38a283e0829",
          "srid_away_sp": null,
          "srid_win": null,
          "srid_loss": null,
          "home_errors": 0,
          "home_hits": 0,
          "away_errors": 0,
          "away_hits": 0
        },
        "title": "",
        "srid_home": "ef64da7f-cfaf-4300-87b0-9313386b977c",
        "start": "2016-03-17T20:05:00Z",
        "srid": "fcd1a636-2e3a-4224-8a48-494a4d29ffd1",
        "day_night": "D",
        "game_number": 1,
        "sport": "mlb",
        "timeRemaining": {
          "duration": 18,
          "decimal": 0.9999
        }
      },
      "b177330b-ec67-4f86-8c0b-b0dfe481b5a4": {
        "srid_away": "f246a5e5-afdb-479c-9aaa-c68beeda7af6",
        "status": "scheduled",
        "title": "",
        "srid_home": "03556285-bdbb-4576-a06d-42f71f46ddc5",
        "start": "2016-03-17T17:05:00Z",
        "srid": "b177330b-ec67-4f86-8c0b-b0dfe481b5a4",
        "day_night": "D",
        "game_number": 1,
        "sport": "mlb",
        "timeRemaining": {
          "duration": 18,
          "decimal": 0.9999
        }
      },
      "8c15f06b-3a2a-44f2-95e8-b25dd8fcdc97": {
        "srid_away": "a09ec676-f887-43dc-bbb3-cf4bbaee9a18",
        "status": "scheduled",
        "title": "",
        "srid_home": "481dfe7e-5dab-46ab-a49f-9dcc2b6e2cfd",
        "start": "2016-03-17T17:05:00Z",
        "srid": "8c15f06b-3a2a-44f2-95e8-b25dd8fcdc97",
        "day_night": "D",
        "game_number": 1,
        "sport": "mlb",
        "timeRemaining": {
          "duration": 18,
          "decimal": 0.9999
        }
      },
      "1264ac53-9c92-4803-b15b-a6485591ab3f": {
        "srid_away": "eb21dadd-8f10-4095-8bf3-dfb3b779f107",
        "status": "scheduled",
        "boxscore": {
          "srid_game": "1264ac53-9c92-4803-b15b-a6485591ab3f",
          "srid_home": "12079497-e414-450a-8bf2-29f91de646bf",
          "srid_away": "eb21dadd-8f10-4095-8bf3-dfb3b779f107",
          "home_score": 0,
          "away_score": 5,
          "status": "inprogress",
          "attendance": 0,
          "coverage": "boxscore",
          "home_scoring_data": null,
          "away_scoring_data": [
            {
              "inning": {
                "number": 1,
                "runs": 0,
                "sequence": 1
              }
            },
            {
              "inning": {
                "number": 2,
                "runs": 0,
                "sequence": 2
              }
            },
            {
              "inning": {
                "number": 3,
                "runs": 0,
                "sequence": 3
              }
            },
            {
              "inning": {
                "number": 4,
                "runs": 2,
                "sequence": 4
              }
            },
            {
              "inning": {
                "number": 5,
                "runs": 0,
                "sequence": 5
              }
            },
            {
              "inning": {
                "number": 6,
                "runs": 0,
                "sequence": 6
              }
            },
            {
              "inning": {
                "number": 7,
                "runs": 0,
                "sequence": 7
              }
            },
            {
              "inning": {
                "number": 8,
                "runs": 3,
                "sequence": 8
              }
            },
            {
              "inning": {
                "number": 9,
                "runs": 0,
                "sequence": 9
              }
            }
          ],
          "day_night": "D",
          "game_number": 1,
          "inning": "9.0",
          "inning_half": "T",
          "srid_home_pp": null,
          "srid_home_sp": null,
          "srid_away_pp": "e0b021ce-33aa-46fc-b673-6bd35f220eb6",
          "srid_away_sp": null,
          "srid_win": null,
          "srid_loss": null,
          "home_errors": 0,
          "home_hits": 0,
          "away_errors": 1,
          "away_hits": 6
        },
        "title": "",
        "srid_home": "12079497-e414-450a-8bf2-29f91de646bf",
        "start": "2016-03-17T17:05:00Z",
        "srid": "1264ac53-9c92-4803-b15b-a6485591ab3f",
        "day_night": "D",
        "game_number": 1,
        "sport": "mlb",
        "timeRemaining": {
          "duration": 0,
          "decimal": 0
        }
      },
      "2ab7238c-f9ac-417b-9908-47cfa01878b0": {
        "srid_away": "1d678440-b4b1-4954-9b39-70afb3ebbcfa",
        "status": "scheduled",
        "title": "",
        "srid_home": "eb21dadd-8f10-4095-8bf3-dfb3b779f107",
        "start": "2016-03-17T17:05:00Z",
        "srid": "2ab7238c-f9ac-417b-9908-47cfa01878b0",
        "day_night": "D",
        "game_number": 1,
        "sport": "mlb",
        "timeRemaining": {
          "duration": 18,
          "decimal": 0.9999
        }
      },
      "0ce5c040-667e-4516-aed9-59103e20843b": {
        "srid_away": "a7723160-10b7-4277-a309-d8dd95a8ae65",
        "status": "scheduled",
        "title": "",
        "srid_home": "d52d5339-cbdd-43f3-9dfa-a42fd588b9a3",
        "start": "2016-03-18T02:10:00Z",
        "srid": "0ce5c040-667e-4516-aed9-59103e20843b",
        "day_night": "N",
        "game_number": 1,
        "sport": "mlb",
        "timeRemaining": {
          "duration": 18,
          "decimal": 0.9999
        }
      },
      "6ad53c29-b887-4508-bec4-905526dd150e": {
        "srid_away": "25507be1-6a68-4267-bd82-e097d94b359b",
        "status": "scheduled",
        "title": "",
        "srid_home": "55714da8-fcaf-4574-8443-59bfb511a524",
        "start": "2016-03-17T23:05:00Z",
        "srid": "6ad53c29-b887-4508-bec4-905526dd150e",
        "day_night": "N",
        "game_number": 1,
        "sport": "mlb",
        "timeRemaining": {
          "duration": 18,
          "decimal": 0.9999
        }
      },
      "b4bc7fb4-1d19-44dd-8b72-c2ff124e6076": {
        "srid_away": "44671792-dc02-4fdd-a5ad-f5f17edaa9d7",
        "status": "scheduled",
        "title": "",
        "srid_home": "575c19b7-4052-41c2-9f0a-1c5813d02f99",
        "start": "2016-03-17T17:05:00Z",
        "srid": "b4bc7fb4-1d19-44dd-8b72-c2ff124e6076",
        "day_night": "D",
        "game_number": 1,
        "sport": "mlb",
        "timeRemaining": {
          "duration": 18,
          "decimal": 0.9999
        }
      },
      "cf792401-24ad-4646-aa8d-34ec34d20db5": {
        "srid_away": "43a39081-52b4-4f93-ad29-da7f329ea960",
        "status": "scheduled",
        "boxscore": {
          "srid_game": "cf792401-24ad-4646-aa8d-34ec34d20db5",
          "srid_home": "27a59d3b-ff7c-48ea-b016-4798f560f5e1",
          "srid_away": "43a39081-52b4-4f93-ad29-da7f329ea960",
          "home_score": 0,
          "away_score": 0,
          "status": "scheduled",
          "attendance": 0,
          "coverage": "boxscore",
          "home_scoring_data": {},
          "away_scoring_data": null,
          "day_night": "D",
          "game_number": 1,
          "inning": "6.0",
          "inning_half": "B",
          "srid_home_pp": "18be2520-ed71-4e1e-94c8-29b0590e2b5c",
          "srid_home_sp": null,
          "srid_away_pp": null,
          "srid_away_sp": null,
          "srid_win": null,
          "srid_loss": null,
          "home_errors": 0,
          "home_hits": 0,
          "away_errors": 0,
          "away_hits": 0
        },
        "title": "",
        "srid_home": "27a59d3b-ff7c-48ea-b016-4798f560f5e1",
        "start": "2016-03-17T20:05:00Z",
        "srid": "cf792401-24ad-4646-aa8d-34ec34d20db5",
        "day_night": "D",
        "game_number": 1,
        "sport": "mlb",
        "timeRemaining": {
          "duration": 5,
          "decimal": 0.2778
        }
      },
      "5a8f08ec-73ea-4273-819d-bb90eba81e24": {
        "srid_away": "80715d0d-0d2a-450f-a970-1b9a3b18c7e7",
        "status": "scheduled",
        "boxscore": {
          "srid_game": "5a8f08ec-73ea-4273-819d-bb90eba81e24",
          "srid_home": "c874a065-c115-4e7d-b0f0-235584fb0e6f",
          "srid_away": "80715d0d-0d2a-450f-a970-1b9a3b18c7e7",
          "home_score": 0,
          "away_score": 0,
          "status": "scheduled",
          "attendance": 0,
          "coverage": "boxscore",
          "home_scoring_data": null,
          "away_scoring_data": null,
          "day_night": "D",
          "game_number": 1,
          "inning": "",
          "inning_half": "",
          "srid_home_pp": null,
          "srid_home_sp": null,
          "srid_away_pp": null,
          "srid_away_sp": null,
          "srid_win": null,
          "srid_loss": null,
          "home_errors": 0,
          "home_hits": 0,
          "away_errors": 0,
          "away_hits": 0
        },
        "title": "",
        "srid_home": "c874a065-c115-4e7d-b0f0-235584fb0e6f",
        "start": "2016-03-17T20:05:00Z",
        "srid": "5a8f08ec-73ea-4273-819d-bb90eba81e24",
        "day_night": "D",
        "game_number": 1,
        "sport": "mlb",
        "timeRemaining": {
          "duration": 18,
          "decimal": 0.9999
        }
      }
    },
    "types": [
      "nba",
      "nhl",
      "mlb"
    ],
    "nba": {
      "gameIds": [
        "e2c33042-9ac9-4462-bbe1-71db18fde051",
        "73e40c5f-c690-4936-8853-339ed43dcc76",
        "9a98eb05-477f-436e-99c7-3c60674055ff",
        "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
        "654a55e1-004a-4d3c-916c-b48eabaab840",
        "440a04df-0caa-4e99-a032-911ddb602576",
        "82a6f3e1-3b5a-420f-9288-85b99f781507",
        "2b9028c3-c482-4300-89fe-64e133aad607"
      ],
      "isFetchingTeams": false,
      "isFetchingGames": false,
      "gamesExpireAt": 1458241478331,
      "teamsExpireAt": 1458262478241,
      "teams": {
        "583ec773-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 12,
          "srid": "583ec773-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Cavaliers",
          "alias": "CLE",
          "city": "Cleveland"
        },
        "583ec87d-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 7,
          "srid": "583ec87d-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "76ers",
          "alias": "PHI",
          "city": "Philadelphia"
        },
        "583ecdfb-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 28,
          "srid": "583ecdfb-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Clippers",
          "alias": "LAC",
          "city": "Los Angeles"
        },
        "583ec97e-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 2,
          "srid": "583ec97e-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Hornets",
          "alias": "CHA",
          "city": "Charlotte"
        },
        "583ece50-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 17,
          "srid": "583ece50-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Jazz",
          "alias": "UTA",
          "city": "Utah"
        },
        "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 3,
          "srid": "583ecb8f-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Hawks",
          "alias": "ATL",
          "city": "Atlanta"
        },
        "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 24,
          "srid": "583ecd4f-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Spurs",
          "alias": "SAS",
          "city": "San Antonio"
        },
        "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 29,
          "srid": "583ecfa8-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Suns",
          "alias": "PHX",
          "city": "Phoenix"
        },
        "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 13,
          "srid": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Pacers",
          "alias": "IND",
          "city": "Indiana"
        },
        "583ecea6-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 4,
          "srid": "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Heat",
          "alias": "MIA",
          "city": "Miami"
        },
        "583ecf50-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 25,
          "srid": "583ecf50-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Mavericks",
          "alias": "DAL",
          "city": "Dallas"
        },
        "583ed0ac-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 30,
          "srid": "583ed0ac-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Kings",
          "alias": "SAC",
          "city": "Sacramento"
        },
        "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 8,
          "srid": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Nets",
          "alias": "BKN",
          "city": "Brooklyn"
        },
        "583eccfa-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 9,
          "srid": "583eccfa-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Celtics",
          "alias": "BOS",
          "city": "Boston"
        },
        "583ec928-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 14,
          "srid": "583ec928-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Pistons",
          "alias": "DET",
          "city": "Detroit"
        },
        "583ecefd-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 15,
          "srid": "583ecefd-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Bucks",
          "alias": "MIL",
          "city": "Milwaukee"
        },
        "583eca2f-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 16,
          "srid": "583eca2f-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Timberwolves",
          "alias": "MIN",
          "city": "Minnesota"
        },
        "583ec825-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 26,
          "srid": "583ec825-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Warriors",
          "alias": "GSW",
          "city": "Golden State"
        },
        "583ed157-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 5,
          "srid": "583ed157-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Magic",
          "alias": "ORL",
          "city": "Orlando"
        },
        "583ecae2-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 27,
          "srid": "583ecae2-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Lakers",
          "alias": "LAL",
          "city": "Los Angeles"
        },
        "583ecda6-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 10,
          "srid": "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Raptors",
          "alias": "TOR",
          "city": "Toronto"
        },
        "583ec70e-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 6,
          "srid": "583ec70e-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Knicks",
          "alias": "NYK",
          "city": "New York"
        },
        "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 1,
          "srid": "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Wizards",
          "alias": "WAS",
          "city": "Washington"
        },
        "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 11,
          "srid": "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Bulls",
          "alias": "CHI",
          "city": "Chicago"
        },
        "583ecfff-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 18,
          "srid": "583ecfff-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Thunder",
          "alias": "OKC",
          "city": "Oklahoma City"
        },
        "583ed056-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 19,
          "srid": "583ed056-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Trail Blazers",
          "alias": "POR",
          "city": "Portland"
        },
        "583ed102-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 20,
          "srid": "583ed102-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Nuggets",
          "alias": "DEN",
          "city": "Denver"
        },
        "583eca88-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 21,
          "srid": "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Grizzlies",
          "alias": "MEM",
          "city": "Memphis"
        },
        "583ecb3a-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 22,
          "srid": "583ecb3a-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Rockets",
          "alias": "HOU",
          "city": "Houston"
        },
        "583ecc9a-fb46-11e1-82cb-f4ce4684ea4c": {
          "id": 23,
          "srid": "583ecc9a-fb46-11e1-82cb-f4ce4684ea4c",
          "name": "Pelicans",
          "alias": "NOP",
          "city": "New Orleans"
        }
      }
    },
    "nhl": {
      "gameIds": [
        "b5a2dab9-98b3-4eeb-a779-0c1c62f8cb6c",
        "5f9175c7-83f8-477a-8fb0-e42a63e6206e",
        "76f98202-6c63-42c5-8d2e-270c20948dac",
        "e496cc84-14bb-4eee-bbae-09d12d253795",
        "93113aa7-5afd-46d1-9c9a-683e13c121f6",
        "633df866-11a6-4801-9090-4c2a1a79d8d5",
        "27c230bc-30b3-40f3-be66-b6aa10c63f8b",
        "395ec023-b416-419c-8368-70e57720f99d"
      ],
      "isFetchingTeams": false,
      "isFetchingGames": false,
      "gamesExpireAt": 1458241478415,
      "teamsExpireAt": 1458262478311,
      "teams": {
        "4416ba1a-0f24-11e2-8525-18a905767e44": {
          "id": 16,
          "srid": "4416ba1a-0f24-11e2-8525-18a905767e44",
          "name": "Bruins",
          "alias": "BOS",
          "city": "Boston"
        },
        "44169bb9-0f24-11e2-8525-18a905767e44": {
          "id": 15,
          "srid": "44169bb9-0f24-11e2-8525-18a905767e44",
          "name": "Red Wings",
          "alias": "DET",
          "city": "Detroit"
        },
        "44155909-0f24-11e2-8525-18a905767e44": {
          "id": 6,
          "srid": "44155909-0f24-11e2-8525-18a905767e44",
          "name": "Sharks",
          "alias": "SJ",
          "city": "San Jose"
        },
        "4416d559-0f24-11e2-8525-18a905767e44": {
          "id": 17,
          "srid": "4416d559-0f24-11e2-8525-18a905767e44",
          "name": "Sabres",
          "alias": "BUF",
          "city": "Buffalo"
        },
        "44167db4-0f24-11e2-8525-18a905767e44": {
          "id": 23,
          "srid": "44167db4-0f24-11e2-8525-18a905767e44",
          "name": "Blue Jackets",
          "alias": "CBJ",
          "city": "Columbus"
        },
        "44174b0c-0f24-11e2-8525-18a905767e44": {
          "id": 24,
          "srid": "44174b0c-0f24-11e2-8525-18a905767e44",
          "name": "Devils",
          "alias": "NJ",
          "city": "New Jersey"
        },
        "4417d3cb-0f24-11e2-8525-18a905767e44": {
          "id": 21,
          "srid": "4417d3cb-0f24-11e2-8525-18a905767e44",
          "name": "Lightning",
          "alias": "TB",
          "city": "Tampa Bay"
        },
        "4418464d-0f24-11e2-8525-18a905767e44": {
          "id": 22,
          "srid": "4418464d-0f24-11e2-8525-18a905767e44",
          "name": "Panthers",
          "alias": "FLA",
          "city": "Florida"
        },
        "441781b9-0f24-11e2-8525-18a905767e44": {
          "id": 26,
          "srid": "441781b9-0f24-11e2-8525-18a905767e44",
          "name": "Rangers",
          "alias": "NYR",
          "city": "New York"
        },
        "4415b0a7-0f24-11e2-8525-18a905767e44": {
          "id": 2,
          "srid": "4415b0a7-0f24-11e2-8525-18a905767e44",
          "name": "Canucks",
          "alias": "VAN",
          "city": "Vancouver"
        },
        "441766b9-0f24-11e2-8525-18a905767e44": {
          "id": 25,
          "srid": "441766b9-0f24-11e2-8525-18a905767e44",
          "name": "Islanders",
          "alias": "NYI",
          "city": "New York"
        },
        "4417b7d7-0f24-11e2-8525-18a905767e44": {
          "id": 28,
          "srid": "4417b7d7-0f24-11e2-8525-18a905767e44",
          "name": "Penguins",
          "alias": "PIT",
          "city": "Pittsburgh"
        },
        "44179d47-0f24-11e2-8525-18a905767e44": {
          "id": 27,
          "srid": "44179d47-0f24-11e2-8525-18a905767e44",
          "name": "Flyers",
          "alias": "PHI",
          "city": "Philadelphia"
        },
        "4416272f-0f24-11e2-8525-18a905767e44": {
          "id": 11,
          "srid": "4416272f-0f24-11e2-8525-18a905767e44",
          "name": "Blackhawks",
          "alias": "CHI",
          "city": "Chicago"
        },
        "441862de-0f24-11e2-8525-18a905767e44": {
          "id": 7,
          "srid": "441862de-0f24-11e2-8525-18a905767e44",
          "name": "Ducks",
          "alias": "ANA",
          "city": "Anaheim"
        },
        "44151f7a-0f24-11e2-8525-18a905767e44": {
          "id": 4,
          "srid": "44151f7a-0f24-11e2-8525-18a905767e44",
          "name": "Kings",
          "alias": "LA",
          "city": "Los Angeles"
        },
        "441713b7-0f24-11e2-8525-18a905767e44": {
          "id": 19,
          "srid": "441713b7-0f24-11e2-8525-18a905767e44",
          "name": "Canadiens",
          "alias": "MTL",
          "city": "Montreal"
        },
        "44153da1-0f24-11e2-8525-18a905767e44": {
          "id": 5,
          "srid": "44153da1-0f24-11e2-8525-18a905767e44",
          "name": "Coyotes",
          "alias": "ARI",
          "city": "Arizona"
        },
        "4415ce44-0f24-11e2-8525-18a905767e44": {
          "id": 9,
          "srid": "4415ce44-0f24-11e2-8525-18a905767e44",
          "name": "Avalanche",
          "alias": "COL",
          "city": "Colorado"
        },
        "4416091c-0f24-11e2-8525-18a905767e44": {
          "id": 10,
          "srid": "4416091c-0f24-11e2-8525-18a905767e44",
          "name": "Wild",
          "alias": "MIN",
          "city": "Minnesota"
        },
        "44182a9d-0f24-11e2-8525-18a905767e44": {
          "id": 30,
          "srid": "44182a9d-0f24-11e2-8525-18a905767e44",
          "name": "Hurricanes",
          "alias": "CAR",
          "city": "Carolina"
        },
        "44157522-0f24-11e2-8525-18a905767e44": {
          "id": 8,
          "srid": "44157522-0f24-11e2-8525-18a905767e44",
          "name": "Stars",
          "alias": "DAL",
          "city": "Dallas"
        },
        "4416f5e2-0f24-11e2-8525-18a905767e44": {
          "id": 18,
          "srid": "4416f5e2-0f24-11e2-8525-18a905767e44",
          "name": "Senators",
          "alias": "OTT",
          "city": "Ottawa"
        },
        "441730a9-0f24-11e2-8525-18a905767e44": {
          "id": 20,
          "srid": "441730a9-0f24-11e2-8525-18a905767e44",
          "name": "Maple Leafs",
          "alias": "TOR",
          "city": "Toronto"
        },
        "4415ea6c-0f24-11e2-8525-18a905767e44": {
          "id": 3,
          "srid": "4415ea6c-0f24-11e2-8525-18a905767e44",
          "name": "Oilers",
          "alias": "EDM",
          "city": "Edmonton"
        },
        "44159241-0f24-11e2-8525-18a905767e44": {
          "id": 1,
          "srid": "44159241-0f24-11e2-8525-18a905767e44",
          "name": "Flames",
          "alias": "CGY",
          "city": "Calgary"
        },
        "441660ea-0f24-11e2-8525-18a905767e44": {
          "id": 13,
          "srid": "441660ea-0f24-11e2-8525-18a905767e44",
          "name": "Blues",
          "alias": "STL",
          "city": "St. Louis"
        },
        "4417eede-0f24-11e2-8525-18a905767e44": {
          "id": 29,
          "srid": "4417eede-0f24-11e2-8525-18a905767e44",
          "name": "Capitals",
          "alias": "WSH",
          "city": "Washington"
        },
        "44180e55-0f24-11e2-8525-18a905767e44": {
          "id": 14,
          "srid": "44180e55-0f24-11e2-8525-18a905767e44",
          "name": "Jets",
          "alias": "WPG",
          "city": "Winnipeg"
        },
        "441643b7-0f24-11e2-8525-18a905767e44": {
          "id": 12,
          "srid": "441643b7-0f24-11e2-8525-18a905767e44",
          "name": "Predators",
          "alias": "NSH",
          "city": "Nashville"
        }
      }
    },
    "mlb": {
      "gameIds": [
        "15ab1217-2fc5-4829-a54e-fa979167f851",
        "a15a9d61-2c05-4e20-ac9f-7f8005b98175",
        "43de6de9-9b26-4ba0-ac98-dcff50a5cc51",
        "b177330b-ec67-4f86-8c0b-b0dfe481b5a4",
        "8c15f06b-3a2a-44f2-95e8-b25dd8fcdc97",
        "1264ac53-9c92-4803-b15b-a6485591ab3f",
        "2ab7238c-f9ac-417b-9908-47cfa01878b0",
        "b4bc7fb4-1d19-44dd-8b72-c2ff124e6076",
        "fcd1a636-2e3a-4224-8a48-494a4d29ffd1",
        "cf792401-24ad-4646-aa8d-34ec34d20db5",
        "5a8f08ec-73ea-4273-819d-bb90eba81e24",
        "a13273ad-dc00-4b91-a3d0-1ee7533989ed",
        "930ba2a6-a528-4bbd-a454-0c3a0127a076",
        "6ad53c29-b887-4508-bec4-905526dd150e",
        "a5ecca24-c461-4292-8f93-a6c7e6ca34d5",
        "0ce5c040-667e-4516-aed9-59103e20843b"
      ],
      "isFetchingTeams": false,
      "isFetchingGames": false,
      "gamesExpireAt": 1458241478458,
      "teamsExpireAt": 1458262478266,
      "teams": {
        "a09ec676-f887-43dc-bbb3-cf4bbaee9a18": {
          "id": 5,
          "srid": "a09ec676-f887-43dc-bbb3-cf4bbaee9a18",
          "name": "Yankees",
          "alias": "NYY",
          "city": "New York"
        },
        "833a51a9-0d84-410f-bd77-da08c3e5e26e": {
          "id": 6,
          "srid": "833a51a9-0d84-410f-bd77-da08c3e5e26e",
          "name": "Royals",
          "alias": "KC",
          "city": "Kansas City"
        },
        "575c19b7-4052-41c2-9f0a-1c5813d02f99": {
          "id": 9,
          "srid": "575c19b7-4052-41c2-9f0a-1c5813d02f99",
          "name": "Tigers",
          "alias": "DET",
          "city": "Detroit"
        },
        "aa34e0ed-f342-4ec6-b774-c79b47b60e2d": {
          "id": 10,
          "srid": "aa34e0ed-f342-4ec6-b774-c79b47b60e2d",
          "name": "Twins",
          "alias": "MIN",
          "city": "Minnesota"
        },
        "27a59d3b-ff7c-48ea-b016-4798f560f5e1": {
          "id": 13,
          "srid": "27a59d3b-ff7c-48ea-b016-4798f560f5e1",
          "name": "Athletics",
          "alias": "OAK",
          "city": "Oakland"
        },
        "d99f919b-1534-4516-8e8a-9cd106c6d8cd": {
          "id": 14,
          "srid": "d99f919b-1534-4516-8e8a-9cd106c6d8cd",
          "name": "Rangers",
          "alias": "TEX",
          "city": "Texas"
        },
        "eb21dadd-8f10-4095-8bf3-dfb3b779f107": {
          "id": 15,
          "srid": "eb21dadd-8f10-4095-8bf3-dfb3b779f107",
          "name": "Astros",
          "alias": "HOU",
          "city": "Houston"
        },
        "c874a065-c115-4e7d-b0f0-235584fb0e6f": {
          "id": 16,
          "srid": "c874a065-c115-4e7d-b0f0-235584fb0e6f",
          "name": "Reds",
          "alias": "CIN",
          "city": "Cincinnati"
        },
        "481dfe7e-5dab-46ab-a49f-9dcc2b6e2cfd": {
          "id": 17,
          "srid": "481dfe7e-5dab-46ab-a49f-9dcc2b6e2cfd",
          "name": "Pirates",
          "alias": "PIT",
          "city": "Pittsburgh"
        },
        "55714da8-fcaf-4574-8443-59bfb511a524": {
          "id": 18,
          "srid": "55714da8-fcaf-4574-8443-59bfb511a524",
          "name": "Cubs",
          "alias": "CHC",
          "city": "Chicago"
        },
        "44671792-dc02-4fdd-a5ad-f5f17edaa9d7": {
          "id": 19,
          "srid": "44671792-dc02-4fdd-a5ad-f5f17edaa9d7",
          "name": "Cardinals",
          "alias": "STL",
          "city": "St. Louis"
        },
        "dcfd5266-00ce-442c-bc09-264cd20cf455": {
          "id": 20,
          "srid": "dcfd5266-00ce-442c-bc09-264cd20cf455",
          "name": "Brewers",
          "alias": "MIL",
          "city": "Milwaukee"
        },
        "ef64da7f-cfaf-4300-87b0-9313386b977c": {
          "id": 21,
          "srid": "ef64da7f-cfaf-4300-87b0-9313386b977c",
          "name": "Dodgers",
          "alias": "LAD",
          "city": "Los Angeles"
        },
        "25507be1-6a68-4267-bd82-e097d94b359b": {
          "id": 22,
          "srid": "25507be1-6a68-4267-bd82-e097d94b359b",
          "name": "Diamondbacks",
          "alias": "ARI",
          "city": "Arizona"
        },
        "a7723160-10b7-4277-a309-d8dd95a8ae65": {
          "id": 23,
          "srid": "a7723160-10b7-4277-a309-d8dd95a8ae65",
          "name": "Giants",
          "alias": "SF",
          "city": "San Francisco"
        },
        "29dd9a87-5bcc-4774-80c3-7f50d985068b": {
          "id": 24,
          "srid": "29dd9a87-5bcc-4774-80c3-7f50d985068b",
          "name": "Rockies",
          "alias": "COL",
          "city": "Colorado"
        },
        "d52d5339-cbdd-43f3-9dfa-a42fd588b9a3": {
          "id": 25,
          "srid": "d52d5339-cbdd-43f3-9dfa-a42fd588b9a3",
          "name": "Padres",
          "alias": "SD",
          "city": "San Diego"
        },
        "2142e1ba-3b40-445c-b8bb-f1f8b1054220": {
          "id": 26,
          "srid": "2142e1ba-3b40-445c-b8bb-f1f8b1054220",
          "name": "Phillies",
          "alias": "PHI",
          "city": "Philadelphia"
        },
        "f246a5e5-afdb-479c-9aaa-c68beeda7af6": {
          "id": 27,
          "srid": "f246a5e5-afdb-479c-9aaa-c68beeda7af6",
          "name": "Mets",
          "alias": "NYM",
          "city": "New York"
        },
        "03556285-bdbb-4576-a06d-42f71f46ddc5": {
          "id": 28,
          "srid": "03556285-bdbb-4576-a06d-42f71f46ddc5",
          "name": "Marlins",
          "alias": "MIA",
          "city": "Miami"
        },
        "12079497-e414-450a-8bf2-29f91de646bf": {
          "id": 29,
          "srid": "12079497-e414-450a-8bf2-29f91de646bf",
          "name": "Braves",
          "alias": "ATL",
          "city": "Atlanta"
        },
        "d89bed32-3aee-4407-99e3-4103641b999a": {
          "id": 30,
          "srid": "d89bed32-3aee-4407-99e3-4103641b999a",
          "name": "Nationals",
          "alias": "WSH",
          "city": "Washington"
        },
        "1d678440-b4b1-4954-9b39-70afb3ebbcfa": {
          "id": 1,
          "srid": "1d678440-b4b1-4954-9b39-70afb3ebbcfa",
          "name": "Blue Jays",
          "alias": "TOR",
          "city": "Toronto"
        },
        "bdc11650-6f74-49c4-875e-778aeb7632d9": {
          "id": 2,
          "srid": "bdc11650-6f74-49c4-875e-778aeb7632d9",
          "name": "Rays",
          "alias": "TB",
          "city": "Tampa Bay"
        },
        "75729d34-bca7-4a0f-b3df-6f26c6ad3719": {
          "id": 3,
          "srid": "75729d34-bca7-4a0f-b3df-6f26c6ad3719",
          "name": "Orioles",
          "alias": "BAL",
          "city": "Baltimore"
        },
        "93941372-eb4c-4c40-aced-fe3267174393": {
          "id": 4,
          "srid": "93941372-eb4c-4c40-aced-fe3267174393",
          "name": "Red Sox",
          "alias": "BOS",
          "city": "Boston"
        },
        "80715d0d-0d2a-450f-a970-1b9a3b18c7e7": {
          "id": 7,
          "srid": "80715d0d-0d2a-450f-a970-1b9a3b18c7e7",
          "name": "Indians",
          "alias": "CLE",
          "city": "Cleveland"
        },
        "47f490cd-2f58-4ef7-9dfd-2ad6ba6c1ae8": {
          "id": 8,
          "srid": "47f490cd-2f58-4ef7-9dfd-2ad6ba6c1ae8",
          "name": "White Sox",
          "alias": "CWS",
          "city": "Chicago"
        },
        "43a39081-52b4-4f93-ad29-da7f329ea960": {
          "id": 11,
          "srid": "43a39081-52b4-4f93-ad29-da7f329ea960",
          "name": "Mariners",
          "alias": "SEA",
          "city": "Seattle"
        },
        "4f735188-37c8-473d-ae32-1f7e34ccf892": {
          "id": 12,
          "srid": "4f735188-37c8-473d-ae32-1f7e34ccf892",
          "name": "Angels",
          "alias": "LAA",
          "city": "Los Angeles"
        }
      }
    }
  },
  "transactions": {
    "allTransactions": [],
    "filteredTransactions": [],
    "focusedTransactionId": {},
    "filters": {
      "startDate": null,
      "endDate": null
    }
  },
  "upcomingContests": {
    "allContests": {},
    "filteredContests": {},
    "focusedContestId": null,
    "isFetchingEntrants": false,
    "entrants": {},
    "filters": {
      "orderBy": {
        "property": "start",
        "direction": "asc"
      },
      "contestSearchFilter": {},
      "sportFilter": {}
    }
  },
  "upcomingDraftGroups": {
    "activeDraftGroupId": null,
    "draftGroupSelectionModalIsOpen": false,
    "sportContestCounts": {},
    "draftGroups": {},
    "boxScores": {
      "isFetching": false
    }
  },
  "upcomingLineups": {
    "lineups": {},
    "draftGroupIdFilter": null,
    "draftGroupsWithLineups": [],
    "lineupBeingEdited": null,
    "focusedLineupId": null,
    "hoveredLineupId": null
  },
  "lineupUsernames": {},
  "user": {
    "username": "ppgogo",
    "info": {
      "isFetching": false
    },
    "infoFormErrors": {},
    "infoFormSaved": false,
    "emailPassFormErrors": {},
    "emailPassFormSaved": false,
    "cashBalance": {
      "isFetching": false
    },
    "notificationSettings": {
      "isFetchingEmail": false,
      "isUpdatingEmail": false,
      "email": [],
      "emailErrors": []
    }
  }
};
