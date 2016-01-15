import { countBy as _countBy } from 'lodash'
import { createSelector } from 'reselect'
import { filter as _filter } from 'lodash'
import { map as _map } from 'lodash'
import { reduce as _reduce } from 'lodash'
import { forEach as _forEach } from 'lodash'
import { updateFantasyPointsForLineup } from './live-contests'

import log from '../lib/logging'
import { GAME_DURATIONS } from '../actions/current-box-scores'


// Input Selectors
import { liveContestsStatsSelector } from './live-contests'


function decimalRemaining(minutesRemaining, totalMinutes) {
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


function addPlayersDetails(lineup, draftGroup, boxScores) {
  const currentPlayers = {}

  _forEach(lineup.roster, (playerId) => {
    let player = {
      id: playerId,
      info: draftGroup.playersInfo[playerId]
    }

    const defaultStats = {
      fp: 0,
      minutesRemaining: GAME_DURATIONS.nba.gameMinutes,
      decimalRemaining: 0.01
    }

    player.stats = Object.assign(
      {},
      defaultStats,
      draftGroup.playersStats[playerId] || {}
    )

    // otherwise pull in accurate data from related game
    const game = boxScores[player.info.game_srid]
    if (game.hasOwnProperty('boxscore')) {
      player.stats.minutesRemaining = game.boxscore.timeRemaining || 1
      player.stats.decimalRemaining = decimalRemaining(player.stats.minutesRemaining, GAME_DURATIONS.nba.gameMinutes)
    }

    currentPlayers[playerId] = player
  })

  return currentPlayers
}


export function generateLineupStats(lineup, draftGroup, boxScores) {
  let stats = {
    id: lineup.id,
    name: lineup.name || 'Example Lineup Name',
    roster: lineup.roster,
    start: lineup.start,
    totalMinutes: lineup.roster.length * 48
  }

  if (lineup.start >= Date.now()) {
    return stats
  }

  stats.rosterDetails = addPlayersDetails(stats, draftGroup, boxScores)

  stats.points = _reduce(stats.rosterDetails, (fp, player) => {
    // only add if they have fantasy points in the first place
    if (isNaN(player.stats.fp)) {
      return fp
    }

    return fp + player.stats.fp
  }, 0)

  stats.minutesRemaining = _reduce(stats.rosterDetails, (timeRemaining, player) => {
    let minutesRemaining = player.stats.minutesRemaining || 1
    return timeRemaining + minutesRemaining
  }, 0)
  stats.decimalRemaining = decimalRemaining(stats.minutesRemaining, stats.totalMinutes)

  return stats
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

    // const liveLineups = _filter(lineups, function(lineup) {
    //   return lineup.start < Date.now()
    // })

    let liveLineupsStats = {}
    _forEach(lineups, (lineup) => {
      const draftGroup = liveDraftGroups[lineup.draft_group]

      if (lineup.start >= Date.parse(new Date())) {
        liveLineupsStats[lineup.id] = {
          id: lineup.id,
          name: lineup.name || 'Example Lineup Name',
          roster: lineup.roster,
          start: lineup.start,
          draftGroup: draftGroup,
          decimalRemaining: 0.01,
          minutesRemaining: 384,
          points: 0
        }

        return
      }

      let stats = generateLineupStats(lineup, draftGroup, currentBoxScores)
      stats.draftGroup = draftGroup

      // used for animations to determine which side
      stats.rosterBySRID = _map(stats.rosterDetails, (player) => {
        return player.info.player_srid
      })

      let totalPotentialEarnings = 0
      _forEach(entries, (entry) => {
        const contestLineups = contestsStats[entry.contest].lineups

        if (entry.lineup in contestLineups === true) {
          totalPotentialEarnings += contestsStats[entry.contest].lineups[entry.lineup].potentialEarnings
        }

        // otherwise this means that the contest is complete, TODO fix this with API calls!
      })
      stats.totalPotentialEarnings = totalPotentialEarnings
      stats.contestsStats = {}

      _forEach(lineup.contests, (contestId) => {
        const contest = liveContests[contestId]
        const contestStats = contestsStats[contestId]
        const entryStats = contestStats.lineups[lineup.id]

        stats.contestsStats[contestId] = Object.assign({}, contestStats, {
          currentPercentagePosition: (entryStats.rank - 1) / contest.info.entries * 100,
          rank: entryStats.rank
        })
      })

      liveLineupsStats[lineup.id] = stats
    })

    log.debug('selectors.currentLineupsStatsSelector() - updated')



    return liveLineupsStats
  }
)