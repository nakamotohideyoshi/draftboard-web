import { Buffer } from 'buffer/'
import { countBy as _countBy } from 'lodash'
import { createSelector } from 'reselect'
import { filter as _filter } from 'lodash'
import { forEach as _forEach } from 'lodash'
import { sortBy as _sortBy } from 'lodash'
import { vsprintf } from 'sprintf-js'


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
function _rankContestLineups(apiContestLineupsBytes, draftGroup) {
  log.debug('_rankContestLineups')

  // add up who's in what place
  let responseByteArray = new Buffer(apiContestLineupsBytes, 'hex')
  let lineups = []

  // each lineup is 20 bytes long
  for (let i=6; i < responseByteArray.length; i += 20) {
    let lineup = _convertLineup(8, responseByteArray, i)

    // potentially combine this with converting bytes to remove one loop, but then
    // each time we get updated fantasy points we'd have to make a different method to just do this part
    lineup.points = _updateFantasyPointsForLineup(lineup, draftGroup)

    // TODO make dynamic based on contest.info, talk to coderden about this
    lineup.potentialEarnings = '5.0'

    lineups.push(lineup)
  }

  return _sortBy(lineups, 'points').reverse()
}


/**
 * Takes the lineup object, loops through the roster, and totals the fantasy points using the latest fantasy stats
 *
 * @param {Object} (required) The lineup object, containing id, roster and points
 * @param {Object} (required) Fantasy points object from API, has player array
 *
 * @return {Integer} Return the total points
 */
function _updateFantasyPointsForLineup (lineup, draftGroup) {
  // log.debug('_updateFantasyPointsForLineup')
  let total = 0

  _forEach(lineup.roster, function(playerId) {
    if (playerId in draftGroup.playersStats === false) {
      log.error(vsprintf('_updateFantasyPointsForLineup() - player does not exist: %d', [playerId]))
      return 0
    }

    total += draftGroup.playersStats[playerId].fp
  })

  return total
}


// Input Selectors
const contestsSelector = (state) => state.contests
const draftGroupsSelector = (state) => state.liveDraftGroups


export const contestsStatsSelector = createSelector(
  [contestsSelector, draftGroupsSelector],
  (contests, draftGroups) => {
    return _map(contests, (contest, id) => {
      let stats = {
        id: contest.id,
        start: contest.start
      }

      if (contest.start >= Date.now()) {
        return stats
      }

      stats.rankedLineups = _rankLineups(contest.lineups, draftGroups[contest.draft_group])

      return stats
    })
  }
)
