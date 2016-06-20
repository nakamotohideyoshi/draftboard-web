const request = require('superagent-promise')(require('superagent'), Promise);
import * as ActionTypes from '../action-types';
import Cookies from 'js-cookie';
import map from 'lodash/map';
import zipObject from 'lodash/zipObject';
import log from '../lib/logging';
import { addMessage } from './message-actions';
import { Buffer } from 'buffer/';
import { dateNow } from '../lib/utils';
import { fetchPrizeIfNeeded } from './prizes';
import forEach from 'lodash/forEach';
import { SPORT_CONST } from '../actions/sports';


// dispatch to reducer methods

/**
 * Dispatch information to reducer that we have completed getting all information related to the contest
 * Used to make the selectors aware that we have finished pulling information.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const confirmRelatedContestInfo = (id) => ({
  type: ActionTypes.CONFIRM_RELATED_LIVE_CONTEST_INFO,
  id,
  stats: {
    updatedAt: dateNow(),
  },
});

/**
 * Dispatch information to reducer that we are trying to get contest lineups
 * Used to prevent repeat calls while requesting.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const requestContestLineups = (id) => ({
  id,
  type: ActionTypes.REQUEST_LIVE_CONTEST_LINEUPS,
});

/**
 * Dispatch information to reducer that we are trying to get contest information
 * Used to prevent repeat calls while requesting.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const requestContestInfo = (id) => ({
  id,
  type: ActionTypes.REQUEST_LIVE_CONTEST_INFO,
});

/**
 * Dispatch information to reducer that we are trying to get contest lineup usernames
 * Used to prevent repeat calls while requesting.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const requestContestLineupsUsernames = (id) => ({
  id,
  type: ActionTypes.REQUEST_LIVE_CONTEST_LINEUPS_USERNAMES,
});

/**
 * Dispatch API response object of contest lineups (in bytes and parsed json)
 * Also pass through an updated at so that we can expire and re-poll after a period of time.
 * NOTE: this method must be wrapped with dispatch()
 * @param  {number} id            Contest ID
 * @param  {bytes}  response      Binary hex of lineup bytes
 * @param  {object} parsedLineups Parsed lineups, generated from binary hex
 * @return {object}               Changes for reducer
 */
const receiveContestLineups = (id, response, parsedLineups) => ({
  type: ActionTypes.RECEIVE_LIVE_CONTEST_LINEUPS,
  id,
  lineupBytes: response,
  lineups: parsedLineups,
  expiresAt: dateNow() + 1000 * 60 * 60 * 24, // 1 day
});

/**
 * Dispatch API response object of contest information to the store
 * Also pass through an expires at so that we can re-poll after a period of time.
 * NOTE: this method must be wrapped with dispatch()
 * @param  {number} id       Contest ID
 * @param  {object} response API response from server
 * @return {object}          Changes for reducer
 */
const receiveContestInfo = (id, response) => ({
  type: ActionTypes.RECEIVE_LIVE_CONTEST_INFO,
  id,
  info: response,
  expiresAt: dateNow() + 1000 * 60 * 60 * 24, // 1 day
});

/**
 * Dispatch API response object of contest lineups usernames to the store
 * NOTE: this method must be wrapped with dispatch()
 * @param  {number} id       Contest ID
 * @param  {object} response API response from server
 * @return {object}          Changes for reducer
 */
const receiveContestLineupsUsernames = (id, response) => ({
  type: ActionTypes.RECEIVE_LIVE_CONTEST_LINEUPS_USERNAMES,
  id,
  lineupsUsernames: zipObject(
    map(response, (lineup) => lineup.id),
    map(response, (lineup) => lineup.user.username)
  ),
  expiresAt: dateNow() + 1000 * 60 * 60 * 24, // 1 day
});


// helper methods


/**
 * Converts big endian byte string of byteLength into an int
 *
 * @param {Integer} (required) Size of each byte, options are 16 or 32
 * @param {ByteArray} (required) Uint8Array of lineups
 * @param {Integer} (required) How many bytes in you should start parsing
 * @param {Integer} (required) The number of bytes to parse starting from byteOffset
 *
 * @return mixed
 */
const convertToInt = (byteSize, byteArray, byteOffset, byteLength) => {
  if (byteSize === 32) {
    return new DataView(byteArray.buffer, byteOffset, byteLength).getInt32(0, false);
  } else if (byteSize === 16) {
    return new DataView(byteArray.buffer, byteOffset, byteLength).getInt16(0, false);
  }

  throw new Error('You must pass in a byteSize of 16 or 32');
};

/**
 * Converts byte array into lineup object with id and roster
 *
 * @param {Integer} (required) Number of each players to parse out
 * @param {ByteArray} (required) Uint8Array of data
 * @param {Integer} (required) Where in the byte array should you start parsing data
 *
 * @return {Object} The parsed lineup object
 */
const convertLineup = (numberOfPlayers, byteArray, firstBytePosition) => {
  const lineup = {
    id: convertToInt(32, byteArray, firstBytePosition, 4),
    roster: [],
    total_points: '',
  };

  if (lineup.id === 0) {
    return null;
  }

  // move from the ID to the start of the players
  const shiftedBytePosition = firstBytePosition + 4;

  // loop through the players
  for (let i = shiftedBytePosition; i < shiftedBytePosition + numberOfPlayers * 2; i += 2) {
    // parse out 2 bytes for each player's value
    lineup.roster.push(convertToInt(16, byteArray, i, 2));
  }

  return lineup;
};

/*
 * Takes the contest lineups, converts each out of bytes, then adds up fantasy total
 *
 * @param {Object} (required) Original set of players from API
 * @param {Object} (required) Final, centralized associative array of players
 * @param {String} (required) Which lineup, mine or opponent?
 *
 * @return {Object, Object} Return the lineups, sorted highest to lowest points
 */
const parseContestLineups = (apiContestLineupsBytes, sport) => {
  // add up who's in what place
  const responseByteArray = new Buffer(apiContestLineupsBytes, 'hex');
  const lineups = {};
  const sportConst = SPORT_CONST[sport];

  // each lineup is 20 bytes long
  for (let i = 6; i < responseByteArray.length; i += sportConst.lineupByteLength) {
    const lineup = convertLineup(sportConst.players, responseByteArray, i);

    if (lineup !== null) {
      lineups[lineup.id] = lineup;
    }
  }

  return lineups;
};

/**
 * API GET to return lineups about a contest
 * NOTE this returns with hexidecimal bytes, which we then parse
 * @param {number} contestId  Contest ID
 * @return {promise}          Promise that resolves with API response body to reducer
 */
export const fetchContestLineups = (id, sport) => (dispatch) => {
  dispatch(requestContestLineups(id));

  return request.get(
    `/api/contest/all-lineups/${id}/`
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
  }).then(
    // NOTE we use res.text instead of res.body because the response is in hex bytes!
    (res) => dispatch(receiveContestLineups(id, res.text, parseContestLineups(res.text, sport)))
  );
};

/**
 * API GET to return information about a contest
 * @param {number} contestId  Contest ID
 * @return {promise}          Promise that resolves with API response body to reducer
 */
const fetchContestInfo = (contestId) => (dispatch) => {
  dispatch(requestContestInfo(contestId));

  return request.get(
    `/api/contest/info/${contestId}/`
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    Accept: 'application/json',
  }).then(
    (res) => dispatch(receiveContestInfo(contestId, res.body))
  );
};

/**
 * API GET to return all the usernames for all the lineups in a contest.
 * Used in the live section for contest pane, and filtering by username
 * @param  {number} contestId  Contest ID
 * @return {promise}           Promise that resolves with API response body to reducer
 */
const fetchContestLineupsUsernames = (contestId) => (dispatch) => {
  dispatch(requestContestLineupsUsernames(contestId));

  return request.post(
    '/api/lineup/usernames/'
  ).send({
    contest_id: contestId,
  }).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    'X-CSRFToken': Cookies.get('csrftoken'),
    Accept: 'application/json',
  }).then(
    (res) => dispatch(receiveContestLineupsUsernames(contestId, res.body))
  );
};

/**
 * Method to determine whether we need to fetch a contest's lineup usernames.
 * @param  {object} state Current Redux state to test
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchContestLineupsUsernames = (state, id) => {
  // fetch if we have no data yet
  if (state.liveContests.hasOwnProperty(id) === false) {
    return true;
  }

  // fetch if we have no usernames yet
  return state.liveContests[id].hasOwnProperty('lineupsUsernames') === false;
};

/**
 * Method to determine whether we need to fetch a contest.
 * @param  {object} state Current Redux state to test
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchContest = (liveContests, id) => {
  // if we have no data yet, fetch
  if (liveContests.hasOwnProperty(id) === false) {
    return true;
  }

  const contest = liveContests[id];

  if (contest.hasOwnProperty('info') === false) {
    return true;
  }

  // if it hasn't started yet, don't bother getting lineups yet
  if (new Date(contest.info.start).getTime() > dateNow()) {
    return false;
  }

  // if we don't yet have lineups (as in not live), then fetch
  if (contest.hasOwnProperty('lineupBytes') === true &&
      contest.lineupBytes !== '') {
    return false;
  }

  return true;
};


// primary methods (mainly exported, some needed in there to have proper init of const)


/**
 * Outside facing method to go ahead and fetch usernames related to a contest after checking whether we should
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchContestLineupsUsernamesIfNeeded = (id) => (dispatch, getState) => {
  if (shouldFetchContestLineupsUsernames(getState(), id) === false) {
    return Promise.resolve('Contest usernames already exists');
  }

  return dispatch(fetchContestLineupsUsernames(id));
};

/**
 * Outside facing method to go ahead and fetch contest information after checking whether we should
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchRelatedContestInfo = (id) => (dispatch, getState) => {
  const contestInfo = getState().liveContests[id].info;
  const prizeId = contestInfo.prize_structure;

  return Promise.all([
    dispatch(fetchPrizeIfNeeded(prizeId)),
  ])
  .then(() =>
    dispatch(confirmRelatedContestInfo(id))
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
 * Outside facing method to go ahead and fetch a contest after checking whether we should
 * Pulls both information and lineups, then gets related draft groups, games, prizes
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchContestIfNeeded = (id, sport, force) => (dispatch, getState) => {
  if (shouldFetchContest(getState().liveContests, id) === false && force !== true) {
    return dispatch(fetchRelatedContestInfo(id));
  }

  return Promise.all([
    dispatch(fetchContestInfo(id)),
    dispatch(fetchContestLineups(id, sport)),
  ])
  .then(() =>
    dispatch(fetchRelatedContestInfo(id))
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
 * Remove all contests that have ended.
 * @return {object}  Changes for reducer, wrapped in thunk
 */
export const removeUnusedContests = () => (dispatch, getState) => {
  const contestIds = [];

  forEach(getState().liveContests, (contest) => {
    const id = contest.id;

    // if there are no lineups the group is related to, then remove
    if (contest.expiresAt < dateNow()) {
      contestIds.push(id);
    }
  });

  if (contestIds.length === 0) return null;

  return dispatch({
    type: ActionTypes.REMOVE_LIVE_CONTESTS,
    ids: contestIds,
    removedAt: dateNow(),
  });
};
