import request from 'superagent';
import Cookies from 'js-cookie';
import log from '../logging.js';
import store from '../../store.js';
import { addMessage } from '../../actions/message-actions.js';
import * as entryRequestActions from '../../actions/entry-request-actions.js';
import { fetchContestPoolEntries } from '../../actions/contest-pool-actions.js';
import { fetchCashBalanceIfNeeded } from '../../actions/user.js';
import { fetchUpcomingContests } from '../../actions/contest-pool-actions.js';


/**
 * This is a Command that gets used by the PollingRequestReceiver. It never
 * gets used directly, it is simply a few methods that let the
 * PollingRequestReceiver know how to work with a contest pool entry request.
 */


/**
 * Get the task out of our store.
 * @param  {int} taskId The task id.
 * @return {object} The task state.
 */
export function getTaskState(taskId) {
  return store.getState().pollingTasks[taskId];
}


/**
 * Determine whether the entry request status should be fetched from the server
 * based off of it's current status.
 * @param  {int} entryRequestId The id of the task. - Found in store.entryRequests.
 * @return {bool}               Should we fetch the status?
 */
export function shouldFetch(entryRequestId) {
  /**
   * FETCHING: We have an outstanding XHR to fetch the status, don't send another.
   * PENDING: The API says the task is still pending and we should fetch again.
   * SUCCESS: Entry attempt was successfull. We should not fetch again, so
   * 					cancel the entry monitor.
   * FAILURE: Entry attempt has failed. Cancel the failed entry monitor.
   * unkown/undefined: We don't have a way to deal with the status returned.
   *
   * @type {String}
   */

  const entryRequest = getTaskState(entryRequestId);

  // If we've reached our maximum number of retries, don't reattempt.
  if (entryRequest.attempt > entryRequest.maxAttempts) {
    store.dispatch(addMessage({
      level: 'warning',
      header: 'Contest entry failed.',
      content: 'Polling attempt timed out.',
    }));

    store.dispatch(entryRequestActions.entryRequestRecieved(entryRequestId, 'POLLING_TIMEOUT'));

    return false;
  }

  switch (entryRequest.status) {
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
      log.error('Encountered unexpected entryRequest.status', entryRequest.status);
      return false;
  }
}

/**
 * Check the status of a contest entry request.
 * This is used to ping the server after a contest entry request has been made in order to see
 * if it has been sucesfully processed by the task queue.
 * @param  {[type]} taskId the ID returned by the enterContest action.
 */
export function fetch(taskId) {
  // Set the state to show that we are currently fetching the entryRequestStatus.
  store.dispatch(entryRequestActions.fetchingEntryRequestStatus(taskId));

  return new Promise((resolve, reject) => {
    request
    .get(`/api/contest/enter-lineup-status/${taskId}/`)
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
        log.error('Contest entry request status error:', res.body);
        const content = 'Contest entry failed.';

        store.dispatch(addMessage({
          level: 'warning',
          content,
        }));

        reject(content);
        // Remove the request from the store.
        return store.dispatch(entryRequestActions.entryRequestRecieved(taskId, 'FAILURE'));
      }

      // If it was a success.
      if (res.body.status === 'SUCCESS') {
        // Because the user just entered a contest, their cash balance should be different.
        store.dispatch(fetchCashBalanceIfNeeded());
        // Fetch the user's current contest pool entries which will force the UI to update.
        store.dispatch(fetchContestPoolEntries());
        // Re-Fetch the contest list that will have an updated current_entries count.
        store.dispatch(fetchUpcomingContests());
        // Display a success message to the user.
        store.dispatch(addMessage({
          level: 'success',
          header: 'Your lineup has been entered.',
          ttl: 2000,
        }));
      }
      // If it was a failure.
      if (res.body.status === 'FAILURE') {
        log.error('Contest entry request status error:', res.body);
        let content = '';
        // Add the response msg to the message we display to the user.
        if (res.body.exception) {
          content = res.body.exception.msg;
        }

        store.dispatch(addMessage({
          level: 'warning',
          header: 'Contest entry failed.',
          content,
        }));

        reject(content);
        // Remove the request from the store.
        return store.dispatch(entryRequestActions.entryRequestRecieved(taskId, res.body.status));
      }

      resolve(res.body.status);
      return store.dispatch(entryRequestActions.entryRequestRecieved(taskId, res.body.status));
    });
  });
}
