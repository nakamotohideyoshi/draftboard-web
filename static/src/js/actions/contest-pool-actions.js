import Raven from 'raven-js';
import { normalize, Schema, arrayOf } from 'normalizr';
import Cookies from 'js-cookie';
import log from '../lib/logging.js';
import * as actionTypes from '../action-types';
import { addMessage } from './message-actions.js';
import { CALL_API } from '../middleware/api';
import { fetchCashBalanceIfNeeded } from './user.js';
import fetch from 'isomorphic-fetch';
// custom API domain for local dev testing
let { API_DOMAIN = '' } = process.env;
// For some dumb reason fetch isn't adding the domain for POST requests, when testing we need
// a full domain in order for nock to work.
if (process.env.NODE_ENV === 'test') { API_DOMAIN = 'http://localhost:80'; }

const contestSchema = new Schema('contests', {
  idAttribute: 'id',
});

const entrySchema = new Schema('entries', {
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
      callback: (json) => {
        // Normalize contest list by ID.
        const normalizedEntries = normalize(
          json,
          arrayOf(entrySchema)
        );

        return normalizedEntries.entities.entries;
      },
    },
  });

  return apiActionResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    if (action.error) {
      return dispatch({
        type: actionTypes.FETCH_CONTEST_POOL_ENTRIES_FAIL,
        response: action.error,
      });
    }

    return action;
  });
};

/**
 *
 * Fetch the usernames of users who have entered into a specific contest.
 *
 * NOTE: disabled due to contest pool entrants not making much sense, but only commented out
 * because legal issues may necessitate this feature.
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
      callback: (json) => ({
        entrants: json,
        contestId,
      }),
    },
  });

  apiActionResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    let result;
    if (action.error) {
      result = dispatch({
        type: actionTypes.FETCH_CONTEST_ENTRANTS_FAIL,
        response: action.error,
      });
    }
    // to reassure eslint
    return result;
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

  return apiActionResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    if (action.error) {
      return dispatch({
        type: actionTypes.FETCH_CONTEST_POOLS_FAIL,
        response: action.error,
      });
    }

    return action;
  });
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
    // Tell the state that we are entering a contest.
    dispatch({
      type: actionTypes.ENTERING_CONTEST_POOL,
      contestPoolId,
      lineupId,
    });


    // Make an API request.
    return fetch(`${API_DOMAIN}/api/contest/enter-lineup/`, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        'X-CSRFToken': Cookies.get('csrftoken'),
        username: Cookies.get('username'),
      },
      body: JSON.stringify(postData),
    }).then((response) => {
      // First, reject a response that isn't in the 200 range.
      if (!response.ok) {
        return response.json().then((json) => {
          // Redirect in case of an invalid location check.
          if (json.detail === 'IP_CHECK_FAILED') {
            window.location.href = '/restricted-location/';
            return false;
          }

          // Log the request error to Sentry with some info.
          Raven.captureMessage(
            'API request failed: /api/contest/enter-lineup/',
            { extra: {
              status: response.status,
              statusText: response.statusText,
              url: response.url,
            },
          });

          // Fetch the user's current contest pool entries which will force the UI to update.
          dispatch(fetchContestPoolEntries());
          // Re-Fetch the contest list that will have an updated current_entries count.
          dispatch(fetchContestPools());

          // Tell the state the entry attempt failed.
          dispatch({
            type: actionTypes.ENTERING_CONTEST_POOL_FAIL,
            contestPoolId,
            lineupId,
          });

          // Show the user a message
          dispatch(addMessage({
            header: 'Unable to join contest.',
            level: 'warning',
            content: json.detail,
          }));

          // Kill the promise chain.
          return Promise.reject({ contestPoolId, lineupId, response: json });
        });
      }

      // If the request was a success, parse the (hopefully) json from the response body.
      return response.json().then(json => ({ json, response }));
    }).then((json) => {
      // Because the user just entered a contest, their cash balance should be different.
      dispatch(fetchCashBalanceIfNeeded());
      // Re-Fetch the contest list that will have an updated current_entries count.
      dispatch(fetchContestPools());
      // Re-Fetch the contest entrants
      dispatch(fetchContestEntrants(contestPoolId));
      // Fetch the user's current contest pool entries which will force the UI to update.
      //
      // Before we show + tell the user that their entry was a success, grab all of their entries
      // from the API.
      //
      // We do this because our options are to:
      // A: Stuff the entry that was just created into our current state.
      // B: Grab ALL entries from the server to make sure we are in sync.
      //
      // B is the chosen path.
      return dispatch(fetchContestPoolEntries()).then(() => {
        // Tell the state the entry attempt succeeded.
        dispatch({
          type: actionTypes.ENTERING_CONTEST_POOL_SUCCESS,
          contestPoolId,
          lineupId,
        });

        // Display a success message to the user.
        dispatch(addMessage({
          level: 'success',
          header: 'Your lineup has been entered.',
          ttl: 2000,
        }));

        return Promise.resolve(json);
      });
    }).catch((ex) => {
      log.error(ex);
    });
  };
}


/**
 *
 * Fetch the usernames of users who have entered into a specific contest.
 *
 * NOTE: disabled due to contest pool entrants not making much sense, but only commented out
 * because legal issues may necessitate this feature.
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
      callback: (json) => ({
        entrants: json,
        contestId,
      }),
    },
  });

  apiActionResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    let result;
    if (action.error) {
      result = dispatch({
        type: actionTypes.FETCH_CONTEST_ENTRANTS_FAIL,
        response: action.error,
      });
    }
    // to reassure eslint
    return result;
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
    // Tell the app we are attempting to unregister this entry.
    dispatch({
      type: actionTypes.REMOVING_CONTEST_POOL_ENTRY,
      entry,
    });

    // Make an API request.
    return fetch(`${API_DOMAIN}/api/contest/unregister-entry/${entry.id}/`, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        'X-CSRFToken': Cookies.get('csrftoken'),
        username: Cookies.get('username'),
      },
    }).then((response) => {
      // First, reject a response that isn't in the 200 range.
      if (!response.ok) {
        // Extract the text and dispatch some actions.
        return response.json().then(
          json => {
            dispatch(addMessage({
              header: 'Unable to remove contest entry.',
              level: 'warning',
              content: json.detail,
            }));

            // tell the state it failed.
            dispatch({
              type: actionTypes.REMOVING_CONTEST_POOL_ENTRY_FAIL,
              entry,
            });

            // Because the user just entered a contest, their cash balance should be different.
            dispatch(fetchCashBalanceIfNeeded());
            // Fetch the user's current contest pool entries which will force the UI to update.
            dispatch(fetchContestPoolEntries());
            // Re-Fetch the contest list that will have an updated current_entries count.
            dispatch(fetchContestPools());

            // Kill the promise chain.
            return Promise.reject({ entry, response: json });
          }
        );
      }

      dispatch({
        type: actionTypes.REMOVING_CONTEST_POOL_ENTRY_SUCCESS,
        entry,
      });

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

      // If the request was a success, parse the (hopefully) json from the response body.
      return response.json().then(json => ({ json, response }));
    }).then((json) => {
      // Re-Fetch the contest entrants
      dispatch(fetchContestEntrants(entry.contest_pool));
      log.debug(json);
      return json;
    }).catch((ex) => {
      // Log the request error to Sentry with some info.
      Raven.captureMessage(
        'API request failed: /api/contest/unregister-entry/{entry.id}',
        { extra: {
          ex,
          entry: entry.id,
        },
      });
    });
  };
}
