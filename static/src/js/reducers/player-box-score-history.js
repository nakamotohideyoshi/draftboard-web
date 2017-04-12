import * as ActionTypes from '../action-types.js';
import merge from 'lodash/merge';

const initialState = {
  isFetching: false,
  nba: {},
  mlb: {},
  nfl: {},
  nhl: {},
};

/**
 * Handle state mutations for player boxscore histories.
 *
 * These actions live in - player-history-actions.js
 */
module.exports = (state = initialState, action = {}) => {
  switch (action.type) {

    case ActionTypes.PLAYER_HISTORY_SINGLE__RECEIVE: {
      const { id, sport, fields } = action.response;

      return merge({}, state, {
        [sport]: {
          [id]: fields,
        },
      });
    }

    default:
      return state;
  }
};
