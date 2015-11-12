import * as types from '../action-types.js'
import request from 'superagent'



function fetchUpcomingLineupsSuccess(body) {
  return {
    type: types.FETCH_UPCOMING_LINEUPS_SUCCESS,
    body
  }
}


function fetchUpcomingLineupsFail(ex) {
  return {
    type: types.FETCH_UPCOMING_LINEUPS_FAIL,
    ex
  }
}


export function fetchUpcomingLineups() {
  return (dispatch) => {
    return request
      .get("/api/lineup/upcoming/")
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          dispatch(fetchUpcomingLineupsFail(err))
        } else {
          dispatch(fetchUpcomingLineupsSuccess(res.body))
        }
    })
  }
}


export function lineupFocused(lineupId) {
  return (dispatch) => {
    dispatch({
      type: types.LINEUP_FOCUSED,
      lineupId
    })
  }
}


// Initialize a blank lineup card based on the sport of the current draftgroup.
export function createLineupInit(sport) {
  return (dispatch) => {
    dispatch({
      type: types.CREATE_LINEUP_INIT,
      sport
    })
  }
}


export function createLineupAddPlayer(player) {
  console.log('createLineupAddPlayer()', player)
}


export function createLineupRemovePlayer(player) {
  console.log('createLineupRemovePlayer()', player)
}


export function createLineupSave() {
  console.log('createLineupSave()')
}


export function createLineupSetTitle(title) {
  console.log('createLineupSetTitle()', title)
}
