import * as ActionTypes from '../action-types.js';
import { merge as _merge } from 'lodash';

const initialState = {
  isFetching: false,
};


/**
 * Handle state mutations for player news entries.
 */
module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCHING_PLAYER_NEWS:
      return _merge({}, state, {
        isFetching: true,
      });


    case ActionTypes.FETCH_PLAYER_NEWS_FAIL:
      return _merge({}, state, {
        isFetching: false,
      });


    case ActionTypes.FETCH_PLAYER_NEWS_SUCCESS:
      const newState = _merge({}, state, {
        isFetching: false,
      });
      // Update the sport entry with the newly fetched data.
      newState[action.sport] = action.playerNews;

      return newState;


    default:
      return state;

  }
};
