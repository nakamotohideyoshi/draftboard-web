import _ from 'lodash'
// so we can use Promises
import 'babel-core/polyfill'
const request = require('superagent-promise')(require('superagent'), Promise)
var moment = require('moment')

import * as ActionTypes from '../action-types'
import log from '../lib/logging'
import { fetchDraftGroupIfNeeded } from './live-draft-groups'


export function fetchRelatedDraftGroupsInfo() {
  log.trace('actionsCurrentDraftGroups.fetchRelatedDraftGroupsInfo')

  return (dispatch, getState) => {
    let calls = []

    _.forEach(getState().currentDraftGroups.items, (draftGroup) => {
      calls.push(dispatch(fetchDraftGroupIfNeeded(draftGroup.pk)))
    })

    return Promise.all(calls)
  }
}


function requestCurrentDraftGroups() {
  log.trace('actionsCurrentDraftGroups.requestCurrentDraftGroups')

  return {
    type: ActionTypes.REQUEST_CURRENT_DRAFT_GROUPS
  }
}


function receiveCurrentDraftGroups(response) {
  log.trace('actionsCurrentDraftGroups.receiveCurrentDraftGroups')

  return {
    type: ActionTypes.RECEIVE_CURRENT_DRAFT_GROUPS,
    draftGroups: response,
    updatedAt: Date.now()
  }
}


function fetchCurrentDraftGroups() {
  log.trace('actionsCurrentDraftGroups.fetchCurrentDraftGroups')

  return dispatch => {
    dispatch(requestCurrentDraftGroups())

    return request.get(
      '/api/draft-group/current/'
    ).set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'Accept': 'application/json'
    }).then(function(res) {
      return dispatch(receiveCurrentDraftGroups(res.body))
    })
  }
}


function shouldFetchCurrentDraftGroups(state) {
  log.trace('actionsCurrentDraftGroups.shouldFetchCurrentDraftGroups')

  // if expired, then get
  let expiration = moment(state.currentDraftGroups.updatedAt).add(1, 'minutes')
  if (moment().isAfter(expiration)) {
    return true
  }

  if ('items' in state.currentDraftGroups === false) {
    return true
  }

  return state.currentDraftGroups.items.length === 0
}


export function fetchCurrentDraftGroupsIfNeeded(id) {
  log.trace('actionsCurrentDraftGroups.fetchCurrentDraftGroupsIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchCurrentDraftGroups(getState()) === false) {
      return Promise.resolve('Draft group exists')
    }

    log.info('actions.currentDraftGroups.fetchCurrentDraftGroupsIfNeeded() - Updating draft groups')

    return dispatch(
      fetchCurrentDraftGroups()
    ).then(() =>
      dispatch(fetchRelatedDraftGroupsInfo())
    )
  }
}
