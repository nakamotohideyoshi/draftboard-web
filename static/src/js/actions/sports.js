// so we can use Promises
import 'babel-core/polyfill'
const request = require('superagent-promise')(require('superagent'), Promise)
import { normalize, Schema, arrayOf } from 'normalizr'
import _ from 'lodash'
var moment = require('moment')

import * as ActionTypes from '../action-types'
import log from '../lib/logging'

export const GAME_DURATIONS = {
  nba: {
    periods: 4,
    periodMinutes: 12,
    gameMinutes: 48,
    players: 8
  }
}

function calculateTimeRemaining(sport, game) {
  log.trace('actionsCurrentBoxScores.calculateTimeRemaining')
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
  return remainingMinutes + parseInt(clockMinSec[0]) + 1
}

function requestTeams(sport) {
  log.trace('actionsLiveTeams.requestTeams')

  return {
    sport: sport,
    type: ActionTypes.REQUEST_TEAMS
  }
}


function receiveTeams(sport, response) {
  log.trace('actionsLiveTeams.receiveTeams')

  let newTeams = {}

  _.forEach(response, (team) => {
    newTeams[team.srid] = team
  })

  return {
    type: ActionTypes.RECEIVE_TEAMS,
    sport: sport,
    teams: newTeams,
    expiresAt: Date.now() + 86400000
  }
}


function fetchTeams(sport) {
  log.trace('actionsLiveTeams.fetchTeams')

  return dispatch => {
    dispatch(requestTeams(sport))

    return request.get(
      '/api/sports/teams/' + sport + '/'
    ).set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'Accept': 'application/json'
    }).then(function(res) {
      return dispatch(receiveTeams(sport, res.body))
    })
  }
}


function shouldFetchTeams(state, sport) {
  log.trace('actionsLiveTeams.shouldFetchTeams')

  return state.sports[sport].isFetchingTeams === false
}


export function fetchTeamsIfNeeded(sport) {
  log.trace('actionsLiveTeams.fetchTeamsIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchTeams(getState(), sport) === false) {
      return Promise.resolve('Teams already exists')
    }

    return dispatch(fetchTeams(sport))
  }
}


// --------------------------------------------------------


export function updateGame(gameId, teamId, points) {
  log.trace('actionsCurrentBoxScores.updateBoxScore')

  return (dispatch, getState) => {
    const state = getState()
    const game = state.sports.games[gameId]
    let updatedGameFields = {}

    // if game does not exist yet, we don't know what sport so just cancel the update and wait for polling call
    if (state.sports.games.hasOwnProperty(gameId) === false) {
      return false
    }

    // if the boxscore doesn't exist yet, that means we need to update games
    if (game.hasOwnProperty('boxscore') === false &&
        state.sports[game.sport].isFetchingGames === false) {
      return dispatch(fetchGames(game.sport))
    }

    const boxscore = game.boxscore

    if (boxscore.srid_home === teamId) {
      updatedGameFields.home_score = points
    } else {
      updatedGameFields.away_score = points
    }

    updatedGameFields.timeRemaining = calculateTimeRemaining(game.sport, game)

    return dispatch({
      type: ActionTypes.UPDATE_GAME,
      gameId: gameId,
      updatedGameFields: updatedGameFields
    })
  }
}


function requestGames(sport) {
  log.trace('actionsSports.requestGames')

  return {
    sport: sport,
    type: ActionTypes.REQUEST_GAMES
  }
}


function receiveGames(sport, response) {
  log.trace('actionsSports.receiveGames')

  // add in the sport so we know how to differentiate it
  let games = Object.assign({}, response)
  _.forEach(games, (game, id) => {
    game.sport = sport

    if (game.hasOwnProperty('boxscore')) {
      game.boxscore.timeRemaining = calculateTimeRemaining(sport, game)
    }
  })

  return {
    type: ActionTypes.RECEIVE_GAMES,
    sport: sport,
    games: games,
    gamesUpdatedAt: Date.now()
  }
}


function fetchGames(sport) {
  log.trace('actionsSports.fetchGames')

  return dispatch => {
    dispatch(requestGames(sport))

    return request.get(
      '/api/sports/scoreboard-games/' + sport + '/'
    ).set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'Accept': 'application/json'
    }).then(function(res) {
      return dispatch(receiveGames(sport, res.body))
    })
  }
}


function shouldFetchGames(state, sport) {
  log.trace('actionsSports.shouldFetchGame')

  // if currently fetching, don't fetch again
  if (state.sports[sport].isFetchingGames === true) {
    return false
  }

  if (state.sports[sport].hasOwnProperty('gamesUpdatedAt')) {
    const expiration = moment(state.sports[sport].gamesUpdatedAt).add(6, 'hours')

    // if not yet expired
    if (moment().isBefore(expiration)) {
      return false
    }
  }

  return true
}


export function fetchGamesIfNeeded(sport) {
  log.trace('actionsSports.fetchGamesIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchGames(getState(), sport) === false) {
      return Promise.resolve('Games already exists')
    }

    return dispatch(fetchGames(sport))
  }
}


export function fetchSportsIfNeeded() {
  log.info('actionsSports.fetchSportsIfNeeded()')

  return (dispatch, getState) => {
    const state = getState()

    _.forEach(state.sports.types, (sport) => {
      dispatch(fetchGamesIfNeeded(sport))
    })
  }
}


