// when the page initial loads
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
    "isFetching": false,
    "items": {}
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
    "expiresAt": 1458243900898,
    "items": []
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
  "liveContests": {},
  "liveDraftGroups": {},
  "eventsMultipart": {
    "events": {},
    "watchablePlayers": []
  },
  "livePlayers": {
    "isFetching": [],
    "relevantPlayers": {},
    "fetched": [],
    "expiresAt": 1458243900898
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
    "nba": {},
    "mlb": {}
  },
  "prizes": {},
  "events": {
    "animationEvents": {},
    "gamesQueue": {},
    "playerEventDescriptions": {},
    "playerHistories": {},
    "playersPlaying": []
  },
  "results": {},
  "routing": {
    "locationBeforeTransitions": null
  },
  "sports": {
    "games": {},
    "types": [
      "nba",
      "nhl",
      "mlb"
    ],
    "nba": {
      "gameIds": [],
      "isFetchingTeams": true,
      "isFetchingGames": false,
      "gamesExpireAt": 1458243900898,
      "teamsExpireAt": 1458243961258
    },
    "nhl": {
      "gameIds": [],
      "isFetchingTeams": false,
      "isFetchingGames": false,
      "gamesExpireAt": 1458243900898,
      "teamsExpireAt": 1458243900898
    },
    "mlb": {
      "gameIds": [],
      "isFetchingTeams": false,
      "isFetchingGames": false,
      "gamesExpireAt": 1458243900898,
      "teamsExpireAt": 1458243900899
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
      "contestTypeFilter": {},
      "contestFeeFilter": {
        "match": {
          "minVal": 0,
          "maxVal": null
        }
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
  },
  "watching": {
    "myLineupId": null,
    "sport": null,
    "contestId": null,
    "opponentLineupId": null
  }
};