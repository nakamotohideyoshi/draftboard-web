import * as ActionTypes from '../action-types';
import filter from 'lodash/filter';
import forEach from 'lodash/forEach';
import log from '../lib/logging';
import map from 'lodash/map';
import merge from 'lodash/merge';
import sortBy from 'lodash/sortBy';
import zipObject from 'lodash/zipObject';
import { addMessage } from './message-actions';
import { CALL_API } from '../middleware/api';
import { dateNow, hasExpired, isDateInTheFuture } from '../lib/utils';

// get custom logger for actions
const logAction = log.getLogger('action');
// custom API domain for local dev testing
const { API_DOMAIN = '' } = process.env;


// global constants

// constant related to game durations
export const SPORT_CONST = {
  nba: {
    gameDuration: 48,
    lineupByteLength: 20,
    periodMinutes: 12,
    periods: 4,
    players: 8,
    pregameStatuses: ['scheduled', 'created', 'time-tbd'],
    liveStats: {
      types: ['points', 'rebounds', 'steals', 'assists', 'blocks', 'turnovers'],
      names: ['PTS', 'RB', 'ST', 'ASST', 'BLK', 'TO'],
    },
    seasonStats: {
      types: ['fp', 'points', 'rebounds', 'assists', 'steals', 'blocks', 'turnovers'],
      names: ['FPPG', 'PPG', 'RPG', 'APG', 'STLPG', 'BLKPG', 'TOPG'],
    },
  },
  nfl: {
    gameDuration: 60,
    lineupByteLength: 20,
    periodMinutes: 15,
    periods: 4,
    players: 8,
    pregameStatuses: ['scheduled'],
    liveStats: {
      qb: {
        types: ['pass_yds', 'pass_td', 'rush_yds', 'rush_td', 'ints', 'off_fum_lost'],
        names: ['YPAS', 'PTD', 'YRSH', 'RTD', 'INT', 'FUM'],
      },
      nonQb: {
        types: ['rush_yds', 'rec_rec', 'rec_yds', 'rush_td', 'off_fum_lost'],
        names: ['YRSH', 'REC', 'YREC', 'TD', 'FUM'],
      },
    },
    seasonStats: {
      qb: {
        types: ['avg_pass_yds', 'avg_pass_td', 'avg_rush_yds', 'avg_rush_td', 'avg_ints', 'avg_off_fum_lost'],
        names: ['YPAS', 'PTD', 'YRSH', 'RTD', 'INT', 'FUM'],
      },
      nonQb: {
        types: ['avg_rush_yds', 'avg_rec_rec', 'avg_rec_yds', 'avg_rush_td', 'avg_off_fum_lost'],
        names: ['YRSH', 'REC', 'YREC', 'TD', 'FUM'],
      },
    },
  },
  nhl: {
    gameDuration: 60,
    lineupByteLength: 20,
    periodMinutes: 20,
    periods: 3,
    players: 8,
    pregameStatuses: ['scheduled', 'created'],
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
    pitchTypes: {
      FA: 'Fastball',
      SI: 'Sinker',
      CT: 'Cutter',
      CU: 'Curveball',
      SL: 'Slider',
      CH: 'Changeup',
      KN: 'Knuckleball',
      SP: 'Splitter',
      SC: 'Screwball',
      FO: 'Forkball',
      IB: 'Intentional Ball',
      PI: 'Pitchout',
      Other: 'Other',
    },
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
    pregameStatuses: ['scheduled'],
    liveStats: {
      types: [],
      names: [],
    },
    seasonStats: {
      types: [],
      names: [],
    },
  },
};


// helper methods

/**
 * TODO move to lib.utils
 *
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
 * This is exported just so we can make sure it's tested individually, important
 * @param  {string} sport     Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @param  {object} game  Game information
 * @return {number}       Minutes remaining in the game
 */
export const calculateTimeRemaining = (sport, game) => {
  logAction.debug('actions.calculateTimeRemaining');

  const sportConst = SPORT_CONST[sport];
  const endStatuses = ['completed', 'complete', 'closed'];

  // if the game hasn't started, return full time
  if (!('boxscore' in game)) return sportConst.gameDuration;

  const boxScore = game.boxscore;

  // if the game is done, then set to 0
  if (endStatuses.indexOf(game.status) > -1) return 0;

  switch (sport) {
    // MLB uses half innings as its time remaining.
    case 'mlb': {
      let durationComplete = parseInt(boxScore.inning || 0, 10) * 2;

      // determine whether to add half inning for being in the bottom
      if (boxScore.inning_half === 'T') {
        durationComplete -= 1;
      }

      // subtract 1 overall, since top of 1st should technically be 0
      durationComplete -= 1;

      // if the game is complete
      if (durationComplete >= sportConst.gameDuration && game.status !== 'inprogress') return 0;

      // if extra innings or bottom of 9th, then return 1
      if (durationComplete >= sportConst.gameDuration) return 1;

      // otherwise return normal remaining
      return sportConst.gameDuration - durationComplete;
    }

    case 'nba':
    case 'nhl':
    case 'nfl':
    default: {
      // if the game hasn't started but we have boxscore, return with full minutes
      if (boxScore.quarter === '' || !('clock' in boxScore)) {
        return sportConst.gameDuration;
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


// dispatch to reducer methods

/**
 * Dispatch parsed API information related to relevant games
 * Also pass through an updated at so that we can expire and re-poll after a period of time.
 * NOTE: this method must be wrapped with dispatch()
 * @param  {string} sport  Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @param  {object} games  Object of games
 * @return {object}        Changes for reducer
 */
const receiveGames = (sport, games) => {
  logAction.debug('receiveGames', sport, games);

  const doneStatuses = ['closed', 'complete'];

  const fixedBoxscores = map(games, (game) => {
    const newGame = merge({}, game);

    newGame.sport = sport;

    // TEMP replace boxscore2 with boxscore
    if ('boxscore2' in game && newGame.boxscore2 instanceof Object) {
      newGame.boxscore = game.boxscore2;
      delete(newGame.boxscore2);
    }

    // remove null boxscores
    if ('boxscore' in newGame && !(newGame.boxscore instanceof Object)) {
      delete(newGame.boxscore);
    }

    // if no boxscore, default to upcoming = 100% remaining
    if (!('boxscore' in newGame)) {
      newGame.timeRemaining = {
        duration: SPORT_CONST[sport].gameDuration,
        decimal: 0.9999,
      };
    } else {
      const durationRemaining = calculateTimeRemaining(sport, game);
      const decimalRemaining = calcDecimalRemaining(durationRemaining, SPORT_CONST[sport].gameDuration);

      newGame.timeRemaining = {
        duration: durationRemaining,
        decimal: decimalRemaining,
      };
    }

    return newGame;
  });

  const mappedBoxscore = zipObject(
    Object.keys(games),
    fixedBoxscores
  );

  const gamesCompleted = map(
    sortBy(
      filter(
        mappedBoxscore, (game) => doneStatuses.indexOf(game.status) !== -1
      ),
      (filteredGame) => filteredGame.start
    ),
    (sortedGame) => sortedGame.srid
  );

  const gamesNotCompleted = map(
    sortBy(
      filter(
        mappedBoxscore, (game) => gamesCompleted.indexOf(game.srid) === -1
      ),
      (filteredGame) => filteredGame.start
    ),
    (sortedGame) => sortedGame.srid
  );

  const gameIds = gamesNotCompleted.concat(gamesCompleted);

  return {
    sport,
    games: mappedBoxscore,
    gameIds,
  };
};

/**
 * TODO switch to fetch
 *
 * API GET to return all the games for a given sport
 * Used in the live section for contest pane, and filtering by username
 * @param  {string} sport     Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @return {promise}          Promise that resolves with API response body to reducer
 */
const fetchGames = (sport) => ({
  [CALL_API]: {
    types: [
      ActionTypes.REQUEST_GAMES,
      ActionTypes.RECEIVE_GAMES,
      ActionTypes.ADD_MESSAGE,
    ],
    expiresAt: dateNow() + 1000 * 60 * 10,  // 10 minutes
    endpoint: `${API_DOMAIN}/api/sports/scoreboard-games/${sport}/`,
    requestFields: { sport },
    callback: (json) => receiveGames(sport, json || {}),
  },
});

/**
 * TODO switch to fetch
 *
 * API GET to return all the teams for a given sport
 * Used in the live section for contest pane, and filtering by username
 * @param  {string} sport     Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @return {promise}          Promise that resolves with API response body to reducer
 */
const fetchTeams = (sport) => ({
  [CALL_API]: {
    types: [
      ActionTypes.REQUEST_TEAMS,
      ActionTypes.RECEIVE_TEAMS,
      ActionTypes.ADD_MESSAGE,
    ],
    expiresAt: dateNow() + 1000 * 60 * 60 * 6,  // 6 hours
    endpoint: `${API_DOMAIN}/api/sports/teams/${sport}/`,
    requestFields: { sport },
    callback: (json) => {
      const teams = {};
      json.forEach((team) => {
        teams[team.srid] = team;
      });

      return {
        sport,
        teams,
      };
    },
  },
});

/**
 * Method to determine whether we need to fetch games for a sport
 * @param  {object} state Current Redux state to test
 * @param  {string} sport     Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchGames = (state, sport, force) => {
  logAction.trace('actions.shouldFetchGames', force);

  // ignore the expiration if forcing
  if (force === true) return true;

  const reasons = [];

  if (!hasExpired(state.sports[sport].gamesExpireAt)) reasons.push('has not expired');

  if (reasons.length > 0) {
    logAction.trace('shouldFetchGames - returned false', reasons);
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
  logAction.trace('actions.shouldFetchGames');
  const reasons = [];

  if (!(sport in state.sports)) reasons.push(`we do not support ${sport} yet`);
  else if (!hasExpired(state.sports[sport].teamsExpireAt)) reasons.push('has not expired');

  if (reasons.length > 0) {
    logAction.trace('shouldFetchTeams - returned false', reasons);
    return false;
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
  logAction.trace('actions.fetchGamesIfNeeded', sport);

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
  logAction.trace('actions.fetchTeamsIfNeeded');

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
  logAction.trace('actions.fetchSportIfNeeded', sport);

  dispatch(fetchTeamsIfNeeded(sport));
  dispatch(fetchGamesIfNeeded(sport, force));
};

/**
 * Fetch games and teams for all relevant sports
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchSportsIfNeeded = () => (dispatch, getState) => {
  logAction.trace('actions.fetchSportsIfNeeded');

  try {
    forEach(getState().sports.types, (sport) => {
      dispatch(fetchSportIfNeeded(sport));
    });
  } catch (err) {
    // TODO: This is silently gobbling up any errors.
    dispatch(addMessage({
      header: 'Failed to connect to API.',
      content: 'Please refresh the page to reconnect.',
      level: 'warning',
      id: 'apiFailure',
    }));
    log.error(err);
  }
};

/**
 * TODO move to lib.utils
 *
 * Check whether a game has started
 * 1. If the start time hasn't passed yet, then return false
 * 2. If the status is closed, we know the game is over, so true
 * 3. If boxscore exists, we know it has started, so true
 *
 * @param  {string} sport  Sport to base statuses on
 * @param  {object} message Current game
 * @return {boolean}       True if game has started, false if not
 */
export const hasGameStarted = (sport, message) => {
  if (isDateInTheFuture(message.start)) return false;

  if (['closed', 'complete'].indexOf(message.status) !== -1) {
    return true;
  }
  return 'boxscore' in message && message.boxscore instanceof Object;
};

/**
 * Helper method to check whether a game is ready to receive data
 * @param  {object} games   Redux state
 * @param  {string} gameId  SportsRadar Game UUID
 * @return {boolean}        Whether the game is ready
 */
export const isGameReady = (state, dispatch, sport, gameId) => {
  logAction.debug('actions.isGameReady');

  const games = state.sports.games;

  // check if game is needed
  if (!games.hasOwnProperty(gameId)) {
    logAction.debug('actions.isGameReady - game does not exist', gameId);
    return false;
  }

  // if no boxscore from the server, ask for it
  if (!games[gameId].hasOwnProperty('boxscore')) {
    dispatch(fetchSportIfNeeded(sport));

    logAction.debug('actions.isGameReady - boxscore does not exist', gameId);
    return false;
  }

  return true;
};

/**
 * Update game information based on pusher stream call
 * @param  {string} gameId  Game SRID
 * @param  {string} teamId  Team SRD
 * @param  {number} points  Number of points to set to the game
 * @return {object}   Changes for reducer, wrapped in a thunk
 */
export const updateGameTeam = (message) => (dispatch, getState) => {
  logAction.debug('actions.updateGameTeam');

  const sports = getState().sports;
  const gameId = message.srid_game;

  // if game does not exist yet, we don't know what sport
  // so just cancel the update and wait for polling call
  const game = sports.games[gameId];
  if (!game) {
    log.warn('Game from "updateGameTeam" does not exist yet.');
    return false;
  }

  const boxscore = game.boxscore;

  if (!boxscore || !hasGameStarted(game.sport, game)) {
    log.warn('We have no boxscore for this game, attempating to fetch games...');
    return dispatch(fetchGames(game.sport));
  }

  const updatedFields = {};
  if (boxscore.home_team === message.srid_team) {
    updatedFields.home_score = message.points;
  } else if (boxscore.away_team === message.srid_team) {
    updatedFields.away_score = message.points;
  } else {
    log.warn('No matching team was found for updateGameTeam.', message, boxscore);
  }

  return dispatch({
    type: ActionTypes.UPDATE_GAME,
    gameId,
    updatedFields,
  });
};

/**
 * Update game information based on pusher stream call
 * @param  {string} gameId  Game SRID
 * @param  {object} event   Returned socket data to parse
 *  * @return {object}   Changes for reducer, wrapped in a thunk
 */
export const updateGameTime = (event) => (dispatch, getState) => {
  logAction.debug('actions.updateGameTime');
  const { gameId } = event;
  const state = getState();

  // if game does not exist yet, we don't know what sport so just cancel the update and wait for polling call
  if (!(gameId in state.sports.games)) return false;

  let game = merge({}, state.sports.games[gameId]);
  const { updatedFields } = event;

  // temp update fields to be able to calculateTimeRemaining
  game = merge({}, game, updatedFields);

  const duration = calculateTimeRemaining(game.sport, game);
  const decimal = calcDecimalRemaining(duration, SPORT_CONST[game.sport].gameDuration);
  updatedFields.timeRemaining = { duration, decimal };

  return dispatch({
    type: ActionTypes.UPDATE_GAME,
    gameId,
    updatedFields,
  });
};
