import _ from 'lodash'
import { createSelector } from 'reselect'

import { currentLineupsStatsSelector } from './current-lineups'

/**
 * Returns hours for provided timestamp with format like: 7pm
 * @param {Number} timestamp
 * @return {String}
 */
export function getFormattedTime(timestamp) {
  let hours = new Date(timestamp).getHours()
  let time = (hours % 12 || 12) + (hours > 12 ? 'pm' : 'am')
  if(time == '12pm') time = '0am'

  return time
}

/**
 * The big scoreboard navigation selector that selects current lineups,
 * current draft groups, current user and some addition data for them.
 */
export const navScoreboardSelector = createSelector(
  currentLineupsStatsSelector,
  state => state.liveDraftGroups,
  state => state.currentBoxScores,
  state => state.sports,
  state => state.user,

  (lineups, draftGroups, boxScores, sports, user) => {
    const resultLineups = _.map(lineups, (lineup) => {
      return Object.assign(
        {},
        lineup,
        {
          time: getFormattedTime(lineup.start),
          contest: 'NBA' // TODO:
        }
      )
    })

    let resultDraftGroups = {}

    // if the sport data has loaded
    if (sports.nba.isFetchingTeams === false &&
        sports.nba.isFetchingGames === false) {

      const teams = sports.nba.teams
      const games = sports.nba.games

      // TODO make this dynamic based on schedule API response
      resultDraftGroups = {
        'nba': {
          sport: 'nba',
          boxScores: _.mapValues(games, (game, id) => {
            let newGame = Object.assign({}, game)

            // get team information
            newGame.homeTeamInfo = teams[game.srid_home]
            newGame.awayTeamInfo = teams[game.srid_away]

            // update quarter to display properly
            if (game.hasOwnProperty('boxscore')) {
              let quarter = _.round(game.boxscore.quarter, 0)

              if (quarter > 4 ) {
                quarter = (quarter % 4).toString() + 'OT'

                if (quarter === '1OT') {
                  quarter = 'OT'
                }
              }

              newGame.boxscore.quarterDisplay = quarter
            }

            return newGame
          })
        }
      }
    }

    return {
      // TODO: No user data.
      user: {
        name: user.name       || '-',
        balance: user.balance || '-'
      },
      gamesByDraftGroup: resultDraftGroups, // TODO:
      lineups: resultLineups
    }
  }
)
