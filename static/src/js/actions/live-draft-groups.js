"use strict"

import 'babel-core/polyfill'; // so I can use Promises
import request from 'superagent'
import { normalize, Schema, arrayOf } from 'normalizr'

import log from '../lib/logging'


export const REQUEST_LIVE_DRAFT_GROUP_INFO = 'REQUEST_LIVE_DRAFT_GROUP_INFO'
export const RECEIVE_LIVE_DRAFT_GROUP_INFO = 'RECEIVE_LIVE_DRAFT_GROUP_INFO'
export const REQUEST_LIVE_DRAFT_GROUP_FP = 'REQUEST_LIVE_DRAFT_GROUP_FP'
export const RECEIVE_LIVE_DRAFT_GROUP_FP = 'RECEIVE_LIVE_DRAFT_GROUP_FP'
export const REQUEST_LIVE_DRAFT_GROUP_BOX_SCORES = 'REQUEST_LIVE_DRAFT_GROUP_BOX_SCORES'
export const RECEIVE_LIVE_DRAFT_GROUP_BOX_SCORES = 'RECEIVE_LIVE_DRAFT_GROUP_BOX_SCORES'

const playerSchema = new Schema('players', {
  idAttribute: 'player_id'
})


// DRAFT GROUP FANTASY POINTS
// -----------------------------------------------------------------------

function requestDraftGroupFP(id) {
  log.debug('actionsLiveDraftGroup.requestDraftGroupFP')

  return {
    id: id,
    type: REQUEST_LIVE_DRAFT_GROUP_FP
  }
}


function fetchDraftGroupFP(id) {
  log.debug('actionsLiveDraftGroup.fetchDraftGroupFP')

  return dispatch => {
    dispatch(requestDraftGroupFP(id))

    request
      .get("/draft-group/fantasy-points/" + id)
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          // TODO
        } else {
          dispatch(receiveDraftGroupFP(id, res.body))
        }
    })
  }
}


function receiveDraftGroupFP(id, response) {
  log.debug('actionsLiveDraftGroup.receiveDraftGroupFP')

  const normalizedPlayers = normalize(
    response.players,
    arrayOf(playerSchema)
  )

  return {
    type: RECEIVE_LIVE_DRAFT_GROUP_FP,
    id: id,
    players: normalizedPlayers.entities.players,
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
    type: REQUEST_LIVE_DRAFT_GROUP_INFO
  }
}


function receiveDraftGroupInfo(id, response) {
  log.debug('actionsLiveDraftGroup.receiveDraftGroupInfo')

  const normalizedPlayers = normalize(
    response.players,
    arrayOf(playerSchema)
  )

  return {
    type: RECEIVE_LIVE_DRAFT_GROUP_INFO,
    id: id,
    players: normalizedPlayers.entities.players,
    expiresAt: Date.now() + 86400000
  }
}


function fetchDraftGroupInfo(id) {
  log.debug('actionsLiveDraftGroup.fetchDraftGroupInfo')

  return dispatch => {
    dispatch(requestDraftGroupInfo(id))

    request
      .get("/draft-group/" + id + '/')
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          // TODO
        } else {
          Promise.all([
            dispatch(receiveDraftGroupInfo(id, res.body))
          ])
        }
    })
  }
}



// DRAFT GROUP INFO
// -----------------------------------------------------------------------

function requestDraftGroupBoxScores(id) {
  log.debug('actionsLiveDraftGroup.requestDraftGroupBoxScores')

  return {
    id: id,
    type: REQUEST_LIVE_DRAFT_GROUP_BOX_SCORES
  }
}


function receiveDraftGroupBoxScores(id, response) {
  log.debug('actionsLiveDraftGroup.receiveDraftGroupBoxScores')

  return {
    type: RECEIVE_LIVE_DRAFT_GROUP_BOX_SCORES,
    id: id,
    boxScores: response,
    updatedAt: Date.now() + 86400000
  }
}


function fetchDraftGroupBoxScores(id) {
  log.debug('actionsLiveDraftGroup.fetchDraftGroupBoxScores')

  return dispatch => {
    dispatch(requestDraftGroupBoxScores(id))

    request
      .get("/draft-group/box-scores/" + id)
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          // TODO
        } else {
          Promise.all([
            dispatch(receiveDraftGroupBoxScores(id, res.body))
          ])
        }
    })
  }
}



function shouldFetchDraftGroup(state, id) {
  log.debug('actionsLiveDraftGroup.shouldFetchDraftGroup')

  return id in state.liveDraftGroups === false
}


export function fetchDraftGroupIfNeeded(id) {
  log.debug('actionsLiveDraftGroup.fetchDraftGroupIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchDraftGroup(getState(), id)) {
      return Promise.all([
        dispatch(fetchDraftGroupInfo(id)),
        dispatch(fetchDraftGroupFP(id)),
        dispatch(fetchDraftGroupBoxScores(id))
      ])
    }
  }
}
