import _ from 'lodash'
import { createSelector } from 'reselect'


/**
 * The big scoreboard navigation selector that selects current lineups,
 * current draft groups, current user and some addition data for them.
 */
export const sportsSelector = createSelector(
  state => state.sports,
  (storeSports) => {
    // copy sports to add relevant data
    const sports = Object.assign({}, storeSports)

    // add in game data
    _.forEach(sports.games, (game) => {
      const sport = game.sport
      const teams = sports[sport].teams

      // add team information
      game.homeTeamInfo = teams[game.srid_home]
      game.awayTeamInfo = teams[game.srid_away]

      // update quarter to display properly
      if (game.hasOwnProperty('boxscore')) {
        let quarter = _.round(game.boxscore.quarter, 0)

        if (quarter > 4) {
          quarter = `${(quarter % 4).toString()}OT`

          if (quarter === '1OT') {
            quarter = 'OT'
          }
        }

        game.boxscore.quarterDisplay = quarter
      }
    })

    return sports
  }
)
