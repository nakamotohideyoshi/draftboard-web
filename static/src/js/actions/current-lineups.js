import * as ActionTypes from '../action-types';
import filter from 'lodash/filter';
import forEach from 'lodash/forEach';
import log from '../lib/logging';
import { CALL_API } from '../middleware/api';
import { camelizeKeys } from 'humps';
import { doesMyLineupExist, resetWatchingAndPath } from './watching';
import { dateNow, hasExpired } from '../lib/utils';
import { fetchContestLineupsIfNeeded } from './live-contests';
import { fetchContestPoolIfNeeded } from './live-contest-pools';
import { fetchDraftGroupIfNeeded } from './live-draft-groups';
import { fetchGamesIfNeeded } from './sports';
import { Schema, arrayOf, normalize } from 'normalizr';
import { trackUnexpected } from './track-exceptions';

// get custom logger for actions
const logAction = log.getLogger('action');


// normalizr schemas for this redux substore

const lineupSchema = new Schema('lineups', {
  idAttribute: 'id',
});
const lineupsRostersSchema = new Schema('lineupsRosters', {
  idAttribute: 'id',
});


// dispatch to reducer methods

/**
 * Dispatch information to reducer that we have completed getting all information related to the lineups
 * Used to make the components aware tht we have finished pulling information.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const confirmRelatedLineupsInfo = () => ({
  type: ActionTypes.CURRENT_LINEUPS__RELATED_INFO_SUCCESS,
});

/**
 * Dispatch information to reducer that we have completed getting all information related to the lineups
 * Used to make the components aware tht we have finished pulling information.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const storeLineupsPlayers = (lineupsPlayers) => ({
  type: ActionTypes.CURRENT_LINEUPS__ADD_PLAYERS,
  lineupsPlayers,
});


// helper methods


/**
 * The lineups API call does not return the players in the lineup's lineup.
 * This method loops through all lineups. Any lineup that is live, it then returns the related roster from its lineup.
 * @return {promise} Returns the object of rosters wrapped in dispatch wrapped in promise, so we can chain
 */
const addLineupsPlayers = () => (dispatch, getState) => {
  logAction.debug('actions.addLineupsPlayers');

  const state = getState();
  const lineupsPlayers = {};

  // filter lineups to only those that have started
  const liveLineups = filter(state.currentLineups.items,
    (lineup) => hasExpired(lineup.start) && lineup.contests.length > 0
  );

  // only add players that have started playing, by checking if they are in the roster
  forEach(liveLineups, (lineup) => {
    if (!(lineup.contests[0] in state.liveContests) || !('lineups' in state.liveContests[lineup.contests[0]])) {
      trackUnexpected(`addLineupsPlayers failed, no lineups for contest 0 in lineup ${lineup.id}`, { state });
    } else {
      // just choose the first contest
      const contestLineup = state.liveContests[lineup.contests[0]].lineups[lineup.id] || {};
      if (contestLineup.roster) {
        lineupsPlayers[lineup.id] = contestLineup.roster;
      }
    }
  });

  if (Object.keys(lineupsPlayers).length === 0) return Promise.resolve();

  // returning a promise such that we can chain this method
  return dispatch(storeLineupsPlayers(lineupsPlayers));
};

/**
 * API GET to return live and upcoming (current) lineups.
 * @return {promise}   Promise that resolves with API response body to reducer
 */
export const fetchCurrentLineups = () => ({
  [CALL_API]: {
    types: [
      ActionTypes.CURRENT_LINEUPS__REQUEST,
      ActionTypes.CURRENT_LINEUPS__RECEIVE,
      ActionTypes.ADD_MESSAGE,
    ],
    expiresAt: dateNow() + 1000 * 60 * 5,  // 5 minutes
    endpoint: '/api/lineup/current/',
    callback: (json) => {
      // normalize and camelcase it
      const camelizedJson = camelizeKeys(json);
      const entries = normalize(camelizedJson, arrayOf(lineupSchema)).entities;

      // API returns [] if there are no entries
      if (!('lineups' in entries)) return {};

      Object.keys(entries.lineups).map((lineupId) => {
        const lineup = entries.lineups[lineupId];
        let contests = [];
        Object.keys(lineup.contestsByPool).map((contestPoolId) => {
          contests = contests.concat(lineup.contestsByPool[contestPoolId]);
        });

        lineup.contests = [...new Set(contests)];
      });

      return entries;
    },
  },
});

/**
 * Right, so when lineups have upcoming contests, we need a way to pull in all upcoming lineups. This takes the upcoming
 * lineups, and then adds them to the associated lineup.
 * @return {promise}          Promise that resolves with API response body to reducer
 */
export const fetchLineupsRosters = () => ({
  [CALL_API]: {
    types: [
      ActionTypes.CURRENT_LINEUPS_ROSTERS__REQUEST,
      ActionTypes.CURRENT_LINEUPS_ROSTERS__RECEIVE,
      ActionTypes.ADD_MESSAGE,
    ],
    expiresAt: dateNow(),  // important! set to now so that it always refreshes
    endpoint: '/api/lineup/upcoming/',
    callback: (json) => {
      const camelizedJson = camelizeKeys(json);
      return normalize(camelizedJson, arrayOf(lineupsRostersSchema)).entities;
    },
  },
});

/**
 * Method to determine whether we need to fetch lineups.
 * Fetch if we are not already fetching.
 * @param  {object} state Current Redux state to test
 * @return {boolean}      True if we should fetch draft groups, false if not
 */
const shouldFetchLineups = (state) => {
  logAction.debug('actions.shouldFetchLineups');

  const reasons = [];

  if (!hasExpired(state.currentLineups.expiresAt)) reasons.push('has not expired');

  if (reasons.length > 0) {
    logAction.debug('shouldFetchLineups - returned false', reasons);

    return false;
  }

  return true;
};

/**
 * Method to determine whether we need to fetch lineups.
 * Fetch if we are not already fetching.
 * @param  {object} state Current Redux state to test
 * @return {boolean}      True if we should fetch draft groups, false if not
 */
const shouldFetchLineupsRosters = (state) => {
  logAction.debug('actions.shouldFetchLineupsRosters');

  const reasons = [];
  const upcomingLineups = filter(state.currentLineups.items, (lineup) => new Date(lineup.start) >= dateNow());

  if (upcomingLineups.length === 0) reasons.push('no upcoming lineups');
  else if (!hasExpired(state.currentLineups.rostersExpireAt)) reasons.push('has not expired');

  if (reasons.length > 0) {
    logAction.debug('shouldFetchLineupsRosters - returned false', reasons, state);
    return false;
  }

  return true;
};


// primary methods (mainly exported, some needed in there to have proper init of const)

const fetchLineupsRostersIfNeeded = () => (dispatch, getState) => {
  logAction.debug('actions.fetchLineupsRostersIfNeeded()');

  const state = getState();

  if (!shouldFetchLineupsRosters(state)) {
    return Promise.resolve('No upcoming lineups, therefore no upcoming lineups needed');
  }

  return dispatch(
    fetchLineupsRosters()
  );
};

/**
 * Crazy method. After we finish GETting current lineups, we go and fetch each related contest.
 * Then that fetchContestLineupsIfNeeded() pulls in related draft groups, games, prizes.
 * This is a key method to the live/nav section, as it connects lineups will all of the related calls and needed info.
 * @return {promise}   Returns chainable promise that first gets contests (and therein draft groups + lineups), then
 *                     takes all that info and incorporates some of it back into lineups. Ends with updating redux store
 *                     with store.lineups.hasRelatedInfo = True so live/nav know to use the information.
 */
export const fetchRelatedLineupsInfo = () => (dispatch, getState) => {
  logAction.debug('actions.fetchRelatedLineupsInfo()');

  const state = getState();

  // if there are no lineups to watch, then reset
  if (!doesMyLineupExist(state)) return dispatch(resetWatchingAndPath());

  const calls = [];

  forEach(state.currentLineups.items, (lineup) => {
    const { contestsByPool, sport, draftGroup } = lineup;

    calls.push(dispatch(fetchDraftGroupIfNeeded(draftGroup, sport)));
    calls.push(dispatch(fetchGamesIfNeeded(sport)));

    // pull in contest pools
    Object.keys(contestsByPool).map((contestPoolId) => calls.push(dispatch(fetchContestPoolIfNeeded(contestPoolId))));

    // only pull contests for the lineup you are watching
    if (hasExpired(lineup.start)) {
      Object.keys(contestsByPool).map((poolId) => {
        const poolContests = contestsByPool[poolId];
        // pull relevant contests
        poolContests.map((contest) => calls.push(dispatch(fetchContestLineupsIfNeeded(contest, sport, poolId))));
      });
    }
  });

  // fetch upcoming lineups if needed
  calls.push(dispatch(fetchLineupsRostersIfNeeded()));

  // first fetch all contest information (which also gets draft groups, games, prizes)
  return Promise.all(
    calls

  // then associate rosters to their lineup
  ).then(
    () => dispatch(addLineupsPlayers())

  // then let's everyone know we're done
  ).then(
    () => dispatch(confirmRelatedLineupsInfo())
  );
};

/**
 * Outside facing method to go ahead and fetch lineups after checking whether we should
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchCurrentLineupsAndRelated = (force) => (dispatch, getState) => {
  logAction.debug('actions.fetchCurrentLineupsAndRelated()');

  if (shouldFetchLineups(getState()) === true || force === true) {
    return dispatch(
      fetchCurrentLineups()
    ).then(
      () => dispatch(fetchRelatedLineupsInfo())
    );
  }

  // otherwise just check on the related info
  return dispatch(fetchRelatedLineupsInfo());
};
