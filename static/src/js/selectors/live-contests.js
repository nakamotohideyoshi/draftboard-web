import { createSelector } from 'reselect'
import _ from 'lodash'

import { compileLineupStats } from './current-lineups'
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
function rankContestLineups(contest, draftGroup, games, prizeStructure, relevantPlayers) {
  const lineups = contest.lineups
  const lineupsUsernames = contest.lineupsUsernames || {}

  const lineupsStats = {}
  let rankedLineups = []

  _.forEach(lineups, (lineup, id) => {
    const stats = compileLineupStats(lineup, draftGroup, games, relevantPlayers)

    if (id in lineupsUsernames) {
      stats.user = lineupsUsernames[id].user
    }

    rankedLineups.push(stats)
    lineupsStats[id] = stats
  })

  // sort then make just ID
  rankedLineups = _.sortBy(rankedLineups, 'points').reverse()
  rankedLineups = _.map(rankedLineups, (lineup) => lineup.id)

  // set standings for use in contests pane
  _.forEach(rankedLineups, (lineupId, index) => {
    const lineupStats = lineupsStats[lineupId]

    lineupStats.rank = parseInt(index) + 1
    lineupStats.potentialEarnings = 0

    if ('ranks' in prizeStructure && parseInt(index) in prizeStructure.ranks) {
      lineupStats.potentialEarnings = prizeStructure.ranks[index].value
    }
  })

  return {
    rankedLineups,
    lineups: lineupsStats,
    hasLineupsUsernames: 'lineupsUsernames' in contest,
  }
}

/**
 * Redux reselect selector to compile all relevant information for contests
 */
export const liveContestsStatsSelector = createSelector(
  state => state.liveContests,
  state => state.liveDraftGroups,
  state => state.sports.games,
  state => state.prizes,
  state => state.entries.hasRelatedInfo,
  state => state.livePlayers.relevantPlayers,

  (contests, draftGroups, games, prizes, hasRelatedInfo, relevantPlayers) => {
    // do not show if we don't have data yet
    if (hasRelatedInfo === false) {
      return {}
    }

    const contestsStats = {}
    let prizeStructure = {}

    _.forEach(contests, (contest, id) => {
      // This seems to be a recurring issue. I believe it has something to do with the logged-in
      // user not having any lineups. For now we'll skip things if we don't have any contest.info.
      if (!contest.info) {
        log.warn('liveContestsStatsSelector - contest has no info', contest)
        return
      }

      const draftGroup = draftGroups[contest.info.draft_group]

      // Make sure we have the prize structure before adding it.
      if (prizes.hasOwnProperty(contest.info.prize_structure)) {
        prizeStructure = prizes[contest.info.prize_structure].info
      }

      const stats = {
        buyin: contest.info.buyin,
        entriesCount: contest.info.entries,
        id: contest.id,
        name: contest.info.name,
        percentageCanWin: prizeStructure.payout_spots / contest.info.entries * 100,
        start: contest.info.start,
      }

      if (contest.start < Date.now()) {
        contestsStats[id] = stats
        return
      }

      contestsStats[id] = Object.assign(
        stats,
        rankContestLineups(contest, draftGroup, games, prizeStructure, relevantPlayers)
      )
    })

    return contestsStats
  }
)
