import request from 'superagent';
import Cookies from 'js-cookie';
import log from '../logging.js';
import store from '../../store.js';
import { addMessage } from '../../actions/message-actions.js';
import * as lineupEditRequestActions from '../../actions/lineup-edit-request-actions.js';


/**
 * This is a Command that gets used by the PollingRequestReceiver. It never
 * gets used directly, it is simply a few methods that let the
 * PollingRequestReceiver know how to work with a lineup edit request.
 */


/**
 * Get the task out of our store.
 * @param  {int} taskId The task id.
 * @return {object} The task state.
 */
export function getTaskState(taskId) {
  return store.getState().lineupEditRequests[taskId];
}


/**
 * Determine whether the lineup edit request status should be fetched from the server
 * based off of it's current status.
 * @param  {int} entryRequestId The id of the task. - Found in store.entryRequests.
 * @return {bool}               Should we fetch the status?
 */
export function shouldFetch(editLineupRequestId) {
  /**
   * FETCHING: We have an outstanding XHR to fetch the status, don't send another.
   * PENDING: The API says the task is still pending and we should fetch again.
   * SUCCESS: Entry attempt was successfull. We should not fetch again, so
   * 					cancel the entry monitor.
   * FAILURE: Entry attempt has failed. Cancel the failed edit monitor.
   * unkown/undefined: We don't have a way to deal with the status returned.
   *
   * @type {String}
   */

  const saveRequest = getTaskState(editLineupRequestId);

  // If the saveRequest has been removed from the state, don't fetch.
  if (!saveRequest) {
    return false;
  }

  // If we've reached our maximum number of retries, don't reattempt.
  if (saveRequest.attempt > saveRequest.maxAttempts) {
    store.dispatch(addMessage({
      level: 'warning',
      header: 'Lineup Save failed.',
      content: 'Polling attempt timed out.',
    }));

    store.dispatch(
      lineupEditRequestActions.editRequestRecieved(editLineupRequestId, 'POLLING_TIMEOUT')
    );
    return false;
  }

  switch (saveRequest.status) {
    case 'FETCHING':
      return false;

    case 'FAILURE':
      return false;

    case 'SUCCESS':
      return false;

    case 'PENDING':
      return true;

    default:
      // We don't have a way to deal with the status returned.
      log.error('Encountered unexpected editRequest.status', saveRequest.status);
      return false;
  }
}


/**
 * Check the status of a lineup edit request.
 * This is used to ping the server after a lineup edit request has been made in order to see
 * if it has been sucesfully processed by the task queue.
 * @param  {[type]} taskId the ID returned by the editLineup action.
 */
export function fetch(taskId) {
  // Set the state to show that we are currently fetching the entryRequestStatus.
  store.dispatch(lineupEditRequestActions.fetchingEditRequestStatus(taskId));

  return new Promise((resolve, reject) => {
    request
    .get(`/api/lineup/edit-status/${taskId}/`)
    .set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      'X-CSRFToken': Cookies.get('csrftoken'),
      Accept: 'application/json',
    })
    .end((err, res) => {
      /**
       * Don't get confused - unless the server actually has an internal error, this will not
       * be reported as 'err'. So expect a 'FAILURE' on the entry status to be a 200 response.
       */
      if (err) {
        log.error('Lineup edit request status error:', res.body);
        const content = 'Lineup edit failed.';

        store.dispatch(addMessage({
          level: 'warning',
          content,
        }));

        reject(content);
        // Remove the request from the store.
        return store.dispatch(lineupEditRequestActions.editRequestRecieved(taskId, 'FAILURE'));
      }

      // If it was a success.
      if (res.body.status === 'SUCCESS') {
        // Redirect to lobby with url param.
        document.location.href = '/lobby/?lineup-saved=true';
      }
      // If it was a failure.
      if (res.body.status === 'FAILURE') {
        log.error('Lineup edit request status error:', res.body);
        let content = '';
        // Add the response msg to the message we display to the user.
        if (res.body.exception) {
          content = res.body.exception.msg;
        }

        store.dispatch(addMessage({
          level: 'warning',
          header: 'Lineup edit failed.',
          content,
        }));

        reject(content);
        // Remove the request from the store.
        return store.dispatch(
          lineupEditRequestActions.editRequestRecieved(taskId, res.body.status)
        );
      }

      resolve(res.body.status);
      return store.dispatch(lineupEditRequestActions.editRequestRecieved(taskId, res.body.status));
    });
  });
}
