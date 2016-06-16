import * as ActionTypes from '../action-types';
import forEach from 'lodash/forEach';
import { fetchContestLineupsUsernamesIfNeeded } from './live-contests';
import { fetchDraftGroupFPIfNeeded } from './live-draft-groups';
import { fetchPlayersStatsIfNeeded } from './live-players';
import log from '../lib/logging';
import { dateNow } from '../lib/utils';
import { push as routerPush } from 'react-router-redux';


export const checkForUpdates = () => (dispatch, getState) => {
  log.trace('actions.watching.checkForUpdates()');

  const state = getState();
  const watching = state.watching;

  if (watching.myLineupId) {
    const myLineup = state.currentLineups.items[watching.myLineupId] || {};

    if (dateNow() > myLineup.start && myLineup.hasOwnProperty('draft_group')) {
      dispatch(fetchPlayersStatsIfNeeded(watching.myLineupId));
      dispatch(fetchDraftGroupFPIfNeeded(myLineup.draft_group));

      if (watching.opponentLineupId) {
        dispatch(fetchPlayersStatsIfNeeded(watching.opponentLineupId));
      }
    }
  }
};

export const updateLiveMode = (changedFields) => (dispatch, getState) => {
  log.trace('updateLiveMode', changedFields);

  const state = getState();

  // check that we have relevant players
  if (changedFields.myLineupId && state.livePlayers.fetched.indexOf(changedFields.myLineupId) === -1) {
    dispatch(fetchPlayersStatsIfNeeded(changedFields.myLineupId));
  }
  if (changedFields.opponentLineupId && state.livePlayers.fetched.indexOf(changedFields.opponentLineupId) === -1) {
    dispatch(fetchPlayersStatsIfNeeded(changedFields.opponentLineupId));
  }

  // make sure to get the usernames as well
  if (changedFields.contestId) {
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

export const updateWatchingAndPath = (path, changedFields) => (dispatch) => {
  log.trace('actions.watching.changePathAndMode()', path, changedFields);

  // update the URL path
  dispatch(routerPush(path));

  // update what user is watching
  dispatch(updateLiveMode(changedFields));

  // if the contest has changed, then get the appropriate usernames for the standings pane
  if (changedFields.hasOwnProperty('contestId')) {
    dispatch(fetchContestLineupsUsernamesIfNeeded(changedFields.contestId));
  }
};
