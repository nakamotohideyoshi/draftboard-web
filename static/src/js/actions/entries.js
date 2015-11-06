"use strict"

import request from 'superagent'
import { normalize, Schema, arrayOf } from 'normalizr'

import log from '../lib/logging'


export const REQUEST_ENTRIES = 'REQUEST_ENTRIES'
export const RECEIVE_ENTRIES = 'RECEIVE_ENTRIES'


function requestEntries() {
  log.debug('actionsEntries.requestEntries')

  return {
    type: REQUEST_ENTRIES
  }
}


function receiveEntries(response) {
  log.debug('actionsEntries.receiveEntries')

  const entries = new Schema('entries', {
    idAttribute: 'id'
  })

  const normalizedEntries = normalize(
    response.results,
    {
      entries: arrayOf(entries)
    }
  )

  return {
    type: RECEIVE_ENTRIES,
    items: normalizedEntries.result,
    receivedAt: Date.now()
  }
}


function fetchEntries() {
  log.debug('actionsEntries.fetchEntries')

  return dispatch => {
    dispatch(requestEntries())

    request
      .get('/contest/current-entries/')
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .end(function(err, res) {
        if(err) {
          // TODO
        } else {
          dispatch(receiveEntries(res.body))
        }
    })
  }
}


function shouldFetchEntries(state) {
  log.debug('actionsEntries.shouldFetchEntries')

  const entries = state.entries
  if (entries.isFetching) {
    return false
  }
  if ('items' in entries === false) {
    return true
  }
  return false
}


export function fetchEntriesIfNeeded() {
  log.debug('actionsEntries.fetchEntriesIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchEntries(getState())) {
      return dispatch(fetchEntries())
    }
  }
}
