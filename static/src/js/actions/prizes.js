const request = require('superagent-promise')(require('superagent'), Promise);
import * as ActionTypes from '../action-types';
import { dateNow } from '../lib/utils';


/**
 * Dispatch prize info to redux reducer
 * @param  {number} id       Prize ID
 * @param  {object} response Prize information
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const receivePrize = (id, response) => ({
  type: ActionTypes.RECEIVE_PRIZE,
  id,
  info: response,
  expiresAt: dateNow() + 1000 * 60 * 60 * 24,  // subtract 1 day
});

/**
 * API GET to return information about a prize
 * @param {number} id  Prize ID
 * @return {promise}   Promise that resolves with API response body to reducer
 */
const fetchPrize = (id) => (dispatch) =>
  request.get(
    `/api/prize/${id}/`
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    Accept: 'application/json',
  }).then(
    (res) => dispatch(receivePrize(id, res.body))
  );

/**
 * Method to determine whether we need to fetch a prize, as they're cached indefinitely.
 * @param  {object} state Current Redux state to test
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchPrize = (state, id) => state.prizes.hasOwnProperty(id) === false;

/**
 * Fetch a prize if we need to
 * @param  {number} id Prize ID
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchPrizeIfNeeded = (id) => (dispatch, getState) => {
  if (shouldFetchPrize(getState(), id)) {
    return dispatch(fetchPrize(id));
  }

  return Promise.resolve('Prize already exists');
};
