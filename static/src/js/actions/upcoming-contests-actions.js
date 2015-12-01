import * as types from '../action-types.js'
import request from 'superagent'
import { normalize, Schema, arrayOf } from 'normalizr'
import Cookies from 'js-cookie'


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
export function setFocusedContest(contestId) {
    return (dispatch) => {
      dispatch({
        type: types.SET_FOCUSED_CONTEST,
        contestId
      });
    };

}


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
          }))
        }
      }
    )
  }
}


/**
 * When one of the contest list filters gets updated, change the state keys for that filter.
 * @param  {[type]} filterName     [description]
 * @param  {[type]} filterProperty [description]
 * @param  {[type]} match          [description]
 * @return {[type]}                [description]
 */
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


export function updateOrderByFilter(property, direction='desc') {
  return {
    type: types.UPCOMING_CONTESTS_ORDER_CHANGED,
    orderBy: {
      property,
      direction
    }
  }
}


/**
 * Enter a lineup into an upcoming contest.
 * @param  {int} contestId The contest to be entered.
 * @param  {int} lineupId  The lineup's id.
 */
export function enterContest(contestId, lineupId) {
  let postData = {
    contest: contestId,
    lineup: lineupId
  }

  return (dispatch) => {
    return request
      .post('/api/contest/enter-lineup/')
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        'X-CSRFToken': Cookies.get('csrftoken'),
        'Accept': 'application/json'
      })
      .send(postData)
      .end(function(err, res) {
        if(err) {
          window.alert(res.body)
          console.error(res.body)
        } else {
          console.log(res)
          // Upon save success, send user to the lobby.
          // document.location.href = '/frontend/lobby/?lineup-saved=true';
        }
    });
  }
}
