const request = require('superagent-promise')(require('superagent'), Promise);
import * as ActionTypes from '../action-types';
import forEach from 'lodash/forEach';
import map from 'lodash/map';
import merge from 'lodash/merge';
import zipObject from 'lodash/zipObject';
import { dateNow } from '../lib/utils';
import { GAME_DURATIONS } from './sports';


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
  expiresAt: dateNow() + 1000 * 60,  // 1 minute before trying again
});

/**
 * Dispatch API response object of contest lineups (in bytes and parsed json)
 * Also pass through an updated at so that we can expire and re-poll after a period of time.
 * NOTE: this method must be wrapped with dispatch()
 * @param  {number} id            Contest ID
 * @param  {object} response      Object of players and stats
 * @return {object}               Changes for reducer
 */
const receivePlayersStats = (lineupId, response) => {
  const players = {};
  forEach(response, (player) => {
    // don't include if the player hasn't started
    if (player.started === false ||
        player.hasOwnProperty('data') === false ||
        player.data.length === 0 ||
        player.data[0].hasOwnProperty('fields') === false) {
      return;
    }

    const playerFields = player.data[0].fields;
    const sport = player.data[0].model.split('.')[0];
    const seasonStatTypes = GAME_DURATIONS[sport].seasonStats.types;

    // combine id with the season stats we need and that's it
    const onlyNeededFields = zipObject(
      seasonStatTypes,
      map(seasonStatTypes, (type) => playerFields[type])
    );

    players[playerFields.srid_player] = merge(
      {
        lineupId,
        sport,
        id: playerFields.player_id,
      },
      onlyNeededFields
    );
  });

  return {
    type: ActionTypes.RECEIVE_LIVE_PLAYERS_STATS,
    lineupId,
    players,
    expiresAt: dateNow() + 1000 * 60 * 10,  // 10 minutes
  };
};

/**
 * Dispatch information to reducer that we have new player stats from pusher call
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
export const updateLivePlayersStats = (playerSRID, fields) => ({
  playerSRID,
  fields,
  type: ActionTypes.UPDATE_LIVE_PLAYER_STATS,
});


// helper methods


/**
 * API GET to return all the stats of players within a contest lineup
 * Used in the live section to get detailed game stats for players
 * @param  {number} lineupId   Lineup ID
 * @return {promise}           Promise that resolves with API response body to reducer
 */
const fetchPlayersStats = (lineupId) => (dispatch) => {
  dispatch(requestPlayersStats(lineupId));

  return request.get(
    `/api/contest/lineup/${lineupId}/`
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    Accept: 'application/json',
  }).then(
    (res) => dispatch(receivePlayersStats(lineupId, res.body))
  );
};

/**
 * Method to determine whether we need to fetch a contest.
 * @param  {object} state   Current Redux state to test
 * @param {number} lineupId Lineup ID
 * @return {boolean}        True if we should fetch, false if not
 */
const shouldFetchPlayersStats = (state, lineupId) => {
  const lineup = state.currentLineups.items[lineupId] || {};

  // if we have not yet expired, don't fetch
  if (dateNow() < state.livePlayers.expiresAt) {
    return false;
  }

  // if it has started yet, get
  if (dateNow() < lineup.start) {
    return false;
  }

  return true;
};


// primary methods


export const fetchPlayersStatsIfNeeded = (lineupId) => (dispatch, getState) => {
  if (shouldFetchPlayersStats(getState(), lineupId) === false) {
    return Promise.resolve('Lineup players stats currently being pulled for this lineup');
  }

  return dispatch(
    fetchPlayersStats(lineupId)
  );
};
