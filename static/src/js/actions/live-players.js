"use strict"

import 'babel-core/polyfill'; // so I can use Promises
import { normalize, Schema, arrayOf } from 'normalizr'
const request = require('superagent-promise')(require('superagent'), Promise)
import _ from 'lodash'

import * as ActionTypes from '../action-types'
import log from '../lib/logging'


function requestPlayersStats(lineupId) {
  log.trace('actionsLivePlayers.requestPlayersStats')

  return {
    lineupId: lineupId,
    type: ActionTypes.REQUEST_LIVE_PLAYERS_STATS
  }
}


function receivePlayersStats(lineupId, response) {
  log.trace('actionsLivePlayers.receivePlayersStats')

  let players = {}
  _.forEach(response, function(player) {
    // don't include if the player hasn't started
    if (player.started === false ||
        player.hasOwnProperty('data') === false ||
        player.data.length === 0 ||
        player.data[0].hasOwnProperty('fields') === false) {
      return
    }

    const playerFields = player.data[0].fields

    players[playerFields.srid_player] = Object.assign(
      { lineup_id: lineupId },
      playerFields
    )
  })

  return {
    type: ActionTypes.RECEIVE_LIVE_PLAYERS_STATS,
    lineupId: lineupId,
    players: players,
    receivedAt: Date.now()
  }
}


export function fetchPlayersStats(lineupId) {
  log.trace('actionsLivePlayers.fetchPlayersStats')

  return dispatch => {
    dispatch(requestPlayersStats(lineupId))

    return request.get(
      '/api/contest/lineup/' + lineupId + '/'
    ).set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'Accept': 'application/json'
    }).then(function(res) {
      return dispatch(receivePlayersStats(lineupId, res.body))
    })
  }
}


function shouldFetchPlayersStats(state, lineupId) {
  log.debug('actionsLivePlayers.shouldFetchPlayersStats')

  // return true if does not exist
  return state.livePlayers.isFetching.indexOf(lineupId) === -1
}


export function fetchPlayersStatsIfNeeded(lineupId) {
  log.debug('actionsLivePlayers.fetchPlayersStatsIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchPlayersStats(getState(), lineupId) === false) {
      return Promise.resolve('Lineup players stats currently being pulled for this lineup')
    }

    return dispatch(
      fetchPlayersStats(lineupId)
    )
  }
}