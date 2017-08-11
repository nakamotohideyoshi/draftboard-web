import ActionTypes from '../action-types';
import merge from 'lodash/merge';


const initialState = {
  contestResults: {},
  focusedContestId: null,
};

module.exports = (state = initialState, action = {}) => {
  switch (action.type) {

    // Recieve the lineup results of a single day.
    case ActionTypes.RECEIVE_RESULTS: {
      return merge({}, state, {
        [action.response.when]: action.response.response,
      });
    }

    // Request the detailed results of a contest.
    case ActionTypes.CONTEST_RESULTS__REQUEST: {
      // set the requested contestId as the focused one.
      // This is used to tell the results pane which result to display.
      return merge({}, state, { focusedContestId: action.contestId });
    }

    case ActionTypes.CONTEST_RESULTS__SUCCESS: {
      return merge({}, state, {
        contestResults: {
          [action.response.id]: action.response,
        },
      });
    }

    case ActionTypes.CONTEST_RESULTS__FAIL: {
      return state;
    }


    default:
      return state;
  }
};
