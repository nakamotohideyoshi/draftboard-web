"use strict"

import update from 'react-addons-update'
import { map as _map, forEach as _forEach } from 'lodash'
const ActionTypes = require('../action-types')


module.exports = function(state = {}, action) {
  switch (action.type) {
    case ActionTypes.REQUEST_PRIZE:
      var newProps = {
        id: action.id,
        isFetching: true
      }

      return update(state, {
        $set: {
          [action.id]: newProps
        }
      })

    case ActionTypes.RECEIVE_PRIZE:
      return update(state, {
        [action.id]: {
          $merge: {
            info: action.info,
            isFetching: false
          }
        }
      })

    default:
      return state
  }
}
