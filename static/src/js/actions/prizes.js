"use strict"

import request from 'superagent'
import { normalize, Schema, arrayOf } from 'normalizr'

import log from '../lib/logging'


export const REQUEST_PRIZE = 'REQUEST_PRIZE'
export const RECEIVE_PRIZE = 'RECEIVE_PRIZE'


function requestPrize(id) {
  log.debug('actionsLivePrize.requestPrize')

  return {
    id: id,
    type: REQUEST_PRIZE
  }
}


function receivePrize(id, response) {
  log.debug('actionsLivePrize.receivePrize')

  return {
    type: RECEIVE_PRIZE,
    id: id,
    info: response,
    expiresAt: Date.now() + 86400000
  }
}


function fetchPrize(id) {
  log.debug('actionsLivePrize.fetchPrize')

  return dispatch => {
    dispatch(requestPrize(id))

    request
      .get('/api/prize/' + id + '/')
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          // TODO
        } else {
          dispatch(receivePrize(id, res.body))
        }
    })
  }
}


function shouldFetchPrize(state, id) {
  log.debug('actionsLivePrize.shouldFetchPrize')

  return id in state === false
}


export function fetchPrizeIfNeeded(id) {
  log.debug('actionsLivePrize.fetchPrizeIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchPrize(getState(), id)) {
      return dispatch(fetchPrize(id))
    }
  }
}
