import ActionTypes from '../action-types';
import filter from 'lodash/filter';
import forEach from 'lodash/forEach';
import merge from 'lodash/merge';
import moment from 'moment';
import reduce from 'lodash/reduce';
import { CALL_API } from '../middleware/api';
import { dateNow } from '../lib/utils';


/**
 * Dispatch API response object of results for a day, including players, lineups, and entries into contests
 * NOTE: this method must be wrapped with dispatch()
 * @param  {string} when          Date of the results, in format YYYY-M-D
 * @param  {object} response      Response of players
 * @return {object}               Changes for reducer
 */
const receiveResults = (when, response) => {
  const filteredResponse = merge({}, response);

  filteredResponse.overall.winnings = +(filteredResponse.overall.winnings);
  filteredResponse.overall.possible = +(filteredResponse.overall.possible);
  filteredResponse.overall.buyins = +(filteredResponse.overall.buyins);

  // TODO receiveResults() - remove this when coderden fixes API call to not return bad entries
  forEach(filteredResponse.lineups, (lineup, index) => {
    const entries = filter(lineup.entries, (entry) => entry.final_rank !== -1);

    filteredResponse.lineups[index].entries = entries;
    filteredResponse.lineups[index].stats = {
      buyin: 100,
      entries: entries.length,
      won: reduce(entries, (sum, entry) => {
        if (!entry.payout) return sum;
        const amount = entry.payout.amount || 0;
        return sum + amount;
      }, 0),
    };
  });

  return {
    response: filteredResponse,
    when,
  };
};

/**
 * Method to determine whether we need to fetch draft group.
 * Fetch if it currently does not exist at all yet.
 * @param  {object} state Current Redux state to test
 * @param {timestampe} when What day should we compare with redux state?
 * @return {boolean}      True if we should fetch, false if not
 */
const shouldFetchResults = (state, when) => state.results.hasOwnProperty(when) === false;

const fetchResults = (whenStr) => ({
  [CALL_API]: {
    types: [
      ActionTypes.REQUEST_RESULTS,
      ActionTypes.RECEIVE_RESULTS,
      ActionTypes.ADD_MESSAGE,
    ],
    expiresAt: dateNow() + 1000 * 60 * 60 * 24 * 30,  // 1 month
    endpoint: `/api/contest/play-history/${moment(whenStr, 'YYYY-MM-DD').format('YYYY/MM/DD')}/`,
    requestFields: { whenStr },
    callback: (json) => receiveResults(whenStr, json),
  },
});

/**
 * Retrive a day worth of results if needed
 * @param  {string}  when  Date of the results, in format YYYY-MM-DD
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchResultsIfNeeded = (when) => (dispatch, getState) => {
  if (shouldFetchResults(getState(), when) === true) {
    return dispatch(fetchResults(when));
  }

  return Promise.resolve('Day of results already exists');
};


/**
 * Fetch the detailed results for a single entry. This will get us everything we
 * need to render the results detail pane.
 * @param  {[type]} whenStr [description]
 * @return {[type]}         [description]
 */
export const fetchEntryResults = (entryId) => (dispatch) => {
  dispatch({
    type: ActionTypes.ENTRY_RESULTS__REQUEST,
    entryId,
  });

  const apiResponse = dispatch({
    [CALL_API]: {
      types: [
        ActionTypes.NULL,
        ActionTypes.ENTRY_RESULTS__SUCCESS,
        ActionTypes.ADD_MESSAGE,
      ],
      endpoint: `/api/contest/entries/${entryId}/results/`,
    },
  });

  return apiResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    if (action.error) {
      return dispatch({
        type: ActionTypes.ENTRY_RESULTS__FAIL,
        response: action.error,
      });
    }

    return action;
  });
};
