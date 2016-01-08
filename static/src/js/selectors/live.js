import { countBy as _countBy } from 'lodash'
import { createSelector } from 'reselect'
import { filter as _filter } from 'lodash'
import { map as _map } from 'lodash'
import { reduce as _reduce } from 'lodash'
import { forEach as _forEach } from 'lodash'
import { union as _union } from 'lodash'

import log from '../lib/logging'


// Input Selectors
import { liveContestsStatsSelector } from './live-contests'
import { currentLineupsStatsSelector } from './current-lineups'


function addPlayersDetails(lineup) {
  const currentPlayers = {}
  _forEach(lineup.roster, (playerId) => {
    currentPlayers[playerId] = {
      id: playerId,
      info: lineup.draftGroup.playersInfo[playerId],
      stats: lineup.draftGroup.playersStats[playerId]
    }
  })

  return currentPlayers
}


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

  (contestStats, currentLineupsStats, mode, hasRelatedInfo) => {
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

      stats.relevantGames = _union(stats.relevantGames, _map(stats.lineups.mine.rosterDetails, (player) => {
        return player.info.game_srid
      }))

      stats.relevantPlayers = _union(stats.relevantPlayers, _map(stats.lineups.mine.rosterDetails, (player) => {
        return player.info.player_srid
      }))
    }

    if (mode.contestId) {
      stats.contest = contestStats[mode.contestId]

      // pull in rank
      stats.lineups.mine = Object.assign(
        {},
        stats.lineups.mine,
        stats.contest.lineups[mode.myLineupId]
      )

      if (mode.opponentLineupId) {
        stats.lineups.opponent = stats.contest.lineups[mode.opponentLineupId]

        stats.relevantGames = _union(stats.relevantGames, _map(stats.lineups.opponent.rosterDetails, (player) => {
          return player.info.game_srid
        }))

        stats.relevantPlayers = _union(stats.relevantPlayers, _map(stats.lineups.opponent.rosterDetails, (player) => {
          return player.info.player_srid
        }))
      }
    }



    log.debug('selectors.liveStatsSelector() - updated')

    return stats
  }
)

