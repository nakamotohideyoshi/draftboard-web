const moment = require('moment');
const request = require('superagent-promise')(require('superagent'), Promise);
import 'babel-core/polyfill';
import { map as _map } from 'lodash';

import * as ActionTypes from '../action-types';
import log from '../lib/logging';
import { fetchDraftGroupIfNeeded } from './live-draft-groups';


// dispatch to reducer methods

/**
 * Dispatch information to reducer that we are trying to get current draft groups.
 * Used to prevent repeat calls while requesting.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const requestCurrentDraftGroups = () => ({
  type: ActionTypes.REQUEST_CURRENT_DRAFT_GROUPS,
});

/**
 * Dispatch API response object of draft groups to the store
 * Also pass through an updated at so that we can expire and re-poll after a period of time.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const receiveCurrentDraftGroups = (response) => ({
  type: ActionTypes.RECEIVE_CURRENT_DRAFT_GROUPS,
  draftGroups: response,
  updatedAt: Date.now(),
});


// internal helpers


/**
 * API GET to return live and upcoming (current) draft groups.
 * @return {promise}   Promise that resolves with API response body to reducer
 */
const fetchCurrentDraftGroups = () => (dispatch) => {
  dispatch(requestCurrentDraftGroups());

  return request.get(
    '/api/draft-group/current/'
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    Accept: 'application/json',
  }).then(
    (res) => dispatch(receiveCurrentDraftGroups(res.body))
  );
};

/**
 * Method to determine whether we need to fetch current draft groups.
 * We check whether any preexisting data is there, and if it does, whether it's expired or not.
 * @param  {object} state Current Redux state to test
 * @return {boolean}      True if we should fetch draft groups, false if not
 */
const shouldFetchCurrentDraftGroups = (state) => {
  // if expired, then get
  const expiration = moment(state.currentDraftGroups.updatedAt).add(10, 'minutes');
  if (moment().isAfter(expiration)) {
    return true;
  }

  // if we have never called, then fetch
  if ('items' in state.currentDraftGroups === false) {
    return true;
  }

  // if we have fetched but have no data, then try again
  return state.currentDraftGroups.items.length === 0;
};


// exported methods


/**
 * Lots of ES6 shorthand here.
 * - Loops through our redux substore of current draft groups
 * - Maps to a list a fetchDraftGroupIfNeeded method for each of these draft groups
 * - Returns a Promise.all() of this list
 * - Returns through the wrapper that gives us the dispatch and state methods with Redux
 * - Returns through anonymous function
 * Eventually this substore will merge with live draft groups and the fetchDraftGroupIfNeeded() will exist here.
 * @return {promise}   Promise of all fetch methods for all draft groups within the substore, each wrapped with dispatch
 */
export const fetchRelatedDraftGroupsInfo = () => (dispatch, getState) => Promise.all(
  _map(getState().currentDraftGroups.items, (draftGroup) => dispatch(fetchDraftGroupIfNeeded(draftGroup.pk)))
);

/**
 * Outside facing method to go ahead and fetch draft groups after checking whether we should
 * @return {promise}   When returned, redux-thunk middleware executes dispatch and returns a promise, either from the
 *                     returned method or directly as a resolved promise
 */
export const fetchCurrentDraftGroupsIfNeeded = () => (dispatch, getState) => {
  if (shouldFetchCurrentDraftGroups(getState()) === false) {
    return Promise.resolve('Draft group exists');
  }

  log.info('actions.currentDraftGroups.fetchCurrentDraftGroupsIfNeeded() - Updating draft groups');

  return dispatch(
    fetchCurrentDraftGroups()
  ).then(() =>
    dispatch(fetchRelatedDraftGroupsInfo())
  );
};
