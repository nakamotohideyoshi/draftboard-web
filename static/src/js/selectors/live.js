import { countBy as _countBy } from 'lodash'
import { createSelector } from 'reselect'
import { filter as _filter } from 'lodash'
import { map as _map } from 'lodash'
import { reduce as _reduce } from 'lodash'
import { forEach as _forEach } from 'lodash'
import { union as _union } from 'lodash'
import _ from 'lodash'

import log from '../lib/logging'


// Input Selectors
import { liveContestsStatsSelector } from './live-contests'
import { currentLineupsStatsSelector } from './current-lineups'


// returns:
// - If lineup mode:
//   - myLineup
//     - name
//     - points
//     - potential earnings
//     - pmr
//     - tmr
//
// - If contest mode:
//   - contestInfo
//     - title
//     - prize structure
//   - myLineup
//     - name
//     - contest title
//     - points (from lineup)
//     - standing
//       - find lineup in contest ranked lineups
//     - potential earnings
//       - use prize structure and standing
//     - pmr (from lineup)
//     - tmr (from lineup)
//   - opponentLineup
//     - points
//     - standing
//       - find lineup in contest ranked lineups
//     - potential earnings
//       - use prize structure and standing
//     - pmr
//     - tmr
export const liveSelector = createSelector(
  liveContestsStatsSelector,
  currentLineupsStatsSelector,
  state => state.live.mode,
  state => state.entries.hasRelatedInfo,
  state => state.playerBoxScoreHistory,

  (contestStats, currentLineupsStats, mode, hasRelatedInfo, playerBoxScoreHistory) => {
    if (hasRelatedInfo === false) {
      // log.debug('selectors.liveStatsSelector() - not ready')
      return {}
    }

    let stats = {
      lineups: {},
      relevantGames: [],
      relevantPlayers: []
    }

    if (mode.myLineupId) {
      stats.lineups.mine = currentLineupsStats[mode.myLineupId]

      // TODO move this into current lineups selector based on mode object
      _forEach(stats.lineups.mine.rosterDetails, (player, playerId) => {
        if (playerBoxScoreHistory.nba.hasOwnProperty(playerId) === true) {
          player.seasonalStats = playerBoxScoreHistory.nba[playerId]
        }
      })

      stats.relevantGames = _union(stats.relevantGames, _map(stats.lineups.mine.rosterDetails, (player) => {
        return player.info.game_srid
      }))

      stats.relevantPlayers = _union(stats.relevantPlayers, _map(stats.lineups.mine.rosterDetails, (player) => {
        return player.info.player_srid
      }))
    }

    if (mode.contestId) {
      stats.contest = contestStats[mode.contestId]

      if (mode.opponentLineupId) {
        stats.lineups.opponent = stats.contest.lineups[mode.opponentLineupId]

        // TODO move this into current lineups selector based on mode object
        _forEach(stats.lineups.opponent.rosterDetails, (player, playerId) => {
          if (playerBoxScoreHistory.nba.hasOwnProperty(playerId) === true) {
            player.seasonalStats = playerBoxScoreHistory.nba[playerId]
          }
        })

        // used for animations to determine which side
        stats.lineups.opponent.rosterBySRID = _map(stats.lineups.opponent.rosterDetails, (player) => {
          return player.info.player_srid
        })

        stats.relevantGames = _union(stats.relevantGames, _map(stats.lineups.opponent.rosterDetails, (player) => {
          return player.info.game_srid
        }))

        stats.relevantPlayers = _union(stats.relevantPlayers, _map(stats.lineups.opponent.rosterDetails, (player) => {
          return player.info.player_srid
        }))

        stats.playersInBothLineups = _.intersection(stats.lineups.mine.rosterBySRID, stats.lineups.opponent.rosterBySRID)
      }

      // update potential earnings of normal lineup
      stats.lineups.mine.potentialEarnings = stats.contest.lineups[mode.myLineupId].potentialEarnings
    }



    log.debug('selectors.liveStatsSelector() - updated')

    return stats
  }
)

