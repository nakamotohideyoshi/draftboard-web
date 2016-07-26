import merge from 'lodash/merge';
import remove from 'lodash/remove';
import * as actionTypes from '../action-types.js';


const initialState = {
  entryRequests: [],
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

    case actionTypes.FETCHING_CONTEST_POOL_ENTRIES:
      return merge({}, state, {
        isFetching: true,
      });


    case actionTypes.FETCH_CONTEST_POOL_ENTRIES_SUCCESS: {
      const newState = merge({}, state, {
        isFetching: false,
      });

      // replace old entries for the current ones.
      newState.entries = action.response;
      return newState;
    }


    case actionTypes.FETCH_CONTEST_POOL_ENTRIES_FAIL:
      return merge({}, state, {
        isFetching: false,
      });


    case actionTypes.REMOVING_CONTEST_POOL_ENTRY:
      if (state.entries[action.entry.id]) {
        return merge({}, state, {
          entries: {
            [action.entry.id]: {
              isRemoving: true,
            },
          },
        });
      }

      return state;


    // case actionTypes.REMOVING_CONTEST_POOL_ENTRY_SUCCESS:
    //   return state;


    case actionTypes.REMOVING_CONTEST_POOL_ENTRY_FAIL:
      if (state.entries[action.entry.id]) {
        return merge({}, state, {
          entries: {
            [action.entry.id]: {
              isRemoving: false,
            },
          },
        });
      }

      return state;


    case actionTypes.ENTERING_CONTEST_POOL:
      return merge({}, state, {
        entryRequests: [{
          contestPoolId: action.contestPoolId,
          lineupId: action.lineupId,
        }],
      });

    case actionTypes.ENTERING_CONTEST_POOL_FAIL:
    case actionTypes.ENTERING_CONTEST_POOL_SUCCESS: {
      const newState = merge({}, state);

      // remove the entryRequest for this lineup & contest.
      newState.entryRequests = remove(newState.entryRequest, (request) =>
        request.contestPoolId === action.contestPoolId && request.lineupId === action.lineupId
      );
      return newState;
    }


    default:
      return state;

  }
};
