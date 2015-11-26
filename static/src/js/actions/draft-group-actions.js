import * as types from '../action-types.js'
import request from 'superagent'
import { normalize, Schema, arrayOf } from 'normalizr'

const playerSchema = new Schema('players', {
  idAttribute: 'player_id'
})



function fetchDraftgroupSuccess(body) {
  return {
    type: types.FETCH_DRAFTGROUP_SUCCESS,
    body
  };
}


function fetchDraftgroupFail(ex) {
  return {
    type: types.FETCH_DRAFTGROUP_FAIL,
    ex
  };
}


export function setFocusedPlayer(playerId) {
  return (dispatch) => {
    dispatch({
      type: types.SET_FOCUSED_PLAYER,
      playerId
    });
  };
}


export function fetchDraftGroup(draftGroupId) {
  console.log('HERE', draftGroupId)
  return (dispatch) => {
    return request
      .get("/api/draft-group/" + draftGroupId + '/')
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        'Accept': 'application/json'
      })
      .end(function(err, res) {
        if(err) {
          console.log('err', err)
          return dispatch(fetchDraftgroupFail(err));
        } else {
          console.log('res', res)
          // Normalize player list by ID.
          const normalizedPlayers = normalize(
            res.body.players,
            arrayOf(playerSchema)
          )

          return dispatch(fetchDraftgroupSuccess({
            players: normalizedPlayers.entities.players,
            start: res.body.start,
            end: res.body.end,
            sport: res.body.sport,
            id: res.body.pk
          }));
        }
      });
  };
}


export function updateFilter(filterName, filterProperty, match) {
  return {
    type: types.DRAFTGROUP_FILTER_CHANGED,
    filter: {
      filterName,
      filterProperty,
      match
    }
  }
}
