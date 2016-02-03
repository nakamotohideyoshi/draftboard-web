import * as types from '../action-types.js';
import request from 'superagent';
import { normalize, Schema, arrayOf } from 'normalizr';
import log from '../lib/logging';


const historySchema = new Schema('history', {
  idAttribute: 'player_id',
});


function fetchFantasyHistorySuccess(body) {
  return {
    type: types.FETCH_FANTASY_HISTORY_SUCCESS,
    body,
  };
}


function fetchFantasyHistoryFail(body) {
  return {
    type: types.FETCH_FANTASY_HISTORY_FAIL,
    body,
  };
}


export function fetchFantasyHistory(sport) {
  if (!sport) {
    log.error('<sport> must be supplied to fetch fantasy point history.');
  }

  return (dispatch) => {
    request
    .get(`/api/sports/fp-history/${sport}/`)
    .set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      Accept: 'application/json',
    })
    .end((err, res) => {
      if (err) {
        log.error(res.body);
        return dispatch(fetchFantasyHistoryFail(res.body));
      }

      // Normalize injuries
      const normalizedHistory = normalize(
        res.body,
        arrayOf(historySchema)
      );

      return dispatch(fetchFantasyHistorySuccess({
        history: normalizedHistory.entities.history,
        sport,
      }));
    });
  };
}
