import * as types from '../action-types.js';
import request from 'superagent';
import { normalize, Schema, arrayOf } from 'normalizr';
import log from '../lib/logging.js';


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
    type: types.FETCH_UPCOMING_DRAFTGROUPS_INFO_SUCCESS,
    body,
  };
}


function fetchFail(ex) {
  return {
    type: types.FETCH_UPCOMING_DRAFTGROUPS_INFO_FAIL,
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
    type: types.OPEN_DRAFT_GROUP_SELECTION_MODAL,
  };
}

// Close the draft group selection modal in the lobby.
export function closeDraftGroupSelectionModal() {
  return {
    type: types.CLOSE_DRAFT_GROUP_SELECTION_MODAL,
  };
}


/**
 * Draft Group Box Score fetching Actions.
 * /api/draft-group/boxscores/${draftGroupId}/
 */

function fetchingDraftGroupBoxScores() {
  return {
    type: types.FETCHING_DRAFTGROUP_BOX_SCORES,
  };
}

function fetchDraftGroupBoxScoresSuccess(draftGroupId, body) {
  return {
    type: types.FETCH_DRAFTGROUP_BOX_SCORES_SUCCESS,
    body,
    draftGroupId,
  };
}

function fetchDraftGroupBoxScoresFail(draftGroupId, body) {
  log.error(body);
  return {
    type: types.FETCH_DRAFTGROUP_BOX_SCORES_FAIL,
  };
}


/**
 * In the draft section, set the id of the draft group that is being drafted (the one in the URL)
 */
export function setActiveDraftGroupId(draftGroupId) {
  return {
    type: types.SET_ACTIVE_DRAFT_GROUP_ID,
    draftGroupId,
  };
}


function fetchDraftGroupBoxScores(draftGroupId) {
  return dispatch => {
    dispatch(fetchingDraftGroupBoxScores());

    return new Promise((resolve, reject) => {
      request
      .get(`/api/draft-group/boxscores/${draftGroupId}/`)
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        Accept: 'application/json',
      })
      .end((err, res) => {
        if (err) {
          reject(err);
          dispatch(fetchDraftGroupBoxScoresFail(draftGroupId, res.body));
        } else {
          resolve(res.body);
          dispatch(fetchDraftGroupBoxScoresSuccess(draftGroupId, res.body));
        }
      });
    });
  };
}


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
