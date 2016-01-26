import * as ActionTypes from '../action-types.js'
import {merge as _merge} from 'lodash'

const initialState = {}


/**
 * When a user requests to enter their lineup into a contest, a background job is queued up on the
 * server. We then ping the server
 */
module.exports = function(state = initialState, action) {
  let newState = Object.assign({}, state)

  switch (action.type) {

    case ActionTypes.ADD_ENTRY_REQUEST_MONITOR:
      newState[action.taskId] = {
        status: 'task pending',
        contestId: action.contestId,
        lineupId: action.lineupId
      }
      return newState


    case ActionTypes.FETCHING_ENTRY_REQUEST_STATUS:
      newState[action.taskId] = {
        status: 'fetching'
      }

      return  _merge(state, newState)


    case ActionTypes.ENTRY_REQUEST_RECIEVED:
      newState[action.taskId] = {
        status: action.status
      }

      return  _merge(state, newState)


    default:
      return state
  }
}
