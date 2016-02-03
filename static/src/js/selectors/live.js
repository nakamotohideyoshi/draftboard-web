import { createSelector } from 'reselect'
import _ from 'lodash'

import { liveContestsSelector } from './live-contests'
import { currentLineupsSelector } from './current-lineups'


/**
 * Fancy Redux reselect selector that compiles together relevant live information.
 * Returns an object with an architecture of:
 *
 * lineups
 *   mine
 *   opponent (optional)
 * contest
 */
export const liveSelector = createSelector(
  liveContestsSelector,
  currentLineupsSelector,
  state => state.live.mode,
  state => state.entries,
  state => state.playerBoxScoreHistory,
  state => state.liveDraftGroups,
  state => state.sports,

  (contestStats, currentLineupsStats, mode, entries, playerBoxScoreHistory, liveDraftGroups, sports) => {
    const uniqueEntries = _.uniq(_.values(entries.items), 'lineup')

    const stats = {
      hasRelatedInfo: false,
      lineups: {},
      mode,
      relevantGames: [],
      relevantPlayers: [],
    }

    if (_.size(entries.items) > 0) {
      stats.entries = uniqueEntries
    }

    if (entries.hasRelatedInfo === false) {
      return stats
    }
    stats.hasRelatedInfo = true

    if (mode.myLineupId) {
      const myLineup = currentLineupsStats[mode.myLineupId]
      const sport = myLineup.draftGroup.sport

      // add in seasonal stats, teams for LivePlayerPane
      _.forEach(myLineup.rosterDetails, (player, playerId) => {
        if (playerBoxScoreHistory.nba.hasOwnProperty(playerId) === true) {
          myLineup.rosterDetails[playerId].seasonalStats = playerBoxScoreHistory.nba[playerId]
        }

        myLineup.rosterDetails[playerId].teamInfo = sports[sport].teams[player.info.team_srid]
      })

      // combine relevant players, games to target pusher calls for animations
      stats.relevantGames = _.union(
        stats.relevantGames,
        _.map(myLineup.rosterDetails, (player) => player.info.game_srid)
      )
      stats.relevantPlayers = _.union(
        stats.relevantPlayers,
        _.map(myLineup.rosterDetails, (player) => player.info.player_srid)
      )


      // add in draft group to update player stats with pusher
      stats.draftGroup = liveDraftGroups[myLineup.draftGroup.id]


      if (mode.contestId) {
        const contest = contestStats[mode.contestId]

        myLineup.myWinPercent = 0
        if (myLineup.rank && contest.entriesCount) {
          myLineup.myWinPercent = myLineup.rank / contest.entriesCount * 100
        }

        if (mode.opponentLineupId) {
          const opponentLineup = contest.lineups[mode.opponentLineupId]

          _.forEach(opponentLineup.rosterDetails, (player, playerId) => {
            if (playerBoxScoreHistory.nba.hasOwnProperty(playerId) === true) {
              opponentLineup.rosterDetails[playerId].seasonalStats = playerBoxScoreHistory.nba[playerId]
            }

            opponentLineup.rosterDetails[playerId].teamInfo = sports[sport].teams[player.info.team_srid]
          })

          opponentLineup.opponentWinPercent = opponentLineup.rank / contest.entriesCount * 100

          // used for animations to determine which side
          opponentLineup.rosterBySRID = _.map(opponentLineup.rosterDetails, (player) => player.info.player_srid)

          stats.relevantGames = _.union(
            stats.relevantGames,
            _.map(opponentLineup.rosterDetails, (player) => player.info.game_srid)
          )
          stats.relevantPlayers = _.union(
            stats.relevantPlayers,
            _.map(opponentLineup.rosterDetails, (player) => player.info.player_srid)
          )
          stats.playersInBothLineups = _.intersection(myLineup.rosterBySRID, opponentLineup.rosterBySRID)
          stats.lineups.opponent = opponentLineup
        }

        // update potential earnings of normal lineup
        myLineup.potentialEarnings = contest.lineups[mode.myLineupId].potentialEarnings

        stats.contest = contest
      }

      stats.lineups.mine = myLineup
    }

    return stats
  }
)
