import * as ActionTypes from '../action-types.js';
import log from '../lib/logging.js';
import forEach from 'lodash/forEach';
import merge from 'lodash/merge';

const initialState = {
  history: {},
};


// Find any inactive entries and move them into the history. DO NOT feed the state into this as it
// will mutate it.
function archiveEntries(newState) {
  const archivedState = merge({}, initialState);

  forEach(newState, (entry, taskId) => {
    // If the status is failure or timeout, move the task into the history.
    if (entry.hasOwnProperty('status')) {
      if (entry.status === 'FAILURE' || entry.status === 'POLLING_TIMEOUT' || entry.status === 'SUCCESS') {
        log.debug('Moving task to history', entry);
        archivedState.history[taskId] = merge({}, entry);
      } else {
        archivedState[taskId] = merge({}, entry);
      }
    } else {
      archivedState[taskId] = merge({}, entry);
    }
  });

  return archivedState;
}


/**
 * When a user requests to enter their lineup into a contest, a background job is queued up on the
 * server. We then ping the server
 */
module.exports = (state = initialState, action) => {
  const stateCopy = merge({}, state);

  switch (action.type) {

    case ActionTypes.ADD_UNREGISTER_REQUEST_MONITOR:
    case ActionTypes.ADD_ENTRY_REQUEST_MONITOR:

      // Find and delete any existing entryRequests for the same lineup+contest.
      // If we have more than 1 entryRequest for a single lineup+contest, we have no way to figure
      // out which is which.
      //
      // The best use-case for this is if a user tries to enter a contest but it fails, then they
      // try to enter again - we need to remove the first entry request.
      forEach(stateCopy, (entryRequest, key) => {
        if (entryRequest.lineupId === action.lineupId && entryRequest.contestPoolId === action.contestPoolId) {
          log.debug('Deleting already-existing request for this entry.', key);
          delete stateCopy[key];
        }
      });

      stateCopy[action.taskId] = {
        status: 'PENDING',
        contestPoolId: action.contestPoolId,
        lineupId: action.lineupId,
        maxAttempts: action.maxAttempts,
        attempt: 0,
        requestType: action.requestType,
      };

      // unregister requests have an entryId, so add that.
      if (action.entryId) {
        stateCopy[action.taskId].entryId = action.entryId;
      }

      return archiveEntries(stateCopy);


    case ActionTypes.FETCHING_UNREGISTER_REQUEST_STATUS:
    case ActionTypes.FETCHING_ENTRY_REQUEST_STATUS: {
      // Add 1 to the attempt count
      let attemptCount = parseInt(stateCopy[action.taskId].attempt, 10) + 1;

      if (typeof attemptCount !== 'number') {
        log.error(`${stateCopy[action.taskId].attempt} is not a number.`);
        attemptCount = 1;
      }

      stateCopy[action.taskId].status = 'FETCHING';
      stateCopy[action.taskId].attempt = attemptCount;

      return archiveEntries(stateCopy);
    }


    case ActionTypes.UNREGISTER_REQUEST_RECIEVED:
    case ActionTypes.ENTRY_REQUEST_RECIEVED:
      // Update the status and merge states
      stateCopy[action.taskId].status = action.status;

      return archiveEntries(stateCopy);


    default:
      return state;
  }
};
