"use strict"

import 'babel-core/polyfill'; // so I can use Promises
var moment = require('moment')
import request from 'superagent'
import { normalize, Schema, arrayOf } from 'normalizr'
import { forEach as _forEach } from 'lodash'
import { filter as _filter } from 'lodash'

import * as ActionTypes from '../action-types'
import log from '../lib/logging'
import { fetchContestIfNeeded } from './live-contests'
import { setCurrentLineups } from './current-lineups'


// NOTE Mock URLs for now rather than hit the Django API
import urlConfig from '../fixtures/live-config'


function requestEntries() {
  log.debug('actionsEntries.requestEntries')

  return {
    type: ActionTypes.REQUEST_ENTRIES
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
    type: ActionTypes.RECEIVE_ENTRIES,
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
    type: ActionTypes.CONFIRM_RELATED_ENTRIES_INFO
  }
}


export function fetchEntriesIfNeeded() {
  log.debug('actionsEntries.fetchEntriesIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchEntries(getState()) === false) {
      return Promise.reject('Entries already fetched')
    }

    return Promise.all([
      dispatch(fetchEntries())
    ]).then(() =>
      dispatch(fetchRelatedEntriesInfo())
    )
  }
}


export function fetchRelatedEntriesInfo() {
  log.debug('actionsEntries.fetchRelatedEntriesInfo')

  return (dispatch, getState) => {
    let calls = []

    _forEach(getState().entries.items, function(entry, id) {
      calls.push(dispatch(fetchContestIfNeeded(entry.contest)))
    })

    return Promise.all(
      calls
    ).then(() =>
      dispatch(confirmRelatedEntriesInfo())
    )
  }
}


function storeEntriesPlayers(entriesPlayers) {
  log.debug('actionsEntries.storeEntriesPlayers')

  return {
    type: ActionTypes.ADD_ENTRIES_PLAYERS,
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

    // returning a promise such that we can chain this method
    return Promise.all([
      dispatch(storeEntriesPlayers(entriesPlayers))
    ])
  }
}


export function generateLineups() {
  log.debug('actionsEntries.generateLineups')

  return (dispatch, getState) => {
    let lineups = {}

    _forEach(getState().entries.items, function(entry) {
      let id = entry.lineup

      if (id in lineups) {
        lineups[id].contests.push(entry.contest)
      } else {
        lineups[id] = {
          id: entry.lineup,
          name: entry.lineup_name,
          start: entry.start,
          roster: entry.roster,
          contests: [entry.contest]
        }
      }
    })

    // returning a promise such that we can chain this method
    return Promise.all([
      dispatch(setCurrentLineups(lineups))
    ])
  }
}
