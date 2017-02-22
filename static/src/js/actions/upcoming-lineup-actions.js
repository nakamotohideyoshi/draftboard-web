import * as actionTypes from '../action-types.js';
import request from 'superagent';
import { CALL_API } from '../middleware/api';
import Cookies from 'js-cookie';
import { normalize, Schema, arrayOf } from 'normalizr';
import forEach from 'lodash/forEach';
import merge from 'lodash/merge';
import sortBy from 'lodash/sortBy';
import uniqWith from 'lodash/uniqWith';
import { validateLineup } from '../lib/lineup.js';
import { addMessage } from './message-actions.js';
import log from '../lib/logging.js';


// Normalization scheme for lineups.
const lineupSchema = new Schema('lineups', {
  idAttribute: 'id',
});


export function filterLineupsByDraftGroupId(draftGroupId) {
  return {
    type: actionTypes.FILTER_UPCOMING_LINEUPS_BY_DRAFTGROUP_ID,
    draftGroupId,
  };
}


export const fetchUpcomingLineups = (draftGroupId = null) => (dispatch) => {
  // The user is not auth'd and anonymous users don't have lineups.
  if (window.dfs.user.isAuthenticated !== true) {
    return {
      type: actionTypes.USER_NOT_AUTHENTICATED,
    };
  }

  const apiActionResponse = dispatch({
    [CALL_API]: {
      types: [
        actionTypes.FETCH_UPCOMING_LINEUPS,
        actionTypes.FETCH_UPCOMING_LINEUPS_SUCCESS,
        actionTypes.ADD_MESSAGE,
      ],
      endpoint: '/api/lineup/upcoming/',
      callback: (json) => {
        // If a specific draft group was requested, update the filter property which will
        // filter them out with a selector.
        if (draftGroupId) {
          dispatch(filterLineupsByDraftGroupId(draftGroupId));
        }

        // Normalize lineups list by ID.
        const normalizedLineups = normalize(
          json,
          arrayOf(lineupSchema)
        );

        // Find unique draft groups that we have a lineup for.
        const draftGroups = uniqWith(
          json.map((lineup) => lineup.draft_group),
          (group) => group
        );

        // Sort playres by roster slot (idx)
        forEach(normalizedLineups.entities.lineups, (lineup, key) => {
          normalizedLineups.entities.lineups[key].players = sortBy(
            normalizedLineups.entities.lineups[key].players, 'idx'
          );
        });

        return {
          draftGroupsWithLineups: draftGroups,
          lineups: normalizedLineups.entities.lineups,
        };
      },
    },
  });

  return apiActionResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    if (action.error) {
      return dispatch({
        type: actionTypes.FETCH_UPCOMING_LINEUPS_FAIL,
        response: action.error,
      });
    }

    return action;
  });
};


export function lineupFocused(lineupId) {
  return (dispatch, getState) => {
    // Find the sport of the lineup so that we can select that filter.
    const state = getState();
    const lineup = state.upcomingLineups.lineups[lineupId];
    let sport = '';
    if (lineup) {
      sport = lineup.sport;
    }
    dispatch({
      type: actionTypes.LINEUP_FOCUSED,
      lineupId,
      sport,
    });
  };
}


export function lineupHovered(lineupId) {
  return (dispatch) => {
    dispatch({
      type: actionTypes.LINEUP_HOVERED,
      lineupId,
    });
  };
}


// Initialize a blank lineup card based on the sport of the current draftgroup.
export function createLineupInit(sport) {
  return (dispatch) => {
    dispatch({
      type: actionTypes.CREATE_LINEUP_INIT,
      sport,
    });
  };
}


export function createLineupAddPlayer(player) {
  return (dispatch) => {
    dispatch({
      type: actionTypes.CREATE_LINEUP_ADD_PLAYER,
      player,
    });
  };
}


export function removePlayer(playerId) {
  return (dispatch) => {
    dispatch({
      type: actionTypes.CREATE_LINEUP_REMOVE_PLAYER,
      playerId,
    });
  };
}


function saveLineupFail(err) {
  return (dispatch) => {
    dispatch({
      type: actionTypes.CREATE_LINEUP_SAVE_FAIL,
      err,
    });
  };
}


export function saveLineup(lineup, title, draftGroupId) {
  return (dispatch) => {
    const lineupErrors = validateLineup(lineup);

    // If we have errors, dispatch a fail action with them.
    if (lineupErrors.length > 0) {
      // format the errors exactly like how the server response with errors.
      return dispatch(saveLineupFail({ detail: lineupErrors }));
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
          window.location.href = `/contests/?action=lineup-saved&lineup=${res.body.lineup_id}`;
        }
      });
  };
}


/**
 * Save an already existing lineup. After this request is done we will have a
 * task_id that we then need to poll for. check lineup-edit-request-actions.js
 * for furthur info.
 * @param  {[type]} lineup       [description]
 * @param  {[type]} title        [description]
 * @return {[type]}              [description]
 */
export function saveLineupEdit(lineup, title, lineupId) {
  return (dispatch) => {
    log.info('saveLineupEdit', lineup, title, lineupId);

    dispatch({
      type: actionTypes.SAVE_LINEUP_EDIT,
      lineupId,
    });

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
          dispatch(addMessage({
            header: 'Unable to edit lineup',
            content: res.text,
            level: 'warning',
            id: 'lineupEdit',
          }));
          log.error(res);
          dispatch({
            type: actionTypes.SAVE_LINEUP_EDIT_FAIL,
            lineupId,
          });
          dispatch(saveLineupFail(res.body));
        } else {
          dispatch({
            type: actionTypes.SAVE_LINEUP_EDIT_SUCCESS,
            lineupId,
          });
          // Redirect to lobby with url param.
          window.location.href = `/contests/?action=lineup-saved&lineup=${lineupId}`;
        }
      });
  };
}


/**
 * When an edit is requested, we need to import the lineup and remove the lineup from our list of
 * lineups.
 * @param  {Integer} lineupId The id of the lineup to be edited.
 */
export function editLineupInit(lineupId) {
  return (dispatch) => {
    log.info(`Lineup #${lineupId} found, importing for editing.`);

    dispatch({
      type: actionTypes.EDIT_LINEUP_INIT,
      lineupId,
    });
  };
}


/**
 * When drafting a lineup, this takes an already-created lineup and copies all players into the
 * lineup card that is currently being drafted.
 *
 * @param  {Object} lineup A valid lineup (most likely from state.upcomingLineups.lineups)
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
    forEach(lineup.players, (player) => {
      // Get the DraftGroup player
      let DraftGroupPlayer = state.draftGroupPlayers.allPlayers[player.player_id];
      //  Copy and append the idx to the player.
      DraftGroupPlayer = merge({}, DraftGroupPlayer, { idx: player.idx });
      // push them into a list of players.
      players.push(DraftGroupPlayer);
    });

    dispatch({
      type: actionTypes.CREATE_LINEUP_IMPORT,
      players,
      title,
    });
  };
}
