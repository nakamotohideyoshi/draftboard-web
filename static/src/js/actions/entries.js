const request = require('superagent-promise')(require('superagent'), Promise);

import filter from 'lodash/filter';
import forEach from 'lodash/forEach';
import map from 'lodash/map';
import merge from 'lodash/merge';
import { normalize, Schema, arrayOf } from 'normalizr';
import { fetchDraftGroupIfNeeded } from './live-draft-groups';
import { fetchGamesIfNeeded } from './sports';

import { dateNow } from '../lib/utils';
import * as ActionTypes from '../action-types';
import log from '../lib/logging';
import { fetchContestIfNeeded } from './live-contests';
import { setCurrentLineups } from './current-lineups';


// dispatch to reducer methods


/**
 * Dispatch information to reducer that we have completed getting all information related to the entries
 * Used to make the components aware tht we have finished pulling information.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const confirmRelatedEntriesInfo = () => ({
  type: ActionTypes.CONFIRM_RELATED_ENTRIES_INFO,
});

/**
 * Dispatch API response object of current entries to the store
 * Also pass through an updated at so that we can expire and re-poll after a period of time.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const receiveEntries = (response) => {
  const yesterday = dateNow() - 1000 * 60 * 60 * 24;  // subtract 1 day
  const filteredResponse = filter(response, (entry) => new Date(entry.start) > yesterday);
  // const withContest = filter(filteredResponse, (entry) =>
  //   new Date(entry.start).getTime() > dateNow() || entry.contest !== null
  // );
  const withDefaultName = map(filteredResponse, (entry) => merge({
    lineup_name: 'My Lineup',
  }, entry));

  // normalize the API call into a list of entry objects
  const entriesSchema = new Schema('entries', {
    idAttribute: 'id',
  });
  const normalizedEntries = normalize(
    withDefaultName,
    arrayOf(entriesSchema)
  );
  const entries = normalizedEntries.entities.entries;

  return {
    type: ActionTypes.RECEIVE_ENTRIES,
    items: entries || [],
    expiresAt: dateNow() + 1000 * 60 * 5,  // 5 minutes
  };
};

/**
 * Dispatch API response object of upcoming lineups to parse into entries
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const receiveUpcomingLineups = (response) => {
  // normalize the API call into a list of entry objects
  const lineupsSchema = new Schema('lineups', {
    idAttribute: 'id',
  });
  const normalizedLineups = normalize(
    response,
    arrayOf(lineupsSchema)
  );

  return {
    type: ActionTypes.RECEIVE_ENTRIES_UPCOMING_LINEUPS,
    lineups: normalizedLineups.entities.lineups,
    expiresAt: dateNow() + 1000 * 60,  // 1 minute
  };
};

/**
 * Dispatch information to reducer that we are trying to get current entries
 * Used to prevent repeat calls while requesting.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const requestEntries = () => ({
  type: ActionTypes.REQUEST_ENTRIES,
  expiresAt: dateNow() + 1000 * 60,  // 1 minute
});

/**
 * Dispatch information to reducer that we have completed getting all information related to the entries
 * Used to make the components aware tht we have finished pulling information.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const storeEntriesPlayers = (entriesPlayers) => ({
  type: ActionTypes.ADD_ENTRIES_PLAYERS,
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

    const lineup = state.liveContests[entry.contest].lineups[entry.lineup];
    if (typeof lineup !== 'undefined' && lineup.hasOwnProperty('roster')) {
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
const fetchEntries = () => (dispatch) => {
  dispatch(requestEntries());

  return request.get(
    '/api/contest/contest-pools/current-entries/'
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    Accept: 'application/json',
  }).then(
    (res) => dispatch(receiveEntries(res.body))
  );
};

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
        draft_group: entry.draft_group,
        name: entry.lineup_name,
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
  if (dateNow() < state.entries.expiresAt) {
    return false;
  }

  // only fetch if not already fetching
  return state.entries.isFetching === false;
};


// primary methods (mainly exported, some needed in there to have proper init of const)


/**
 * Right, so when entries have upcoming contests, we need a way to pull in all upcoming lineups. This takes the upcoming
 * lineups, and then adds them to the associated entry.
 * @return {promise}          Promise that resolves with API response body to reducer
 */
export const fetchUpcomingLineups = () => (dispatch) =>
  request.get(
    '/api/lineup/upcoming/'
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',

  // then associate rosters to their entries
  }).then(
    (res) => dispatch(receiveUpcomingLineups(res.body))

  // then stores related lineups
  ).then(() =>
    dispatch(generateLineups())
  );

/**
 * Crazy method. After we finish GETting current entries, we go and fetch each related contest.
 * Then that fetchContestIfNeeded() pulls in related draft groups, games, prizes.
 * This is a key method to the live/nav section, as it connects entries will all of the related calls and needed info.
 * @return {promise}   Returns chainable promise that first gets contests (and therein draft groups + lineups), then
 *                     takes all that info and incorporates some of it back into entries. Ends with updating redux store
 *                     with store.entries.hasRelatedInfo = True so live/nav know to use the information.
 */
export const fetchRelatedEntriesInfo = () => (dispatch, getState) => {
  const calls = [];

  forEach(getState().entries.items, (entry) => {
    if (entry.hasOwnProperty('contest') && entry.contest !== null) {
      calls.push(dispatch(fetchContestIfNeeded(entry.contest, entry.sport)));
    }
    calls.push(dispatch(fetchDraftGroupIfNeeded(entry.draft_group, entry.sport)));
    calls.push(dispatch(fetchGamesIfNeeded(entry.sport)));
  });

  // first fetch all contest information (which also gets draft groups, games, prizes)
  return Promise.all(
    calls

  // then associate rosters to their entry
  ).then(() =>
    dispatch(addEntriesPlayers())

  // then stores related lineups
  ).then(() =>
    dispatch(generateLineups())

  // then let's everyone know we're done
  ).then(() =>
    dispatch(confirmRelatedEntriesInfo())
  );
};

/**
 * Outside facing method to go ahead and fetch entries after checking whether we should
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchEntriesIfNeeded = (force) => (dispatch, getState) => {
  if (shouldFetchEntries(getState()) === true || force === true) {
    log.info('actions.fetchEntriesIfNeeded() - Updating entries');

    return dispatch(
      fetchEntries()
    ).then(() =>
      dispatch(fetchRelatedEntriesInfo())
    );
  }

  return Promise.resolve('Entries already fetched');
};

/**
 * Once an entry is created, the server returns it to us in Entry object form. We then need to
 * stuff it into our entries store via receiveEntries().
 * @return {func}   Thunk wrapped data
 */
export const insertEntry = (entry) => (dispatch) => dispatch(receiveEntries([entry]));
