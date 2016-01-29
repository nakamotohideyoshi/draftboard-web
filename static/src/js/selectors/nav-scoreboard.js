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
  state => state.sports,
  state => state.user,

  (storeLineups, draftGroups, storeSports, user) => {
    const lineups = _.map(storeLineups, (lineup) => {
      return Object.assign(
        {},
        lineup,
        {
          time: getFormattedTime(lineup.start),
          contest: 'NBA' // TODO:
        }
      )
    })

    // copy sports to add relevant data
    let sports = Object.assign({}, storeSports)

    // add in game data
    _.forEach(sports.games, (game, id) => {
      const sport = game.sport
      const teams = sports[sport].teams

      // add team information
      game.homeTeamInfo = teams[game.srid_home]
      game.awayTeamInfo = teams[game.srid_away]

      // update quarter to display properly
      if (game.hasOwnProperty('boxscore')) {
        let quarter = _.round(game.boxscore.quarter, 0)

        if (quarter > 4 ) {
          quarter = (quarter % 4).toString() + 'OT'

          if (quarter === '1OT') {
            quarter = 'OT'
          }
        }

        game.boxscore.quarterDisplay = quarter
      }
    })

    return {
      user: {
        name: user.name       || '-',
        balance: user.balance || '-'
      },
      sports: sports,
      lineups: lineups
    }
  }
)
