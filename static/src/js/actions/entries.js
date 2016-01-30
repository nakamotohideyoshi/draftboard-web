const moment = require('moment')
// so we can use Promises
const request = require('superagent-promise')(require('superagent'), Promise)
import 'babel-core/polyfill'
import {filter as _filter} from 'lodash'
import {forEach as _forEach} from 'lodash'
import {normalize, Schema, arrayOf} from 'normalizr'

import * as ActionTypes from '../action-types'
import log from '../lib/logging'
import {fetchContestIfNeeded} from './live-contests'
import {setCurrentLineups} from './current-lineups'


// ACTIONS TO REDUCERS
// --------------------------------------------------------

const confirmRelatedEntriesInfo = () => {
  return {
    type: ActionTypes.CONFIRM_RELATED_ENTRIES_INFO
  }
}

const requestEntries = () => {
  return {
    type: ActionTypes.REQUEST_ENTRIES
  }
}

const receiveEntries = (response) => {
  const entriesSchema = new Schema('entries', {
    idAttribute: 'id'
  })
  const normalizedEntries = normalize(
    response,
    arrayOf(entriesSchema)
  )

  let entries = normalizedEntries.entities.entries

  _forEach(entries, (entry) => {
    entry.start = moment(entry.start).valueOf()
  })

  return {
    type: ActionTypes.RECEIVE_ENTRIES,
    items: entries || [],
    receivedAt: Date.now()
  }
}

const storeEntriesPlayers = (entriesPlayers) => {
  return {
    type: ActionTypes.ADD_ENTRIES_PLAYERS,
    entriesPlayers: entriesPlayers
  }
}


// LOCAL HELPER METHODS
// --------------------------------------------------------

const shouldFetchEntries = (state) => {
  const entries = state.entries
  if (entries.isFetching) {
    return false
  }

  return true
}


// PRIMARY METHODS
// --------------------------------------------------------

export const fetchEntries = () => {
  log.trace('actionsEntries.fetchEntries')

  return dispatch => {
    dispatch(requestEntries())

    return request.get(
      '/api/contest/current-entries/'
    ).set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      Accept: 'application/json'
    }).then((res) => {
      return dispatch(receiveEntries(res.body))
    })
  }
}

export const generateLineups = () => {
  return (dispatch, getState) => {
    let lineups = {}

    _forEach(getState().entries.items, (entry) => {
      let id = entry.lineup

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

export const addEntriesPlayers = () => {
  log.trace('actionsEntries.addEntriesPlayers')

  return (dispatch, getState) => {
    const state = getState()
    let entriesPlayers = {}

    const liveEntries = _filter(state.entries.items, (entry) => {
      return entry.start < Date.now()
    })

    _forEach(liveEntries, (entry) => {
      const lineup = state.liveContests[entry.contest].lineups[entry.lineup]
      if (typeof lineup !== 'undefined' && lineup.hasOwnProperty('roster')) {
        entriesPlayers[entry.id] = lineup.roster
      }
    })

    // returning a promise such that we can chain this method
    return Promise.all([
      dispatch(storeEntriesPlayers(entriesPlayers))
    ])
  }
}

const fetchRelatedEntriesInfo = () => {
  log.trace('actionsEntries.fetchRelatedEntriesInfo')

  return (dispatch, getState) => {
    let calls = []

    _forEach(getState().entries.items, (entry) => {
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

export const fetchEntriesIfNeeded = (force) => {
  log.trace('actionsEntries.fetchEntriesIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchEntries(getState()) === true || force === true) {
      log.info('actions.entries.fetchEntriesIfNeeded() - Updating entries')

      return dispatch(
        fetchEntries()
      ).then(() =>
        dispatch(fetchRelatedEntriesInfo())
      )
    }

    return Promise.resolve('Entries already fetched')
  }
}

// Once an entry is created, the server returns it to us in Entry object form. We then need to
// stuff it into our entries store via receiveEntries().
export const insertEntry = (entry) => {
  log.trace('actionsEntries.insertEntry')
  return (dispatch) => {
    dispatch(receiveEntries([entry]))
  }
}
