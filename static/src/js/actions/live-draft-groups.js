var moment = require('moment')
// so we can use Promises
import 'babel-core/polyfill'
const request = require('superagent-promise')(require('superagent'), Promise)
import { forEach as _forEach } from 'lodash'
import { normalize, Schema, arrayOf } from 'normalizr'

import * as ActionTypes from '../action-types'
import log from '../lib/logging'
import { mergeBoxScores } from './current-box-scores'
import { fetchTeamsIfNeeded } from './sports'


const playerSchema = new Schema('players', {
  idAttribute: 'player_id'
})


// TODO make this sport dependent
function _calculateTimeRemaining(boxScore) {
  log.debug('actionsLiveDraftGroup._calculateTimeRemaining')

  const clockMinSec = boxScore.fields.clock.split(':')
  const remainingMinutes = (4 - parseInt(boxScore.fields.quarter)) * 12

  // round up to the nearest minute
  return remainingMinutes + parseInt(clockMinSec[0]) + 1
}


// Used to update a player's FP when a Pusher call sends us new info
export function updatePlayerFP(id, playerId, fp) {
  return {
    id: id,
    type: ActionTypes.UPDATE_LIVE_DRAFT_GROUP_PLAYER_FP,
    playerId: playerId,
    fp: fp
  }
}


// DRAFT GROUP FANTASY POINTS
// -----------------------------------------------------------------------

function requestDraftGroupFP(id) {
  log.debug('actionsLiveDraftGroup.requestDraftGroupFP')

  return {
    id: id,
    type: ActionTypes.REQUEST_LIVE_DRAFT_GROUP_FP
  }
}


function fetchDraftGroupFP(id) {
  log.debug('actionsLiveDraftGroup.fetchDraftGroupFP')

  return dispatch => {
    dispatch(requestDraftGroupFP(id))

    return request.get(
      '/api/draft-group/fantasy-points/' + id + '/'
    ).set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'Accept': 'application/json'
    }).then(function(res) {
      return dispatch(receiveDraftGroupFP(id, res.body))
    })
  }
}


function receiveDraftGroupFP(id, response) {
  log.debug('actionsLiveDraftGroup.receiveDraftGroupFP')

  return {
    type: ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_FP,
    id: id,
    players: response.players,
    updatedAt: Date.now()
  }
}


function shouldFetchDraftGroupFP(state, id) {
  log.debug('actionsLiveDraftGroup.shouldFetchDraftGroupFP')

  var liveDraftGroups = state.liveDraftGroups;

  if (id in liveDraftGroups === false)
    throw new Error('You cannot get fantasy points for a player that is not in the draft group')
  if (liveDraftGroups[id].isFetchingInfo === true)
    return false
  if (liveDraftGroups[id].isFetchingFP === true)
    return false

  return true
}


export function fetchDraftGroupFPIfNeeded(id) {
  log.debug('actionsLiveDraftGroup.fetchDraftGroupFPIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchDraftGroupFP(getState(), id)) {
      return dispatch(fetchDraftGroupFP(id))
    }
  }
}



// DRAFT GROUP INFO
// -----------------------------------------------------------------------

function requestDraftGroupInfo(id) {
  log.debug('actionsLiveDraftGroup.requestDraftGroupInfo')

  return {
    id: id,
    type: ActionTypes.REQUEST_LIVE_DRAFT_GROUP_INFO
  }
}


function receiveDraftGroupInfo(id, response) {
  log.debug('actionsLiveDraftGroup.receiveDraftGroupInfo')

  const normalizedPlayers = normalize(
    response.players,
    arrayOf(playerSchema)
  )

  return {
    type: ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_INFO,
    id: id,
    players: normalizedPlayers.entities.players,
    sport: response.sport,
    start: moment(response.start).valueOf(),
    end: moment(response.end).valueOf(),
    expiresAt: Date.now() + 86400000
  }
}


function fetchDraftGroupInfo(id) {
  log.debug('actionsLiveDraftGroup.fetchDraftGroupInfo')

  return dispatch => {
    dispatch(requestDraftGroupInfo(id))

    return request.get(
      '/api/draft-group/' + id + '/'
    ).set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'Accept': 'application/json'
    }).then(function(res) {
      return Promise.all([
        dispatch(receiveDraftGroupInfo(id, res.body)),
        dispatch(fetchTeamsIfNeeded(res.body.sport))
      ])
    })
  }
}



// DRAFT GROUP INFO
// -----------------------------------------------------------------------

function requestDraftGroupBoxScores(id) {
  log.debug('actionsLiveDraftGroup.requestDraftGroupBoxScores')

  return {
    id: id,
    type: ActionTypes.REQUEST_LIVE_DRAFT_GROUP_BOX_SCORES
  }
}


function receiveDraftGroupBoxScores(id, response) {
  log.debug('actionsLiveDraftGroup.receiveDraftGroupBoxScores')

  _forEach(response, (boxScore) => {
    boxScore.timeRemaining = _calculateTimeRemaining(boxScore)
  })

  return {
    type: ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_BOX_SCORES,
    id: id,
    boxScores: response,
    updatedAt: Date.now() + 86400000
  }
}


function fetchDraftGroupBoxScores(id) {
  log.debug('actionsLiveDraftGroup.fetchDraftGroupBoxScores')

  return dispatch => {
    dispatch(requestDraftGroupBoxScores(id))

    return request.get(
      '/api/draft-group/boxscores/' + id + '/'
    ).set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'Accept': 'application/json'
    }).then(function(res) {
      dispatch(receiveDraftGroupBoxScores(id, res.body))

      return dispatch(
        mergeBoxScores(res.body)
      )
    })
  }
}


function confirmDraftGroupStored(id) {
  log.debug('actionsEntries.confirmRelatedEntriesInfo')

  return {
    type: ActionTypes.CONFIRM_LIVE_DRAFT_GROUP_STORED,
    id: id
  }
}


function shouldFetchDraftGroup(state, id) {
  log.debug('actionsLiveDraftGroup.shouldFetchDraftGroup')

  return id in state.liveDraftGroups === false
}


export function fetchDraftGroupIfNeeded(id) {
  log.debug('actionsLiveDraftGroup.fetchDraftGroupIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchDraftGroup(getState(), id) === false) {
      log.debug('actionsLiveDraftGroup.fetchDraftGroupIfNeeded() - Draft group exists')
      return Promise.resolve('Draft group exists')
    }
    return Promise.all([
      dispatch(fetchDraftGroupInfo(id)),
      dispatch(fetchDraftGroupFP(id)),
      dispatch(fetchDraftGroupBoxScores(id))
    ])
    .then(() =>
      dispatch(confirmDraftGroupStored(id))
    )
  }
}
