import merge from 'lodash/merge';
import * as ActionTypes from '../action-types.js';


const initialState = {
  sport: null,
  id: null,
  isFetching: false,
  allPlayers: {},
};


/**
 * Reducer for the players of a single draft group - used in the draft section.
 */
module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCHING_DRAFT_GROUPS:
      return merge({}, state, {
        isFetching: true,
      });


    case ActionTypes.FETCH_DRAFTGROUP_FAIL:
      return merge({}, state, {
        isFetching: false,
      });


    case ActionTypes.FETCH_DRAFTGROUP_SUCCESS:
      // Return a copy of the previous state with our new things added to it.
      return merge({}, state, {
        sport: action.response.sport,
        allPlayers: action.response.players,
        id: action.response.id,
        start: action.response.start,
        end: action.response.end,
        isFetching: false,
      });


    default:
      return state;
  }
};
