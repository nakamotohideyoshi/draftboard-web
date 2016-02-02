import 'babel-core/polyfill'
const request = require('superagent-promise')(require('superagent'), Promise)
import _ from 'lodash'
import Cookies from 'js-cookie'
import { Buffer } from 'buffer/'

import * as ActionTypes from '../action-types'
import { fetchDraftGroupIfNeeded } from './live-draft-groups'
import { fetchPrizeIfNeeded } from './prizes'
import { fetchGamesIfNeeded } from './sports'


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
    updatedAt: Date.now(),
  },
})

/**
 * Dispatch information to reducer that we are trying to get contest lineups
 * Used to prevent repeat calls while requesting.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const requestContestLineups = (id) => ({
  id,
  type: ActionTypes.REQUEST_LIVE_CONTEST_LINEUPS,
})

/**
 * Dispatch information to reducer that we are trying to get contest information
 * Used to prevent repeat calls while requesting.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const requestContestInfo = (id) => ({
  id,
  type: ActionTypes.REQUEST_LIVE_CONTEST_INFO,
})

/**
 * Dispatch information to reducer that we are trying to get contest lineup usernames
 * Used to prevent repeat calls while requesting.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const requestContestLineupsUsernames = (id) => ({
  id,
  type: ActionTypes.REQUEST_LIVE_CONTEST_LINEUPS_USERNAMES,
})

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
  expiresAt: Date.now() + 86400000,
})

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
  expiresAt: Date.now() + 86400000,
})

/**
 * Dispatch API response object of contest lineups usernames to the store
 * NOTE: this method must be wrapped with dispatch()
 * @param  {number} id       Contest ID
 * @param  {object} response API response from server
 * @return {object}          Changes for reducer
 */
const receiveContestLineupsUsernames = (id, response) => {
  const lineupsUsernames = {}
  _.forEach(response, (lineup) => {
    lineupsUsernames[lineup.id] = {
      id: lineup.id,
      user: lineup.user,
    }
  })

  return {
    type: ActionTypes.RECEIVE_LIVE_CONTEST_LINEUPS_USERNAMES,
    id,
    lineupsUsernames,
    expiresAt: Date.now() + 86400000,
  }
}


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
    return new DataView(byteArray.buffer, byteOffset, byteLength).getInt32(0, false)
  } else if (byteSize === 16) {
    return new DataView(byteArray.buffer, byteOffset, byteLength).getInt16(0, false)
  }

  throw new Error('You must pass in a byteSize of 16 or 32')
}

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
  }

  // move from the ID to the start of the players
  const shiftedBytePosition = firstBytePosition + 4

  // loop through the players
  for (let i = shiftedBytePosition; i < shiftedBytePosition + numberOfPlayers * 2; i += 2) {
    // parse out 2 bytes for each player's value
    lineup.roster.push(convertToInt(16, byteArray, i, 2))
  }

  return lineup
}

/*
 * Takes the contest lineups, converts each out of bytes, then adds up fantasy total
 *
 * @param {Object} (required) Original set of players from API
 * @param {Object} (required) Final, centralized associative array of players
 * @param {String} (required) Which lineup, mine or opponent?
 *
 * @return {Object, Object} Return the lineups, sorted highest to lowest points
 */
const parseContestLineups = (apiContestLineupsBytes) => {
  // add up who's in what place
  const responseByteArray = new Buffer(apiContestLineupsBytes, 'hex')
  const lineups = {}

  // each lineup is 20 bytes long
  for (let i = 6; i < responseByteArray.length; i += 20) {
    const lineup = convertLineup(8, responseByteArray, i)

    lineups[lineup.id] = lineup
  }

  return lineups
}

/**
 * API GET to return lineups about a contest
 * NOTE this returns with hexidecimal bytes, which we then parse
 * @param {number} contestId  Contest ID
 * @return {promise}          Promise that resolves with API response body to reducer
 */
const fetchContestLineups = (id) => (dispatch) => {
  dispatch(requestContestLineups(id))

  return request.get(
    `/api/contest/all-lineups/${id}/`
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
  }).then(
    // NOTE we use res.text instead of res.body because the response is in hex bytes!
    (res) => dispatch(receiveContestLineups(id, res.text, parseContestLineups(res.text)))
  )
}

/**
 * API GET to return information about a contest
 * @param {number} contestId  Contest ID
 * @return {promise}          Promise that resolves with API response body to reducer
 */
const fetchContestInfo = (contestId) => (dispatch) => {
  dispatch(requestContestInfo(contestId))

  return request.get(
    `/api/contest/info/${contestId}/`
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    Accept: 'application/json',
  }).then(
    (res) => dispatch(receiveContestInfo(contestId, res.body))
  )
}

/**
 * API GET to return all the usernames for all the lineups in a contest.
 * Used in the live section for contest pane, and filtering by username
 * @param  {number} contestId  Contest ID
 * @return {promise}           Promise that resolves with API response body to reducer
 */
const fetchContestLineupsUsernames = (contestId) => (dispatch) => {
  dispatch(requestContestLineupsUsernames(contestId))

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
  )
}

/**
 * Method to determine whether we need to fetch a contest's lineup usernames.
 * @param  {object} state Current Redux state to test
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchContestLineupsUsernames = (state, id) => {
  // fetch if we have no data yet
  if (id in state.liveContests === false) {
    return true
  }

  // fetch if we have no usernames yet
  return 'lineupsUsernames' in state.liveContests[id] === false
}

/**
 * Method to determine whether we need to fetch a contest.
 * @param  {object} state Current Redux state to test
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchContest = (state, id) => {
  // if we have no data yet, fetch
  if (id in state.liveContests === false) {
    return true
  }

  // if we don't yet have lineups (as in not live), then fetch
  if ('lineupBytes' in state.liveContests[id] === false ||
      state.liveContests[id].lineupBytes === '') {
    return true
  }

  return false
}


// primary methods (mainly exported, some needed in there to have proper init of const)


/**
 * Outside facing method to go ahead and fetch usernames related to a contest after checking whether we should
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchContestLineupsUsernamesIfNeeded = (id) => (dispatch, getState) => {
  if (shouldFetchContestLineupsUsernames(getState(), id) === false) {
    return Promise.resolve('Contest usernames already exists')
  }

  return dispatch(fetchContestLineupsUsernames(id))
}

/**
 * Outside facing method to go ahead and fetch contest information after checking whether we should
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchRelatedContestInfo = (id) => (dispatch, getState) => {
  const contestInfo = getState().liveContests[id].info
  const draftGroupId = contestInfo.draft_group
  const prizeId = contestInfo.prize_structure
  const sport = contestInfo.sport

  return Promise.all([
    dispatch(fetchDraftGroupIfNeeded(draftGroupId)),
    dispatch(fetchGamesIfNeeded(sport)),
    dispatch(fetchPrizeIfNeeded(prizeId)),
  ]).then(() =>
    dispatch(confirmRelatedContestInfo(id))
  )
}

/**
 * Outside facing method to go ahead and fetch a contest after checking whether we should
 * Pulls both information and lineups, then gets related draft groups, games, prizes
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchContestIfNeeded = (id) => (dispatch, getState) => {
  if (shouldFetchContest(getState(), id) === false) {
    return Promise.resolve('Contest already exists')
  }

  return Promise.all([
    dispatch(fetchContestInfo(id)),
    dispatch(fetchContestLineups(id)),
  ]).then(() =>
    dispatch(fetchRelatedContestInfo(id))
  )
}
