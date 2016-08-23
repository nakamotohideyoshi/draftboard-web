import * as ActionTypes from '../action-types';
import log from '../lib/logging';
import map from 'lodash/map';
import merge from 'lodash/merge';
import request from 'superagent';
import zipObject from 'lodash/zipObject';
import { CALL_API } from '../middleware/api';
import { dateNow } from '../lib/utils';
import { normalize, Schema, arrayOf } from 'normalizr';
import { SPORT_CONST } from './sports';
const playerHistorySchema = new Schema('playerHistory', {
  idAttribute: 'id',
});

// get custom logger for actions
const logAction = log.getLogger('action');


const fetchSinglePlayerBoxScoreHistory = (sport, id) => ({
  [CALL_API]: {
    types: [
      ActionTypes.PLAYER_HISTORY_SINGLE__REQUEST,
      ActionTypes.PLAYER_HISTORY_SINGLE__RECEIVE,
      ActionTypes.ADD_MESSAGE,
    ],
    expiresAt: dateNow() + 1000 * 60 * 60 * 12,  // 12 hours, aka end of night
    endpoint: `/api/sports/player/history/${sport}/20/${id}/`,  // fetch the average history of last 20 games
    requestFields: { sport, id },
    callback: (json) => ({
      id,
      sport,
      fields: json[0],
    }),
  },
});

/**
 * Quick check to see if we should fetch the history of a player
 * Essentially, fetch if it doesn't exist
 * @param  {object} state Redux state
 * @param  {string} sport Sport to filter by
 * @param  {number} id    Django model ID for the player
 * @return {boolean}      True if we should fetch
 */
const shouldFetchSinglePlayerBoxScoreHistory = (state, sport, id) => !(id in state.playerBoxScoreHistory[sport]);


export const fetchSinglePlayerBoxScoreHistoryIfNeeded = (sport, id) => (dispatch, getState) => {
  logAction.debug('actions.fetchSinglePlayerBoxScoreHistoryIfNeeded', sport, id);

  if (shouldFetchSinglePlayerBoxScoreHistory(getState(), sport, id)) {
    return dispatch(fetchSinglePlayerBoxScoreHistory(sport, id));
  }

  return Promise.resolve();
};

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
    type: ActionTypes.FETCHING_PLAYER_BOX_SCORE_HISTORY,
  };
}

function fetchPlayerBoxScoreHistorySuccess(body) {
  return {
    type: ActionTypes.FETCH_PLAYER_BOX_SCORE_HISTORY_SUCCESS,
    sport: body.sport,
    playerHistory: body.playerHistory,
    updatedAt: dateNow(),
  };
}

function fetchPlayerBoxScoreHistoryFail(ex) {
  log.error(ex);
  return {
    type: ActionTypes.FETCH_PLAYER_BOX_SCORE_HISTORY_FAIL,
    ex,
  };
}


// Do we need to fetch the specified player history items?
function shouldFetchPlayerBoxScoreHistory(state, sport) {
  const history = state.playerBoxScoreHistory;

  // TODO Craig/Zach allow MLB once Caleb fixes API call
  if (sport === 'mlb') {
    log.warn('Not fetching MLB PlayerBoxScoreHistory.');
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
    type: ActionTypes.REMOVE_PLAYER_BOX_SCORE_HISTORY,
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
          const seasonStatTypes = SPORT_CONST[sport].seasonStats.types;
          // combine id with the season stats we need and that's it
          const onlyNeededFields = map(res.body, (player) => merge(
            {},
            {
              id: player.player_id,
            },
            zipObject(
              seasonStatTypes,
              map(seasonStatTypes, (type) => player[`avg_${type}`])
            )
          ));

          const normalizedPlayerHistory = normalize(
            onlyNeededFields,
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
