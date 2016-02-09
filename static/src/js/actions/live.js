import * as ActionTypes from '../action-types';
import _ from 'lodash';
// import moment from 'moment'

import { fetchContestLineupsUsernamesIfNeeded } from './live-contests';
// import { fetchContestLineups } from './live-contests'
import { fetchDraftGroupFPIfNeeded } from './live-draft-groups';
import { fetchPlayersStatsIfNeeded } from './live-players';
// import log from '../lib/logging'


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

  // if contest doesn't have lineup bytes yet and is live, then check for them
  // if (mode.contestId && state.liveContests.hasOwnProperty(mode.contestId)) {
  //   const contest = state.liveContests[mode.contestId]

  //   // if the contest has started
  //   if (moment.isAfter(moment(contest.info.start))) {
  //     // if there's no lineup bytes yet
  //     if ('lineupBytes' in state.liveContests[mode.contestId] === false ||
  //         state.liveContests[mode.contestId].lineupBytes === '') {
  //       log.info(`actions.checkForUpdates() - fetch lineup bytes for contest ${mode.contestId}`)
  //       dispatch(fetchContestLineups(mode.contestId))
  //     }
  //   }
  // }

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
  _.forEach(changedFields, (val, key) => {
    newMode[key] = (val === undefined) ? undefined : parseInt(val, 10);
  });

  return dispatch({
    type: ActionTypes.LIVE_MODE_CHANGED,
    mode: newMode,
  });
};
