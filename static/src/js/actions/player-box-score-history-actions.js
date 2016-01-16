import log from '../lib/logging'
import * as types from '../action-types.js'
import request from 'superagent'
// so we can use Promises
import 'babel-core/polyfill';
import {normalize, Schema, arrayOf} from 'normalizr'
const playerHistorySchema = new Schema('playerHistory', {
  idAttribute: 'player_id'
})



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
    type: types.FETCHING_PLAYER_BOX_SCORE_HISTORY
  };
}

function fetchPlayerBoxScoreHistorySuccess(body) {
  return {
    type: types.FETCH_PLAYER_BOX_SCORE_HISTORY_SUCCESS,
    sport: body.sport,
    playerHistory: body.playerHistory
  };
}

function fetchPlayerBoxScoreHistoryFail(ex) {
  log.error(ex)
  return {
    type: types.FETCH_PLAYER_BOX_SCORE_HISTORY_FAIL,
    ex
  };
}


// Do we need to fetch the specified player history items?
function shouldFetchPlayerBoxScoreHistory(state, sport) {
  const history = state.playerBoxScoreHistory

  if (history[sport] && Object.keys(history[sport]).length > 0) {
    // do we have any PlayerHistory for the sport in the store, if so, is it empty?
    return false
  } else if (history.isFetching) {
    // are we currently fetching it?
    return false
  } else {
    // Default to true.
    return true
  }
}


export function fetchPlayerBoxScoreHistoryIfNeeded(sport) {
  return (dispatch, getState) => {
    if (shouldFetchPlayerBoxScoreHistory(getState(), sport)) {
      return dispatch(fetchPlayerBoxScoreHistory(sport))
    } else {
      return Promise.resolve()
    }
  }
}


function fetchPlayerBoxScoreHistory(sport) {
  return dispatch => {
    // update the fetching state.
    dispatch(fetchingPlayerBoxScoreHistory())

    return new Promise((resolve, reject) => {
      request
      .get('/api/sports/player/history/' + sport + '/20/')
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        'Accept': 'application/json'
      })
      .end(function(err, res) {
        if(err) {
          dispatch(fetchPlayerBoxScoreHistoryFail(err));
          reject(err)
        } else {
          const normalizedPlayerHistory = normalize(
            res.body,
            arrayOf(playerHistorySchema)
          )

          dispatch(fetchPlayerBoxScoreHistorySuccess({
            sport: sport,
            playerHistory: normalizedPlayerHistory.entities.playerHistory
          }));

          resolve(res)
        }
      });
    });
  }
}
