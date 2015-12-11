"use strict"

import update from 'react-addons-update'
import { map as _map, forEach as _forEach } from 'lodash'
const ActionTypes = require('../action-types')


module.exports = function(state = {}, action) {
  switch (action.type) {
    case ActionTypes.REQUEST_TEAMS:
      var newProps = {
        sport: action.sport,
        isFetching: true
      }

      return update(state, {
        $set: {
          [action.sport]: newProps
        }
      })

    case ActionTypes.RECEIVE_TEAMS:
      return update(state, {
        [action.sport]: {
          $merge: {
            teams: action.teams,
            isFetching: false
          }
        }
      })

    default:
      return state
  }
}
