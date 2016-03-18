const request = require('superagent-promise')(require('superagent'), Promise);
import { filter as _filter } from 'lodash';
import { forEach as _forEach } from 'lodash';
import { merge as _merge } from 'lodash';
import { reduce as _reduce } from 'lodash';
import ActionTypes from '../action-types';
import log from '../lib/logging';
import moment from 'moment';


/**
 * Dispatch API response object of results for a day, including players, lineups, and entries into contests
 * NOTE: this method must be wrapped with dispatch()
 * @param  {string} when          Date of the results, in format YYYY-M-D
 * @param  {object} response      Response of players
 * @return {object}               Changes for reducer
 */
const receiveResults = (when, response) => {
  const filteredResponse = _merge({}, response);

  // TODO receiveResults() - remove this when coderden fixes API call to not return bad entries
  _forEach(filteredResponse.lineups, (lineup, index) => {
    const entries = _filter(lineup.entries, (entry) => entry.final_rank !== -1);

    filteredResponse.lineups[index].entries = entries;
    filteredResponse.lineups[index].stats = {
      buyin: 100,
      entries: entries.length,
      won: _reduce(entries, (sum, entry) => sum + entry.payout.amount, 0),
    };
  });

  return {
    response: filteredResponse,
    when,
    type: ActionTypes.RECEIVE_RESULTS,
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

const fetchResults = (whenStr) => (dispatch) => {
  log.info('actions.fetchResults()', whenStr);
  const when = moment(whenStr, 'YYYY-MM-DD');

  return request.get(
    `/api/contest/play-history/${when.format('YYYY/MM/DD')}/`
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    Accept: 'application/json',
  }).then(
    (res) => dispatch(receiveResults(whenStr, res.body))
  );

  // dispatch(receiveResults(id, {
  //   stats: {
  //     winnings: '0$',
  //     possible: '$542,50',
  //     fees: '$220',
  //     entries: 24,
  //     contests: 18,
  //   },
  //   lineups: [
  //     {
  //       id: 1,
  //       name: 'Warrior\'s Stack',
  //       players: [
  //         {
  //           id: 1,
  //           name: 'name.1',
  //           score: 70,
  //           image: '../img/blocks/results/avatar.png',
  //           position: 'pg',
  //         },
  //         {
  //           id: 2,
  //           name: 'name.1',
  //           score: 70,
  //           image: '../img/blocks/results/avatar.png',
  //           position: 'pg',
  //         },
  //       ],
  //       contests: [
  //         {
  //           id: 1,
  //           factor: 2,
  //           title: '$25 - Anonymous Head-to-Head',
  //           place: 16,
  //           prize: '$20',
  //         },
  //         {
  //           id: 2,
  //           factor: 1,
  //           title: '$10,000 - Guaranteed Tier Anonymous Head-to-Head',
  //           place: 1,
  //           prize: '$500',
  //         },
  //       ],
  //       stats: {
  //         fees: '$120',
  //         won: '$1,850.50',
  //         entries: 22,
  //       },
  //     },
  //   ],
  // }));
};

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
