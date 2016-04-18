import * as types from '../action-types.js';
import { addPollingRequest } from
  '../lib/polling-request-command/polling-request-receiver.js';
import log from '../lib/logging.js';
import { find as _find } from 'lodash';


/**
 * Create an entryRequest in the state.
 * @param {[type]} taskId    [description]
 * @param {[type]} contestId [description]
 * @param {[type]} lineupId  [description]
 */
export function addLineupEditRequestMonitor(taskId, lineupId) {
  return {
    type: types.ADD_LINEUP_EDIT_REQUEST_MONITOR,
    taskId,
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
export function editRequestRecieved(taskId, status) {
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
export function fetchingEditRequestStatus(taskId) {
  return {
    type: types.FETCHING_LINEUP_EDIT_REQUEST_STATUS,
    taskId,
  };
}


/**
 * Periodically check the status of a lineup edit task. Once we get a response
 * that tells us the task has been processed, stop checking and return the
 * status.
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
      log.warn('LineupEditRequest for this lineup already exists', lineupId);
      return {
        type: types.ADD_LINEUP_EDIT_REQUEST_MONITOR_EXISTS,
      };
    }

    dispatch(addLineupEditRequestMonitor(taskId, lineupId));
    addPollingRequest('LineupEditRequest', taskId);
    log.info('monitoring LineupEditRequest taskId: ', taskId);
  };
}
