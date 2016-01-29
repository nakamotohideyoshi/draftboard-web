import update from 'react-addons-update'

import * as ActionTypes from '../action-types'
import log from '../lib/logging'


// update initialState to be a function to get from localStorage if it exists
module.exports = (state = {
  items: [],
}, action) => {
  switch (action.type) {
    case ActionTypes.REQUEST_CURRENT_DRAFT_GROUPS:
      log.trace('reducersCurrentDraftGroup.REQUEST_CURRENT_DRAFT_GROUPS')

      return update(state, {
        $set: {
          isFetching: true,
        },
      })


    case ActionTypes.RECEIVE_CURRENT_DRAFT_GROUPS:
      log.trace('reducersCurrentDraftGroup.RECEIVE_CURRENT_LIVE_DRAFT_GROUPS')

      return update(state, {
        $set: {
          isFetching: false,
          items: action.draftGroups,
          updatedAt: action.updatedAt,
        },
      })


    default:
      return state
  }
}
