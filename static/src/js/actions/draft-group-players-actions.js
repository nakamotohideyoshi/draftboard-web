import log from '../lib/logging';
import * as types from '../action-types.js';
import request from 'superagent';
// so we can use Promise

import { normalize, Schema, arrayOf } from 'normalizr';
import { fetchSportInjuries } from './injury-actions.js';
import { fetchFantasyHistory } from './fantasy-history-actions.js';
import { fetchTeamsIfNeeded } from './sports.js';
import { fetchPlayerNewsIfNeeded } from './player-news-actions.js';
import { fetchPlayerBoxScoreHistoryIfNeeded } from './player-box-score-history-actions.js';

const playerSchema = new Schema('players', {
  idAttribute: 'player_id',
});


// Player filter actions.
//
// These control the filter + sorting of the player list in the draft section.
export function updateFilter(filterName, filterProperty, match) {
  return {
    type: types.DRAFTGROUP_FILTER_CHANGED,
    filter: {
      filterName,
      filterProperty,
      match,
    },
  };
}

export function updateOrderByFilter(property, direction = 'desc') {
  return {
    type: types.DRAFTGROUP_ORDER_CHANGED,
    orderBy: {
      property,
      direction,
    },
  };
}

export function setFocusedPlayer(playerId) {
  return (dispatch) => {
    dispatch({
      type: types.SET_FOCUSED_PLAYER,
      playerId,
    });
  };
}


/**
 * Draft Group fetching actions
 * /api/draft-group/draftGroupId
 */
function fetchingDraftgroup() {
  return {
    type: types.FETCHING_DRAFT_GROUPS,
  };
}

function fetchDraftgroupSuccess(body) {
  return {
    type: types.FETCH_DRAFTGROUP_SUCCESS,
    body,
  };
}

function fetchDraftgroupFail(ex) {
  log.error(ex);
  return {
    type: types.FETCH_DRAFTGROUP_FAIL,
    ex,
  };
}


// Do we need to fetch the specified draft group?
function shouldFetchDraftGroup(state, draftGroupId) {
  const draftGroup = state.draftGroupPlayers;

  if (!draftGroup.id || draftGroupId !== draftGroup.id) {
    // do we have a draftgroup AND the right draftgroup in the store?
    return true;
  } else if (draftGroup.isFetching) {
    // are we currently fetching it?
    return false;
  }

  // Default to true.
  return true;
}


function fetchDraftGroup(draftGroupId) {
  return dispatch => {
    // update the fetching state.
    dispatch(fetchingDraftgroup());

    const promise = new Promise((resolve, reject) => {
      request
      .get(`/api/draft-group/${draftGroupId}/`)
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        Accept: 'application/json',
      })
      .end((err, res) => {
        if (err) {
          dispatch(fetchDraftgroupFail(err));
          reject(err);
        } else {
          // Now that we know which sport we're dealing with, fetch the injuries + fp history for
          // these players.
          dispatch(fetchFantasyHistory(res.body.sport));
          dispatch(fetchSportInjuries(res.body.sport));
          dispatch(fetchTeamsIfNeeded(res.body.sport));
          dispatch(fetchPlayerNewsIfNeeded(res.body.sport));
          dispatch(fetchPlayerBoxScoreHistoryIfNeeded(res.body.sport));

          // Normalize player list by ID.
          const normalizedPlayers = normalize(
            res.body.players,
            arrayOf(playerSchema)
          );

          dispatch(fetchDraftgroupSuccess({
            players: normalizedPlayers.entities.players,
            start: res.body.start,
            end: res.body.end,
            sport: res.body.sport,
            id: res.body.pk,
          }));

          resolve(res);
        }
      });

      return promise;
    });
  };
}

export function fetchDraftGroupIfNeeded(draftGroupId) {
  return (dispatch, getState) => {
    if (shouldFetchDraftGroup(getState(), draftGroupId)) {
      return dispatch(fetchDraftGroup(draftGroupId));
    }

    return Promise.resolve();
  };
}
