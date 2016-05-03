import * as ActionTypes from '../action-types';
import { forEach as _forEach } from 'lodash';
import { fetchContestLineupsUsernamesIfNeeded } from './live-contests';
import { fetchDraftGroupFPIfNeeded } from './live-draft-groups';
import { fetchPlayersStatsIfNeeded } from './live-players';
import log from '../lib/logging';
import { dateNow } from '../lib/utils';


export const checkForUpdates = () => (dispatch, getState) => {
  log.trace('actions.watching.checkForUpdates()');

  const state = getState();
  const watching = state.watching;

  if (watching.myLineupId) {
    dispatch(fetchPlayersStatsIfNeeded(watching.myLineupId));

    const myLineup = state.currentLineups.items[watching.myLineupId] || {};

    if (dateNow() > myLineup.start && myLineup.hasOwnProperty('draft_group')) {
      dispatch(fetchDraftGroupFPIfNeeded(myLineup.draft_group));
    }
  }

  if (watching.opponentLineupId) {
    dispatch(fetchPlayersStatsIfNeeded(watching.opponentLineupId));
  }
};

export const updateLiveMode = (changedFields) => (dispatch, getState) => {
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
  _forEach(changedFields, (val, key) => {
    if (key === 'sport') {
      newMode[key] = val;
    } else {
      newMode[key] = (val === null) ? null : parseInt(val, 10);
    }
  });

  return dispatch({
    type: ActionTypes.WATCHING_UPDATE,
    watching: newMode,
  });
};
