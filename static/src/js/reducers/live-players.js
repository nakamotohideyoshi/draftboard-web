"use strict";

import update from 'react-addons-update'
const ActionTypes = require('../action-types');


module.exports = function(state = {
  isFetching: [],
  relevantPlayers: {},
  fetched: []
}, action) {
  switch (action.type) {
    case ActionTypes.REQUEST_LIVE_PLAYERS_STATS:
      return update(state, {
        isFetching: {
          $push: [action.lineupId]
        }
      })

    case ActionTypes.RECEIVE_LIVE_PLAYERS_STATS:
      let newState = update(state, {
        // add in players
        relevantPlayers: {
          $merge: action.players
        },
        // add to fetched list
        fetched: {
          $push: [action.lineupId]
        }
      })

      newState.isFetching = newState.isFetching.filter(item => item !== action.lineupId)

      return newState

    default:
      return state
  }
};
