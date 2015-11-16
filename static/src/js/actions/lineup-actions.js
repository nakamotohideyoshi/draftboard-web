import * as types from '../action-types.js'
import request from 'superagent'
import Cookies from 'js-cookie'
import {forEach as _forEach} from 'lodash'


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
  return (dispatch) => {
    dispatch({
      type: types.CREATE_LINEUP_ADD_PLAYER,
      player
    })
  }
}


export function removePlayer(playerId) {
  return (dispatch) => {
    dispatch({
      type: types.CREATE_LINEUP_REMOVE_PLAYER,
      playerId
    })
  }
}


function saveLineupFail(err) {
  return (dispatch) => {
    dispatch({
      type: types.CREATE_LINEUP_SAVE_FAIL,
      err
    })
  }

}


// TODO: some basic save lineup validation
// Check for salary cap restrictions
function isValidLineup(lineup) {
  // Does each slot have a player in it?
  for (let slot of lineup) {
    if (!slot.player) {
      return false
    }
  }

  return true
}



export function saveLineup(lineup, title, draftGroupId) {

  console.log('lineup', lineup)

  return (dispatch) => {
    if (!isValidLineup(lineup)) {
      return dispatch(saveLineupFail('lineup is not valid'))
    }
    else {
      // Build an array of player_ids.
      var playerIds = lineup.map(function(slot) {
        return slot.player.player_id;
      });

      var postData = {
        name: title || '',
        players: playerIds,
        // Grab the current draftGroupId from the DraftGroupStore.
        draft_group: draftGroupId
      };

      request.post('/api/lineup/create/')
        .set({
          'X-REQUESTED-WITH':  'XMLHttpRequest',
          'X-CSRFToken': Cookies.get('csrftoken'),
          'Accept': 'application/json'
        })
        .send(postData)
        .end(function(err, res) {
          if(err) {
            dispatch(saveLineupFail(res.body))
          } else {
            // Upon save success, send user to the lobby.
            document.location.href = '/frontend/lobby/?lineup-saved=true';
          }
      }.bind(this));
    }


  }
}


//TODO: add lineup name change action.
export function createLineupSetTitle(title) {
  // CREATE_LINEUP_SAVE
  console.log('createLineupSetTitle()', title)
}



export function importLineup(lineup, getState) {
  return (dispatch, getState) => {
    let state = getState()
    let players = [];

    // Since the lineup API endpoint 'player' doesn't have the same info as the DraftGruoup
    // 'player', we need to grab the corresponding DraftGroup player object and use that.
    _forEach(lineup.players, function(player) {
      // Get the DraftGroup player
      let DraftGroupPlayer = state.draftDraftGroup.allPlayers[player.player_id];
      //  Copy and append the idx to the player.
      DraftGroupPlayer = Object.assign({}, DraftGroupPlayer, {'idx': player.idx})
      // push them into a list of players.
      players.push(DraftGroupPlayer)
    })

    dispatch({
      type: types.CREATE_LINEUP_IMPORT,
      players: players
    })
  }
}
