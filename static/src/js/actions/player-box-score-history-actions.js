import log from '../lib/logging';
import * as types from '../action-types.js';
import request from 'superagent';
import { dateNow } from '../lib/utils';
import { normalize, Schema, arrayOf } from 'normalizr';
const playerHistorySchema = new Schema('playerHistory', {
  idAttribute: 'player_id',
});


/**
 * Player history fetching actions.
 *
 * This gets the players REAL LIFE box score history for the past X number of games.
 * It's used in the draft section to populate the player detail pane stats.
 *
 * API endpoint used:
 * /api/sports/player/history/<sport>/<# of previous games>/
 *
 * The only exposed function is fetchPlayerBoxScoreHistoryIfNeeded(sport)
 */

function fetchingPlayerBoxScoreHistory() {
  return {
    type: types.FETCHING_PLAYER_BOX_SCORE_HISTORY,
  };
}

function fetchPlayerBoxScoreHistorySuccess(body) {
  return {
    type: types.FETCH_PLAYER_BOX_SCORE_HISTORY_SUCCESS,
    sport: body.sport,
    playerHistory: body.playerHistory,
    updatedAt: dateNow(),
  };
}

function fetchPlayerBoxScoreHistoryFail(ex) {
  log.error(ex);
  return {
    type: types.FETCH_PLAYER_BOX_SCORE_HISTORY_FAIL,
    ex,
  };
}


// Do we need to fetch the specified player history items?
function shouldFetchPlayerBoxScoreHistory(state, sport) {
  const history = state.playerBoxScoreHistory;

  // TODO Craig allow MLB once Caleb fixes API call
  if (sport === 'mlb') {
    return false;
  }

  if (history[sport] && Object.keys(history[sport]).length > 0) {
    // do we have any PlayerHistory for the sport in the store, if so, is it empty?
    return false;
  } else if (history.isFetching) {
    // are we currently fetching it?
    return false;
  }

  // Default to true.
  return true;
}


function removeExpiredHistory(body) {
  return {
    type: types.REMOVE_PLAYER_BOX_SCORE_HISTORY,
    sport: body.sport,
  };
}


function shouldRemoveExpiredHistory(state, sport) {
  const history = state.playerBoxScoreHistory;

  // don't remove if doesn't exist
  if (history.hasOwnProperty('updatedAt') === false || history.hasOwnProperty(sport) === false) {
    return false;
  }

  const expiration = dateNow() + 1000 * 60 * 60 * 24;  // add 1 day
  if (expiration < dateNow()) {
    return true;
  }

  return false;
}


function fetchPlayerBoxScoreHistory(sport) {
  return dispatch => {
    // update the fetching state.
    dispatch(fetchingPlayerBoxScoreHistory());

    return new Promise((resolve, reject) => {
      request
      .get(`/api/sports/player/history/${sport}/20/`)
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        Accept: 'application/json',
      })
      .end((err, res) => {
        if (err) {
          dispatch(fetchPlayerBoxScoreHistoryFail(err));
          reject(err);
        } else {
          const normalizedPlayerHistory = normalize(
            res.body,
            arrayOf(playerHistorySchema)
          );

          dispatch(fetchPlayerBoxScoreHistorySuccess({
            sport,
            playerHistory: normalizedPlayerHistory.entities.playerHistory,
          }));

          resolve(res);
        }
      });
    });
  };
}


export function fetchPlayerBoxScoreHistoryIfNeeded(sport) {
  return (dispatch, getState) => {
    if (shouldRemoveExpiredHistory(getState(), sport)) {
      dispatch(removeExpiredHistory(sport));
    }

    if (shouldFetchPlayerBoxScoreHistory(getState(), sport)) {
      return dispatch(fetchPlayerBoxScoreHistory(sport));
    }

    return Promise.resolve();
  };
}
