"use strict"

import request from 'superagent'
import { normalize, Schema, arrayOf } from 'normalizr'

import * as ActionTypes from '../action-types'
import log from '../lib/logging'


function requestPrize(id) {
  log.debug('actionsLivePrize.requestPrize')

  return {
    id: id,
    type: ActionTypes.REQUEST_PRIZE
  }
}


function receivePrize(id, response) {
  log.debug('actionsLivePrize.receivePrize')

  return {
    type: ActionTypes.RECEIVE_PRIZE,
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

  return id in state.prizes === false
}


export function fetchPrizeIfNeeded(id) {
  log.debug('actionsLivePrize.fetchPrizeIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchPrize(getState(), id)) {
      return dispatch(fetchPrize(id))
    } else {
      return Promise.reject('Prize already exists')
    }
  }
}
