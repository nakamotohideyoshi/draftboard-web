import * as ActionTypes from '../action-types';
import filter from 'lodash/filter';
import forEach from 'lodash/forEach';
import uniqBy from 'lodash/uniqBy';
import log from '../lib/logging';
import { CALL_API } from '../middleware/api';
import { camelizeKeys } from 'humps';  // TODO remove this once API calls are camel-cased
import { compose } from 'redux';
import { dateNow, hasExpired } from '../lib/utils';
import { fetchContestIfNeeded } from './live-contests';
import { fetchDraftGroupIfNeeded } from './live-draft-groups';
import { fetchGamesIfNeeded } from './sports';
import { Schema, arrayOf, normalize } from 'normalizr';
import { setCurrentLineups } from './current-lineups';


// normalizr schemas for this redux substore

const entrySchema = new Schema('entries', {
  idAttribute: 'id',
});
const entriesRostersSchema = new Schema('entriesRosters', {
  idAttribute: 'id',
});


// dispatch to reducer methods

/**
 * Dispatch information to reducer that we have completed getting all information related to the entries
 * Used to make the components aware tht we have finished pulling information.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const confirmRelatedEntriesInfo = () => ({
  type: ActionTypes.ENTRIES__RELATED_INFO_SUCCESS,
});

/**
 * Dispatch information to reducer that we have completed getting all information related to the entries
 * Used to make the components aware tht we have finished pulling information.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const storeEntriesPlayers = (entriesPlayers) => ({
  type: ActionTypes.ENTRIES__ADD_PLAYERS,
  entriesPlayers,
});


// helper methods


/**
 * The entries API call does not return the players in the entry's lineup.
 * This method loops through all entries. Any entry that is live, it then returns the related roster from its lineup.
 * @return {promise} Returns the object of rosters wrapped in dispatch wrapped in promise, so we can chain
 */
const addEntriesPlayers = () => (dispatch, getState) => {
  log.trace('actions.entries.addEntriesPlayers');

  const state = getState();
  const entriesPlayers = {};

  // filter entries to only those that have started
  const liveEntries = filter(state.entries.items, (entry) => new Date(entry.start) < dateNow());

  // only add players that have started playing, by checking if they are in the roster
  forEach(liveEntries, (entry) => {
    if (entry.contest === null) {
      log.warn('Entry has no contest', entry);
      return;
    }

    const lineup = state.liveContests[entry.contest].lineups[entry.lineup] || {};
    if (lineup.hasOwnProperty('roster')) {
      entriesPlayers[entry.id] = lineup.roster;
    }
  });

  // returning a promise such that we can chain this method
  return Promise.all([
    dispatch(storeEntriesPlayers(entriesPlayers)),
  ]);
};

/**
 * API GET to return live and upcoming (current) entries.
 * @return {promise}   Promise that resolves with API response body to reducer
 */
export const fetchCurrentEntries = () => ({
  [CALL_API]: {
    types: [
      ActionTypes.ENTRIES__REQUEST,
      ActionTypes.ENTRIES__RECEIVE,
      ActionTypes.ADD_MESSAGE,
    ],
    expiresAt: dateNow() + 1000 * 60 * 5,  // 5 minutes
    endpoint: '/api/contest/contest-pools/current-entries/',
    callback: (json) => {
      // TODO remove once this API stops returning past entries
      const yesterday = dateNow() - 1000 * 60 * 60 * 24;  // subtract 1 day

      // filters
      const yesterdayOrNewerFilter = (x) => filter(x, (entry) => new Date(entry.start).getTime() > yesterday);
      const noContestFilter = (x) => filter(x, (entry) => entry.contest === '');
      const withContestFilter = (x) => filter(x, (entry) => entry.contest !== '');
      const uniqEntries = (x) => uniqBy(x, 'lineup');

      // pare down to only the lineups we need
      const upcomingLineups = compose(yesterdayOrNewerFilter, noContestFilter, uniqEntries)(json);
      const liveLineups = compose(yesterdayOrNewerFilter, withContestFilter, uniqEntries)(json);
      const currentLineups = liveLineups.concat(upcomingLineups);

      // normalize and camelcase it
      const camelizedJson = camelizeKeys(currentLineups);
      return normalize(camelizedJson, arrayOf(entrySchema)).entities;
    },
  },
});

/**
 * Right, so when entries have upcoming contests, we need a way to pull in all upcoming lineups. This takes the upcoming
 * lineups, and then adds them to the associated entry.
 * @return {promise}          Promise that resolves with API response body to reducer
 */
export const fetchEntriesRosters = () => ({
  [CALL_API]: {
    types: [
      ActionTypes.ENTRIES_ROSTERS__REQUEST,
      ActionTypes.ENTRIES_ROSTERS__RECEIVE,
      ActionTypes.ADD_MESSAGE,
    ],
    expiresAt: dateNow() + 1000 * 60 * 5,  // 5 minutes
    endpoint: '/api/lineup/upcoming/',
    callback: (json) => {
      const camelizedJson = camelizeKeys(json);
      return normalize(camelizedJson, arrayOf(entriesRostersSchema)).entities;
    },
  },
});

/**
 * Generates object of objects of all the lineups related to the current entries, then returns a promise
 * @return {promise}   Promise that resolves with lineup information to lineup action, then to reducer
 */
export const generateLineups = () => (dispatch, getState) => {
  const lineups = {};

  forEach(getState().entries.items, (entry) => {
    const id = entry.lineup;

    if (lineups.hasOwnProperty(id)) {
      lineups[id].contests.push(entry.contest);
    } else {
      lineups[id] = {
        id: entry.lineup,
        draft_group: entry.draftGroup,
        name: entry.lineupName,
        start: new Date(entry.start).getTime(),
        roster: entry.roster,
        contests: [entry.contest],
      };
    }
  });

  // returning a promise such that we can chain this method
  return Promise.all([
    dispatch(setCurrentLineups(lineups)),
  ]);
};

/**
 * Method to determine whether we need to fetch entries.
 * Fetch if we are not already fetching.
 * @param  {object} state Current Redux state to test
 * @return {boolean}      True if we should fetch draft groups, false if not
 */
const shouldFetchEntries = (state) => {
  // fetch if expired
  if (hasExpired(state.entries.expiresAt)) return false;

  // only fetch if not already fetching
  return state.entries.isFetching === false;
};


// primary methods (mainly exported, some needed in there to have proper init of const)

const fetchEntriesRostersIfNeeded = () => (dispatch, getState) => {
  const upcomingEntries = filter(getState().entries.items, (entry) => new Date(entry.start) >= dateNow());

  if (upcomingEntries.length === 0) return Promise.resolve('No upcoming entries, therefore no upcoming lineups needed');

  return dispatch(
    fetchEntriesRosters()
  ).then(
    () => dispatch(generateLineups())
  );
};

/**
 * Crazy method. After we finish GETting current entries, we go and fetch each related contest.
 * Then that fetchContestIfNeeded() pulls in related draft groups, games, prizes.
 * This is a key method to the live/nav section, as it connects entries will all of the related calls and needed info.
 * @return {promise}   Returns chainable promise that first gets contests (and therein draft groups + lineups), then
 *                     takes all that info and incorporates some of it back into entries. Ends with updating redux store
 *                     with store.entries.hasRelatedInfo = True so live/nav know to use the information.
 */
export const fetchRelatedEntriesInfo = () => (dispatch, getState) => {
  log.info('actions.fetchRelatedEntriesInfo()');

  const calls = [];
  const state = getState();

  forEach(state.entries.items, (entry) => {
    const { contest, sport, draftGroup } = entry;

    calls.push(dispatch(fetchDraftGroupIfNeeded(draftGroup, sport)));
    calls.push(dispatch(fetchGamesIfNeeded(sport)));
    if (contest) calls.push(dispatch(fetchContestIfNeeded(contest, sport)));
  });

  // fetch upcoming lineups if needed
  calls.push(dispatch(fetchEntriesRostersIfNeeded()));

  // first fetch all contest information (which also gets draft groups, games, prizes)
  return Promise.all(
    calls

  // then associate rosters to their entry
  ).then(
    () => dispatch(addEntriesPlayers())

  // then stores related lineups
  ).then(
    () => dispatch(generateLineups())

  // then let's everyone know we're done
  ).then(
    () => dispatch(confirmRelatedEntriesInfo())
  );
};

/**
 * Outside facing method to go ahead and fetch entries after checking whether we should
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchCurrentEntriesAndRelated = (force) => (dispatch, getState) => {
  if (shouldFetchEntries(getState()) === true || force === true) {
    log.info('actions.fetchCurrentEntriesIfNeeded() - Updating entries');

    return dispatch(
      fetchCurrentEntries()
    ).then(
      () => dispatch(fetchRelatedEntriesInfo())
    );
  }

  return Promise.resolve('Entries already fetched');
};
