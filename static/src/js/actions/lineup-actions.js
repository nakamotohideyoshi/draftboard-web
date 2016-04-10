import * as types from '../action-types.js';
import request from 'superagent';
import Cookies from 'js-cookie';
import { normalize, Schema, arrayOf } from 'normalizr';
import { forEach as _forEach } from 'lodash';
import { merge as _merge } from 'lodash';
import { sortBy as _sortBy } from 'lodash';
import { uniqWith as _uniqWith } from 'lodash';
import { addMessage } from './message-actions.js';
import log from '../lib/logging.js';
import { monitorLineupEditRequest } from './lineup-edit-request.js';

// Normalization scheme for lineups.
const lineupSchema = new Schema('lineups', {
  idAttribute: 'id',
});


function fetchUpcomingLineupsSuccess(res) {
  return {
    type: types.FETCH_UPCOMING_LINEUPS_SUCCESS,
    lineups: res.lineups,
    draftGroupsWithLineups: res.draftGroupsWithLineups,
  };
}


function fetchUpcomingLineupsFail(ex) {
  return {
    type: types.FETCH_UPCOMING_LINEUPS_FAIL,
    ex,
  };
}


export function filterLineupsByDraftGroupId(draftGroupId) {
  return {
    type: types.FILTER_UPCOMING_LINEUPS_BY_DRAFTGROUP_ID,
    draftGroupId,
  };
}


export function fetchUpcomingLineups(draftGroupId = null) {
  if (window.dfs.user.isAuthenticated !== true) {
    return {
      type: types.USER_NOT_AUTHENTICATED,
    };
  }

  return (dispatch) => {
    const promise = new Promise((resolve, reject) => {
      request
        .get('/api/lineup/upcoming/')
        .set({ 'X-REQUESTED-WITH': 'XMLHttpRequest' })
        .set('Accept', 'application/json')
        .end((err, res) => {
          if (err) {
            dispatch(fetchUpcomingLineupsFail(err));
            reject(err);
          } else {
            // If a specific draft group was requested, update the filter property which will
            // filter them out with a selector.
            if (draftGroupId) {
              dispatch(filterLineupsByDraftGroupId(draftGroupId));
            }

            // Normalize lineups list by ID.
            const normalizedLineups = normalize(
              res.body,
              arrayOf(lineupSchema)
            );

            // Find unique draft groups that we have a lineup for.
            const draftGroups = _uniqWith(
              res.body.map((lineup) => lineup.draft_group),
              (group) => group
            );

            // Sort playres by roster slot (idx)
            _forEach(normalizedLineups.entities.lineups, (lineup, key) => {
              normalizedLineups.entities.lineups[key].players = _sortBy(
                normalizedLineups.entities.lineups[key].players, 'idx'
              );
            });

            dispatch(fetchUpcomingLineupsSuccess({
              draftGroupsWithLineups: draftGroups,
              lineups: normalizedLineups.entities.lineups,
            }));
          }

          resolve(res);
        });
    });

    return promise;
  };
}


export function lineupFocused(lineupId) {
  return (dispatch) => {
    dispatch({
      type: types.LINEUP_FOCUSED,
      lineupId,
    });
  };
}


export function lineupHovered(lineupId) {
  return (dispatch) => {
    dispatch({
      type: types.LINEUP_HOVERED,
      lineupId,
    });
  };
}


// Initialize a blank lineup card based on the sport of the current draftgroup.
export function createLineupInit(sport) {
  return (dispatch) => {
    dispatch({
      type: types.CREATE_LINEUP_INIT,
      sport,
    });
  };
}


export function createLineupAddPlayer(player) {
  return (dispatch) => {
    dispatch({
      type: types.CREATE_LINEUP_ADD_PLAYER,
      player,
    });
  };
}


export function removePlayer(playerId) {
  return (dispatch) => {
    dispatch({
      type: types.CREATE_LINEUP_REMOVE_PLAYER,
      playerId,
    });
  };
}


function saveLineupFail(err) {
  return (dispatch) => {
    dispatch({
      type: types.CREATE_LINEUP_SAVE_FAIL,
      err,
    });
  };
}


// TODO: some basic save lineup validation
// Check for salary cap restrictions
function validateLineup(lineup) {
  const errors = [];
  // Does each slot have a player in it?
  for (const slot of lineup) {
    if (!slot.player) {
      errors.push('lineup is not completely filled.');
      break;
    }
  }

  return errors;
}


export function saveLineup(lineup, title, draftGroupId) {
  return (dispatch) => {
    const lineupErrors = validateLineup(lineup);

    // If we have errors, dispatch a fail action with them.
    if (lineupErrors.length > 0) {
      return dispatch(saveLineupFail(lineupErrors));
    }

    // Build an array of player_ids.
    const playerIds = lineup.map((slot) => slot.player.player_id);

    const postData = {
      name: title || '',
      players: playerIds,
      draft_group: draftGroupId,
    };

    request.post('/api/lineup/create/')
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        'X-CSRFToken': Cookies.get('csrftoken'),
        Accept: 'application/json',
      })
      .send(postData)
      .end((err, res) => {
        if (err) {
          dispatch(saveLineupFail(res.body));
        } else {
          // Upon save success, send user to the lobby.
          document.location.href = '/lobby/?lineup-saved=true';
        }
      });
  };
}


/**
 * Save an already existing lineup.
 * @param  {[type]} lineup       [description]
 * @param  {[type]} title        [description]
 * @return {[type]}              [description]
 */
export function saveLineupEdit(lineup, title, lineupId) {
  log.info('saveLineupEdit', lineup, title, lineupId);
  return (dispatch) => {
    const lineupErrors = validateLineup(lineup);

    // If we have errors, dispatch a fail action with them.
    if (lineupErrors.length > 0) {
      return dispatch(saveLineupFail(lineupErrors));
    }

    // Build an array of player_ids.
    const playerIds = lineup.map((slot) => slot.player.player_id);

    const postData = {
      name: title || '',
      players: playerIds,
      lineup: parseInt(lineupId, 10),
    };

    request.post('/api/lineup/edit/')
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        'X-CSRFToken': Cookies.get('csrftoken'),
        Accept: 'application/json',
      })
      .send(postData)
      .end((err, res) => {
        if (err) {
          addMessage({
            title: 'Unable to edit contest.',
            level: 'warning',
          });
          log.error(res);
          dispatch(saveLineupFail(res.body));
        } else {
          log.info(res.body);
          dispatch(monitorLineupEditRequest(res.body.task_id, lineupId));
        }
      });
  };
}


/**
 * When an edit is requested, we need to import the lineup and remove the lineup from our list of
 * lineups.
 * @param  {[type]} lineupId [description]
 * @return {[type]}          [description]
 */
export function editLineupInit(lineupId) {
  return (dispatch, getState) => {
    const state = getState();

    if (state.upcomingLineups.lineups.hasOwnProperty(lineupId)) {
      log.info(`Lineup #${lineupId} found, importing for editing.`);
      dispatch({
        type: types.EDIT_LINEUP_INIT,
        lineupId,
      });
    } else {
      log.warn(`Lineup #${lineupId} does not exist in upcoming lineups.`);
      dispatch({
        type: types.EDIT_LINEUP_INIT,
        lineupId,
      });
    }
  };
}


/**
 * When drafting a lineup, this takes an already-created lineup and copies all players into the
 * lineup card that is currently being drafted.
 *
 * @param  {Object} lineup   A valid lineup (most likely from state.upcomingLineups.lineups)
 */
export function importLineup(lineup, importTitle = false) {
  return (dispatch, getState) => {
    const state = getState();
    const players = [];
    let title = '';

    if (importTitle) {
      title = lineup.name;
    }

    // Since the lineup API endpoint 'player' doesn't have the same info as the DraftGruoup
    // 'player', we need to grab the corresponding DraftGroup player object and use that.
    _forEach(lineup.players, (player) => {
      // Get the DraftGroup player
      let DraftGroupPlayer = state.draftGroupPlayers.allPlayers[player.player_id];
      //  Copy and append the idx to the player.
      DraftGroupPlayer = _merge({}, DraftGroupPlayer, { idx: player.idx });
      // push them into a list of players.
      players.push(DraftGroupPlayer);
    });

    dispatch({
      type: types.CREATE_LINEUP_IMPORT,
      players,
      title,
    });
  };
}


/**
 * When a user wants to create a new lineup via copying another one of their lineups, this takes
 * the first lineup's id, and imports it.
 * @param  {Int} lineupId Which lineup should be copied.
 */
export function createLineupViaCopy(lineupId) {
  return (dispatch, getState) => {
    const state = getState();
    // When copying a lineup is requested, import a lineup by id (via url), check if we have the
    // necessary data, if so then import it.
    if (lineupId && state.draftGroupPlayers.id) {
      // Does this lineup exist in our lineups list?
      if (state.upcomingLineups.lineups.hasOwnProperty(lineupId)) {
        dispatch(importLineup(state.upcomingLineups.lineups[lineupId], getState));
      } else {
        log.error(`Lineup #${lineupId} is not in upcoming lineups.`);
      }
    }
  };
}
