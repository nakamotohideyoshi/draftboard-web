import * as actionTypes from '../action-types.js';
import { CALL_API } from '../middleware/api';
// import { normalize, Schema, arrayOf } from 'normalizr';
import log from '../lib/logging.js';


const fetchUpcomingDraftGroupUpdates = (draftGroupId) => (dispatch) => {
  const apiActionResponse = dispatch({
    [CALL_API]: {
      types: [
        actionTypes.DRAFTGROUP_UPDATES__FETCHING,
        actionTypes.DRAFTGROUP_UPDATES__FETCH_SUCCESS,
        actionTypes.ADD_MESSAGE,
      ],
      endpoint: `/api/draft-group/game-updates/${draftGroupId}/`,
      callback: (json) => ({
        draftGroupId,
        updates: json,
      }),
    },
  });

  apiActionResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    if (action.error) {
      dispatch({
        type: actionTypes.DRAFTGROUP_UPDATES__FETCH_FAIL,
        response: action.error,
      });
    }
  });

  // Return the promise chain in case we want to use it elsewhere.
  return apiActionResponse;
};


function shouldFetchUpcomingDraftGroupUpdates(state, draftGroupId) {
  if (state.UpcomingDraftGroupUpdates && state.UpcomingDraftGroupUpdates[draftGroupId]) {
    return !state.UpcomingDraftGroupUpdates[draftGroupId].isFetching;
  }

  return true;
}


export function fetchUpcomingDraftGroupUpdatesIfNeeded(draftGroupId) {
  return (dispatch, getState) => {
    if (!draftGroupId) {
      log.warn('Not fetching DraftGroupGameUpdates, no draftGroupId was supplied.');
      return Promise.reject();
    }

    if (shouldFetchUpcomingDraftGroupUpdates(getState(), draftGroupId)) {
      return dispatch(fetchUpcomingDraftGroupUpdates(draftGroupId));
    }

    log.info('shouldFetchUpcomingDraftGroupUpdates == false');
  };
}
