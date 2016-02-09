// import Raven from 'raven-js';
import * as types from '../action-types.js';
import 'babel-core/polyfill';
// so we can use superagent with Promises
import request from 'superagent';
import Cookies from 'js-cookie';
import log from '../lib/logging.js';
import { addMessage } from './message-actions.js';
import { find as _find } from 'lodash';
import store from '../store.js';


// A place to store setInterval IDs. This should probably be put in the store instead.
const editMonitors = [];
// When polling, how many milleseconds should we continue to poll for before giving up?
const maxRetrytime = 10000; // 10 seconds
// How often should we attemt to re-poll?
const minimumPollInterval = 250;


/**
 * Create an entryRequest in the state.
 * @param {[type]} taskId    [description]
 * @param {[type]} contestId [description]
 * @param {[type]} lineupId  [description]
 */
function addEditRequestMonitor(taskId, lineupId) {
  return {
    type: types.ADD_LINEUP_EDIT_REQUEST_MONITOR,
    taskId,
    lineupId,
    maxAttempts: maxRetrytime / minimumPollInterval,
    attempt: 0,
  };
}


/**
 * The XHR has been recieved, update the store with it's response.
 * @param  {[type]} taskId [description]
 * @param  {[type]} status [description]
 * @return {[type]}        [description]
 */
function editRequestRecieved(taskId, status) {
  return {
    type: types.LINEUP_EDIT_REQUEST_RECIEVED,
    taskId,
    status,
  };
}


/**
 * We are making an XHR to retrieve the status of the entry request
 * @param  {[type]} taskId [description]
 * @return {[type]}        [description]
 */
function fetchingEditRequestStatus(taskId) {
  return {
    type: types.FETCHING_LINEUP_EDIT_REQUEST_STATUS,
    taskId,
  };
}


/**
 * Clear the loop that repeatedly attempts to check the status of an entry.
 * @param  {[type]} taskId [description]
 * @return {[type]}        [description]
 */
function clearMonitor(taskId) {
  log.debug(`Clearing monitor for task ${taskId}`);
  window.clearInterval(editMonitors[taskId].loop);
  // remove the task
  store.dispatch({
    type: types.DELETE_LINEUP_EDIT_REQUEST,
    taskId,
  });
}


/**
 * Determine whether we actually need to fetch the status.
 * If we already have a pending XHR, we don't want to send another. If the entry request has failed,
 * cancel the monitor for it.
 *
 * @param  {string} taskId [description]
 * @param  {object} state  [description]
 * @return {bool}        [description]
 */
function shouldFetchEditRequestStatus(taskId, state) {
  // Is this entryRequest have a key in the state?
  if (state.lineupEditRequests.hasOwnProperty(taskId)) {
    switch (state.lineupEditRequests[taskId].status) {
      case 'FETCHING':
        // We have a pending XHR to fetch the status, don't send another.
        return false;

      case 'FAILURE':
        // Entry attempt has failed. Cancel the failed entry monitor.
        clearMonitor(taskId);
        return false;

      case 'SUCCESS':
        // Entry attempt was successfull. We should not fetch again, so cancel the entry monitor.
        clearMonitor(taskId);
        return false;

      case 'PENDING':
        // The API says the task is still pending and we should fetch again.
        return true;

      default:
        // We don't have a way to deal with the status returned.
        log.error('Encountered unexpected editRequest.status', state.lineupEditRequests[taskId].status);
        return false;
    }
  } else {
    // No entry request exists, do nothing.
    log.error(`EditRequest ${taskId} does not exist. Clearing Monitor'`);
    clearMonitor(taskId);
    return false;
  }
}


/**
 * Check the status of a contest entry request.
 * This is used to ping the server after a contest entry request has been made in order to see
 * if it has been sucesfully processed by the task queue.
 * @param  {[type]} taskId the ID returned by the enterContest action.
 */
function fetchEditRequestStatus(taskId) {
  return (dispatch) => {
    // Set the state to show that we are currently fetching the entryRequestStatus.
    dispatch(fetchingEditRequestStatus(taskId));

    return request
    .get(`/api/lineup/edit-status/${taskId}/`)
    .set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'X-CSRFToken': Cookies.get('csrftoken'),
      Accept: 'application/json',
    })
    .end((err, res) => {
      /**
       * Don't get confused - unless the server actually has an internal error, this will not
       * be reported as 'err'. So expect a 'FAILURE' on the entery status to be a 200 response.
       */
      if (err) {
        log.error('Lineup edit request status error:', res.body);
        const content = 'Lineup edit failed.';

        dispatch(addMessage({
          level: 'warning',
          content,
        }));

        return dispatch(editRequestRecieved(taskId, res.body.status));
      }

      log.info('Lineup edit request status:', res.body);
      // If it was a success.
      if (res.body.status === 'SUCCESS') {
        // Upon save success, send user to the lobby.
        document.location.href = '/lobby/?lineup-saved=true';

        // Fetch new entries.
        // dispatch(fetchEntriesIfNeeded());
        // Display a success message to the user.
        // dispatch(addMessage({
        //   level: 'success',
        //   header: 'Your lineup has been saved.',
        //   ttl: 2000,
        // }));
      }
      // If it was a failure.
      if (res.body.status === 'FAILURE') {
        log.error('Lineup edit request status error:', res.body);
        let content = '';
        // Add the response msg to the message we display to the user.
        if (res.body.exception) {
          content = res.body.exception.msg;
        }

        dispatch(addMessage({
          level: 'warning',
          header: 'Lineup edit failed.',
          content,
        }));
      }

      return dispatch(editRequestRecieved(taskId, res.body.status));
    });
  };
}


/**
 * This gets repeatedly called to handle whether we make an XHR to fetch the status?
 * @param  {[type]} taskId [description]
 * @return {[type]}        [description]
 */
function fetchIfNeeded(taskId) {
  return (dispatch, getState) => {
    log.trace('shouldFetchLoop', taskId);
    const shouldFetch = shouldFetchEditRequestStatus(taskId, getState());
    const state = getState();

    if (!state.lineupEditRequests.hasOwnProperty(taskId)) {
      log.warn('ignoring fetchIfNeeded request, task no longer exists.', taskId);
      return dispatch({
        type: types.IGNORING_FETCH_LINEUP_EDIT_REQUEST,
      });
    }

    // If we have attempted to poll for long enough, don't poll again.
    if (state.lineupEditRequests[taskId].attempt > state.lineupEditRequests[taskId].maxAttempts) {
      // We don't have a way to deal with the status returned.
      log.error('lineupEdit polling has timed out.', state.lineupEditRequests[taskId]);
      clearMonitor(taskId);
      dispatch(addMessage({
        level: 'warning',
        header: 'Lineup edit failed.',
        content: 'Polling attempt timed out.',
      }));
      return dispatch(editRequestRecieved(taskId, 'POLLING_TIMEOUT'));
    }

    //  We should fetch the status, dispatch that event.
    if (shouldFetch === true) {
      return dispatch(fetchEditRequestStatus(taskId));
    }
    // There is an outstanding XHR, or the previous request failed, so don't attempt to fetch.
    // If the entry failed, the monitor has been cleared and another attempt will not be made.
    dispatch({
      type: types.IGNORING_FETCH_LINEUP_EDIT_REQUEST,
    });
  };
}


/**
 * Periodically check the status of a contest entry task. Once we get a response that tells us the
 * task has been processed, stop checking and return the status.
 * @param  {[type]} taskId [description]
 * @return {[type]}        [description]
 */
export function monitorLineupEditRequest(taskId, lineupId) {
  return (dispatch, getState) => {
    const state = getState();

    const existingRequest = _find(state.lineupEditRequests, {
      lineupId,
    });

    if (existingRequest) {
      log.warn('editRequests for this lineup & contest already exists', lineupId);
      return {
        type: types.ADD_LINEUP_EDIT_REQUEST_MONITOR_EXISTS,
      };
    }

    dispatch(addEditRequestMonitor(taskId, lineupId));

    // Create a monitor to repeatedly poll the entry status api.
    editMonitors[taskId] = {
      lineupId,
    };

    // immediately try to fetch.
    dispatch(fetchIfNeeded(taskId));
    // Create a monitor loop that will contantly attempt to re-fetch the status of the entry.
    editMonitors[taskId].loop = window.setInterval(
      () => dispatch(fetchIfNeeded(taskId)),
       minimumPollInterval
    );
    log.info('monitoring lineup edit request: ', editMonitors[taskId]);
  };
}
