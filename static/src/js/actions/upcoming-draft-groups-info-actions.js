import * as types from '../action-types.js'
import request from 'superagent'
import { normalize, Schema, arrayOf } from 'normalizr'


/**
 * Upcoming draft groups is not a full draft group with players and everything,
 * it's just a bunch of info about the upcoming draft groups, it's used to create
 * the draft group selection modal in the lobby.
 */


 const draftGroupInfoSchema = new Schema('draftGroups', {
   idAttribute: 'pk'
 })


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
      .get("/api/draft-group/upcoming/")
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          return dispatch(fetchFail(err));
        } else {
          // Normalize player list by ID.
          const normalizedDraftGroupInfo = normalize(
            res.body,
            arrayOf(draftGroupInfoSchema)
          )

          return dispatch(fetchSuccess({
            draftGroups: normalizedDraftGroupInfo.entities.draftGroups
          }))
        }
    })
  }
}
