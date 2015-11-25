"use strict"

import 'babel-core/polyfill'; // so I can use Promises
import request from 'superagent'
import { Buffer } from 'buffer/'
import { normalize, Schema, arrayOf } from 'normalizr'

import log from '../lib/logging'
import { fetchDraftGroupIfNeeded } from './live-draft-groups'
import { fetchPrizeIfNeeded } from './prizes'


export const CONFIRM_RELATED_LIVE_CONTEST_INFO = 'CONFIRM_RELATED_LIVE_CONTEST_INFO'
export const UPDATE_LIVE_CONTEST_STATS = 'UPDATE_LIVE_CONTEST_STATS'
export const REQUEST_LIVE_CONTEST_INFO = 'REQUEST_LIVE_CONTEST_INFO'
export const RECEIVE_LIVE_CONTEST_INFO = 'RECEIVE_LIVE_CONTEST_INFO'
export const REQUEST_LIVE_CONTEST_LINEUPS = 'REQUEST_LIVE_CONTEST_LINEUPS'
export const RECEIVE_LIVE_CONTEST_LINEUPS = 'RECEIVE_LIVE_CONTEST_LINEUPS'


// INTERNAL HELPER METHODS ----------------------------------------------

/**
 * Converts byte array into lineup object with id and roster
 *
 * @param {Integer} (required) Number of each players to parse out
 * @param {ByteArray} (required) Uint8Array of data
 * @param {Integer} (required) Where in the byte array should you start parsing data
 *
 * @return {Object} The parsed lineup object
 */
function _convertLineup(numberOfPlayers, byteArray, firstBytePosition) {
  log.debug('_convertLineup')

  let lineup = {
    'id': _convertToInt(32, byteArray, firstBytePosition, 4),
    'roster': [],
    'total_points': ''
  }

  // move from the ID to the start of the players
  firstBytePosition += 4

  // loop through the players
  for (let i = firstBytePosition; i < firstBytePosition + numberOfPlayers * 2; i += 2) {
    // parse out 2 bytes for each player's value
    lineup.roster.push(_convertToInt(16, byteArray, i, 2))
  }

  return lineup
}


/**
 * Converts big endian byte string of byteLength into an int
 *
 * @param {Integer} (required) Size of each byte, options are 16 or 32
 * @param {ByteArray} (required) Uint8Array of lineups
 * @param {Integer} (required) How many bytes in you should start parsing
 * @param {Integer} (required) The number of bytes to parse starting from byteOffset
 *
 * @return undefined
 */
function _convertToInt(byteSize, byteArray, byteOffset, byteLength) {
  if (byteSize === 32) {
    return new DataView(byteArray.buffer, byteOffset, byteLength).getInt32(0, false)
  } else if (byteSize === 16) {
    return new DataView(byteArray.buffer, byteOffset, byteLength).getInt16(0, false)
  } else {
    throw new Error('You must pass in a byteSize of 16 or 32')
  }
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
function parseContestLineups(apiContestLineupsBytes, draftGroup) {
  log.debug('_rankContestLineups')

  // add up who's in what place
  let responseByteArray = new Buffer(apiContestLineupsBytes, 'hex')
  let lineups = {}

  // each lineup is 20 bytes long
  for (let i=6; i < responseByteArray.length; i += 20) {
    let lineup = _convertLineup(8, responseByteArray, i)

    lineups[lineup.id] = lineup
  }

  return lineups
}



// CONTEST LINEUPS
// -----------------------------------------------------------------------

function requestContestLineups(id) {
  log.debug('actionsLiveContest.requestContestLineups')

  return {
    id: id,
    type: REQUEST_LIVE_CONTEST_LINEUPS
  }
}


function receiveContestLineups(id, response) {
  log.debug('actionsLiveContest.receiveContestLineups')

  return {
    type: RECEIVE_LIVE_CONTEST_LINEUPS,
    id: id,
    lineupBytes: response,
    lineups: parseContestLineups(response),
    expiresAt: Date.now() + 86400000
  }
}


function fetchContestLineups(id) {
  log.debug('actionsLiveContest.fetchContestLineups')

  return dispatch => {
    dispatch(requestContestLineups(id))

    request
      .get('/contest/all-lineups/' + id)
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .end(function(err, res) {
        if(err) {
          // TODO
        } else {
          dispatch(receiveContestLineups(id, res.text))
        }
    })
  }
}


// CONTEST INFO
// -----------------------------------------------------------------------

function requestContestInfo(id) {
  log.debug('actionsLiveContest.requestContestInfo')

  return {
    id: id,
    type: REQUEST_LIVE_CONTEST_INFO
  }
}


function receiveContestInfo(id, response) {
  log.debug('actionsLiveContest.receiveContestInfo')

  return {
    type: RECEIVE_LIVE_CONTEST_INFO,
    id: id,
    info: response,
    expiresAt: Date.now() + 86400000
  }
}


function fetchContestInfo(id) {
  log.debug('actionsLiveContest.fetchContestInfo')

  return dispatch => {
    dispatch(requestContestInfo(id))

    request
      .get('/api/contest/info/' + id + '/')
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          // TODO
        } else {
          dispatch(receiveContestInfo(id, res.body))
        }
    })
  }
}


function shouldFetchContest(state, id) {
  log.debug('actionsLiveContest.shouldFetchContest')

  return id in state.liveContests === false
}


export function fetchContestIfNeeded(id) {
  log.debug('actionsLiveContest.fetchContestIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchContest(getState(), id)) {
      return Promise.all([
        dispatch(fetchContestInfo(id)),
        dispatch(fetchContestLineups(id))
      ]).then(() => {
        dispatch(fetchRelatedContestInfo(id))
      })
    }
  }
}


function updateContestStats(id, rankedLineups) {
  return {
    type: UPDATE_LIVE_CONTEST_STATS,
    id: id,
    stats: {
      rankedLineups: rankedLineups,
      updatedAt: Date.now()
    }
  }
}


function confirmRelatedContestInfo(id) {
  return {
    type: CONFIRM_RELATED_LIVE_CONTEST_INFO,
    id: id,
    stats: {
      // rankedLineups: rankedLineups,
      updatedAt: Date.now()
    }
  }
}


export function fetchRelatedContestInfo(id) {
  log.debug('actionsLiveContest.fetchRelatedContestInfo')

  return (dispatch, getState) => {
    const contestInfo = getState().liveContests[id].info
    const draftGroupId = contestInfo.draft_group
    const prizeId = contestInfo.prize_structure

    return Promise.all([
      dispatch(fetchDraftGroupIfNeeded(draftGroupId)),
      dispatch(fetchPrizeIfNeeded(prizeId))
    ]).then(() => {
      dispatch(confirmRelatedContestInfo(id))
    })
  }
}
