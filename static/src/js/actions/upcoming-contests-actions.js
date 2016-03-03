import * as types from '../action-types.js';
import request from 'superagent';
import { normalize, Schema, arrayOf } from 'normalizr';
import Cookies from 'js-cookie';
import { fetchPrizeIfNeeded } from './prizes.js';
import { monitorEntryRequest } from './entry-request-actions.js';
import { addMessage } from './message-actions.js';
import log from '../lib/logging.js';


const contestSchema = new Schema('contests', {
  idAttribute: 'id',
});


function fetchUpcomingContestsSuccess(body) {
  return {
    type: types.FETCH_UPCOMING_CONTESTS_SUCCESS,
    body,
  };
}


function fetchUpcomingContestsFail(ex) {
  return {
    type: types.FETCH_UPCOMING_CONTESTS_FAIL,
    ex,
  };
}


function fetchFocusedContestInfo(dispatch, contest) {
  dispatch(fetchPrizeIfNeeded(contest.prize_structure));
  fetchPrizeIfNeeded(contest.prize_structure);
}


/**
 * Set the focused contest based on the provided contest ID.
 * @param {number} contestId the ID of the contest to set as active.
 */
export function setFocusedContest(contestId) {
  return (dispatch, getState) => {
    const state = getState();

    if (
      state.upcomingContests.hasOwnProperty('allContests') &&
      state.upcomingContests.hasOwnProperty(contestId)
    ) {
      fetchFocusedContestInfo(state.upcomingContests.allContests[contestId]);
    }

    dispatch({
      type: types.SET_FOCUSED_CONTEST,
      contestId,
    });
  };
}


export function fetchUpcomingContests() {
  return (dispatch, getState) => {
    request
    .get('/api/contest/lobby/')
    .set({ 'X-REQUESTED-WITH': 'XMLHttpRequest' })
    .set('Accept', 'application/json')
    .end((err, res) => {
      if (err) {
        return dispatch(fetchUpcomingContestsFail(err));
      }

      // Normalize contest list by ID.
      const normalizedContests = normalize(
        res.body,
        arrayOf(contestSchema)
      );

      // Now that we have contests, check if a contest is already set to be focused (probably
      // via URL param). if set, fetch the necessary info for the contest detail pane.
      const state = getState();

      if (state.upcomingContests.focusedContestId && normalizedContests.entities.contests) {
        if (normalizedContests.entities.contests.hasOwnProperty(state.upcomingContests.focusedContestId)) {
          const contest = normalizedContests.entities.contests[state.upcomingContests.focusedContestId];
          fetchFocusedContestInfo(dispatch, contest);
        } else {
          log.error("404! that contest isn't in the lobby!");
        }
      }

      return dispatch(fetchUpcomingContestsSuccess({
        contests: normalizedContests.entities.contests || {},
      }));
    });
  };
}


/**
 * When one of the contest list filters gets updated, change the state keys for that filter.
 */
export function updateFilter(filterName, filterProperty, match) {
  return {
    type: types.UPCOMING_CONTESTS_FILTER_CHANGED,
    filter: {
      filterName,
      filterProperty,
      match,
    },
  };
}


export function updateOrderByFilter(property, direction = 'desc') {
  return {
    type: types.UPCOMING_CONTESTS_ORDER_CHANGED,
    orderBy: {
      property,
      direction,
    },
  };
}


/**
 * Enter a lineup into an upcoming contest.
 * @param  {int} contestId The contest to be entered.
 * @param  {int} lineupId  The lineup's id.
 */
export function enterContest(contestId, lineupId) {
  const postData = {
    contest: contestId,
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
        addMessage({
          title: 'Unable to join contest.',
          level: 'warning',
        });
        log.error(res);
      } else {
        dispatch(monitorEntryRequest(res.body.buyin_task_id, contestId, lineupId));
      }
    });
  };
}


/**
 *
 * Fetch the usernames of users who have entered into a specific contest.
 *
 */

function fetchingContestEntrants() {
  return {
    type: types.FETCHING_CONTEST_ENTRANTS,
  };
}

function fetchContestEntrantsSuccess(body, contestId) {
  return {
    type: types.FETCH_CONTEST_ENTRANTS_SUCCESS,
    entrants: body,
    contestId,
  };
}

function fetchContestEntrantsFail(ex) {
  log.error(ex);
  return {
    type: types.FETCH_CONTEST_ENTRANTS_FAIL,
    ex,
  };
}

// Do we need to fetch the specified contest entrants?
function shouldFetchContestEntrants(state, contestId) {
  const entrants = state.upcomingContests.entrants;

  if (entrants.hasOwnProperty(contestId)) {
    // does the state already have entrants for this contest?
    return false;
  } else if (state.upcomingContests.isFetchingEntrants) {
    // are we currently fetching it?
    return false;
  }

  // Default to true.
  return true;
}

function fetchContestEntrants(contestId) {
  return dispatch => {
    // update the fetching state.
    dispatch(fetchingContestEntrants());

    return new Promise((resolve, reject) => {
      request
      .get(`/api/contest/registered-users/${contestId}/`)
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        Accept: 'application/json',
      })
      .end((err, res) => {
        if (err) {
          dispatch(fetchContestEntrantsFail(err));
          reject(err);
        } else {
          dispatch(fetchContestEntrantsSuccess(res.body, contestId));
          resolve(res);
        }
      });
    });
  };
}

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
    type: types.UPCOMING_CONTESTS_UPDATE_RECEIVED,
    contest,
  });
}
