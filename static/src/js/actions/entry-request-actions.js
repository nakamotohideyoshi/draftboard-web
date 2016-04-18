// import Raven from 'raven-js';
import * as types from '../action-types.js';
import { addPollingRequest } from '../lib/polling-request-command/polling-request-receiver.js';
import log from '../lib/logging.js';
import { find as _find } from 'lodash';


/**
 * Create an entryRequest in the state.
 * @param {[type]} taskId    [description]
 * @param {[type]} contestPoolId [description]
 * @param {[type]} lineupId  [description]
 */
export function addEntryRequestMonitor(taskId, contestPoolId, lineupId) {
  return {
    type: types.ADD_ENTRY_REQUEST_MONITOR,
    taskId,
    contestPoolId,
    lineupId,
    maxAttempts: 10,
    attempt: 0,
  };
}


/**
 * The XHR has been recieved, update the store with it's response.
 * @param  {[type]} taskId [description]
 * @param  {[type]} status [description]
 * @return {[type]}        [description]
 */
export function entryRequestRecieved(taskId, status) {
  return {
    type: types.ENTRY_REQUEST_RECIEVED,
    taskId,
    status,
  };
}


/**
 * We are making an XHR to retrieve the status of the entry request
 * @param  {[type]} taskId [description]
 * @return {[type]}        [description]
 */
export function fetchingEntryRequestStatus(taskId) {
  return {
    type: types.FETCHING_ENTRY_REQUEST_STATUS,
    taskId,
  };
}


/**
 * Periodically check the status of a contest entry task. Once we get a response that tells us the
 * task has been processed, stop checking and return the status.
 * @param  {[type]} taskId [description]
 * @return {[type]}        [description]
 */
export function monitorEntryRequest(taskId, contestPoolId, lineupId) {
  return (dispatch, getState) => {
    const state = getState();

    const existingRequest = _find(state.entryRequests, {
      lineupId,
      contestPoolId,
    });

    if (existingRequest) {
      log.warn('entryRequests for this lineup & contest pool already exists', contestPoolId, lineupId);
      return {
        type: types.ADD_ENTRY_REQUEST_MONITOR_EXISTS,
      };
    }

    dispatch(addEntryRequestMonitor(taskId, contestPoolId, lineupId));
    addPollingRequest('entryRequest', taskId);
    log.info('monitoring entry taskId: ', taskId);
  };
}
