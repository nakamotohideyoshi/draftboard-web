import * as ActionTypes from '../action-types.js';
import merge from 'lodash/merge';

const initialState = {
  isFetching: false,
  nba: {},
  mlb: {},
};

/**
 * Handle state mutations for player boxscore histories.
 *
 * These actions live in - player-history-actions.js
 */
module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCHING_PLAYER_BOX_SCORE_HISTORY:
      return merge({}, state, {
        isFetching: true,
      });


    case ActionTypes.FETCH_PLAYER_BOX_SCORE_HISTORY_FAIL:
      return merge({}, state, {
        isFetching: false,
      });


    case ActionTypes.REMOVE_PLAYER_BOX_SCORE_HISTORY: {
      const newState = merge({}, state);

      delete newState.updatedAt;
      delete newState[action.sport];

      return newState;
    }


    case ActionTypes.FETCH_PLAYER_BOX_SCORE_HISTORY_SUCCESS: {
      const newState = merge({}, state, {
        isFetching: false,
        updatedAt: action.updatedAt,
      });
      // Update the sport entry with the newly fetched data.
      newState[action.sport] = action.playerHistory;

      return newState;
    }


    default:
      return state;

  }
};
