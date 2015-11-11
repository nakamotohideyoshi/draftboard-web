import * as types from '../action-types.js'
import request from 'superagent'


/**
 * Upcoming draft groups is not a full draft group with players and everything,
 * it's just a bunch of info about the upcoming draft groups, it's used to create
 * the draft group selection modal in the lobby.
 */


function fetchSuccess(body) {
  return {
    type: types.FETCH_UPCOMING_DRAFTGROUPS_INFO_SUCCESS,
    body
  }
}


function fetchFail(ex) {
  return {
    type: types.FETCH_UPCOMING_DRAFTGROUPS_INFO_FAIL,
    ex
  }
}


export function fetchUpcomingDraftGroupsInfo() {
  return (dispatch) => {
    return request
      .get("/draft-group/upcoming/")
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          return dispatch(fetchFail(err));
        } else {
          return dispatch(fetchSuccess({
            draftGroups: res.body.results
          }))
        }
    })
  }
}
