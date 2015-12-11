import * as types from '../action-types.js'
import request from 'superagent'
import { normalize, Schema, arrayOf } from 'normalizr'
import log from '../lib/logging'


const historySchema = new Schema('history', {
  idAttribute: 'player_id'
})


function fetchFantasyHistorySuccess(body) {
  return {
    type: types.FETCH_FANTASY_HISTORY_SUCCESS,
    body
  }
}


export function fetchFantasyHistory(sport) {
  if (!sport) {
    log.error('<sport> must be supplied to fetch fantasy point history.')
    return
  }

  return (dispatch, getState) => {
    return request
    .get(`/api/sports/fp-history/${sport}/`)
    .set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'Accept':'application/json'
    })
    .end(function(err, res) {
      if(err) {
        window.alert(res.body)
      } else {
        // Normalize injuries
        const normalizedHistory = normalize(
          res.body,
          arrayOf(historySchema)
        )
        return dispatch(fetchFantasyHistorySuccess({
            history: normalizedHistory.entities.history,
            sport: sport
        }))
      }
    })
  }
}
