import _ from 'lodash'
import update from 'react-addons-update'
import * as ActionTypes from '../action-types'


module.exports = (state = {
  isFetching: false,
  hasRelatedInfo: false,
  items: [],
}, action) => {
  switch (action.type) {
    case ActionTypes.ADD_ENTRIES_PLAYERS:
      const newState = Object.assign({}, state)

      _.forEach(action.entriesPlayers, (roster, entryId) => {
        newState.items[entryId].roster = roster
      })

      return newState

    case ActionTypes.CONFIRM_RELATED_ENTRIES_INFO:
      return update(state, {
        $merge: {
          hasRelatedInfo: true,
        },
      })

    case ActionTypes.REQUEST_ENTRIES:
      return update(state, {
        $merge: {
          isFetching: true,
        },
      })

    case ActionTypes.RECEIVE_ENTRIES:
      return update(state, {
        $set: {
          isFetching: false,
          hasRelatedInfo: false,
          items: action.items,
          updatedAt: action.updatedAt,
        },
      })

    default:
      return state
  }
};
