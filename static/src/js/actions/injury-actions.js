import * as types from '../action-types.js'
import request from 'superagent'
import { normalize, Schema, arrayOf } from 'normalizr'
import log from '../lib/logging'


const injurySchema = new Schema('injuries', {
  idAttribute: 'player_id'
})


function fetchSportInjuriesSuccess(body) {
  return {
    type: types.FETCH_INJURIES_SUCCESS,
    body
  }
}


export function fetchSportInjuries(sport) {
  if (!sport) {
    log.error('<sport> must be supplied to fetch injuries.')
    return
  }

  return (dispatch, getState) => {
    return request
    .get(`/api/sports/injuries/${sport}/`)
    .set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'Accept':'application/json'
    })
    .end(function(err, res) {
      if(err) {
        window.alert(res.body)
      } else {
        // Normalize injuries
        const normalizedInjuries = normalize(
          res.body,
          arrayOf(injurySchema)
        )
        return dispatch(fetchSportInjuriesSuccess({
            injuries: normalizedInjuries.entities.injuries,
            sport: sport
        }))
      }
    })
  }
}
