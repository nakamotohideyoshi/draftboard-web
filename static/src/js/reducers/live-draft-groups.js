import update from 'react-addons-update'
import { map as _map, forEach as _forEach } from 'lodash'

import * as ActionTypes from '../action-types'
import log from '../lib/logging'


// shortcut method to $set new state if the key doesn't exist, otherwise $merges the properties in to existing
function setOrMerge(state, action, props) {
  // if does not exist, then $set to create
  if (action.id in state === false) {
    var proprops = Object.assign({}, proprops, {
      playersInfo: {},
      playersStats: {},
      boxScores: {}
    })

    return update(state, {
      $set: {
        [action.id]: proprops
      }
    })
  }

  // otherwise merge
  return update(state, {
    [action.id]: {
      $merge: props
    }
  })
}


// update initialState to be a function to get from localStorage if it exists
module.exports = (state = {}, action) => {
  let newProps = {};

  switch (action.type) {
    case ActionTypes.UPDATE_LIVE_DRAFT_GROUP_PLAYER_FP:
      log.debug('reducersLiveDraftGroup.UPDATE_LIVE_DRAFT_GROUP_PLAYER_FP')

      return update(state, {
        [action.id]: {
          playersStats: {
            [action.playerId]: {
              $set: {
                fp: action.fp
              }
            }
          }
        }
      })


    case ActionTypes.REQUEST_LIVE_DRAFT_GROUP_INFO:
      log.debug('reducersLiveDraftGroup.REQUEST_LIVE_DRAFT_GROUP_INFO')

      newProps = {
        id: action.id,
        isFetchingInfo: true,
        hasAllInfo: false
      }

      return setOrMerge(state, action, newProps)


    case ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_INFO:
      log.debug('reducersLiveDraftGroup.RECEIVE_LIVE_DRAFT_GROUP_INFO')

      return update(state, {
        [action.id]: {
          $merge: {
            isFetchingInfo: false,
            expiresAt: action.expiresAt,
            playersInfo: action.players,
            start: action.start,
            end: action.end,
            sport: action.sport
          }
        }
      })


    case ActionTypes.REQUEST_LIVE_DRAFT_GROUP_FP:
      log.debug('reducersLiveDraftGroup.REQUEST_LIVE_DRAFT_GROUP_FP')

      newProps = {
        id: action.id,
        isFetchingFP: true
      }

      return setOrMerge(state, action, newProps)


    case ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_FP:
      log.debug('reducersLiveDraftGroup.RECEIVE_LIVE_DRAFT_GROUP_FP')

      return update(state, {
        [action.id]: {
          $merge: {
            isFetchingFP: false,
            fpUpdatedAt: action.updatedAt,
            playersStats: action.players
          }
        }
      })


    case ActionTypes.REQUEST_LIVE_DRAFT_GROUP_BOX_SCORES:
      log.debug('reducersLiveDraftGroup.REQUEST_LIVE_DRAFT_GROUP_BOX_SCORES')

      newProps = {
        id: action.id,
        isFetchingBoxScores: true
      }

      return setOrMerge(state, action, newProps)


    case ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_BOX_SCORES:
      log.debug('reducersLiveDraftGroup.RECEIVE_LIVE_DRAFT_GROUP_BOX_SCORES')

      return update(state, {
        [action.id]: {
          $merge: {
            isFetchingBoxScores: true,
            boxScoresUpdatedAt: action.updatedAt,
            boxScores: action.boxScores
          }
        }
      })


    case ActionTypes.CONFIRM_LIVE_DRAFT_GROUP_STORED:
      log.debug('reducersLiveDraftGroup.RECEIVE_LIVE_DRAFT_GROUP_BOX_SCORES')

      return update(state, {
        [action.id]: {
          $merge: {
            hasAllInfo: true
          }
        }
      })


    default:
      return state
  }
}
