import { countBy as _countBy } from 'lodash'
import { createSelector } from 'reselect'
import { filter as _filter } from 'lodash'
import { map as _map } from 'lodash'
import { reduce as _reduce } from 'lodash'
import { forEach as _forEach } from 'lodash'
import { updateFantasyPointsForLineup } from './live-contests'

import log from '../lib/logging'


// Input Selectors
import { liveContestsStatsSelector } from './live-contests'


export function decimalRemaining(minutesRemaining, totalMinutes) {
  let decimalRemaining = 1 - minutesRemaining / totalMinutes

  // trickery to prevent arc issues, TODO clean this up math-wise
  if (decimalRemaining === 1) {
    return 0.99
  }
  if (decimalRemaining === 0) {
    return 0.01
  }

  return decimalRemaining
}


function addPlayersDetails(lineup, boxScores) {
  const currentPlayers = {}

  _forEach(lineup.roster, (playerId) => {
    let player = {
      id: playerId,
      info: lineup.draftGroup.playersInfo[playerId],
      stats: lineup.draftGroup.playersStats[playerId]
    }

    if (player.stats === undefined) {
      player.stats = {}
    }

    const game = boxScores[player.info.game_srid]

    // if the game hasn't started, then give full minutes remaining
    let minutesRemaining = (game === undefined) ? 48 : game.timeRemaining

    player.stats.minutesRemaining = minutesRemaining
    player.stats.decimalRemaining = decimalRemaining(minutesRemaining, 48)

    currentPlayers[playerId] = player
  })

  return currentPlayers
}


// Crazy selector that
// - loops through the entries per lineup and calculates potential earnings
// - loops through the players per lineup and calculates PMR
export const currentLineupsStatsSelector = createSelector(
  liveContestsStatsSelector,
  state => state.liveContests,
  state => state.liveDraftGroups,
  state => state.currentBoxScores,
  state => state.entries.items,
  state => state.currentLineups.items,
  state => state.entries.hasRelatedInfo,

  (contestsStats, liveContests, liveDraftGroups, currentBoxScores, entries, lineups, hasRelatedInfo) => {

    if (hasRelatedInfo === false) {
      // log.debug('selectors.currentLineupsStatsSelector() - not ready')
      return {}
    }

    const liveLineups = _filter(lineups, function(lineup) {
      return lineup.start < Date.now()
    })

    let liveLineupsStats = {}
    _forEach(liveLineups, (lineup) => {
      const liveDraftGroup = liveDraftGroups[lineup.draft_group]

      let stats = {
        id: lineup.id,
        name: lineup.name,
        roster: lineup.roster,
        start: lineup.start,
        totalMinutes: lineup.roster.length * 48,
        draftGroup: liveDraftGroup,
        contestsStats: {}
      }

      if (lineup.start >= Date.now()) {
        liveLineupsStats[lineup.id] = stats
        return
      }

      stats.points = updateFantasyPointsForLineup(lineup, liveDraftGroup)

      let potentialEarnings = 0
      _forEach(entries, (entry) => {
        potentialEarnings += contestsStats[entry.contest].entriesStats[entry.lineup].potentialEarnings
      })
      stats.potentialEarnings = potentialEarnings

      _forEach(lineup.contests, (contestId) => {
        const contest = liveContests[contestId]
        const contestStats = contestsStats[contestId]
        const entryStats = contestStats.entriesStats[lineup.id]

        stats.contestsStats[contestId] = Object.assign({}, contestStats, {
          currentPercentagePosition: (entryStats.rank - 1) / contest.info.entries * 100,
          rank: entryStats.rank
        })
      })

      stats.rosterDetails = addPlayersDetails(stats, currentBoxScores)

      stats.minutesRemaining = _reduce(stats.rosterDetails, (timeRemaining, player) => {
        return timeRemaining + player.stats.minutesRemaining
      }, 0)
      stats.decimalRemaining = decimalRemaining(stats.minutesRemaining, stats.totalMinutes)

      liveLineupsStats[lineup.id] = stats
    })

    log.debug('selectors.currentLineupsStatsSelector() - updated')



    return liveLineupsStats
  }
)