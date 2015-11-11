import update from 'react-addons-update'
const ActionTypes = require('../action-types');


module.exports = function(state = {
  isFetching: false,
  items: []
}, action) {
  switch (action.type) {
    case ActionTypes.REQUEST_ENTRIES:
      return update(state, { $set: {
        isFetching: true
      }})

    case ActionTypes.RECEIVE_POSTS:
      return update(state, { $set: {
        isFetching: false,
        items: action.items,
        lastUpdated: action.receivedAt
      }})

    default:
      return state
  }
};
