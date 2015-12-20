"use strict"

import * as ActionTypes from '../action-types'
import log from '../lib/logging'
import _ from 'lodash'


export function addEvent(gameId, event) {
  log.debug('actionsLiveGameQueues.addEvent')

  return {
    type: ActionTypes.ADD_LIVE_GAME_QUEUES_EVENT,
    gameId: gameId,
    event: event
  }
}


export function removeOldestEvent(gameId) {
  log.debug('actionsLiveGameQueues.removeOldestEvent')

  return {
    type: ActionTypes.REMOVE_OLDEST_LIVE_GAME_QUEUES_EVENT,
    gameId: gameId
  }
}
