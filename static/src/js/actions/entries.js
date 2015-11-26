"use strict"

import 'babel-core/polyfill'; // so I can use Promises
var moment = require('moment')
import request from 'superagent'
import { normalize, Schema, arrayOf } from 'normalizr'
import { forEach as _forEach } from 'lodash'
import { filter as _filter } from 'lodash'

import log from '../lib/logging'
import { fetchContestIfNeeded } from './live-contests'
import { setCurrentLineups } from './current-lineups'


export const ADD_ENTRIES_PLAYERS = 'ADD_ENTRIES_PLAYERS'
export const CONFIRM_RELATED_ENTRIES_INFO = 'CONFIRM_RELATED_ENTRIES_INFO'
export const REQUEST_ENTRIES = 'REQUEST_ENTRIES'
export const RECEIVE_ENTRIES = 'RECEIVE_ENTRIES'

import urlConfig from '../fixtures/live-config'


export function errorHandler(reason) {
  console.error('uh oh', reason)
}


function requestEntries() {
  log.debug('actionsEntries.requestEntries')

  return {
    type: REQUEST_ENTRIES
  }
}


function receiveEntries(response) {
  log.debug('actionsEntries.receiveEntries')

  const entriesSchema = new Schema('entries', {
    idAttribute: 'id'
  })
  const normalizedEntries = normalize(
    response.results,
    arrayOf(entriesSchema)
  )

  let entries = normalizedEntries.entities.entries

  _forEach(entries, function(entry) {
    entry.start = moment(entry.start).valueOf()
  })

  return {
    type: RECEIVE_ENTRIES,
    items: entries || [],
    receivedAt: Date.now()
  }
}


export function fetchEntries() {
  log.debug('actionsEntries.fetchEntries')

  return dispatch => {
    dispatch(requestEntries())

    return request
      .get('/api/contest/current-entries/')
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          console.error(err)
          // TODO
        } else {
          return dispatch(receiveEntries(res.body))
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

  if ('items' in entries === false || entries.items.length === 0) {
    return true
  }
  return false
}


function confirmRelatedEntriesInfo() {
  log.debug('actionsEntries.confirmRelatedEntriesInfo')

  return {
    type: CONFIRM_RELATED_ENTRIES_INFO
  }
}


export function fetchEntriesIfNeeded() {
  log.debug('actionsEntries.fetchEntriesIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchEntries(getState())) {
      return Promise.all([
        Promise.all([
          dispatch(fetchEntries())
        ]).catch(errorHandler).then(() => {
          dispatch(fetchRelatedEntriesInfo())
        })
      ]).catch(errorHandler)
    } else {
      return Promise.reject('Entries already fetched')
    }
  }
}


export function fetchRelatedEntriesInfo() {
  log.debug('actionsEntries.fetchRelatedEntriesInfo')

  return (dispatch, getState) => {
    let calls = []

    _forEach(getState().entries.items, function(entry, id) {
      calls.push(dispatch(fetchContestIfNeeded(entry.contest)))
    })

    return Promise.all(calls).catch(errorHandler).then(() => {
      Promise.all([
        dispatch(confirmRelatedEntriesInfo())
      ]).catch(errorHandler)
    })

  }
}


function storeEntriesPlayers(entriesPlayers) {
  log.debug('actionsEntries.storeEntriesPlayers')

  return {
    type: ADD_ENTRIES_PLAYERS,
    entriesPlayers: entriesPlayers
  }
}


export function addEntriesPlayers() {
  log.debug('actionsEntries.addEntriesPlayers')

  return (dispatch, getState) => {
    const state = getState()
    let entriesPlayers = {}

    const liveEntries = _filter(state.entries.items, (entry) => {
      return entry.start < Date.now()
    })

    _forEach(liveEntries, (entry) => {
      entriesPlayers[entry.id] = state.liveContests[entry.contest].lineups[entry.lineup].roster
    })

    return Promise.all([
      dispatch(storeEntriesPlayers(entriesPlayers))
    ]).catch(errorHandler)
  }
}


export function generateLineups() {
  log.debug('actionsEntries.generateLineups')

  return (dispatch, getState) => {
    let lineups = []

    _forEach(getState().entries.items, function(entry) {
      lineups.push({
        id: entry.lineup,
        name: entry.lineup_name,
        start: entry.start,
        roster: entry.roster
      })
    })

    return Promise.all([
      dispatch(setCurrentLineups(lineups))
    ]).catch(errorHandler)
  }
}
