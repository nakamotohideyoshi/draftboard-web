"use strict";

import update from 'react-addons-update'
import { map as _map, forEach as _forEach } from 'lodash'

import ActionTypes from '../action-types'


module.exports = function(state = {}, action) {
  switch (action.type) {
    case ActionTypes.REQUEST_LINEUP_USERNAMES:
      return update(state, {
        [action.contestId]: {
          $set: {
            isFetching: true,
            lineups: []
          }
        }
      })

    case ActionTypes.RECEIVE_LINEUP_USERNAMES:
      return update(state, {
        [action.contestId]: {
          $set: {
            isFetching: true,
            lineups: action.lineups
          }
        }
      })

  default:
    return state
  }
}
