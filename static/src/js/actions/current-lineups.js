import * as ActionTypes from '../action-types';
import filter from 'lodash/filter';
import forEach from 'lodash/forEach';
import log from '../lib/logging';
import { addMessage } from './message-actions';
import { CALL_API } from '../middleware/api';
import { camelizeKeys } from 'humps';  // TODO remove this once API calls are camel-cased
import { dateNow, hasExpired } from '../lib/utils';
import { fetchContestIfNeeded } from './live-contests';
import { fetchDraftGroupIfNeeded } from './live-draft-groups';
import { fetchGamesIfNeeded } from './sports';
import { Schema, arrayOf, normalize } from 'normalizr';


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
  log.trace('actions.lineups.addLineupsPlayers');

  const state = getState();
  const lineupsPlayers = {};

  // filter lineups to only those that have started
  const liveLineups = filter(state.currentLineups.items,
    (lineup) =>
      new Date(lineup.start) < dateNow() &&
      lineup.contests.length > 0
  );

  // only add players that have started playing, by checking if they are in the roster
  forEach(liveLineups, (lineup) => {
    // just choose the first contest
    const contestLineup = state.liveContests[lineup.contests[0]].lineups[lineup.id] || {};
    if (contestLineup.roster) {
      lineupsPlayers[lineup.id] = contestLineup.roster;
    }
  });

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
      return normalize(camelizedJson, arrayOf(lineupSchema)).entities;
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
    expiresAt: dateNow() + 1000 * 60 * 5,  // 5 minutes
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
  // fetch if expired
  if (hasExpired(state.currentLineups.expiresAt)) return false;

  // only fetch if not already fetching
  return state.currentLineups.isFetching === false;
};

/**
 * Method to determine whether we need to fetch lineups.
 * Fetch if we are not already fetching.
 * @param  {object} state Current Redux state to test
 * @return {boolean}      True if we should fetch draft groups, false if not
 */
const shouldFetchLineupsRosters = (state) => {
  const upcomingLineups = filter(state.currentLineups.items, (lineup) => new Date(lineup.start) >= dateNow());

  if (upcomingLineups.length === 0) return false;
  if (state.currentLineups.rostersExpireAt > dateNow()) return false;

  return true;
};


// primary methods (mainly exported, some needed in there to have proper init of const)

const fetchLineupsRostersIfNeeded = () => (dispatch, getState) => {
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
 * Then that fetchContestIfNeeded() pulls in related draft groups, games, prizes.
 * This is a key method to the live/nav section, as it connects lineups will all of the related calls and needed info.
 * @return {promise}   Returns chainable promise that first gets contests (and therein draft groups + lineups), then
 *                     takes all that info and incorporates some of it back into lineups. Ends with updating redux store
 *                     with store.lineups.hasRelatedInfo = True so live/nav know to use the information.
 */
export const fetchRelatedLineupsInfo = () => (dispatch, getState) => {
  log.info('actions.fetchRelatedLineupsInfo()');

  const calls = [];
  const state = getState();

  forEach(state.currentLineups.items, (lineup) => {
    const { contests, sport, draftGroup } = lineup;

    calls.push(dispatch(fetchDraftGroupIfNeeded(draftGroup, sport)));
    calls.push(dispatch(fetchGamesIfNeeded(sport)));

    // only pull contests for the lineup you are watching
    if (contests.length > 0 &&
        new Date(lineup.start).getTime() < dateNow() &&
        state.watching.myLineupId === lineup.id
    ) {
      contests.map(
        (contest) => calls.push(dispatch(fetchContestIfNeeded(contest, sport)))
      );
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
  )
  .catch((err) => {
    dispatch(addMessage({
      header: 'Failed to connect to API.',
      content: 'Please refresh the page to reconnect.',
      level: 'warning',
    }));
    log.error(err);
  });
};

/**
 * Outside facing method to go ahead and fetch lineups after checking whether we should
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchCurrentLineupsAndRelated = (force) => (dispatch, getState) => {
  if (shouldFetchLineups(getState()) === true || force === true) {
    log.info('actions.fetchCurrentLineupsIfNeeded() - Updating lineups');

    return dispatch(
      fetchCurrentLineups()
    ).then(
      () => dispatch(fetchRelatedLineupsInfo())
    )
    .catch((err) => {
      dispatch(addMessage({
        header: 'Failed to connect to API.',
        content: 'Please refresh the page to reconnect.',
        level: 'warning',
      }));
      log.error(err);
    });
  }

  return Promise.resolve('Lineups already fetched');
};
