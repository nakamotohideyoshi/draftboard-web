// so we can use Promises
import 'babel-core/polyfill'
const request = require('superagent-promise')(require('superagent'), Promise)
import moment from 'moment'
import { forEach as _forEach } from 'lodash'
import _ from 'lodash'
import { normalize, Schema, arrayOf } from 'normalizr'

import * as ActionTypes from '../action-types'
import log from '../lib/logging'
import { fetchTeamsIfNeeded } from './sports'
import { updateLivePlayersStats } from './live-players'
import { fetchPlayerBoxScoreHistoryIfNeeded } from './player-box-score-history-actions.js'


// dispatch to reducer methods


/**
 * Dispatch information to reducer that we have completed getting all information related to the draft group
 * Used to make the components aware tht we have finished pulling information.
 * NOTE: this method must be wrapped with dispatch()
 * @param  {number} id  Contest ID
 * @return {object}     Changes for reducer
 */
const confirmDraftGroupStored = (id) => ({
  type: ActionTypes.CONFIRM_LIVE_DRAFT_GROUP_STORED,
  id,
})

/**
 * Dispatch information to reducer that we are trying to get fantasy points for players in a draft group
 * Used to prevent repeat calls while requesting.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const requestDraftGroupFP = (id) => ({
  id,
  type: ActionTypes.REQUEST_LIVE_DRAFT_GROUP_FP,
})

/**
 * Dispatch information to reducer that we are trying to get draft group information
 * Used to prevent repeat calls while requesting.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const requestDraftGroupInfo = (id) => ({
  id,
  type: ActionTypes.REQUEST_LIVE_DRAFT_GROUP_INFO,
})

/**
 * Dispatch API response object of players with fantasy points in a draft group
 * Also pass through an updated at so that we can expire and re-poll after a period of time.
 * NOTE: this method must be wrapped with dispatch()
 * @param  {number} id            Contest ID
 * @param  {object} response      Response of players
 * @return {object}               Changes for reducer
 */
const receiveDraftGroupFP = (id, players) => ({
  type: ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_FP,
  id,
  players,
  expiresAt: moment(Date.now()).add(10, 'minutes'),
})

/**
 * Dispatch API response object of draft group information
 * Also pass through an updated at so that we can expire and re-poll after a period of time.
 * NOTE: this method must be wrapped with dispatch()
 * @param  {number} id            Contest ID
 * @param  {object} response      API response
 * @return {object}               Changes for reducer
 */
const receiveDraftGroupInfo = (id, response) => {
  const playerSchema = new Schema('players', {
    idAttribute: 'player_id',
  })

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
    expiresAt: moment(Date.now()).add(12, 'hours'),
  }
}


// helper methods


/**
 * API GET to return draft group info
 * @param {number} id  Draft group ID
 * @return {promise}   Promise that resolves with API response body to reducer
 */
const fetchDraftGroupInfo = (id) => (dispatch) => {
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

/**
 * Method to determine whether we need to fetch fantasy points for draft group players.
 * @param  {object} state Current Redux state to test
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchDraftGroupFP = (state, id) => {
  const liveDraftGroups = state.liveDraftGroups;

  // error if no draft group to associate players to
  if (id in liveDraftGroups === false) {
    throw new Error('You cannot get fantasy points for a player that is not in the draft group')
  }
  // do not fetch if fetching info
  if (liveDraftGroups[id].isFetchingInfo === true) {
    return false
  }
  // do not fetch if fetching fp
  if (liveDraftGroups[id].isFetchingFP === true) {
    return false
  }

  // fetch if expired
  if (moment().isBefore(liveDraftGroups[id].fpExpiresAt)) {
    return false
  }

  return true
}

/**
 * Method to determine whether we need to fetch draft group.
 * Fetch if it currently does not exist at all yet.
 * @param  {object} state Current Redux state to test
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchDraftGroup = (state, id) => {
  const liveDraftGroups = state.liveDraftGroups;

  // fetch if draft group does not exist yet
  if (liveDraftGroups.hasOwnProperty(id) === false) {
    return true
  }

  // fetch if expired
  if (moment().isBefore(liveDraftGroups[id].infoExpiresAt)) {
    return false
  }

  return false
}


// primary methods (mainly exported, some needed in there to have proper init of const)


/**
 * API GET to return fantasy points of players in a draft group
 * @param {number} id  Draft group ID
 * @return {promise}   Promise that resolves with API response body to reducer
 */
export const fetchDraftGroupFP = (id) => (dispatch) => {
  dispatch(requestDraftGroupFP(id))

  log.info('actions.fetchDraftGroupFP() - Updating player fantasy points')

  return request.get(
    `/api/draft-group/fantasy-points/${id}/`
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    Accept: 'application/json',
  }).then((res) => {
    let players = res.body.players
    if (_.size(players) === 0) {
      players = {}
      log.debug('shouldFetchDraftGroupFP() - FP not available yet', id)
    }

    return dispatch(receiveDraftGroupFP(id, players))
  })
}

/**
 * Get fantasy points for players in a draft group if need be
 * @param {number} id  Draft group ID
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchDraftGroupFPIfNeeded = (id) => (dispatch, getState) => {
  if (shouldFetchDraftGroupFP(getState(), id) === true) {
    return dispatch(fetchDraftGroupFP(id))
  }

  return Promise.resolve('Draft group FP not needed')
}

/**
 * Get draft group if needed, which involves getting info, fantasy points of players, and seasonal stats for players
 * @param {number} id  Draft group ID
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchDraftGroupIfNeeded = (id) => (dispatch, getState) => {
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

/**
 * Remove all draft groups that have ended. While looping through, aggregate all related lineups and contests and remove
 * those as well.
 * @return {Promise} Return the promise of all of the calls being run simultaneously.
 */
export const removeUnusedDraftGroups = () => (dispatch, getState) => {
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

  if (draftGroupIds.length === 0) return null

  return dispatch({
    type: ActionTypes.REMOVE_LIVE_DRAFT_GROUPS,
    ids: draftGroupIds,
    removedAt: Date.now(),
  })
}

/**
 * Used to update a player's stats when a Pusher call sends us new info
 * @param  {number} playerId      Player ID
 * @param  {object} eventCall     Pusher event that came through
 * @param  {number} draftGroupId) Draft group ID to find player in redux store
 * @return {object}               Changes for reducer, wrapped in thunk
 */
export const updatePlayerStats = (playerId, eventCall, draftGroupId) => (dispatch, getState) => {
  // if this is a relevant player, update their stats
  if (getState().livePlayers.relevantPlayers.hasOwnProperty(eventCall.fields.srid_player)) {
    log.info('stats are for relevantPlayer, calling updateLivePlayersStats()', eventCall)

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
