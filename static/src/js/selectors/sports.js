import forEach from 'lodash/forEach';
import merge from 'lodash/merge';
import mapValues from 'lodash/mapValues';
import round from 'lodash/round';
import { createSelector } from 'reselect';
import ordinal from '../lib/ordinal';
import { SPORT_CONST } from '../actions/sports';


const currentGames = (state) => state.sports.games;


/**
 * The big scoreboard navigation selector that selects current lineups,
 * current draft groups, current user and some addition data for them.
 */
export const sportsSelector = createSelector(
  state => state.sports,
  (storeSports) => {
    // copy sports to add relevant data
    const sports = merge({}, storeSports);

    // add in game data
    forEach(sports.games, (game, gameId) => {
      const newGame = sports.games[gameId];
      const sport = game.sport;
      const sportConst = SPORT_CONST[sport];
      const teams = sports[sport].teams || {};

      // Add team information - In case we don't have team info yet, default to
      // an empty object so things don't die looking for properties.
      newGame.homeTeamInfo = teams[game.srid_home] || {};
      newGame.awayTeamInfo = teams[game.srid_away] || {};

      // update quarter to display properly
      if ('boxscore' in newGame) {
        let period = 1;

        switch (sport) {
          case 'nhl':
            period = round(newGame.boxscore.period, 0);

            if (period > sportConst.periods) {
              period = `${(period % sportConst.periods).toString()}OT`;

              if (period === '1OT') {
                period = 'OT';
              }
            }
            break;
          case 'nba':
          default:
            period = newGame.boxscore.quarter;
        }

        // If we have a period (the game has started), add an ordinal to it.
        if (period) {
          newGame.boxscore.periodDisplay = ordinal(period);
        } else {
          newGame.boxscore.periodDisplay = '';
        }
        newGame.start = new Date(game.start).getTime();
      }
    });

    return sports;
  }
);


export const gamesTimeRemainingSelector = createSelector(
  [currentGames],
  (games) => mapValues(games, 'timeRemaining')
);
