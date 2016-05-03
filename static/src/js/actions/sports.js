const request = require('superagent-promise')(require('superagent'), Promise);
import * as ActionTypes from '../action-types';
import { dateNow } from '../lib/utils';
import { forEach as _forEach } from 'lodash';
import { filter as _filter } from 'lodash';
import { map as _map } from 'lodash';
import { merge as _merge } from 'lodash';
import { sortBy as _sortBy } from 'lodash';
import log from '../lib/logging';


// global constants


// constant related to game durations
export const GAME_DURATIONS = {
  nba: {
    gameDuration: 48,
    lineupByteLength: 20,
    periodMinutes: 12,
    periods: 4,
    players: 8,
    seasonStats: {
      types: ['fp', 'points', 'rebounds', 'assists', 'steals', 'blocks', 'turnovers'],
      names: ['FPPG', 'PPG', 'RPG', 'APG', 'STLPG', 'BLKPG', 'TOPG'],
    },
  },
  nhl: {
    gameDuration: 60,
    lineupByteLength: 20,
    periodMinutes: 20,
    periods: 3,
    players: 8,
    seasonStats: {
      types: ['saves', 'assist', 'sog', 'fp', 'goal', 'blk'],
      names: ['S', 'A', 'SOG', 'FP', 'G', 'BLK'],
    },
  },
  mlb: {
    // total half innings, or innings * 2
    gameDuration: 18,
    lineupByteLength: 22,
    players: 9,
    pitchOutcomes: {
      aBK: 'Balk',
      aCI: 'Catcher Interference',
      aD: 'Double',
      aDAD3: 'Double - Adv 3rd',
      aDAD4: 'Double - Adv Home',
      aFCAD2: 'Fielders Choice - Adv 2nd ',
      aFCAD3: 'Fielders Choice - Adv 3rd ',
      aFCAD4: 'Fielders Choice - Adv Home ',
      aHBP: 'Hit By Pitch',
      aHR: 'Homerun',
      aKLAD1: 'Strike Looking - Adv 1st ',
      aKLAD2: 'Strike Looking - Adv 2nd ',
      aKLAD3: 'Strike Looking - Adv 3rd ',
      aKLAD4: 'Strike Looking - Adv Home ',
      aKSAD1: 'Strike Swinging - Adv 1st ',
      aKSAD2: 'Strike Swinging - Adv 2nd',
      aKSAD3: 'Strike Swinging - Adv 3rd ',
      aKSAD4: 'Strike Swinging - Adv Home ',
      aROE: 'Reached On Error',
      aROEAD2: 'Reached On Error - Adv 2nd ',
      aROEAD3: 'Reached On Error - Adv 3rd ',
      aROEAD4: 'Reached On Error - Adv Home ',
      aS: 'Single',
      aSAD2: 'Single - Adv 2nd',
      aSAD3: 'Single - Adv 3rd',
      aSAD4: 'Single - Adv Home',
      aSBAD1: 'Sacrifice Bunt - Adv 1st ',
      aSBAD2: 'Sacrifice Bunt - Adv 2nd ',
      aSBAD3: 'Sacrifice Bunt - Adv 3rd ',
      aSBAD4: 'Sacrifice Bunt - Adv Home ',
      aSFAD1: 'Sacrifice Fly - Adv 1st ',
      aSFAD2: 'Sacrifice Fly - Adv 2nd ',
      aSFAD3: 'Sacrifice Fly - Adv 3rd ',
      aSFAD4: 'Sacrifice Fly - Adv Home ',
      aT: 'Triple',
      aTAD4: 'Triple - Adv Home',
      bB: 'Ball',
      bDB: 'Dirt Ball',
      bIB: 'Intentional Ball',
      bPO: 'Pitchout',
      kF: 'Foul Ball',
      kFT: 'Foul Tip',
      kKL: 'Strike Looking',
      kKS: 'Strike Swinging',
      oBI: 'Hitter Interference',
      oDT3: 'Double - Out at 3rd ',
      oDT4: 'Double - Out at Home ',
      oFC: 'Fielders Choice',
      oFCT2: 'Fielders Choice - Out at 2nd ',
      oFCT3: 'Fielders Choice - Out at 3rd ',
      oFCT4: 'Fielders Choice - Out at Home ',
      oFO: 'Fly Out',
      oGO: 'Ground Out',
      oKLT1: 'Strike Looking - Out at 1st',
      oKLT2: 'Strike Looking - Out at 2nd',
      oKLT3: 'Strike Looking - Out at 3rd',
      oKLT4: 'Strike Looking - Out at Home ',
      oKST1: 'Strike Swinging - Out at 1st ',
      oKST2: 'Strike Swinging - Out at 2nd ',
      oKST3: 'Strike Swinging - Out at 3rd ',
      oKST4: 'Strike Swinging - Out at Home ',
      oLO: 'Line Out',
      oOBB: 'Out of Batters Box',
      oOP: 'Out on Appeal',
      oPO: 'Pop Out',
      oROET2: 'Reached On Error - Out at 2nd ',
      oROET3: 'Reached On Error - Out at 3rd ',
      oROET4: 'Reached On Error - Out at Home ',
      oSB: 'Sacrifice Bunt',
      oSBT2: 'Sacrifice Bunt - Out at 2nd',
      oSBT3: 'Sacrifice Bunt - Out at 3rd ',
      oSBT4: 'Sacrifice Bunt - Out at Home ',
      oSF: 'Sacrifice Fly',
      oSFT2: 'Sacrifice Fly - Out at 2nd ',
      oSFT3: 'Sacrifice Fly - Out at 3rd ',
      oSFT4: 'Sacrifice Fly - Out at Home ',
      oST2: 'Single - Out at 2nd',
      oST3: 'Single - Out at 3rd ',
      oST4: 'Single - Out at Home ',
      oTT4: 'Triple - Out at Home',
    },
    runnerOutcomes: {
      CK: 'Checked',
      ERN: 'Earned Run/RBI',
      eRN: 'Earned Run/No RBI',
      URN: 'Unearned Run/RBI',
      uRN: 'Unearned Run/No RBI',
      PO: 'Pickoff',
      POCS2: 'Pickoff/Caught Stealing 2nd ',
      POCS3: 'Pickoff/Caught Stealing 3nd ',
      POCS4: 'Pickoff/Caught Stealing Home ',
      AD1: 'Advance 1st',
      AD2: 'Advance 2nd',
      AD3: 'Advance 3rd',
      SB2: 'Stole 2nd',
      SB3: 'Stole 3rd',
      SB4: 'Stole Home',
      TO2: 'Tag out 2nd',
      TO3: 'Tag out 3rd',
      TO4: 'Tag out Home',
      FO1: 'Force out 1st',
      FO2: 'Force out 2nd',
      FO3: 'Force out 3rd',
      FO4: 'Force out Home',
      CS2: 'Caught Stealing 2nd',
      CS3: 'Caught Stealing 3rd',
      CS4: 'Caught Stealing Home',
      SB2E3: 'Stole 2nd, error to 3rd',
      SB2E4: 'Stole 2nd, error to Home ',
      SB3E4: 'Stole 3nd, error to Home',
      DI2: 'Indifference to 2nd',
      DI3: 'Indifference to 3rd',
      DO1: 'Doubled off 1st',
      DO2: 'Doubled off 2nd',
      DO3: 'Doubled off 3rd',
      RI: 'Runner Interference',
      OOA: 'Out on Appeal',
      OBP: 'Out of Base Path',
      HBB: 'Hit by Batted Ball',
    },
    seasonStats: {
      types: [],
      names: [],
    },
  },
};


// dispatch to reducer methods


/**
 * Dispatch information to reducer that we are trying to get games
 * Used to prevent repeat calls while requesting.
 * NOTE: Set expires to 30 sec when retrieve, and then set again with receive, that way if gets stuck it unfreezes
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const requestGames = (sport) => ({
  sport,
  type: ActionTypes.REQUEST_GAMES,
  expiresAt: dateNow() + 1000 * 60,  // 1 minute
});

/**
 * Dispatch information to reducer that we are trying to get teams
 * Used to prevent repeat calls while requesting.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const requestTeams = (sport) => ({
  sport,
  type: ActionTypes.REQUEST_TEAMS,
  expiresAt: dateNow() + 1000 * 60,  // 1 minute
});

/**
 * Dispatch parsed API information related to relevant games
 * Also pass through an updated at so that we can expire and re-poll after a period of time.
 * NOTE: this method must be wrapped with dispatch()
 * @param  {string} sport  Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @param  {object} games  Object of games
 * @return {object}        Changes for reducer
 */
const receiveGames = (sport, games) => {
  const doneStatuses = ['closed', 'complete'];

  const gamesCompleted = _map(
    _sortBy(
      _filter(
        games, (game) => game.hasOwnProperty('boxscore') && doneStatuses.indexOf(game.boxscore.status) !== -1
      ),
      (filteredGame) => filteredGame.start
    ),
    (sortedGame) => sortedGame.srid
  );

  const gamesNotCompleted = _map(
    _sortBy(
      _filter(
        games, (game) => gamesCompleted.indexOf(game.srid) === -1
      ),
      (filteredGame) => filteredGame.start
    ),
    (sortedGame) => sortedGame.srid
  );

  const gameIds = gamesNotCompleted.concat(gamesCompleted);

  return {
    type: ActionTypes.RECEIVE_GAMES,
    sport,
    games,
    gameIds,
    expiresAt: dateNow() + 1000 * 60 * 10,  // 10 minutes
  };
};

/**
 * Dispatch parsed API information related to relevant games
 * Also pass through an updated at so that we can expire and re-poll after a period of time.
 * NOTE: this method must be wrapped with dispatch()
 * @param  {string} sport     Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @param  {object} response  API response object
 * @return {object}           Changes for reducer
 */
const receiveTeams = (sport, response) => {
  const newTeams = {};
  _forEach(response, (team) => {
    newTeams[team.srid] = team;
  });

  return {
    type: ActionTypes.RECEIVE_TEAMS,
    sport,
    teams: newTeams,
    expiresAt: dateNow() + 1000 * 60 * 60 * 6,  // 6 hours
  };
};


// helper methods


/**
 * Calculate the amount of time remaining in decimal between 0 and 1, where 1 is 100% of the time remaining
 * @param  {number} durationRemaining Number of minutes remaining
 * @param  {number} totalQuantity     Total number of minutes/innings/measurement possible for a player
 * @return {number}                   Remaining time in decimal form
 */
export const calcDecimalRemaining = (durationRemaining, gameDuration) => {
  const decimalRemaining = durationRemaining / gameDuration;

  // we don't want 1 exactly, as that messes with the calculations, 0.99 looks full
  if (decimalRemaining === 1) return 0.9999;

  // round to the nearest 4th decimal
  return Math.ceil(decimalRemaining * 10000) / 10000;
};

/**
 * Helper method to determine amount of time remaining in a game
 * @param  {string} sport     Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @param  {object} game  Game information
 * @return {number}       Minutes remaining in the game
 */
const calculateTimeRemaining = (sport, game) => {
  const sportConst = GAME_DURATIONS[sport];

  // if the game hasn't started, return full time
  if (!game.hasOwnProperty('boxscore')) {
    return sportConst.gameDuration;
  }
  const boxScore = game.boxscore;

  switch (sport) {
    // MLB uses half innings as its time remaining.
    case 'mlb': {
      let durationComplete = parseInt(boxScore.inning || 0, 10) * 2;

      // determine whether to add half inning for being in the bottom
      if (boxScore.inning_half === 'B') {
        durationComplete += 1;
      }

      return sportConst.gameDuration - durationComplete;
    }

    case 'nba':
    case 'nhl':
    default: {
      // if the game hasn't started but we have boxscore, return with full minutes
      if (boxScore.quarter === '') {
        return sportConst.gameDuration;
      }

      // if the game is done, then set to 0
      const endOfGameStatuses = ['completed', 'closed'];
      if (endOfGameStatuses.indexOf(boxScore.status) > -1) {
        return 0;
      }

      const currentPeriod = boxScore.quarter;
      const clockMinSec = boxScore.clock.split(':');

      // determine remaining minutes based on quarters
      const remainingPeriods = (currentPeriod > sportConst.periods) ? 0 : sportConst.periods - currentPeriod;
      const remainingMinutes = remainingPeriods * sportConst.periodMinutes;

      const periodMinutesRemaining = parseInt(clockMinSec[0], 10);

      // if less than a minute left, then add one minute
      if (periodMinutesRemaining === 0 && parseInt(clockMinSec[1], 10) !== 0) {
        return remainingMinutes + 1;
      }

      // round up to the nearest minute
      return remainingMinutes + periodMinutesRemaining;
    }
  }
};

/**
 * API GET to return all the games for a given sport
 * Used in the live section for contest pane, and filtering by username
 * @param  {string} sport     Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @return {promise}          Promise that resolves with API response body to reducer
 */
const fetchGames = (sport) => (dispatch) => {
  dispatch(requestGames(sport));

  return request.get(
    `/api/sports/scoreboard-games/${sport}/`
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    Accept: 'application/json',
  }).then((res) => {
    // add in the sport so we know how to differentiate it.
    const games = _merge({}, res.body || {});
    _forEach(games, (game, id) => {
      games[id].sport = sport;

      // if no boxscore, default to upcoming = 100% remaining
      if (game.hasOwnProperty('boxscore') === false) {
        games[id].timeRemaining = {
          duration: GAME_DURATIONS[sport].gameDuration,
          decimal: 0.9999,
        };
      } else {
        const durationRemaining = calculateTimeRemaining(sport, game);
        const decimalRemaining = calcDecimalRemaining(durationRemaining, GAME_DURATIONS[sport].gameDuration);

        games[id].timeRemaining = {
          duration: durationRemaining,
          decimal: decimalRemaining,
        };
      }
    });

    return dispatch(receiveGames(sport, games));
  });
};

/**
 * API GET to return all the teams for a given sport
 * Used in the live section for contest pane, and filtering by username
 * @param  {string} sport     Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @return {promise}          Promise that resolves with API response body to reducer
 */
const fetchTeams = (sport) => (dispatch) => {
  dispatch(requestTeams(sport));

  return request.get(
    `/api/sports/teams/${sport}/`
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    Accept: 'application/json',
  }).then(
    (res) => dispatch(receiveTeams(sport, res.body))
  );
};

/**
 * Helper method to convert an object of pitch types into a readable sentence
 * Example pitchCount:
 * "count__list": {
 *    "pitch_count": 5,
 *    "strikes": 1,
 *    "balls": 3,
 *    "outs": 3
 *  },
 * @param  {object} pitchCount Types of pitches and their count
 * @return {string}            Human readable pitch count
 */
export const humanizePitchCount = (pitchCount) =>
  `${pitchCount.balls}B/${pitchCount.strikes}S - ${pitchCount.outs} Outs`;

/**
 * Method to determine whether we need to fetch games for a sport
 * @param  {object} state Current Redux state to test
 * @param  {string} sport     Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchGames = (state, sport, force) => {
  // ignore the expiration if forcing
  if (force === true) {
    return true;
  }

  // don't fetch until expired
  if (dateNow() < state.sports[sport].gamesExpireAt) {
    return false;
  }

  return true;
};

/**
 * Method to determine whether we need to fetch teams for a sport
 * Fetch if we are currently not fetching.
 * @param  {object} state Current Redux state to test
 * @param  {string} sport     Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchTeams = (state, sport) => {
  // First, check if the sport has an entry.
  if (state.sports.hasOwnProperty(sport)) {
    // don't fetch until expired
    if (dateNow() < state.sports[sport].teamsExpireAt) {
      return false;
    }
  } else {
    log.error('We aren\'t set up to accommodate teams for sport: ${sport}');
  }

  return true;
};


// primary methods


/**
 * Fetch games if we need to
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchGamesIfNeeded = (sport, force) => (dispatch, getState) => {
  if (shouldFetchGames(getState(), sport, force) === false) {
    return Promise.resolve('Games already exists');
  }

  return dispatch(fetchGames(sport));
};

/**
 * Fetch teams if we need to
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchTeamsIfNeeded = (sport) => (dispatch, getState) => {
  if (shouldFetchTeams(getState(), sport) === false) {
    return Promise.resolve('Teams already exists');
  }

  return dispatch(fetchTeams(sport));
};

/**
 * Fetch sport if needed
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchSportIfNeeded = (sport, force) => (dispatch) => {
  dispatch(fetchTeamsIfNeeded(sport));
  dispatch(fetchGamesIfNeeded(sport, force));
};

/**
 * Fetch games and teams for all relevant sports
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchSportsIfNeeded = () => (dispatch, getState) => {
  log.trace('actions.sports.fetchSportsIfNeeded()');

  _forEach(
    getState().sports.types, (sport) => {
      dispatch(fetchSportIfNeeded(sport));
    }
  );
};

/**
 * Update game information based on pusher stream call
 * @param  {string} gameId  Game SRID
 * @param  {string} teamId  Team SRD
 * @param  {number} points  Number of points to set to the game
 * @return {object}   Changes for reducer, wrapped in a thunk
 */
export const updateGameTeam = (gameId, teamId, points) => (dispatch, getState) => {
  const state = getState();
  const game = state.sports.games[gameId];
  const updatedGameFields = {};

  // if game does not exist yet, we don't know what sport so just cancel the update and wait for polling call
  if (state.sports.games.hasOwnProperty(gameId) === false) {
    return false;
  }

  if (state.sports[game.sport].isFetchingGames === false) {
    // if the boxscore doesn't exist yet, that means we need to update games
    if (game.hasOwnProperty('boxscore') === false) {
      return dispatch(fetchGames(game.sport));
    }

    // if the boxscore doesn't have quarters yet, update the game
    if (game.boxscore.hasOwnProperty('quarter') === false) {
      return dispatch(fetchGames(game.sport));
    }

    // if we think the game hasn't started, also update the games
    const upcomingStates = ['scheduled', 'created'];
    if (upcomingStates.indexOf(game.boxscore.status) > -1) {
      return dispatch(fetchGames(game.sport));
    }
  }

  const boxscore = game.boxscore;

  if (boxscore === undefined) {
    return false;
  }

  if (boxscore.srid_home === teamId) {
    updatedGameFields.home_score = points;
  } else {
    updatedGameFields.away_score = points;
  }

  return dispatch({
    type: ActionTypes.UPDATE_GAME,
    gameId,
    updatedGameFields,
  });
};

/**
 * Update game information based on pusher stream call
 * @param  {string} gameId  Game SRID
 * @param  {string} clock   Time remaining in period
 * @param  {string} quarter Period in play
 * @return {object}   Changes for reducer, wrapped in a thunk
 */
export const updateGameTime = (gameId, clock, quarter, status) => (dispatch, getState) => {
  const state = getState();
  const game = _merge({}, state.sports.games[gameId]);

  // if game does not exist yet, we don't know what sport so just cancel the update and wait for polling call
  if (state.sports.games.hasOwnProperty(gameId) === false) {
    return false;
  }

  if (state.sports[game.sport].isFetchingGames === false) {
    // if the boxscore doesn't exist yet, that means we need to update games
    if (game.hasOwnProperty('boxscore') === false) {
      return dispatch(fetchGames(game.sport));
    }

    // if the boxscore doesn't have quarter yet, update the game
    if (game.boxscore.hasOwnProperty('quarter') === false) {
      return dispatch(fetchGames(game.sport));
    }

    // if we think the game hasn't started, also update the games
    const upcomingStates = ['scheduled', 'created'];
    if (upcomingStates.indexOf(game.boxscore.status) > -1) {
      return dispatch(fetchGames(game.sport));
    }
  }

  const boxscore = game.boxscore;

  if (boxscore === undefined) {
    return false;
  }

  const updatedGameFields = {
    clock,
    quarter,
    status,
  };

  // find time remaining through these new fields
  game.boxscore.clock = clock;
  game.boxscore.quarter = quarter;
  updatedGameFields.durationRemaining = calculateTimeRemaining(game.sport, game);

  return dispatch({
    type: ActionTypes.UPDATE_GAME,
    gameId,
    updatedGameFields,
  });
};
