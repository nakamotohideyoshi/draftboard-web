import * as ActionTypes from '../action-types';
import { dateNow, hasExpired } from '../lib/utils';
import { CALL_API } from '../middleware/api';


/**
 * API GET to return information about a prize
 * @param {number} id  Prize ID
 * @return {promise}   Promise that resolves with API response body to reducer
 */
const fetchPrize = (id) => ({
  [CALL_API]: {
    types: [
      ActionTypes.REQUEST_PRIZE,
      ActionTypes.RECEIVE_PRIZE,
      ActionTypes.ADD_MESSAGE,
    ],
    expiresAt: dateNow() + 1000 * 60 * 60 * 24 * 30,  // 1 month, aka indefinitely, as they'll be logged out before
    endpoint: `/api/prize/${id}/`,
    requestFields: { id },
    callback: (json) => ({
      id,
      info: json,
    }),
  },
});

/**
 * Method to determine whether we need to fetch a prize, as they're cached indefinitely.
 * @param  {object} state Current Redux state to test
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchPrize = (state, id) => {
  if (!(id in state.prizes)) return true;
  if (hasExpired(state.prizes[id].expiresAt)) return true;

  return false;
};

/**
 * Fetch a prize if we need to
 * @param  {number} id Prize ID
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchPrizeIfNeeded = (id) => (dispatch, getState) => {
  if (shouldFetchPrize(getState(), id)) return dispatch(fetchPrize(id));

  return Promise.resolve('Prize already exists');
};
