import * as ActionTypes from '../action-types';
import forEach from 'lodash/forEach';
import merge from 'lodash/merge';
import { CALL_API } from '../middleware/api';
import { dateNow, hasExpired } from '../lib/utils';

// custom API domain for local dev testing
const { API_DOMAIN = '' } = process.env;


// dispatch to reducer methods

/**
 * Dispatch API response object of contest lineups (in bytes and parsed json)
 * Also pass through an updated at so that we can expire and re-poll after a period of time.
 * NOTE: this method must be wrapped with dispatch()
 * @param  {number} lineupId      Contest ID
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

    players[playerFields.srid_player] = merge(
      {
        lineupId,
        sport,
        id: playerFields.player_id,
      },
      playerFields
    );
  });

  return {
    lineupId,
    players,
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
const fetchPlayersStats = (lineupId) => ({
  [CALL_API]: {
    types: [
      ActionTypes.REQUEST_LIVE_PLAYERS_STATS,
      ActionTypes.RECEIVE_LIVE_PLAYERS_STATS,
      ActionTypes.ADD_MESSAGE,
    ],
    expiresAt: dateNow() + 1000 * 60 * 1,  // 1 minutes
    endpoint: `${API_DOMAIN}/api/contest/lineup/${lineupId}/`,
    requestFields: { lineupId },
    callback: (json) => receivePlayersStats(lineupId, json),
  },
});

/**
 * Method to determine whether we need to fetch a contest.
 * @param  {object} state   Current Redux state to test
 * @param {number} lineupId Lineup ID
 * @return {boolean}        True if we should fetch, false if not
 */
const shouldFetchPlayersStats = (state, lineupId) => {
  // fetch if first time
  if (!(lineupId in state.livePlayers.expiresAt)) return true;

  // fetch if expired
  if (hasExpired(state.livePlayers.expiresAt[lineupId])) return true;

  // fetch if lineup has started
  const lineup = state.currentLineups.items[lineupId] || {};

  return dateNow() > lineup.start;
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
