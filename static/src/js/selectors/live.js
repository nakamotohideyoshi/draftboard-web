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
  state => state.liveDraftGroups,
  state => state.sports,

  (contestStats, currentLineupsStats, mode, hasRelatedInfo, playerBoxScoreHistory, liveDraftGroups, sports) => {
    let stats = {
      hasRelatedInfo: false,
      lineups: {},
      mode: mode,
      relevantGames: [],
      relevantPlayers: []
    }

    if (hasRelatedInfo === false) {
      log.trace('selectors.liveStatsSelector() - not ready')
      return stats
    }
    stats.hasRelatedInfo = true

    if (mode.myLineupId) {
      let myLineup = currentLineupsStats[mode.myLineupId]
      const sport = myLineup.draftGroup.sport

      // TODO move this into current lineups selector based on mode object
      _forEach(myLineup.rosterDetails, (player, playerId) => {
        if (playerBoxScoreHistory.nba.hasOwnProperty(playerId) === true) {
          player.seasonalStats = playerBoxScoreHistory.nba[playerId]
        }

        player.teamInfo = sports[sport].teams[player.info.team_srid]
      })

      stats.relevantGames = _union(stats.relevantGames, _map(myLineup.rosterDetails, (player) => {
        return player.info.game_srid
      }))

      stats.relevantPlayers = _union(stats.relevantPlayers, _map(myLineup.rosterDetails, (player) => {
        return player.info.player_srid
      }))


      // add in draft group to update player stats with pusher
      stats.draftGroup = liveDraftGroups[myLineup.draftGroup.id]


      if (mode.contestId) {
        let contest = contestStats[mode.contestId]
        myLineup.myWinPercent = myLineup.rank / contest.entriesCount * 100

        if (mode.opponentLineupId) {
          let opponentLineup = contest.lineups[mode.opponentLineupId]

          // TODO move this into current lineups selector based on mode object
          _forEach(opponentLineup.rosterDetails, (player, playerId) => {
            if (playerBoxScoreHistory.nba.hasOwnProperty(playerId) === true) {
              player.seasonalStats = playerBoxScoreHistory.nba[playerId]
            }

            player.teamInfo = sports[sport].teams[player.info.team_srid]
          })

          opponentLineup.opponentWinPercent = opponentLineup.rank / contest.entriesCount * 100

          // used for animations to determine which side
          opponentLineup.rosterBySRID = _map(opponentLineup.rosterDetails, (player) => {
            return player.info.player_srid
          })

          stats.relevantGames = _union(stats.relevantGames, _map(opponentLineup.rosterDetails, (player) => {
            return player.info.game_srid
          }))

          stats.relevantPlayers = _union(stats.relevantPlayers, _map(opponentLineup.rosterDetails, (player) => {
            return player.info.player_srid
          }))

          stats.playersInBothLineups = _.intersection(myLineup.rosterBySRID, opponentLineup.rosterBySRID)

          stats.lineups.opponent = opponentLineup
        }

        // update potential earnings of normal lineup
        myLineup.potentialEarnings = contest.lineups[mode.myLineupId].potentialEarnings

        stats.contest = contest
      }

      stats.lineups.mine = myLineup
    }




    log.debug('selectors.liveStatsSelector() - updated')

    return stats
  }
)

