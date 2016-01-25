// so we can use Promises
import 'babel-core/polyfill'
const request = require('superagent-promise')(require('superagent'), Promise)
import { normalize, Schema, arrayOf } from 'normalizr'
import _ from 'lodash'
var moment = require('moment')

import * as ActionTypes from '../action-types'
import log from '../lib/logging'


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
    const game = state.games[gameId]
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
