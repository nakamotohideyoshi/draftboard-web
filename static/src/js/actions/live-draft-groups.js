var moment = require('moment')
// so we can use Promises
import 'babel-core/polyfill'
const request = require('superagent-promise')(require('superagent'), Promise)
import { forEach as _forEach } from 'lodash'
import _ from 'lodash'
import { normalize, Schema, arrayOf } from 'normalizr'

import * as ActionTypes from '../action-types'
import log from '../lib/logging'
import { mergeBoxScores } from './current-box-scores'
import { fetchTeamsIfNeeded } from './sports'


const playerSchema = new Schema('players', {
  idAttribute: 'player_id'
})


// TODO make this sport dependent
function _calculateTimeRemaining(boxScore) {
  log.debug('actionsLiveDraftGroup._calculateTimeRemaining')

  // if the game hasn't started, return full time
  if (boxScore.fields.quarter === '') {
    return 48
  }

  const clockMinSec = boxScore.fields.clock.split(':')
  const remainingMinutes = (4 - parseInt(boxScore.fields.quarter)) * 12

  // round up to the nearest minute
  return remainingMinutes + parseInt(clockMinSec[0]) + 1
}


// Used to update a player's FP when a Pusher call sends us new info
export function updatePlayerFP(id, playerId, fp) {
  log.warn('actionsLiveDraftGroup.updatePlayerFP', id, playerId, fp)
  return {
    id: id,
    type: ActionTypes.UPDATE_LIVE_DRAFT_GROUP_PLAYER_FP,
    playerId: playerId,
    fp: fp
  }
}


// DRAFT GROUP FANTASY POINTS
// -----------------------------------------------------------------------

function requestDraftGroupFP(id) {
  log.debug('actionsLiveDraftGroup.requestDraftGroupFP')

  return {
    id: id,
    type: ActionTypes.REQUEST_LIVE_DRAFT_GROUP_FP
  }
}


function fetchDraftGroupFP(id) {
  log.debug('actionsLiveDraftGroup.fetchDraftGroupFP')

  return dispatch => {
    dispatch(requestDraftGroupFP(id))

    return request.get(
      '/api/draft-group/fantasy-points/' + id + '/'
    ).set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'Accept': 'application/json'
    }).then(function(res) {
      if (_.size(res.body.players) === 0) {
        log.debug('shouldFetchDraftGroupFP() - FP not available yet', id)
        return Promise.resolve('Fantasy points not available yet')
      }

      return dispatch(receiveDraftGroupFP(id, res.body))
    })
  }
}


function receiveDraftGroupFP(id, response) {
  log.debug('actionsLiveDraftGroup.receiveDraftGroupFP')

  return {
    type: ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_FP,
    id: id,
    players: response.players,
    updatedAt: Date.now()
  }
}


function shouldFetchDraftGroupFP(state, id) {
  log.debug('actionsLiveDraftGroup.shouldFetchDraftGroupFP')

  var liveDraftGroups = state.liveDraftGroups;

  if (id in liveDraftGroups === false)
    throw new Error('You cannot get fantasy points for a player that is not in the draft group')
  if (liveDraftGroups[id].isFetchingInfo === true)
    return false
  if (liveDraftGroups[id].isFetchingFP === true)
    return false

  return true
}


export function fetchDraftGroupFPIfNeeded(id) {
  log.debug('actionsLiveDraftGroup.fetchDraftGroupFPIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchDraftGroupFP(getState(), id)) {
      return dispatch(fetchDraftGroupFP(id))
    }
  }
}



// UPDATE DRAFT GROUP STATS
// -----------------------------------------------------------------------

export function fetchDraftGroupStats(id) {
  log.debug('actionsLiveDraftGroup.fetchDraftGroupStats')
  return (dispatch, getState) => {
    if (shouldFetchDraftGroupFP(getState(), id)) {
      return Promise.all([
        dispatch(fetchDraftGroupFP(id)),
        dispatch(fetchDraftGroupBoxScores(id))
      ])
    }
  }
}



// DRAFT GROUP INFO
// -----------------------------------------------------------------------

function requestDraftGroupInfo(id) {
  log.debug('actionsLiveDraftGroup.requestDraftGroupInfo')

  return {
    id: id,
    type: ActionTypes.REQUEST_LIVE_DRAFT_GROUP_INFO
  }
}


function receiveDraftGroupInfo(id, response) {
  log.debug('actionsLiveDraftGroup.receiveDraftGroupInfo')

  const normalizedPlayers = normalize(
    response.players,
    arrayOf(playerSchema)
  )

  let players = normalizedPlayers.entities.players
  let playersBySRID = {}

  _forEach(players, (player) => {
    playersBySRID[player.player_srid] = player.player_id
  })

  return {
    type: ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_INFO,
    id: id,
    players: players,
    playersBySRID: playersBySRID,
    sport: response.sport,
    start: moment(response.start).valueOf(),
    end: moment(response.end).valueOf(),
    expiresAt: Date.now() + 86400000
  }
}


function fetchDraftGroupInfo(id) {
  log.debug('actionsLiveDraftGroup.fetchDraftGroupInfo')

  return dispatch => {
    dispatch(requestDraftGroupInfo(id))

    return request.get(
      '/api/draft-group/' + id + '/'
    ).set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'Accept': 'application/json'
    }).then(function(res) {
      return Promise.all([
        dispatch(receiveDraftGroupInfo(id, res.body)),
        dispatch(fetchTeamsIfNeeded(res.body.sport))
      ])
    })
  }
}



// DRAFT GROUP INFO
// -----------------------------------------------------------------------

function requestDraftGroupBoxScores(id) {
  log.debug('actionsLiveDraftGroup.requestDraftGroupBoxScores')

  return {
    id: id,
    type: ActionTypes.REQUEST_LIVE_DRAFT_GROUP_BOX_SCORES
  }
}


function receiveDraftGroupBoxScores(id, boxScores) {
  log.debug('actionsLiveDraftGroup.receiveDraftGroupBoxScores')

  return {
    type: ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_BOX_SCORES,
    id: id,
    boxScores: boxScores,
    updatedAt: Date.now() + 86400000
  }
}


function organizeBoxScores(response) {
  let boxScores = {}

  // SO HACKY
  _forEach(response.games, (game) => {
    boxScores[game.srid] = {
      timeRemaining: null,
      fields: {
        srid_game: game.srid,
        srid_away: game.srid_away,
        srid_home: game.srid_home,
        start: game.start
      }
    }
  })

  _forEach(response.boxscores, (boxScore) => {
    boxScore.timeRemaining = _calculateTimeRemaining(boxScore)
    boxScores[boxScore.srid_game] = boxScore
  })

  return boxScores
}


function fetchDraftGroupBoxScores(id) {
  log.debug('actionsLiveDraftGroup.fetchDraftGroupBoxScores')

  return dispatch => {
    dispatch(requestDraftGroupBoxScores(id))

    return request.get(
      '/api/draft-group/boxscores/' + id + '/'
    ).set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'Accept': 'application/json'
    }).then(function(res) {
      if (res.body.length === 0) {
        log.debug('shouldFetchDraftGroupFP() - Box scores not available yet', id)
        return Promise.resolve('Box scores not available yet')
      }

      const boxScores = organizeBoxScores(res.body)

      dispatch(receiveDraftGroupBoxScores(id, boxScores))

      return dispatch(
        mergeBoxScores(boxScores)
      )
    })
  }
}


function confirmDraftGroupStored(id) {
  log.debug('actionsEntries.confirmRelatedEntriesInfo')

  return {
    type: ActionTypes.CONFIRM_LIVE_DRAFT_GROUP_STORED,
    id: id
  }
}


function shouldFetchDraftGroup(state, id) {
  log.debug('actionsLiveDraftGroup.shouldFetchDraftGroup')

  return id in state.liveDraftGroups === false
}


export function fetchDraftGroupIfNeeded(id) {
  log.debug('actionsLiveDraftGroup.fetchDraftGroupIfNeeded')

  return (dispatch, getState) => {
    if (shouldFetchDraftGroup(getState(), id) === false) {
      log.debug('actionsLiveDraftGroup.fetchDraftGroupIfNeeded() - Draft group exists')
      return Promise.resolve('Draft group exists')
    }
    return Promise.all([
      dispatch(fetchDraftGroupInfo(id)),
      dispatch(fetchDraftGroupFP(id)),
      dispatch(fetchDraftGroupBoxScores(id))
    ])
    .then(() =>
      dispatch(confirmDraftGroupStored(id))
    )
  }
}
