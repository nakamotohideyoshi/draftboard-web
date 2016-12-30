import * as actionTypes from '../action-types.js';
import request from 'superagent';
import { CALL_API } from '../middleware/api';
import { normalize, Schema, arrayOf } from 'normalizr';


/**
 * Upcoming draft groups is not a full draft group with players and everything,
 * it's just a bunch of info about the upcoming draft groups, it's used to create
 * the draft group selection modal in the lobby.
 */


const draftGroupInfoSchema = new Schema('draftGroups', {
  idAttribute: 'pk',
});


function fetchSuccess(body) {
  return {
    type: actionTypes.FETCH_UPCOMING_DRAFTGROUPS_INFO_SUCCESS,
    body,
  };
}


function fetchFail(ex) {
  return {
    type: actionTypes.FETCH_UPCOMING_DRAFTGROUPS_INFO_FAIL,
    ex,
  };
}


export function fetchUpcomingDraftGroupsInfo() {
  return (dispatch) => {
    request.get('/api/draft-group/upcoming/')
      .set({ 'X-REQUESTED-WITH': 'XMLHttpRequest' })
      .set('Accept', 'application/json')
      .end((err, res) => {
        if (err) {
          return dispatch(fetchFail(err));
        }

        // Normalize player list by ID.
        const normalizedDraftGroupInfo = normalize(
          res.body,
          arrayOf(draftGroupInfoSchema)
        );

        return dispatch(fetchSuccess({
          draftGroups: normalizedDraftGroupInfo.entities.draftGroups,
        }));
      }
    );
  };
}

// Open the draft group selection modal in the lobby.
export function openDraftGroupSelectionModal() {
  return {
    type: actionTypes.OPEN_DRAFT_GROUP_SELECTION_MODAL,
  };
}

// Close the draft group selection modal in the lobby.
export function closeDraftGroupSelectionModal() {
  return {
    type: actionTypes.CLOSE_DRAFT_GROUP_SELECTION_MODAL,
  };
}


/**
 * In the draft section, set the id of the draft group that is being drafted (the one in the URL)
 */
export function setActiveDraftGroupId(draftGroupId) {
  return {
    type: actionTypes.SET_ACTIVE_DRAFT_GROUP_ID,
    draftGroupId,
  };
}


/**
 * Draft Group Box Score fetching Actions.
 * /api/draft-group/boxscores/${draftGroupId}/
 */
export const fetchDraftGroupBoxScores = (draftGroupId) => (dispatch) => {
  const apiActionResponse = dispatch({
    [CALL_API]: {
      types: [
        actionTypes.FETCHING_DRAFTGROUP_BOX_SCORES,
        actionTypes.FETCH_DRAFTGROUP_BOX_SCORES_SUCCESS,
        actionTypes.ADD_MESSAGE,
      ],
      endpoint: `/api/draft-group/boxscores/${draftGroupId}/`,
      callback: (json) => ({
        draftGroupId,
        boxScores: json,
      }),
    },
  });

  return apiActionResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    if (action.error) {
      return dispatch({
        type: actionTypes.FETCH_DRAFTGROUP_BOX_SCORES_FAIL,
        response: action.error,
      });
    }

    return action;
  });
};


function shouldFetchDraftGroupBoxScores(state, draftGroupId) {
  const boxScores = state.upcomingDraftGroups.boxScores;

  if (boxScores.hasOwnProperty(draftGroupId)) {
    // If we have the boxscores, don't re-fetch
    return false;
  } else if (boxScores.isFetching) {
    // are we currently fetching it?
    return false;
  }

  // Default to true.
  return true;
}


export function fetchDraftGroupBoxScoresIfNeeded(draftGroupId) {
  return (dispatch, getState) => {
    if (shouldFetchDraftGroupBoxScores(getState(), draftGroupId)) {
      return dispatch(fetchDraftGroupBoxScores(draftGroupId));
    }

    return Promise.resolve();
  };
}
