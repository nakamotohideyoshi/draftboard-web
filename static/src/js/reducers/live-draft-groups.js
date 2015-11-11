"use strict"

import update from 'react-addons-update'
import { map as _map, forEach as _forEach } from 'lodash'
const ActionTypes = require('../action-types')


// update initialState to be a function to get from localStorage if it exists
module.exports = (state = {}, action) => {
  switch (action.type) {
    // note that the way this is written, it will overwrite the draft group
    case ActionTypes.REQUEST_LIVE_DRAFT_GROUP_INFO:
      return update(state, { $merge: {
        [action.id]: {
          id: action.id,
          isFetchingInfo: true,
          isFetchingFP: false
        }
      }})

    case ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_INFO:
      return update(state, {
        [action.id]: {
          $merge: {
            players: action.players,
            expiresAt: action.expiresAt,
            isFetchingInfo: false
          }
        }
      })

    case ActionTypes.REQUEST_LIVE_DRAFT_GROUP_FP:
      return update(state, {
        [action.id]: {
          $merge: {
            isFetchingFP: true
          }
        }
      })

    case ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_FP:
      var newState = Object.assign({}, state)
      var draftGroup = newState[action.id]

      _forEach(draftGroup.players, (player, id) => {
        if (id in action.playersFP === false) {
          return
        }

        var playerFP = action.playersFP[id]

        player['fp'] = playerFP.fp
        player['fpLastUpdated'] = Date.now()
      })

      return newState

    default:
      return state
  }
}
