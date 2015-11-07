import * as types from '../action-types.js'
import request from 'superagent'
import { normalize, Schema, arrayOf } from 'normalizr'

const contestSchema = new Schema('contests', {
  idAttribute: 'id'
})




function fetchUpcomingContestsSuccess(body) {
  return {
    type: types.FETCH_UPCOMING_CONTESTS_SUCCESS,
    body
  };
}


function fetchUpcomingContestsFail(ex) {
  return {
    type: types.FETCH_UPCOMING_CONTESTS_FAIL,
    ex
  };
}


// export function setFocusedPlayer(playerId) {
//   return (dispatch) => {
//     dispatch({
//       type: types.SET_FOCUSED_PLAYER,
//       playerId
//     });
//   };
// }


export function fetchUpcomingContests() {
  return (dispatch) => {
    return request
      .get("/contest/lobby/")
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          return dispatch(fetchUpcomingContestsFail(err));
        } else {
          // Normalize contest list by ID.
          const normalizedContests = normalize(
            res.body.results,
            arrayOf(contestSchema)
          )

          return dispatch(fetchUpcomingContestsSuccess({
            contests: normalizedContests.entities.contests
          }));
        }
      });
  };
}
