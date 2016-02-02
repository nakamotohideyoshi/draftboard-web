const moment = require('moment')
// so we can use Promises
import 'babel-core/polyfill'
const request = require('superagent-promise')(require('superagent'), Promise)
import { forEach as _forEach } from 'lodash'
import _ from 'lodash'
import { normalize, Schema, arrayOf } from 'normalizr'

import * as ActionTypes from '../action-types'
import log from '../lib/logging'
import { fetchTeamsIfNeeded } from './sports'
import { updateLivePlayersStats } from './live-players'
import { fetchPlayerBoxScoreHistoryIfNeeded } from './player-box-score-history-actions.js'


const playerSchema = new Schema('players', {
  idAttribute: 'player_id',
})


// Used to update a player's stats when a Pusher call sends us new info
export function updatePlayerStats(playerId, eventCall, draftGroupId) {
  log.trace('actionsLiveDraftGroup.updatePlayerStats')

  return (dispatch, getState) => {
    const state = getState()

    // if this is a relevant player, update their stats
    if (state.livePlayers.relevantPlayers.hasOwnProperty(eventCall.fields.srid_player)) {
      log.info('stats are for relevantPlayer, calling updateLivePlayersStats()', eventCall.fields.srid_player)
      dispatch(updateLivePlayersStats(
        eventCall.fields.srid_player,
        eventCall.fields
      ))
    }

    return dispatch({
      id: draftGroupId,
      type: ActionTypes.UPDATE_LIVE_DRAFT_GROUP_PLAYER_FP,
      playerId,
      fp: eventCall.fields.fantasy_points,
    })
  }
}


// DRAFT GROUP FANTASY POINTS
// -----------------------------------------------------------------------

function requestDraftGroupFP(id) {
  log.trace('actionsLiveDraftGroup.requestDraftGroupFP')

  return {
    id,
    type: ActionTypes.REQUEST_LIVE_DRAFT_GROUP_FP,
  }
}

function receiveDraftGroupFP(id, players) {
  log.trace('actionsLiveDraftGroup.receiveDraftGroupFP')

  return {
    type: ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_FP,
    id,
    players,
    updatedAt: Date.now(),
  }
}

function fetchDraftGroupFP(id) {
  log.trace('actionsLiveDraftGroup.fetchDraftGroupFP')

  return dispatch => {
    dispatch(requestDraftGroupFP(id))

    return request.get(
      `/api/draft-group/fantasy-points/${id}/`
    ).set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      Accept: 'application/json',
    }).then((res) => {
      let players = res.body.players
      if (_.size(players) === 0) {
        players = {}
        log.trace('shouldFetchDraftGroupFP() - FP not available yet', id)
      }

      return dispatch(receiveDraftGroupFP(id, players))
    })
  }
}


function shouldFetchDraftGroupFP(state, id) {
  log.trace('actionsLiveDraftGroup.shouldFetchDraftGroupFP')

  const liveDraftGroups = state.liveDraftGroups;

  if (id in liveDraftGroups === false) {
    throw new Error('You cannot get fantasy points for a player that is not in the draft group')
  }
  if (liveDraftGroups[id].isFetchingInfo === true) {
    return false
  }
  if (liveDraftGroups[id].isFetchingFP === true) {
    return false
  }

  return true
}


export function fetchDraftGroupFPIfNeeded(id) {
  log.trace('actionsLiveDraftGroup.fetchDraftGroupFPIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchDraftGroupFP(getState(), id)) {
      return dispatch(fetchDraftGroupFP(id))
    }
  }
}


// UPDATE DRAFT GROUP STATS
// -----------------------------------------------------------------------

export function fetchDraftGroupStats(id) {
  log.trace('actionsLiveDraftGroup.fetchDraftGroupStats')
  return (dispatch, getState) => {
    if (shouldFetchDraftGroupFP(getState(), id)) {
      return dispatch(fetchDraftGroupFP(id))
    }
  }
}


// DRAFT GROUP INFO
// -----------------------------------------------------------------------

function requestDraftGroupInfo(id) {
  log.trace('actionsLiveDraftGroup.requestDraftGroupInfo')

  return {
    id,
    type: ActionTypes.REQUEST_LIVE_DRAFT_GROUP_INFO,
  }
}


function receiveDraftGroupInfo(id, response) {
  log.trace('actionsLiveDraftGroup.receiveDraftGroupInfo')

  const normalizedPlayers = normalize(
    response.players,
    arrayOf(playerSchema)
  )

  const players = normalizedPlayers.entities.players
  const playersBySRID = {}

  _forEach(players, (player) => {
    playersBySRID[player.player_srid] = player.player_id
  })

  return {
    type: ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_INFO,
    id,
    players,
    playersBySRID,
    sport: response.sport,
    start: moment(response.start).valueOf(),
    end: moment(response.end).valueOf(),
    expiresAt: Date.now() + 86400000,
  }
}


export function fetchDraftGroupInfo(id) {
  log.trace('actionsLiveDraftGroup.fetchDraftGroupInfo')

  return dispatch => {
    dispatch(requestDraftGroupInfo(id))

    return request.get(
      `/api/draft-group/${id}/`
    ).set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      Accept: 'application/json',
    }).then((res) => Promise.all([
      dispatch(receiveDraftGroupInfo(id, res.body)),
      dispatch(fetchTeamsIfNeeded(res.body.sport)),
    ]))
  }
}


function confirmDraftGroupStored(id) {
  log.trace('actionsEntries.confirmRelatedEntriesInfo')

  return {
    type: ActionTypes.CONFIRM_LIVE_DRAFT_GROUP_STORED,
    id,
  }
}


function shouldFetchDraftGroup(state, id) {
  log.trace('actionsLiveDraftGroup.shouldFetchDraftGroup')

  return id in state.liveDraftGroups === false
}


export function fetchDraftGroupIfNeeded(id) {
  log.trace('actionsLiveDraftGroup.fetchDraftGroupIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchDraftGroup(getState(), id) === false) {
      log.trace('actionsLiveDraftGroup.fetchDraftGroupIfNeeded() - Draft group exists')
      return Promise.resolve('Draft group exists')
    }
    return Promise.all([
      dispatch(fetchDraftGroupInfo(id)),
      dispatch(fetchDraftGroupFP(id)),
      dispatch(fetchPlayerBoxScoreHistoryIfNeeded('nba')),
    ])
    .then(() =>
      dispatch(confirmDraftGroupStored(id))
    )
  }
}


/**
 * Remove all draft groups that have ended. While looping through, aggregate all related lineups and contests and remove
 * those as well.
 * @return {Promise} Return the promise of all of the calls being run simultaneously.
 */
export const removeUnusedDraftGroups = () => {
  log.trace('actionsLiveDraftGroup.removeEndedDraftGroups')

  return (dispatch, getState) => {
    const draftGroupIds = []
    const currentLineups = getState().currentLineups.items || {}

    _forEach(getState().liveDraftGroups, (draftGroup) => {
      const id = draftGroup.id
      const lineups = _.filter(currentLineups, (lineup) => lineup.draft_group === id)

      // if there are no lineups the group is related to, then remove
      if (lineups.length === 0) {
        draftGroupIds.push(id)
      }
    })

    return dispatch({
      type: ActionTypes.REMOVE_LIVE_DRAFT_GROUPS,
      ids: draftGroupIds,
      removedAt: Date.now(),
    })
  }
}
