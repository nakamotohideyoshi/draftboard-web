"use strict";

import update from 'react-addons-update'
const ActionTypes = require('../action-types');


module.exports = function(state = {
  isFetching: false,
  items: {}
}, action) {
  switch (action.type) {
    case ActionTypes.SET_CURRENT_LINEUPS:
      console.info('SET_CURRENT_LINEUPS', action)
      return update(state, { $set: {
        updatedAt: action.updatedAt,
        items: action.lineups
      }})

    default:
      return state
  }
};
