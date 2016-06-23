import merge from 'lodash/merge';

const ActionTypes = require('../action-types');
const initialState = {
  entries: {},
  isFetching: false,
};


/**
 * When a users enters a contest, they are actually entered into a contest pool.
 * Their entry will later be converted into a contest entry by the server.
 * This store holds their CONTEST POOL entries which are not guaranteed to ever
 * be contest entries.
 */
module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCHING_CONTEST_POOL_ENTRIES:
      return merge({}, state, {
        isFetching: true,
      });


    case ActionTypes.FETCH_CONTEST_POOL_ENTRIES_SUCCESS: {
      const newState = merge({}, state, {
        isFetching: false,
      });
      // replace old entries for the current ones.
      newState.entries = action.response;
      return newState;
    }


    case ActionTypes.FETCH_CONTEST_POOL_ENTRIES_FAIL:
      return merge({}, state, {
        isFetching: false,
      });


    default:
      return state;

  }
};
