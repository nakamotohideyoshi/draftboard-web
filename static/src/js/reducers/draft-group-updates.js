import merge from 'lodash/merge';
import * as actionTypes from '../action-types.js';


const initialState = {
  // separate fetching states for each sport.
  isFetching: { nba: false, mlb: false, nfl: false, nhl: false },
  // stuff responses in here, separated by sport.
  sports: {
    nba: {},
    mlb: {},
    nfl: {},
    nhl: {},
  },
};


/**
 * Reducer for drafgroup updates. this includes player injury status, player news status, starting
 * pitchers, etc.
 */
module.exports = (state = initialState, action = {}) => {
  switch (action.type) {

    case actionTypes.DRAFT_GROUP_UPDATES__FETCHING: {
      return merge({}, state, {
        isFetching: {
          [action.sport]: true,
        },
      });
    }


    case actionTypes.DRAFT_GROUP_UPDATES__FETCH_FAIL: {
      return merge({}, state, {
        isFetching: {
          [action.sport]: false,
        },
      });
    }


    case actionTypes.DRAFT_GROUP_UPDATES__FETCH_SUCCESS: {
      // Return a copy of the previous state with our new things added to it.
      const newState = merge({}, state);

      newState.isFetching[action.response.sport] = false;
      newState.sports[action.response.sport] = {
        playerUpdates: action.response.updates.playerUpdates,
        gameUpdates: action.response.updates.gameUpdates,
        // An array containing the values (player.srid) of probable pitchers.
        probablePitchers: action.response.updates.probablePitchers,
      };

      return newState;
    }


    default:
      return state;
  }
};
