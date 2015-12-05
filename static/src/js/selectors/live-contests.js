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
function rankContestLineups(lineups, draftGroup, prizeStructure) {
  log.debug('rankContestLineups')
  let rankedLineups = []
  let lineupsStats = {}

  _forEach(lineups, (lineup, id) => {
    let stats = {
      id: id,
      points: updateFantasyPointsForLineup(lineup, draftGroup),
      potentialEarnings: 0
    }

    rankedLineups.push(stats)
    lineupsStats[id] = stats
  })

  rankedLineups = _sortBy(rankedLineups, 'points').reverse()

  // set standings for use in contests pane
  _forEach(rankedLineups, (lineup, index) => {
    const lineupStats = lineupsStats[lineup.id]

    lineupStats.rank = parseInt(index) + 1

    if (parseInt(index) in prizeStructure.ranks) {
      lineupStats.potentialEarnings = prizeStructure.ranks[index].value
    }
  })

  return {
    rankedLineups: rankedLineups,
    entriesStats: lineupsStats
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
export function updateFantasyPointsForLineup (lineup, draftGroup) {
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
  state => state.prizes,
  state => state.entries.hasRelatedInfo,

  (contests, draftGroups, prizes, hasRelatedInfo) => {
    log.debug('selectors.liveContestsStatsSelector')

    if (hasRelatedInfo === false) {
      return {}
    }

    let contestsStats = {}

    _forEach(contests, (contest, id) => {
      const draftGroup = draftGroups[contest.info.draft_group]
      const prizeStructure = prizes[contest.info.prize_structure].info

      let stats = {
        id: contest.id,
        name: contest.info.name,
        start: contest.info.start,
        percentageCanWin: prizeStructure.payout_spots / contest.info.entries * 100,
        entriesCount: contest.info.entries,
        buyin: contest.info.buyin
      }

      if (contest.start >= Date.now()) {
        contestsStats[id] = stats
        return
      }


      stats = Object.assign({}, stats,
        rankContestLineups(contest.lineups, draftGroup, prizeStructure)
      )

      contestsStats[id] = stats
    })

    return contestsStats
  }
)
