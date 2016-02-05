// so we can use Promises
import 'babel-core/polyfill'
const request = require('superagent-promise')(require('superagent'), Promise)
import _ from 'lodash'
import moment from 'moment'

import * as ActionTypes from '../action-types'


// global constants


// constant related to game durations
export const GAME_DURATIONS = {
  nba: {
    periods: 4,
    periodMinutes: 12,
    gameMinutes: 48,
    players: 8,
  },
}


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
  expiresAt: moment(Date.now()).add(1, 'minute'),
})

/**
 * Dispatch information to reducer that we are trying to get teams
 * Used to prevent repeat calls while requesting.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const requestTeams = (sport) => ({
  sport,
  type: ActionTypes.REQUEST_TEAMS,
})

/**
 * Dispatch parsed API information related to relevant games
 * Also pass through an updated at so that we can expire and re-poll after a period of time.
 * NOTE: this method must be wrapped with dispatch()
 * @param  {string} sport  Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @param  {object} games  Object of games
 * @return {object}        Changes for reducer
 */
const receiveGames = (sport, games) => {
  const gameIds = _.map(
    _.sortBy(
      games, (game) => game.start
    ),
    (game) => game.srid
  )

  return {
    type: ActionTypes.RECEIVE_GAMES,
    sport,
    games,
    gameIds,
    expiresAt: moment(Date.now()).add(10, 'minutes'),
  }
}

/**
 * Dispatch parsed API information related to relevant games
 * Also pass through an updated at so that we can expire and re-poll after a period of time.
 * NOTE: this method must be wrapped with dispatch()
 * @param  {string} sport     Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @param  {object} response  API response object
 * @return {object}           Changes for reducer
 */
const receiveTeams = (sport, response) => {
  const newTeams = {}
  _.forEach(response, (team) => {
    newTeams[team.srid] = team
  })

  return {
    type: ActionTypes.RECEIVE_TEAMS,
    sport,
    teams: newTeams,
    expiresAt: moment(Date.now()).add(6, 'hours'),
  }
}


// helper methods


/**
 * Helper method to determine amount of time remaining in a game
 * @param  {string} sport     Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @param  {object} game  Game information
 * @return {number}       Minutes remaining in the game
 */
const calculateTimeRemaining = (sport, game) => {
  const sportDurations = GAME_DURATIONS[sport]

  // if the game hasn't started, return full time
  if (!game.hasOwnProperty('boxscore')) {
    return sportDurations.gameMinutes
  }
  const boxScore = game.boxscore

  // if the game hasn't started but we have boxscore, return with full minutes
  if (boxScore.quarter === '') {
    return sportDurations.gameMinutes
  }

  const currentQuarter = boxScore.quarter
  const clockMinSec = boxScore.clock.split(':')

  // determine remaining minutes based on quarters
  const remainingQuarters = (currentQuarter > sportDurations.periods) ? 0 : sportDurations.periods - currentQuarter
  const remainingMinutes = remainingQuarters * 12

  // round up to the nearest minute
  return remainingMinutes + parseInt(clockMinSec[0], 10) + 1
}

/**
 * API GET to return all the games for a given sport
 * Used in the live section for contest pane, and filtering by username
 * @param  {string} sport     Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @return {promise}          Promise that resolves with API response body to reducer
 */
const fetchGames = (sport) => (dispatch) => {
  dispatch(requestGames(sport))

  return request.get(
    `/api/sports/scoreboard-games/${sport}/`
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    Accept: 'application/json',
  }).then((res) => {
    // add in the sport so we know how to differentiate it
    const games = Object.assign({}, res.body)
    _.forEach(games, (game, id) => {
      games[id].sport = sport

      if (game.hasOwnProperty('boxscore')) {
        games[id].boxscore.timeRemaining = calculateTimeRemaining(sport, game)
      }
    })

    return dispatch(receiveGames(sport, games))
  })
}

/**
 * API GET to return all the teams for a given sport
 * Used in the live section for contest pane, and filtering by username
 * @param  {string} sport     Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @return {promise}          Promise that resolves with API response body to reducer
 */
const fetchTeams = (sport) => (dispatch) => {
  dispatch(requestTeams(sport))

  return request.get(
    `/api/sports/teams/${sport}/`
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    Accept: 'application/json',
  }).then(
    (res) => dispatch(receiveTeams(sport, res.body))
  )
}

/**
 * Method to determine whether we need to fetch games for a sport
 * @param  {object} state Current Redux state to test
 * @param  {string} sport     Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchGames = (state, sport, force) => {
  // ignore the expiration if forcing
  if (force === true) {
    return true
  }

  // don't fetch until expired
  if (moment().isBefore(state.sports[sport].gamesExpireAt)) {
    return false
  }

  // fetch if not currently fetching
  if (state.sports[sport].isFetchingGames === true) {
    return false
  }

  return true
}

/**
 * Method to determine whether we need to fetch teams for a sport
 * Fetch if we are currently not fetching.
 * @param  {object} state Current Redux state to test
 * @param  {string} sport     Sport for these games ['nba', 'nfl', 'nhl', 'mlb']
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchTeams = (state, sport) => {
  // if currently fetching, don't fetch again
  if (state.sports[sport].isFetchingTeams === true) {
    return false
  }

  // fetch if expired
  if (moment().isBefore(state.sports[sport].teamsExpireAt)) {
    return false
  }

  return true
}


// primary methods


/**
 * Fetch games if we need to
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchGamesIfNeeded = (sport, force) => (dispatch, getState) => {
  if (shouldFetchGames(getState(), sport, force) === false) {
    return Promise.resolve('Games already exists')
  }

  return dispatch(fetchGames(sport))
}

/**
 * Fetch teams if we need to
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchTeamsIfNeeded = (sport) => (dispatch, getState) => {
  if (shouldFetchTeams(getState(), sport) === false) {
    return Promise.resolve('Teams already exists')
  }

  return dispatch(fetchTeams(sport))
}

export const fetchSportIfNeeded = (sport, force) => (dispatch) => {
  dispatch(fetchTeamsIfNeeded(sport))
  dispatch(fetchGamesIfNeeded(sport, force))
}

/**
 * Fetch games and teams for all relevant sports
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchSportsIfNeeded = () => (dispatch, getState) => {
  _.forEach(
    getState().sports.types, (sport) => {
      dispatch(fetchSportIfNeeded(sport))
    }
  )
}

/**
 * Update game information based on pusher stream call
 * @param  {string} gameId  Game SRID
 * @param  {string} teamId  Team SRD
 * @param  {number} points  Number of points to set to the game
 * @return {object}   Changes for reducer, wrapped in a thunk
 */
export const updateGame = (gameId, teamId, points) => (dispatch, getState) => {
  const state = getState()
  const game = state.sports.games[gameId]
  const updatedGameFields = {}

  // if game does not exist yet, we don't know what sport so just cancel the update and wait for polling call
  if (state.sports.games.hasOwnProperty(gameId) === false) {
    return false
  }

  // if the boxscore doesn't exist yet, that means we need to update games
  if (game.hasOwnProperty('boxscore') === false &&
      state.sports[game.sport].isFetchingGames === false) {
    return dispatch(fetchGames(game.sport))
  }

  // if we think the game hasn't started, also update the games
  if (game.hasOwnProperty('boxscore') === true &&
      game.boxscore.status === 'scheduled') {
    return dispatch(fetchGames(game.sport))
  }

  const boxscore = game.boxscore

  if (boxscore === undefined) {
    return false
  }

  if (boxscore.srid_home === teamId) {
    updatedGameFields.home_score = points
  } else {
    updatedGameFields.away_score = points
  }

  updatedGameFields.timeRemaining = calculateTimeRemaining(game.sport, game)

  return dispatch({
    type: ActionTypes.UPDATE_GAME,
    gameId,
    updatedGameFields,
  })
}
