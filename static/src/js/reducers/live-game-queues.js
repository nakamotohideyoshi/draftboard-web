"use strict";

import update from 'react-addons-update'
const ActionTypes = require('../action-types');
import log from '../lib/logging'


// shortcut method to $set new state if the key doesn't exist, otherwise $merges the properties in to existing
function setOrPush(state, action) {
  // if does not exist, then $set to create
  if (action.gameId in state === false) {
    return update(state, {
      $set: {
        [action.gameId]: {
          isRunning: false,
          queue: [action.event]
        }
      }
    })
  }

  // otherwise merge
  return update(state, {
    [action.gameId]: {
      queue: {
        $push: action.event
      }
    }
  })
}


module.exports = function(state = {
}, action) {
  switch (action.type) {
    case ActionTypes.ADD_LIVE_GAME_QUEUES_EVENT:
      log.debug('reducersLiveGameQueues.ADD_LIVE_GAME_QUEUES_EVENT')

      return setOrPush(state, action)

    case ActionTypes.REMOVE_OLDEST_LIVE_GAME_QUEUES_EVENT:
      log.debug('reducersLiveGameQueues.REMOVE_OLDEST_LIVE_GAME_QUEUES_EVENT')

      if (state[action.gameId].length > 1) {
        return update(state, {
          [action.gameId]: {
            [action.gameId]: {
              queue: {
                $splice: [0, 1]
              }
            }
          }
        })
      }
      return state

    default:
      return state
  }
};
