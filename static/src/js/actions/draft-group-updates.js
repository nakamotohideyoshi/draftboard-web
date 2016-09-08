import * as actionTypes from '../action-types.js';
import { CALL_API } from '../middleware/api';
import log from '../lib/logging.js';
import groupBy from 'lodash/groupBy';
import forEach from 'lodash/forEach';


/**
 * Get draft group from the server. These are things like injury status,
 * starting pitchers, game delays, player news, etc.
 * @param  {string} sport one of ['nfl', 'nba', 'mlb', 'nhl']
 * @return {Promise}
 */
const fetchDraftGroupUpdates = (sport) => (dispatch) => {
  // Because we need the sport in the reducer, we have to manually dispatch this action, the
  // API middleware doens't have support for that. This means that
  // DRAFT_GROUP_UPDATES__FETCHING_NULL is just a dummy action that should never be used by a
  // reducer.
  dispatch({
    type: actionTypes.DRAFT_GROUP_UPDATES__FETCHING,
    sport,
  });

  const apiActionResponse = dispatch({
    [CALL_API]: {
      types: [
        actionTypes.DRAFT_GROUP_UPDATES__FETCHING_NULL,
        actionTypes.DRAFT_GROUP_UPDATES__FETCH_SUCCESS,
        actionTypes.ADD_MESSAGE,
      ],
      endpoint: `/api/sports/updates/${sport}/`,
      callback: (json) => {
        const categories = groupBy(json.player_updates, 'category');
        const playerUpdates = {};

        forEach(categories, (updates, key) => {
          playerUpdates[key] = groupBy(updates, 'srid');
        });

        return {
          sport,
          updates: {
            playerUpdates,
            gameUpdates: json.game_updates,
          },
        };
      },
    },
  });

  apiActionResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    if (action.error) {
      dispatch({
        type: actionTypes.DRAFT_GROUP_UPDATES__FETCH_FAIL,
        response: action.error,
        sport,
      });
    }
  });

  // Return the promise chain in case we want to use it elsewhere.
  return apiActionResponse;
};


function shouldfetchDraftGroupUpdates(state, sport) {
  if (state.draftGroupUpdates && state.draftGroupUpdates[sport]) {
    return !state.draftGroupUpdates[sport].isFetching;
  }

  return true;
}


export function fetchDraftGroupUpdatesIfNeeded(sport) {
  return (dispatch, getState) => {
    if (!sport) {
      return Promise.reject('Not fetching draftGroupUpdates, no sport was supplied.');
    }

    if (shouldfetchDraftGroupUpdates(getState(), sport)) {
      return dispatch(fetchDraftGroupUpdates(sport));
    }

    log.info('shouldfetchDraftGroupUpdates == false');
  };
}
