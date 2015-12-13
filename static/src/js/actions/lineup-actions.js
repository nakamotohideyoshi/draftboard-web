import * as types from '../action-types.js'
import 'babel-core/polyfill';
// so we can use superagent with Promises
import request from 'superagent'
import Cookies from 'js-cookie'
import { normalize, Schema, arrayOf } from 'normalizr'
import {forEach, uniq} from 'lodash'


// Normalization scheme for lineups.
const lineupSchema = new Schema('lineups', {
  idAttribute: 'id'
})


function fetchUpcomingLineupsSuccess(res) {
  return {
    type: types.FETCH_UPCOMING_LINEUPS_SUCCESS,
    lineups: res.lineups,
    draftGroupsWithLineups: res.draftGroupsWithLineups
  }
}


function fetchUpcomingLineupsFail(ex) {
  window.alert(ex)
  return {
    type: types.FETCH_UPCOMING_LINEUPS_FAIL,
    ex
  }
}


export function filterLineupsByDraftGroupId(draftGroupId) {
  return {
    type: types.FILTER_UPCOMING_LINEUPS_BY_DRAFTGROUP_ID,
    draftGroupId
  }
}


export function fetchUpcomingLineups(draftGroupId=null) {
  if (window.dfs.user.isAuthenticated !== true) {
    return {
      type: types.USER_NOT_AUTHENTICATED
    }
  }

  return (dispatch, getState) => {
    return new Promise((resolve, reject) => {
      return request
        .get("/api/lineup/upcoming/")
        .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
        .set('Accept', 'application/json')
        .end(function(err, res) {
          if(err) {
            dispatch(fetchUpcomingLineupsFail(err))
            reject(err)
          } else {

            // If a specific draft group was requested, update the filter property which will
            // filter them out with a selector.
            if (draftGroupId) {
              dispatch(filterLineupsByDraftGroupId(draftGroupId))
            }

            // Normalize lineups list by ID.
            let normalizedLineups = normalize(
              res.body,
              arrayOf(lineupSchema)
            )

            // Find unique draft groups that we have a lineup for.
            let draftGroups = uniq(
              res.body.map((lineup) => {return lineup.draft_group}),
              function(group) {
                return group
              }
            )

            dispatch(fetchUpcomingLineupsSuccess({
              draftGroupsWithLineups: draftGroups,
              lineups: normalizedLineups.entities.lineups
            }))

            resolve(res)
          }
      })
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


export function lineupHovered(lineupId) {
  return (dispatch) => {
    dispatch({
      type: types.LINEUP_HOVERED,
      lineupId
    })
  }
}


/**
 * When a user wants to create a new lineup via copying another one of their lineups, this takes
 * the first lineup's id, and imports it.
 * @param  {Int} lineupId Which lineup should be copied.
 */
export function createLineupViaCopy(lineupId, getState) {
  return(dispatch, getState) => {
    const state = getState()
    // When copying a lineup is requested, import a lineup by id (via url), check if we have the
    // necessary data, if so then import it.
    if (lineupId && state.draftDraftGroup.id) {
      // Does this lineup exist in our lineups list?
      if (state.upcomingLineups.lineups.hasOwnProperty(lineupId)) {
        dispatch(importLineup(state.upcomingLineups.lineups[lineupId], getState))
      } else {
        console.error(`Lineup #${lineupId} is not in upcoming lineups.`)
      }
    }
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
            document.location.href = '/lobby/?lineup-saved=true';
          }
      });
    }
  }
}


/**
 * Once a lineup is edited, save it.
 * @param  {[type]} lineup   [description]
 * @param  {[type]} title    [description]
 * @param  {[type]} lineupId [description]
 * @param  {[type]} getState [description]
 * @return {[type]}          [description]
 */
export function saveLineupEdit(lineup, title, lineupId) {
  return (dispatch, getState) => {
    console.log('saveLineupEdit', lineup, title, lineupId)
  }
}



/**
 * When an edit is requested, we need to import the lineup and remove the lineup from our list of
 * lineups.
 * @param  {[type]} lineupId [description]
 * @return {[type]}          [description]
 */
export function editLineupInit(lineupId) {
  return (dispatch, getState) => {
    let state = getState()

    if (state.upcomingLineups.lineups.hasOwnProperty(lineupId)) {
      dispatch({
        type: types.EDIT_LINEUP_INIT,
        lineupId
      })
    } else {
      console.error(`Lineup #${lineupId} does not exist in upcoming lineups.`)
      dispatch({
        type: types.EDIT_LINEUP_INIT,
        lineupId
      })

    }
  }
}


/**
 * When drafting a lineup, this takes an already-created lineup and copies all players into the
 * lineup card that is currently being drafted.
 *
 * @param  {Object} lineup   A valid lineup (most likely from state.upcomingLineups.lineups)
 */
export function importLineup(lineup, importTitle=false) {
  return (dispatch, getState) => {
    let state = getState()
    let players = [];
    let title = ''

    if (importTitle) {
      title = lineup.name
    }

    // Since the lineup API endpoint 'player' doesn't have the same info as the DraftGruoup
    // 'player', we need to grab the corresponding DraftGroup player object and use that.
    forEach(lineup.players, function(player) {
      // Get the DraftGroup player
      let DraftGroupPlayer = state.draftDraftGroup.allPlayers[player.player_id];
      //  Copy and append the idx to the player.
      DraftGroupPlayer = Object.assign({}, DraftGroupPlayer, {'idx': player.idx})
      // push them into a list of players.
      players.push(DraftGroupPlayer)
    })

    dispatch({
      type: types.CREATE_LINEUP_IMPORT,
      players: players,
      title
    })
  }
}
