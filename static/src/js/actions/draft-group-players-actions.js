import log from '../lib/logging';
import * as actionTypes from '../action-types.js';
import { CALL_API } from '../middleware/api';
import { normalize, Schema, arrayOf } from 'normalizr';
// import { dateNow } from '../lib/utils';
// import { fetchSportInjuries } from './injury-actions.js';
import { fetchFantasyHistory } from './fantasy-history-actions.js';
import { fetchTeamsIfNeeded } from './sports.js';
import { fetchPlayerNewsIfNeeded } from './player-news-actions.js';
import { fetchPlayerBoxScoreHistoryIfNeeded } from './player-box-score-history-actions.js';

const playerSchema = new Schema('players', {
  idAttribute: 'player_id',
});


// Player filter actions.
//
// These control the filter + sorting of the player list in the draft section.
export function updateFilter(filterName, filterProperty, match) {
  return {
    type: actionTypes.DRAFTGROUP_FILTER_CHANGED,
    filter: {
      filterName,
      filterProperty,
      match,
    },
  };
}

export function updateOrderByFilter(property, direction = 'desc') {
  return {
    type: actionTypes.DRAFTGROUP_ORDER_CHANGED,
    orderBy: {
      property,
      direction,
    },
  };
}

export function setFocusedPlayer(playerId) {
  return (dispatch) => {
    dispatch({
      type: actionTypes.SET_FOCUSED_PLAYER,
      playerId,
    });
  };
}


/**
 * Draft Group fetching actions
 * /api/draft-group/<draftGroupId>/
 */

// Do we need to fetch the specified draft group?
function shouldFetchDraftGroup(state, draftGroupId) {
  const draftGroup = state.draftGroupPlayers;

  if (!draftGroup.id || draftGroupId !== draftGroup.id) {
    // do we have a draftgroup AND the right draftgroup in the store?
    return true;
  } else if (draftGroup.isFetching) {
    // are we currently fetching it?
    return false;
  }

  // Default to true.
  return true;
}


const fetchDraftGroup = (draftGroupId) => (dispatch) => {
  const apiActionResponse = dispatch({
    [CALL_API]: {
      types: [
        actionTypes.FETCHING_DRAFT_GROUPS,
        actionTypes.FETCH_DRAFTGROUP_SUCCESS,
        actionTypes.ADD_MESSAGE,
      ],
      endpoint: `/api/draft-group/${draftGroupId}/`,
      // expiresAt: dateNow() + 1000 * 60 * 5,  // 5 minutes
      callback: (json) => {
        // Now that we know which sport we're dealing with, fetch the injuries + fp history for
        // these players.
        dispatch(fetchFantasyHistory(json.sport));
        // TODO: zach: not loading injuries untill we get the API source sorted out.
        log.warn('not loading injuries until we get the API source sorted out.');
        // dispatch(fetchSportInjuries(res.body.sport));
        dispatch(fetchTeamsIfNeeded(json.sport));
        dispatch(fetchPlayerNewsIfNeeded(json.sport));
        dispatch(fetchPlayerBoxScoreHistoryIfNeeded(json.sport));

        // Normalize player list by ID.
        const normalizedPlayers = normalize(
          json.players,
          arrayOf(playerSchema)
        );

        // If there are no probable pitcher updates, disable the filter.
        if (!json.game_updates.filter((update) => update.type === 'pp').length) {
          log.warn('No probable pitcher info was recieved, disabling filter.');
          dispatch(updateFilter('probablePitchersFilter', 'srid', false));
        }

        // return some normalized json to the success action.
        return {
          players: normalizedPlayers.entities.players,
          start: json.start,
          end: json.end,
          sport: json.sport,
          id: json.pk,
          game_updates: json.game_updates,
        };
      },
    },
  });

  apiActionResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    if (action.error) {
      dispatch({
        type: actionTypes.FETCH_DRAFTGROUP_FAIL,
        response: action.error,
      });
    }
  });

  // Return the promise chain in case we want to use it elsewhere.
  return apiActionResponse;
};


export function fetchDraftGroupIfNeeded(draftGroupId) {
  return (dispatch, getState) => {
    if (shouldFetchDraftGroup(getState(), draftGroupId)) {
      return dispatch(fetchDraftGroup(draftGroupId));
    }

    return Promise.resolve();
  };
}
