import 'babel-core/polyfill';  // so I can use Promises
const request = require('superagent-promise')(require('superagent'), Promise)
import _ from 'lodash'

import * as ActionTypes from '../action-types'


// dispatch to reducer methods


/**
 * Dispatch information to reducer that we are trying to get player stats
 * Used to prevent repeat calls while requesting.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const requestPlayersStats = (lineupId) => ({
  lineupId,
  type: ActionTypes.REQUEST_LIVE_PLAYERS_STATS,
})

/**
 * Dispatch API response object of contest lineups (in bytes and parsed json)
 * Also pass through an updated at so that we can expire and re-poll after a period of time.
 * NOTE: this method must be wrapped with dispatch()
 * @param  {number} id            Contest ID
 * @param  {object} response      Object of players and stats
 * @return {object}               Changes for reducer
 */
const receivePlayersStats = (lineupId, response) => {
  const players = {}
  _.forEach(response, (player) => {
    // don't include if the player hasn't started
    if (player.started === false ||
        player.hasOwnProperty('data') === false ||
        player.data.length === 0 ||
        player.data[0].hasOwnProperty('fields') === false) {
      return
    }

    const playerFields = player.data[0].fields

    players[playerFields.srid_player] = Object.assign(
      { lineup_id: lineupId },
      playerFields
    )
  })

  return {
    type: ActionTypes.RECEIVE_LIVE_PLAYERS_STATS,
    lineupId,
    players,
    receivedAt: Date.now(),
  }
}

/**
 * Dispatch information to reducer that we have new player stats from pusher call
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
export const updateLivePlayersStats = (playerSRID, fields) => ({
  playerSRID,
  fields,
  type: ActionTypes.UPDATE_LIVE_PLAYER_STATS,
})


// helper methods


/**
 * API GET to return all the stats of players within a contest lineup
 * Used in the live section to get detailed game stats for players
 * @param  {number} lineupId   Lineup ID
 * @return {promise}           Promise that resolves with API response body to reducer
 */
const fetchPlayersStats = (lineupId) => (dispatch) => {
  dispatch(requestPlayersStats(lineupId))

  return request.get(
    `/api/contest/lineup/${lineupId}/`
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    Accept: 'application/json',
  }).then(
    (res) => dispatch(receivePlayersStats(lineupId, res.body))
  )
}

/**
 * Method to determine whether we need to fetch a contest.
 * @param  {object} state   Current Redux state to test
 * @param {number} lineupId Lineup ID
 * @return {boolean}        True if we should fetch, false if not
 */
const shouldFetchPlayersStats = (state, lineupId) => state.livePlayers.isFetching.indexOf(lineupId) === -1


// primary methods


export const fetchPlayersStatsIfNeeded = (lineupId) => (dispatch, getState) => {
  if (shouldFetchPlayersStats(getState(), lineupId) === false) {
    return Promise.resolve('Lineup players stats currently being pulled for this lineup')
  }

  return dispatch(
    fetchPlayersStats(lineupId)
  )
}
