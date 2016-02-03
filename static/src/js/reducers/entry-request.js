import * as ActionTypes from '../action-types.js';
import log from '../lib/logging.js';
import { merge as _merge } from 'lodash';
import { forEach as _forEach } from 'lodash';

const initialState = {
  history: {},
};


// Find any inactive entries and move them into the history. DO NOT feed the state into this as it
// will mutate it.
function archiveEntries(newState) {
  const archivedState = initialState;

  _forEach(newState, (entry, taskId) => {
    // If the status is failure or timeout, move the task into the history.
    if (entry.hasOwnProperty('status')) {
      if (entry.status === 'FAILURE' || entry.status === 'POLLING_TIMEOUT') {
        log.trace(`Moving task to history`, entry);
        archivedState.history[taskId] = entry;
      }
    } else {
      archivedState[taskId] = entry;
    }
  });

  return newState;
}


/**
 * When a user requests to enter their lineup into a contest, a background job is queued up on the
 * server. We then ping the server
 */
module.exports = (state = initialState, action) => {
  let newState = initialState;
  const stateCopy = Object.assign({}, state);

  switch (action.type) {

    case ActionTypes.ADD_ENTRY_REQUEST_MONITOR:
      newState = Object.assign({}, state);

      // Find and delete any existing entryRequests for the same lineup+contest.
      // If we have more than 1 entryRequest for a single lineup+contest, we have no way to figure
      // out which is which.
      //
      // The best use-case for this is if a user tries to enter a contest but it fails, then they
      // try to enter again - we need to remove the first entry request.
      _forEach(newState, (entryRequest, key) => {
        if (entryRequest.lineupId === action.lineupId && entryRequest.contestId === action.contestId) {
          delete newState[key];
        }
      });

      newState[action.taskId] = {
        status: 'PENDING',
        contestId: action.contestId,
        lineupId: action.lineupId,
        maxAttempts: action.maxAttempts,
        attempt: action.attempt,
      };

      return archiveEntries(newState);


    case ActionTypes.FETCHING_ENTRY_REQUEST_STATUS:
      // Add 1 to the attempt count
      let attemptCount = parseInt(state[action.taskId].attempt, 10) + 1;

      if (typeof attemptCount !== 'number') {
        log.error(`${state[action.taskId].attempt} is not a number.`);
        attemptCount = 1;
      }

      newState[action.taskId] = {
        status: 'FETCHING',
        attempt: attemptCount,
      };

      return archiveEntries(_merge(stateCopy, newState));


    case ActionTypes.ENTRY_REQUEST_RECIEVED:
      // Update the status and merge states.
      newState[action.taskId] = {
        status: action.status,
      };

      return archiveEntries(_merge(stateCopy, newState));


    default:
      return state;
  }
};
