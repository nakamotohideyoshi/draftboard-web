import merge from 'lodash/merge';
import * as actionTypes from '../action-types.js';


const initialState = {
  isFetching: false,
  draftGroups: {},
};


/**
 * Reducer for the players of a single draft group - used in the draft section.
 */
module.exports = (state = initialState, action) => {
  switch (action.type) {

    case actionTypes.DRAFTGROUP_UPDATES__FETCHING:
      return merge({}, state, {
        isFetching: true,
      });


    case actionTypes.DRAFTGROUP_UPDATES__FETCH_FAIL:
      return merge({}, state, {
        isFetching: false,
      });


    case actionTypes.DRAFTGROUP_UPDATES__FETCH_SUCCESS:
      // Return a copy of the previous state with our new things added to it.
      return merge({}, state, {
        isFetching: false,
        draftGroups: {
          [action.response.draftGroupId]: {
            // An array containing the values (player.srid) of probably pitchers.
            probablePitchers: action.response.updates.filter((update) => update.type === 'pp').map((pp) => pp.value),
          },
        },
      });


    default:
      return state;
  }
};
