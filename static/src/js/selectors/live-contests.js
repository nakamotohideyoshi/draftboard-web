import { Buffer } from 'buffer/'
import { countBy as _countBy } from 'lodash'
import { createSelector } from 'reselect'
import { filter as _filter } from 'lodash'
import { forEach as _forEach } from 'lodash'
import { map as _map } from 'lodash'
import { sortBy as _sortBy } from 'lodash'
import { vsprintf } from 'sprintf-js'

import { generateLineupStats } from './current-lineups'
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
function rankContestLineups(contest, draftGroup, boxScores, prizeStructure) {
  log.debug('rankContestLineups')
  const lineups = contest.lineups

  let lineupsUsernames = {}
  if ('lineupsUsernames' in contest) {
    lineupsUsernames = contest.lineupsUsernames
  }

  let rankedLineups = []
  let lineupsStats = {}

  _forEach(lineups, (lineup, id) => {
    let stats = generateLineupStats(lineup, draftGroup, boxScores)

    if (id in lineupsUsernames) {
      stats['user'] = lineupsUsernames[id].user
    }

    rankedLineups.push(stats)
    lineupsStats[id] = stats
  })

  // sort then make just ID
  rankedLineups = _sortBy(rankedLineups, 'points').reverse()
  rankedLineups = _map(rankedLineups, (lineup) => {
    return lineup.id
  })

  // set standings for use in contests pane
  _forEach(rankedLineups, (lineupId, index) => {
    const lineupStats = lineupsStats[lineupId]

    lineupStats.rank = parseInt(index) + 1
    lineupStats.potentialEarnings = 0

    if (parseInt(index) in prizeStructure.ranks) {
      lineupStats.potentialEarnings = prizeStructure.ranks[index].value
    }
  })

  return {
    rankedLineups: rankedLineups,
    lineups: lineupsStats,
    hasLineupsUsernames: 'lineupsUsernames' in contest
  }
}


export const liveContestsStatsSelector = createSelector(
  state => state.liveContests,
  state => state.liveDraftGroups,
  state => state.currentBoxScores,
  state => state.prizes,
  state => state.entries.hasRelatedInfo,

  (contests, draftGroups, boxScores, prizes, hasRelatedInfo) => {
    if (hasRelatedInfo === false) {
      // log.debug('selectors.liveContestsStatsSelector() - not ready')
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

      stats = Object.assign(
        {},
        stats,
        rankContestLineups(contest, draftGroup, boxScores, prizeStructure)
      )

      contestsStats[id] = stats
    })

    log.debug('selectors.liveContestsStatsSelector() - updated')

    return contestsStats
  }
)
