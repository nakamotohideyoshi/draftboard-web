import ActionTypes from '../action-types';
import merge from 'lodash/merge';


const initialState = {
  entryResults: {},
  focusedEntryId: null,
};

module.exports = (state = initialState, action = {}) => {
  switch (action.type) {

    // Recieve the lineup results of a single day.
    case ActionTypes.RECEIVE_RESULTS: {
      return merge({}, state, {
        [action.response.when]: action.response.response,
      });
    }

    // Request the detailed results of an entry.
    case ActionTypes.ENTRY_RESULTS__REQUEST: {
      // set the requested entryId as the focused one.
      // This is used to tell the results pane which result to display.
      return merge({}, state, { focusedEntryId: action.entryId });
    }

    case ActionTypes.ENTRY_RESULTS__SUCCESS: {
      return merge({}, state, {
        entryResults: {
          [action.response.id]: action.response,
        },
      });
    }

    case ActionTypes.ENTRY_RESULTS__FAIL: {
      return state;
    }


    default:
      return state;
  }
};
