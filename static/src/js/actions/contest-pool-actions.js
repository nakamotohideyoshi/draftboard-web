import request from 'superagent';
import { normalize, Schema, arrayOf } from 'normalizr';
import Cookies from 'js-cookie';
import log from '../lib/logging.js';
import * as actionTypes from '../action-types';
import { addMessage } from './message-actions.js';
import { CALL_API } from '../middleware/api';
import { fetchCashBalanceIfNeeded } from './user.js';


const contestSchema = new Schema('contests', {
  idAttribute: 'id',
});


/**
 * Contests Pool Entry Actions
 */
export const fetchContestPoolEntries = () => (dispatch) => {
  const apiActionResponse = dispatch({
    [CALL_API]: {
      types: [
        actionTypes.FETCHING_CONTEST_POOL_ENTRIES,
        actionTypes.FETCH_CONTEST_POOL_ENTRIES_SUCCESS,
        actionTypes.ADD_MESSAGE,
      ],
      endpoint: '/api/contest/contest-pools/entries/',
    },
  });

  apiActionResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    if (action.error) {
      dispatch({
        type: actionTypes.FETCH_CONTEST_POOL_ENTRIES_FAIL,
        response: action.error,
      });
    }
  });

  // Return the promise chain in case we want to use it elsewhere.
  return apiActionResponse;
};


/**
 * Contests Pool Actions
 */


/**
 * Set the focused contest based on the provided contest ID.
 * @param {number} contestId the ID of the contest to set as active.
 */
export function setFocusedContest(contestId) {
  return (dispatch) => {
    dispatch({
      type: actionTypes.SET_FOCUSED_CONTEST,
      contestId,
    });
  };
}


export const fetchContestPools = () => (dispatch, getState) => {
  const apiActionResponse = dispatch({
    [CALL_API]: {
      types: [
        actionTypes.FETCH_CONTEST_POOLS,
        actionTypes.FETCH_CONTEST_POOLS_SUCCESS,
        actionTypes.ADD_MESSAGE,
      ],
      endpoint: '/api/contest/lobby/',
      callback: (json) => {
        // Normalize contest list by ID.
        const normalizedContests = normalize(
          json,
          arrayOf(contestSchema)
        );

        // Now that we have contests, check if a contest is already set to be focused (probably
        // via URL param). if set, fetch the necessary info for the contest detail pane.
        const state = getState();

        if (state.contestPools.focusedContestId && normalizedContests.entities.contests) {
          if (!normalizedContests.entities.contests.hasOwnProperty(state.contestPools.focusedContestId)) {
            log.error("404! that contest isn't in the lobby!");
          }
        }

        return normalizedContests.entities.contests;
      },
    },
  });

  apiActionResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    if (action.error) {
      dispatch({
        type: actionTypes.FETCH_CONTEST_POOLS_FAIL,
        response: action.error,
      });
    }
  });

  // Return the promise chain in case we want to use it elsewhere.
  return apiActionResponse;
};


/**
 * When one of the contest list filters gets updated, change the state keys for that filter.
 */
export function updateFilter(filterName, filterProperty, match) {
  return {
    type: actionTypes.UPCOMING_CONTESTS_FILTER_CHANGED,
    filter: {
      filterName,
      filterProperty,
      match,
    },
  };
}


export function updateOrderByFilter(property, direction = 'desc') {
  return {
    type: actionTypes.UPCOMING_CONTESTS_ORDER_CHANGED,
    orderBy: {
      property,
      direction,
    },
  };
}


/**
 * Enter a lineup into an upcoming contest.
 * @param  {int} contestPoolId The contest pool to be entered into.
 * @param  {int} lineupId  The lineup's id.
 */
export function enterContest(contestPoolId, lineupId) {
  const postData = {
    contest_pool: contestPoolId,
    lineup: lineupId,
  };

  return (dispatch) => {
    request
    .post('/api/contest/enter-lineup/')
    .set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'X-CSRFToken': Cookies.get('csrftoken'),
      Accept: 'application/json',
    })
    .send(postData)
    .end((err, res) => {
      if (err) {
        log.error('Contest entry request status error:', res);
        // Fetch the user's current contest pool entries which will force the UI to update.
        dispatch(fetchContestPoolEntries());
        // Re-Fetch the contest list that will have an updated current_entries count.
        dispatch(fetchContestPools());

        dispatch(addMessage({
          header: 'Unable to join contest.',
          level: 'warning',
          content: res.text,
        }));
      } else {
        // Because the user just entered a contest, their cash balance should be different.
        dispatch(fetchCashBalanceIfNeeded());
        // Fetch the user's current contest pool entries which will force the UI to update.
        dispatch(fetchContestPoolEntries());
        // Re-Fetch the contest list that will have an updated current_entries count.
        dispatch(fetchContestPools());
        // Display a success message to the user.
        dispatch(addMessage({
          level: 'success',
          header: 'Your lineup has been entered.',
          ttl: 2000,
        }));
      }
    });
  };
}


/**
 *
 * Fetch the usernames of users who have entered into a specific contest.
 *
 */

// Do we need to fetch the specified contest entrants?
function shouldFetchContestEntrants(state, contestId) {
  const entrants = state.contestPools.entrants;

  if (entrants.hasOwnProperty(contestId)) {
    // does the state already have entrants for this contest?
    return false;
  } else if (state.contestPools.isFetchingEntrants) {
    // are we currently fetching it?
    return false;
  }

  // Default to true.
  return true;
}


const fetchContestEntrants = (contestId) => (dispatch) => {
  const apiActionResponse = dispatch({
    [CALL_API]: {
      types: [
        actionTypes.FETCHING_CONTEST_ENTRANTS,
        actionTypes.FETCH_CONTEST_ENTRANTS_SUCCESS,
        actionTypes.ADD_MESSAGE,
      ],
      endpoint: `/api/contest/registered-users/${contestId}/`,
      callback: (json) => {
        /* eslint-disable no-param-reassign */
        json.contestId = contestId;
        /* eslint-enable no-param-reassign */
        return json;
      },
    },
  });

  apiActionResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    if (action.error) {
      dispatch({
        type: actionTypes.FETCH_CONTEST_ENTRANTS_FAIL,
        response: action.error,
      });
    }
  });

  // Return the promise chain in case we want to use it elsewhere.
  return apiActionResponse;
};


export function fetchContestEntrantsIfNeeded(contestId) {
  return (dispatch, getState) => {
    if (shouldFetchContestEntrants(getState(), contestId)) {
      return dispatch(fetchContestEntrants(contestId));
    }

    return Promise.resolve();
  };
}


export function upcomingContestUpdateReceived(contest) {
  return ({
    type: actionTypes.UPCOMING_CONTESTS_UPDATE_RECEIVED,
    contest,
  });
}


export function removeContestPoolEntry(entry) {
  return (dispatch) => {
    request
    .post(`/api/contest/unregister-entry/${entry.id}/`)
    .set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'X-CSRFToken': Cookies.get('csrftoken'),
      Accept: 'application/json',
    })
    .end((err, res) => {
      if (err) {
        dispatch(addMessage({
          header: 'Unable to remove contest entry.',
          content: res.body.error,
          level: 'warning',
        }));
        // Because the user just entered a contest, their cash balance should be different.
        dispatch(fetchCashBalanceIfNeeded());
        // Fetch the user's current contest pool entries which will force the UI to update.
        dispatch(fetchContestPoolEntries());
        // Re-Fetch the contest list that will have an updated current_entries count.
        dispatch(fetchContestPools());

        log.error(res);
      } else {
        // Because the user just entered a contest, their cash balance should be different.
        dispatch(fetchCashBalanceIfNeeded());
        // Fetch the user's current contest pool entries which will force the UI to update.
        dispatch(fetchContestPoolEntries());
        // Re-Fetch the contest list that will have an updated current_entries count.
        dispatch(fetchContestPools());
        // Display a success message to the user.
        dispatch(addMessage({
          level: 'success',
          header: 'Your lineup entry has been removed.',
          ttl: 3000,
        }));
      }
    });
  };
}
