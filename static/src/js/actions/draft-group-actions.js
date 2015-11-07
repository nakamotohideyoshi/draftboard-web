import * as types from '../action-types.js'
import request from 'superagent'
import { normalize, Schema, arrayOf } from 'normalizr'

const playerSchema = new Schema('players', {
  idAttribute: 'player_id'
})


// function determineDraftability(player) {
//   return true;
// }


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
  return (dispatch) => {
    return request
      .get("/draft-group/" + draftGroupId + '/')
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          return dispatch(fetchDraftgroupFail(err));
        } else {
          // Normalize player list by ID.
          const normalizedPlayers = normalize(
            res.body.players,
            arrayOf(playerSchema)
          )

          return dispatch(fetchDraftgroupSuccess({
            players: normalizedPlayers.entities.players,
            start: res.body.start,
            end: res.body.end,
            sport: res.body.sport
          }));
        }
      });
  };
}
