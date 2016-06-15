const request = require('superagent-promise')(require('superagent'), Promise);
import { forEach as _forEach } from 'lodash';
import { filter as _filter } from 'lodash';
import { size as _size } from 'lodash';
import { normalize, Schema, arrayOf } from 'normalizr';

import * as ActionTypes from '../action-types';
import log from '../lib/logging';
import { dateNow } from '../lib/utils';
import { fetchTeamsIfNeeded } from './sports';
import { updateLivePlayersStats } from './live-players';
import { fetchPlayerBoxScoreHistoryIfNeeded } from './player-box-score-history-actions.js';


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
  expiresAt: dateNow() + 1000 * 60,  // 1 minute
});

/**
 * Dispatch information to reducer that we are trying to get fantasy points for players in a draft group
 * Used to prevent repeat calls while requesting.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const requestDraftGroupFP = (id) => ({
  id,
  type: ActionTypes.REQUEST_LIVE_DRAFT_GROUP_FP,
  expiresAt: dateNow() + 1000 * 60,  // 1 minute
});

/**
 * Dispatch information to reducer that we are trying to get draft group boxscores (only used for results)
 * Used to prevent repeat calls while requesting.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const requestDraftGroupBoxscores = (id) => ({
  id,
  type: ActionTypes.REQUEST_DRAFT_GROUP_BOXSCORES,
  expiresAt: dateNow() + 1000 * 60,  // 1 minute
});

/**
 * Dispatch information to reducer that we are trying to get draft group information
 * Used to prevent repeat calls while requesting.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const requestDraftGroupInfo = (id) => ({
  id,
  type: ActionTypes.LIVE_DRAFT_GROUP__INFO__REQUEST,
  expiresAt: dateNow() + 1000 * 60,  // 1 minute
});

/**
 * Dispatch API response object of boxscores for a draft group (only used for results)
 * NOTE: this method must be wrapped with dispatch()
 * @param  {number} id            Contest ID
 * @param  {object} response      Response of players
 * @return {object}               Changes for reducer
 */
const receiveDraftGroupBoxscores = (id, boxscores) => ({
  type: ActionTypes.RECEIVE_DRAFT_GROUP_BOXSCORES,
  id,
  boxscores,
  expiresAt: dateNow() + 1000 * 60 * 10,  // 10 minutes
});

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
  expiresAt: dateNow() + 1000 * 60 * 10,  // 10 minutes
});

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
  });

  const normalizedPlayers = normalize(
    response.players,
    arrayOf(playerSchema)
  );

  const players = normalizedPlayers.entities.players;
  const playersBySRID = {};

  _forEach(players, (player) => {
    playersBySRID[player.player_srid] = player.player_id;
  });

  return {
    type: ActionTypes.LIVE_DRAFT_GROUP__INFO__RECEIVE,
    id,
    players,
    playersBySRID,
    sport: response.sport,
    start: new Date(response.start).getTime(),
    end: new Date(response.end).getTime(),
    closed: (response.closed !== null) ? new Date(response.closed).getTime() : null,
    expiresAt: dateNow() + 1000 * 60 * 60 * 12,  // 12 hours
  };
};


// helper methods


/**
 * API GET to return draft group info
 * @param {number} id  Draft group ID
 * @return {promise}   Promise that resolves with API response body to reducer
 */
const fetchDraftGroupInfo = (id) => (dispatch) => {
  dispatch(requestDraftGroupInfo(id));

  return request.get(
    `/api/draft-group/${id}/`
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    Accept: 'application/json',
  }).then((res) => Promise.all([
    dispatch(receiveDraftGroupInfo(id, res.body)),
    dispatch(fetchTeamsIfNeeded(res.body.sport)),
  ]));
};

/**
 * Method to determine whether we need to fetch boxscores for a draft group.
 * @param  {object} state Current Redux state to test
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchDraftGroupBoxscores = (state, id) => {
  const liveDraftGroups = state.liveDraftGroups;

  // error if no draft group to associate players to
  if (liveDraftGroups.hasOwnProperty(id) === false) {
    throw new Error('You cannot get boxscore data for a draft group that does not exist yet');
  }

  // don't fetch until expired
  if (dateNow() < liveDraftGroups[id].boxscoresExpiresAt) {
    return false;
  }

  // do not fetch if fetching info
  if (liveDraftGroups[id].isFetchingBoxscores === true) {
    return false;
  }

  return true;
};

/**
 * Method to determine whether we need to fetch fantasy points for draft group players.
 * @param  {object} state Current Redux state to test
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchDraftGroupFP = (state, id) => {
  const liveDraftGroups = state.liveDraftGroups;

  // error if no draft group to associate players to
  if (liveDraftGroups.hasOwnProperty(id) === false) {
    throw new Error('You cannot get fantasy points for a draft group that does not exist yet');
  }

  // don't fetch until expired
  if (dateNow() < liveDraftGroups[id].fpExpiresAt) {
    return false;
  }

  return true;
};

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
    return true;
  }

  // fetch if expired
  if (dateNow() > liveDraftGroups[id].infoExpiresAt) {
    return true;
  }

  return false;
};


// primary methods (mainly exported, some needed in there to have proper init of const)

/**
 * API GET to return boxscores for a draft group (used in results only)
 * @param {number} id  Draft group ID
 * @return {promise}   Promise that resolves with API response body to reducer
 */
export const fetchDraftGroupBoxscores = (id) => (dispatch) => {
  dispatch(requestDraftGroupBoxscores(id));

  return request.get(
    `/api/draft-group/boxscores/${id}/`
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    Accept: 'application/json',
  }).then(
    (res) => dispatch(receiveDraftGroupBoxscores(id, res.body))
  );
};

/**
 * API GET to return fantasy points of players in a draft group
 * @param {number} id  Draft group ID
 * @return {promise}   Promise that resolves with API response body to reducer
 */
export const fetchDraftGroupFP = (id) => (dispatch) => {
  dispatch(requestDraftGroupFP(id));

  log.info('actions.fetchDraftGroupFP() - Updating player fantasy points');

  return request.get(
    `/api/draft-group/fantasy-points/${id}/`
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    Accept: 'application/json',
  }).then((res) => {
    let players = res.body.players;

    // default to empty if FP isn't available yet
    if (_size(players) === 0) players = {};

    return dispatch(receiveDraftGroupFP(id, players));
  });
};

/**
 * Get fantasy points for players in a draft group if need be
 * @param {number} id  Draft group ID
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchDraftGroupBoxscoresIfNeeded = (id) => (dispatch, getState) => {
  if (shouldFetchDraftGroupBoxscores(getState(), id) === true) {
    return dispatch(fetchDraftGroupBoxscores(id));
  }

  return Promise.resolve('Draft group boxscores not needed');
};

/**
 * Get fantasy points for players in a draft group if need be
 * @param {number} id  Draft group ID
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchDraftGroupFPIfNeeded = (id) => (dispatch, getState) => {
  if (shouldFetchDraftGroupFP(getState(), id) === true) {
    return dispatch(fetchDraftGroupFP(id));
  }

  return Promise.resolve('Draft group FP not needed');
};

/**
 * Get draft group if needed, which involves getting info, fantasy points of players, and seasonal stats for players
 * @param {number} id  Draft group ID
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchDraftGroupIfNeeded = (id, sport) => (dispatch, getState) => {
  if (shouldFetchDraftGroup(getState(), id) === false) {
    log.trace('actionsLiveDraftGroup.fetchDraftGroupIfNeeded() - Draft group exists');
    return Promise.resolve('Draft group exists');
  }
  return Promise.all([
    dispatch(fetchDraftGroupInfo(id)),
    dispatch(fetchDraftGroupFP(id)),
    dispatch(fetchPlayerBoxScoreHistoryIfNeeded(sport)),
  ])
  .then(() =>
    dispatch(confirmDraftGroupStored(id))
  );
};

/**
 * Remove all draft groups that have ended.
 * @return {object}  Changes for reducer, wrapped in thunk
 */
export const removeUnusedDraftGroups = () => (dispatch, getState) => {
  const draftGroupIds = [];
  const currentLineups = getState().currentLineups.items || {};

  _forEach(getState().liveDraftGroups, (draftGroup) => {
    const id = draftGroup.id;
    const lineups = _filter(currentLineups, (lineup) => lineup.draft_group === id);

    // if there are no lineups the group is related to, then remove
    if (lineups.length === 0) {
      draftGroupIds.push(id);
    }
  });

  if (draftGroupIds.length === 0) return null;

  return dispatch({
    type: ActionTypes.REMOVE_LIVE_DRAFT_GROUPS,
    ids: draftGroupIds,
    removedAt: dateNow(),
  });
};

/**
 * Used to update a player's stats when a Pusher call sends us new info
 * @param  {number} playerId      Player ID
 * @param  {object} eventCall     Pusher event that came through
 * @param  {number} draftGroupId) Draft group ID to find player in redux store
 * @return {object}               Changes for reducer, wrapped in thunk
 */
export const updatePlayerStats = (message, draftGroupId) => (dispatch, getState) => {
  const playerId = message.fields.player_id;

  // if this is a relevant player, update their stats
  if (getState().livePlayers.relevantPlayers.hasOwnProperty(playerId)) {
    log.info('stats are for relevantPlayer, calling updateLivePlayersStats()', message);

    dispatch(updateLivePlayersStats(
      playerId,
      message.fields
    ));
  }

  return dispatch({
    id: draftGroupId,
    type: ActionTypes.UPDATE_LIVE_DRAFT_GROUP_PLAYER_FP,
    playerId,
    fp: message.fields.fantasy_points,
  });
};
