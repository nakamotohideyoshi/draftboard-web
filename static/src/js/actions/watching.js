import * as ActionTypes from '../action-types';
import forEach from 'lodash/forEach';
import { fetchContestLineupsUsernamesIfNeeded } from './live-contests';
import { fetchDraftGroupFPIfNeeded } from './live-draft-groups';
import { fetchPlayersStatsIfNeeded } from './live-players';
import log from '../lib/logging';
import { dateNow } from '../lib/utils';
import { push as routerPush } from 'react-router-redux';

// get custom logger for actions
const logAction = log.getLogger('action');


const resetWatching = () => ({
  type: ActionTypes.WATCHING__RESET,
});

export const updateLiveMode = (changedFields) => (dispatch, getState) => {
  logAction.debug('actions.updateLiveMode', changedFields);

  const state = getState();

  // check that we have relevant players
  if (changedFields.myLineupId && state.livePlayers.fetched.indexOf(changedFields.myLineupId) === -1) {
    dispatch(fetchPlayersStatsIfNeeded(changedFields.myLineupId));
  }
  if (changedFields.opponentLineupId && state.livePlayers.fetched.indexOf(changedFields.opponentLineupId) === -1) {
    dispatch(fetchPlayersStatsIfNeeded(changedFields.opponentLineupId));
  }

  // make sure to get the usernames as well
  if (changedFields.contestId && changedFields.contestId !== null) {
    dispatch(fetchContestLineupsUsernamesIfNeeded(changedFields.contestId));
  }

  // make sure every defined field is an integer
  const newMode = {};
  const integerFields = ['myLineupId', 'contestId', 'opponentLineupId'];
  forEach(changedFields, (val, key) => {
    if (integerFields.indexOf(key) !== -1) {
      newMode[key] = (val === null) ? null : parseInt(val, 10);
    } else {
      newMode[key] = val;
    }
  });

  return dispatch({
    type: ActionTypes.WATCHING_UPDATE,
    watching: newMode,
  });
};

export const resetWatchingAndPath = () => (dispatch) => {
  logAction.debug('actions.resetWatchingAndPath');

  // update the URL path
  dispatch(routerPush('/live/'));

  // reset what user is watching
  dispatch(resetWatching());
};

export const updateWatchingAndPath = (path, changedFields) => (dispatch) => {
  logAction.debug('actions.updateWatchingAndPath', path, changedFields);

  // update the URL path
  dispatch(routerPush(path));

  // update what user is watching
  dispatch(updateLiveMode(changedFields));
};

export const doesMyLineupExist = (state) => {
  logAction.debug('actions.doesMyLineupExist');

  const watching = state.watching;

  if (watching.myLineupId) {
    const myLineup = state.currentLineups.items[watching.myLineupId] || false;

    // if we no longer have a lineup to look at, reset
    if (!myLineup) return false;
  }

  return true;
};

export const checkForUpdates = () => (dispatch, getState) => {
  logAction.trace('actions.checkForUpdates');

  const state = getState();
  const watching = state.watching;

  if (watching.myLineupId) {
    const myLineup = state.currentLineups.items[watching.myLineupId] || {};

    // if we no longer have a lineup to look at, reset
    if (!myLineup) {
      return dispatch(resetWatching());
    }

    dispatch(fetchPlayersStatsIfNeeded(watching.myLineupId));

    if (watching.opponentLineupId) {
      dispatch(fetchPlayersStatsIfNeeded(watching.opponentLineupId));
    }

    if (dateNow() > myLineup.start && myLineup.hasOwnProperty('draft_group')) {
      dispatch(fetchDraftGroupFPIfNeeded(myLineup.draft_group));
    }
  }
};


/**
 * Look through each hof the currently live lineups and fetch their player stats and the
 * draft group fantasy points so that we can update the live cards on the results page.
 */
export const checkForLiveUpdatesResultsPage = () => (dispatch, getState) => {
  const state = getState();
  const currentLineups = state.currentLineups.items;

  // Fetch info for each of the player's currently live lineups.
  forEach(currentLineups, (lineup) => {
    if (lineup.hasOwnProperty('draftGroup')) {
      dispatch(fetchPlayersStatsIfNeeded(parseInt(lineup.id, 10)));
      dispatch(fetchDraftGroupFPIfNeeded(parseInt(lineup.draftGroup, 10)));
    }
  });
};
