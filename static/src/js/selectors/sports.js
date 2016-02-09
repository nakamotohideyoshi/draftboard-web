import _ from 'lodash';
import { createSelector } from 'reselect';


/**
 * The big scoreboard navigation selector that selects current lineups,
 * current draft groups, current user and some addition data for them.
 */
export const sportsSelector = createSelector(
  state => state.sports,
  (storeSports) => {
    // copy sports to add relevant data
    const sports = Object.assign({}, storeSports);

    // add in game data
    _.forEach(sports.games, (game, gameId) => {
      const newGame = sports.games[gameId];
      const sport = game.sport;
      const teams = sports[sport].teams;

      // add team information
      newGame.homeTeamInfo = teams[game.srid_home];
      newGame.awayTeamInfo = teams[game.srid_away];

      // update quarter to display properly
      if (newGame.hasOwnProperty('boxscore')) {
        let quarter = _.round(newGame.boxscore.quarter, 0);

        if (quarter > 4) {
          quarter = `${(quarter % 4).toString()}OT`;

          if (quarter === '1OT') {
            quarter = 'OT';
          }
        }

        newGame.boxscore.quarterDisplay = quarter;
      }
    });

    return sports;
  }
);
