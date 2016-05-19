import {
  forEach as _forEach,
  merge as _merge,
  mapValues as _mapValues,
  round as _round,
} from 'lodash';
import { createSelector } from 'reselect';
import { GAME_DURATIONS } from '../actions/sports';


const currentGames = (state) => state.sports.games;


/**
 * The big scoreboard navigation selector that selects current lineups,
 * current draft groups, current user and some addition data for them.
 */
export const sportsSelector = createSelector(
  state => state.sports,
  (storeSports) => {
    // copy sports to add relevant data
    const sports = _merge({}, storeSports);

    // add in game data
    _forEach(sports.games, (game, gameId) => {
      const newGame = sports.games[gameId];
      const sport = game.sport;
      const sportConst = GAME_DURATIONS[sport];
      const teams = sports[sport].teams;

      // Add team information - In case we don't have team info yet, default to
      // an empty object so things don't die looking for properties.
      newGame.homeTeamInfo = teams[game.srid_home] || {};
      newGame.awayTeamInfo = teams[game.srid_away] || {};

      // update quarter to display properly
      if (newGame.hasOwnProperty('boxscore')) {
        let period = 1;

        switch (sport) {
          case 'nhl':
            period = _round(newGame.boxscore.period, 0);

            if (period > sportConst.periods) {
              period = `${(period % sportConst.periods).toString()}OT`;

              if (period === '1OT') {
                period = 'OT';
              }
            }
            break;
          case 'nba':
          default:
            period = _round(newGame.boxscore.quarter, 0);
        }

        newGame.boxscore.periodDisplay = period;
      }
    });

    return sports;
  }
);


export const gamesTimeRemainingSelector = createSelector(
  [currentGames],
  (games) => _mapValues(games, 'timeRemaining')
);
