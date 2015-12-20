// so we can use Promises
import 'babel-core/polyfill'
const request = require('superagent-promise')(require('superagent'), Promise)
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

    return request.get(
      '/api/prize/' + id + '/'
    ).set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'Accept': 'application/json'
    }).then(function(res) {
      return dispatch(receivePrize(id, res.body))
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
      return Promise.resolve('Prize already exists')
    }
  }
}
