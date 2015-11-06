"use strict"

import request from 'superagent'
import { normalize, Schema, arrayOf } from 'normalizr'

import log from '../lib/logging'


export const REQUEST_LIVE_DRAFT_GROUP_INFO = 'REQUEST_LIVE_DRAFT_GROUP_INFO'
export const RECEIVE_LIVE_DRAFT_GROUP_INFO = 'RECEIVE_LIVE_DRAFT_GROUP_INFO'
export const REQUEST_LIVE_DRAFT_GROUP_FP = 'REQUEST_LIVE_DRAFT_GROUP_FP'
export const RECEIVE_LIVE_DRAFT_GROUP_FP = 'RECEIVE_LIVE_DRAFT_GROUP_FP'

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
    playersFP: normalizedPlayers.entities.players
  }
}


function shouldFetchDraftGroupFP(state, id) {
  log.debug('actionsLiveDraftGroup.shouldFetchDraftGroupFP')

  if (id in state === false)
    throw new Error('You cannot get fantasy points for a player that is not in the draft group')
  if (state[id].isFetchingInfo === true)
    return false
  if (state[id].isFetchingFP === true)
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

function requestDraftGroup(id) {
  log.debug('actionsLiveDraftGroup.requestDraftGroup')

  return {
    id: id,
    type: REQUEST_LIVE_DRAFT_GROUP_INFO
  }
}


function receiveDraftGroup(id, response) {
  log.debug('actionsLiveDraftGroup.receiveDraftGroup')

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


function fetchDraftGroup(id) {
  log.debug('actionsLiveDraftGroup.fetchDraftGroup')

  return dispatch => {
    dispatch(requestDraftGroup(id))

    request
      .get("/draft-group/" + id + '/')
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          // TODO
        } else {
          dispatch(receiveDraftGroup(id, res.body))
          dispatch(fetchDraftGroupFP(id))
        }
    })
  }
}


function shouldFetchDraftGroup(state, id) {
  log.debug('actionsLiveDraftGroup.shouldFetchDraftGroup')

  return id in state === false
}


export function fetchDraftGroupIfNeeded(id) {
  log.debug('actionsLiveDraftGroup.fetchDraftGroupIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchDraftGroup(getState(), id)) {
      return dispatch(fetchDraftGroup(id))
    }
  }
}
