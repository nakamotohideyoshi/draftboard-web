import * as ActionTypes from '../action-types';
import { forEach as _forEach } from 'lodash';
import { fetchContestLineupsUsernamesIfNeeded } from './live-contests';
import { fetchDraftGroupFPIfNeeded } from './live-draft-groups';
import { fetchPlayersStatsIfNeeded } from './live-players';


export const checkForUpdates = () => (dispatch, getState) => {
  const state = getState();
  const mode = state.live.mode;

  if (mode.myLineupId) {
    dispatch(fetchPlayersStatsIfNeeded(mode.myLineupId));

    const myLineup = state.currentLineups.items[mode.myLineupId] || {};

    if (myLineup.hasOwnProperty('draft_group')) {
      dispatch(fetchDraftGroupFPIfNeeded(myLineup.draft_group));
    }
  }

  if (mode.opponentLineupId) {
    dispatch(fetchPlayersStatsIfNeeded(mode.opponentLineupId));
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
    newMode[key] = (val === undefined) ? undefined : parseInt(val, 10);
  });

  return dispatch({
    type: ActionTypes.LIVE_MODE_CHANGED,
    mode: newMode,
  });
};
