import update from 'react-addons-update'
import * as ActionTypes from '../action-types'


// update initialState to be a function to get from localStorage if it exists
module.exports = (state = {
  items: [],
}, action) => {
  switch (action.type) {
    case ActionTypes.RECEIVE_CURRENT_DRAFT_GROUPS:
      return update(state, {
        $set: {
          isFetching: false,
          items: action.draftGroups,
          updatedAt: action.updatedAt,
        },
      })

    case ActionTypes.REQUEST_CURRENT_DRAFT_GROUPS:
      return update(state, {
        $set: {
          isFetching: true,
        },
      })

    default:
      return state
  }
}
