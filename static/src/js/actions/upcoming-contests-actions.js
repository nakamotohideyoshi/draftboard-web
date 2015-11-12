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


/**
 * Set the focused contest based on the provided contest ID.
 * @param {number} contestId the ID of the contest to set as active.
 */
// setFocusedContest: function(contestId) {
//   if(typeof contestId === 'number') {
//     this.data.focusedContestId = contestId;
//     this.trigger(this.data);
//   }
// },

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
      .get("/api/contest/lobby/")
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
      }
    );
  };
}


export function updateFilter(filterName, filterProperty, match) {
  return {
    type: types.UPCOMING_CONTESTS_FILTER_CHANGED,
    filter: {
      filterName,
      filterProperty,
      match
    }
  }
}
