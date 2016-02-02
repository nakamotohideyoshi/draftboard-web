import update from 'react-addons-update'
import * as ActionTypes from '../action-types'
import { forEach as _forEach } from 'lodash'


module.exports = function(state = {
  isFetching: false,
  hasRelatedInfo: false,
  items: []
}, action) {
  switch (action.type) {
    case ActionTypes.REQUEST_ENTRIES:
      return update(state, { $merge: {
        isFetching: true
      }})

    case ActionTypes.RECEIVE_ENTRIES:
      return update(state, { $set: {
        isFetching: false,
        hasRelatedInfo: false,
        items: action.items,
        updatedAt: action.receivedAt
      }})

    case ActionTypes.CONFIRM_RELATED_ENTRIES_INFO:
      return update(state, { $merge: {
        hasRelatedInfo: true
      }})

    case ActionTypes.ADD_ENTRIES_PLAYERS:
      let newState = Object.assign({}, state)

      _forEach(action.entriesPlayers, (roster, entryId) => {
        newState.items[entryId].roster = roster
      })

      return newState


    default:
      return state
  }
};
