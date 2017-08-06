import * as ActionTypes from '../action-types';
import filter from 'lodash/filter';
import forEach from 'lodash/forEach';
import log from '../lib/logging';
import { CALL_API } from '../middleware/api';
import { dateNow, hasExpired } from '../lib/utils';
import { fetchTeamsIfNeeded } from './sports';
import { normalize, Schema, arrayOf } from 'normalizr';
import { trackUnexpected } from './track-exceptions';
import { updateLivePlayersStats } from './live-players';

// get custom logger for actions
const logAction = log.getLogger('action');


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
});


// helper methods


/**
 * API GET to return draft group info
 * @param {number} id  Draft group ID
 * @return {promise}   Promise that resolves with API response body to reducer
 */
const fetchDraftGroupInfo = (id) => ({
  [CALL_API]: {
    types: [
      ActionTypes.LIVE_DRAFT_GROUP__INFO__REQUEST,
      ActionTypes.LIVE_DRAFT_GROUP__INFO__RECEIVE,
      ActionTypes.ADD_MESSAGE,
    ],
    expiresAt: dateNow() + 1000 * 60 * 60 * 12,  // 12 hours
    endpoint: `/api/draft-group/${id}/`,
    requestFields: { id },
    callback: (json) => {
      const playerSchema = new Schema('players', {
        idAttribute: 'player_id',
      });

      const normalizedPlayers = normalize(
        json.players,
        arrayOf(playerSchema)
      );

      return {
        closed: (json.closed !== null) ? new Date(json.closed).getTime() : null,
        end: new Date(json.end).getTime(),
        id,
        players: normalizedPlayers.entities.players,
        sport: json.sport,
        start: new Date(json.start).getTime(),
      };
    },
  },
});

/**
 * Method to determine whether we need to fetch boxscores for a draft group.
 * @param  {object} state Current Redux state to test
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchDraftGroupBoxscores = (state, id) => {
  logAction.debug('actions.shouldFetchDraftGroupBoxscores');

  const liveDraftGroups = state.liveDraftGroups;
  const reasons = [];

  // error if no draft group to associate players to
  if (liveDraftGroups.hasOwnProperty(id) === false) {
    throw new Error('You cannot get boxscore data for a draft group that does not exist yet');
  }

  if (!hasExpired(liveDraftGroups[id].boxscoresExpiresAt)) reasons.push('has not expired');

  if (reasons.length > 0) {
    logAction.debug('shouldFetchDraftGroupBoxscores - returned false', reasons);
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
  logAction.debug('actions.shouldFetchDraftGroupFP');

  const liveDraftGroups = state.liveDraftGroups;
  const reasons = [];

  // error if no draft group to associate players to
  if (liveDraftGroups.hasOwnProperty(id) === false) {
    return trackUnexpected('actions.shouldFetchDraftGroupFP returned false', {
      liveDraftGroups,
      id,
      reason: 'Draft group does not exist yet',
    });
  }

  if (!hasExpired(liveDraftGroups[id].fpExpiresAt)) reasons.push('has not expired');

  if (reasons.length > 0) {
    logAction.debug('shouldFetchDraftGroupFP - returned false', reasons);
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
  logAction.debug('actions.shouldFetchDraftGroup');

  const liveDraftGroups = state.liveDraftGroups;

  // fetch if draft group does not exist yet
  if (liveDraftGroups.hasOwnProperty(id) === false) return true;

  // fetch if expired
  if (hasExpired(liveDraftGroups[id].infoExpiresAt)) return true;

  return false;
};


// primary methods (mainly exported, some needed in there to have proper init of const)

/**
 * API GET to return boxscores for a draft group (used in results only)
 * @param {number} id  Draft group ID
 * @return {promise}   Promise that resolves with API response body to reducer
 */
const fetchDraftGroupBoxscores = (id) => ({
  [CALL_API]: {
    types: [
      ActionTypes.REQUEST_DRAFT_GROUP_BOXSCORES,
      ActionTypes.RECEIVE_DRAFT_GROUP_BOXSCORES,
      ActionTypes.ADD_MESSAGE,
    ],
    expiresAt: dateNow() + 1000 * 60 * 5,  // 5 minutes
    endpoint: `/api/draft-group/boxscores/${id}/`,
    requestFields: { id },
    callback: (json) => ({
      id,
      boxscores: json,
    }),
  },
});

/**
 * API GET to return fantasy points of players in a draft group
 * @param {number} id  Draft group ID
 * @return {promise}   Promise that resolves with API response body to reducer
 */
const fetchDraftGroupFP = (id) => ({
  [CALL_API]: {
    types: [
      ActionTypes.REQUEST_LIVE_DRAFT_GROUP_FP,
      ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_FP,
      ActionTypes.ADD_MESSAGE,
    ],
    expiresAt: dateNow() + 1000 * 60 * 1,  // 1 minute cache exire time.
    endpoint: `/api/draft-group/fantasy-points/${id}/`,
    requestFields: { id },
    callback: (json) => ({
      id,
      players: json.players || {},
    }),
  },
});

/**
 * Get fantasy points for players in a draft group if need be
 * @param {number} id  Draft group ID
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchDraftGroupBoxscoresIfNeeded = (id) => (dispatch, getState) => {
  logAction.debug('actions.fetchDraftGroupBoxscoresIfNeeded');

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
  logAction.debug('actions.fetchDraftGroupFPIfNeeded', id);

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
  logAction.debug('actions.fetchDraftGroupIfNeeded');

  if (shouldFetchDraftGroup(getState(), id) === false) return Promise.resolve('Draft group exists');

  return Promise.all([
    dispatch(fetchDraftGroupInfo(id)),
    dispatch(fetchTeamsIfNeeded(sport)),
  ])
  .then(() =>
    dispatch(fetchDraftGroupFPIfNeeded(id))
  )
  .then(() =>
    dispatch(confirmDraftGroupStored(id))
  );
};

/**
 * Remove all draft groups that have ended.
 * @return {object}  Changes for reducer, wrapped in thunk
 */
export const removeUnusedDraftGroups = () => (dispatch, getState) => {
  logAction.debug('actions.removeUnusedDraftGroups');

  const draftGroupIds = [];
  const currentLineups = getState().currentLineups.items || {};

  forEach(getState().liveDraftGroups, (draftGroup) => {
    const id = draftGroup.id;
    const lineups = filter(currentLineups, (lineup) => lineup.draftGroup === id);

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
export const updatePlayerStats = (sport, message) => (dispatch, getState) => {
  logAction.debug('actions.updatePlayerStats', sport, message);

  const state = getState();
  const playerId = message.player_id;
  const playerSrid = message.srid_player;

  let draftGroupId = null;

  // this means we're in the results section
  // loop through each draft group
  Object.keys(state.liveDraftGroups).map((currentDraftGroupId) => {
    const liveDraftGroup = state.liveDraftGroups[currentDraftGroupId];
    if (
      liveDraftGroup.sport === sport &&
      message.player_id in liveDraftGroup.playersStats) {
      draftGroupId = currentDraftGroupId;
    }
  });

  if (draftGroupId === null) {
    // no player to update
    log.info('actions.updatePlayerStats - player not in any draft group', message);

    return false;
  }

  // if this is a relevant player, update their stats
  if (getState().livePlayers.relevantPlayers.hasOwnProperty(playerSrid)) {
    log.info('stats are for relevantPlayer, calling updateLivePlayersStats()', message);

    dispatch(updateLivePlayersStats(
      playerSrid,
      message
    ));
  }

  return dispatch({
    id: draftGroupId,
    type: ActionTypes.UPDATE_LIVE_DRAFT_GROUP_PLAYER_FP,
    playerId,
    fp: message.fantasy_points,
  });
};
