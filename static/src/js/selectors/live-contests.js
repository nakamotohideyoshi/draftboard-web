import { Buffer } from 'buffer/'
import { countBy as _countBy } from 'lodash'
import { createSelector } from 'reselect'
import { filter as _filter } from 'lodash'
import { forEach as _forEach } from 'lodash'
import { map as _map } from 'lodash'
import { sortBy as _sortBy } from 'lodash'
import { vsprintf } from 'sprintf-js'

import log from '../lib/logging'


/*
 * Takes the contest lineups, converts each out of bytes, then adds up fantasy total
 *
 * @param {Object} (required) Original set of players from API
 * @param {Object} (required) Final, centralized associative array of players
 * @param {String} (required) Which lineup, mine or opponent?
 *
 * @return {Object, Object} Return the lineups, sorted highest to lowest points
 */
function rankContestLineups(lineups, draftGroup) {
  log.debug('rankContestLineups')
  let rankedLineups = []
  let lineupsStats = {}

  _forEach(lineups, (lineup, id) => {
    let stats = {
      id: id,
      points: updateFantasyPointsForLineup(lineup, draftGroup),
      potentialEarnings: '5.0'
    }

    rankedLineups.push(stats)
    lineupsStats[id] = stats
  })

  return {
    rankedLineups: _sortBy(rankedLineups, 'points').reverse(),
    stats: lineupsStats
  }
}


/**
 * Takes the lineup object, loops through the roster, and totals the fantasy points using the latest fantasy stats
 *
 * @param {Object} (required) The lineup object, containing id, roster and points
 * @param {Object} (required) Fantasy points object from API, has player array
 *
 * @return {Integer} Return the total points
 */
function updateFantasyPointsForLineup (lineup, draftGroup) {
  log.debug('_updateFantasyPointsForLineup')
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


export const liveContestsStatsSelector = createSelector(
  state => state.liveContests,
  state => state.liveDraftGroups,

  (contests, draftGroups) => {
    log.debug('selectors.liveContestsStatsSelector')

    var foo = _map(contests, (contest, id) => {
      let stats = {
        id: contest.id,
        start: contest.info.start
      }

      if (contest.start >= Date.now()) {
        return stats
      }

      stats = Object.assign({}, stats,
        rankContestLineups(contest.lineups, draftGroups[contest.info.draft_group])
      )

      return stats
    })

    return foo
  }
)
