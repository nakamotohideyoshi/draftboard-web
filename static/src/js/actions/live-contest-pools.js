import * as ActionTypes from '../action-types';
import log from '../lib/logging';
import { CALL_API } from '../middleware/api';
import { dateNow, hasExpired } from '../lib/utils';
import { trackUnexpected } from './track-exceptions';
import { fetchPrizeIfNeeded } from './prizes';

// get custom logger for actions
const logAction = log.getLogger('action');


/**
 * API GET to return information about a contest
 * @param {number} contestId  Contest ID
 * @return {promise}          Promise that resolves with API response body to reducer
 */
const fetchContestPoolInfo = (id) => ({
  [CALL_API]: {
    types: [
      ActionTypes.REQUEST_CONTEST_POOL_INFO,
      ActionTypes.RECEIVE_CONTEST_POOL_INFO,
      ActionTypes.ADD_MESSAGE,
    ],
    expiresAt: dateNow() + 1000 * 60 * 60 * 24,  // 1 day
    endpoint: `/api/contest/info/contest_pool/${id}/`,
    requestFields: { id },
    callback: (json) => ({
      id,
      info: json,
    }),
  },
});

/**
 * Outside facing method to go ahead and fetch contest information after checking whether we should
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchRelatedContestPoolInfo = (id) => (dispatch, getState) => {
  logAction.debug('actions.fetchRelatedContestPoolInfo');

  const state = getState();

  // don't bother if there is no contest yet!
  if (!(id in state.liveContestPools)) {
    return trackUnexpected(`fetchRelatedContestPoolInfo failed, no contest ${id} in Redux`, { state });
  }

  const pool = getState().liveContestPools[id] || {};

  if (!('prize_structure' in pool)) {
    return trackUnexpected(`fetchRelatedContestPoolInfo failed, no prize structure in contest ${id}`, { state });
  }

  const prizeId = pool.prize_structure;

  return Promise.all([
    dispatch(fetchPrizeIfNeeded(prizeId)),
  ]);
  // .then(() =>
  //   dispatch(confirmRelatedContestInfo(id))
  // );
};

/**
 * Method to determine whether we need to fetch a contest.
 * @param  {object} state Current Redux state to test
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchContestPool = (liveContestPools, id) => {
  logAction.debug('actions.shouldFetchLineups');

  const pool = liveContestPools[id] || false;

  // if we have no data yet, fetch
  if (pool === false) return true;

  if (!hasExpired(pool.expiresAt)) return false;

  return true;
};

/**
 * Outside facing method to go ahead and fetch a contest after checking whether we should
 * Pulls both information and lineups, then gets related draft groups, games, prizes
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchContestPoolIfNeeded = (id) => (dispatch, getState) => {
  logAction.debug('actions.fetchContestLineupsIfNeeded');

  if (shouldFetchContestPool(getState().liveContestPools, id) === false) {
    return fetchRelatedContestPoolInfo(id);
  }

  return dispatch(fetchContestPoolInfo(id))
    .then(() =>
      dispatch(fetchRelatedContestPoolInfo(id))
    );
};
