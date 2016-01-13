var moment = require('moment')
// so we can use Promises
import 'babel-core/polyfill'
import { normalize, Schema, arrayOf } from 'normalizr'
import { forEach as _forEach } from 'lodash'
import { filter as _filter } from 'lodash'
const request = require('superagent-promise')(require('superagent'), Promise)

import * as ActionTypes from '../action-types'
import log from '../lib/logging'
import { fetchContestIfNeeded } from './live-contests'
import { setCurrentLineups } from './current-lineups'


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
    response,
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

    return request.get(
      '/api/contest/current-entries/'
    ).set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'Accept': 'application/json'
    }).then(function(res) {
      return dispatch(receiveEntries(res.body))
    })
  }
}


function shouldFetchEntries(state) {
  log.debug('actionsEntries.shouldFetchEntries')

  const entries = state.entries
  if (entries.isFetching) {
    return false
  }

  return true
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
      return Promise.resolve('Entries already fetched')
    }

    log.info('actions.entries.fetchEntriesIfNeeded() - Updating entries')

    return dispatch(
      fetchEntries()
    ).then(() =>
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
      dispatch(addEntriesPlayers())
    ).then(() =>
      dispatch(generateLineups())
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
    const state = getState()
    let lineups = {}

    _forEach(getState().entries.items, function(entry) {
      let id = entry.lineup
      // let contest = state.liveContests[entry.contest]

      if (id in lineups) {
        lineups[id].contests.push(entry.contest)
      } else {
        lineups[id] = {
          id: entry.lineup,
          draft_group: entry.draft_group,
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


// Once an entry is created, the server returns it to us in Entry object form. We then need to
// stuff it into our entries store via receiveEntries().
export function insertEntry(entry) {
  log.debug('actionsEntries.insertEntry')
  return(dispatch) => {
    dispatch(receiveEntries([entry]))
  }
}
