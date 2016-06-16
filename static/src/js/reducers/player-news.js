import * as ActionTypes from '../action-types.js';
import merge from 'lodash/merge';

const initialState = {
  isFetching: false,
};


/**
 * Handle state mutations for player news entries.
 */
module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCHING_PLAYER_NEWS:
      return merge({}, state, {
        isFetching: true,
      });


    case ActionTypes.FETCH_PLAYER_NEWS_FAIL:
      return merge({}, state, {
        isFetching: false,
      });


    case ActionTypes.FETCH_PLAYER_NEWS_SUCCESS: {
      const newState = merge({}, state, {
        isFetching: false,
      });
      // Update the sport entry with the newly fetched data.
      newState[action.sport] = action.playerNews;

      return newState;
    }


    default:
      return state;

  }
};
