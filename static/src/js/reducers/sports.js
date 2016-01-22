"use strict"

import update from 'react-addons-update'
import { map as _map, forEach as _forEach } from 'lodash'
const ActionTypes = require('../action-types')

// TODO remove this hardcode of nba
module.exports = function(state = {
  'nba': {
    isFetchingTeams: false,
    isFetchingGames: false
  }
}, action) {
  switch (action.type) {
    case ActionTypes.REQUEST_TEAMS:
      return update(state, {
        [action.sport]: {
          $merge: {
            isFetchingTeams: true
          }
        }
      })

    case ActionTypes.RECEIVE_TEAMS:
      return update(state, {
        [action.sport]: {
          $merge: {
            teams: action.teams,
            isFetchingTeams: false
          }
        }
      })

    case ActionTypes.REQUEST_GAMES:
      return update(state, {
        [action.sport]: {
          $merge: {
            isFetchingGames: true
          }
        }
      })

    case ActionTypes.RECEIVE_GAMES:
      return update(state, {
        [action.sport]: {
          $merge: {
            games: action.games,
            isFetchingGames: false,
            gamesUpdatedAt: action.gamesUpdatedAt
          }
        }
      })

    case ActionTypes.UPDATE_GAME:
      return update(state, {
        [action.sport]: {
          games: {
            [action.gameId]: {
              boxscore: {
                $merge: action.updatedGameFields
              }
            }
          }
        }
      })

    default:
      return state
  }
}
