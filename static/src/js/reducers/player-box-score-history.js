import * as ActionTypes from '../action-types.js';
import { merge as _merge } from 'lodash';

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
      return _merge({}, state, {
        isFetching: true,
      });


    case ActionTypes.FETCH_PLAYER_BOX_SCORE_HISTORY_FAIL:
      return _merge({}, state, {
        isFetching: false,
      });


    case ActionTypes.REMOVE_PLAYER_BOX_SCORE_HISTORY:
      let newState = _merge({}, state);

      delete newState.updatedAt;
      delete newState[action.sport];

      return newState;


    case ActionTypes.FETCH_PLAYER_BOX_SCORE_HISTORY_SUCCESS:
      newState = _merge({}, state, {
        isFetching: false,
        updatedAt: action.updatedAt,
      });
      // Update the sport entry with the newly fetched data.
      newState[action.sport] = action.playerHistory;

      return newState;


    default:
      return state;

  }
};
