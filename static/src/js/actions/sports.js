// so we can use Promises
import 'babel-core/polyfill'
const request = require('superagent-promise')(require('superagent'), Promise)
import { normalize, Schema, arrayOf } from 'normalizr'
import _ from 'lodash'

import * as ActionTypes from '../action-types'
import log from '../lib/logging'


function requestTeams(sport) {
  log.debug('actionsLiveTeams.requestTeams')

  return {
    sport: sport,
    type: ActionTypes.REQUEST_TEAMS
  }
}


function receiveTeams(sport, response) {
  log.debug('actionsLiveTeams.receiveTeams')

  let newTeams = {}

  _.forEach(response, (team) => {
    newTeams[team.id] = team
  })

  return {
    type: ActionTypes.RECEIVE_TEAMS,
    sport: sport,
    teams: newTeams,
    expiresAt: Date.now() + 86400000
  }
}


function fetchTeams(sport) {
  log.debug('actionsLiveTeams.fetchTeams')

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
  log.debug('actionsLiveTeams.shouldFetchTeams')

  return sport in state.sports === false
}


export function fetchTeamsIfNeeded(sport) {
  log.debug('actionsLiveTeams.fetchTeamsIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchTeams(getState(), sport) === false) {
      return Promise.resolve('Teams already exists')
    }

    return dispatch(fetchTeams(sport))
  }
}
