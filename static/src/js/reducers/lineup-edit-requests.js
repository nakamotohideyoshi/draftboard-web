import * as ActionTypes from '../action-types.js';
import log from '../lib/logging.js';
import forEach from 'lodash/forEach';
import merge from 'lodash/merge';


const initialState = {};


/**
 * When a user requests to enter their lineup into a contest, a background job is queued up on the
 * server. We then ping the server
 */
module.exports = (state = initialState, action) => {
  const stateCopy = merge({}, state);

  switch (action.type) {

    case ActionTypes.ADD_LINEUP_EDIT_REQUEST_MONITOR:

      // Find and delete any existing entryRequests for the same lineup+contest.
      // If we have more than 1 entryRequest for a single lineup+contest, we have no way to figure
      // out which is which.
      //
      // The best use-case for this is if a user tries to enter a contest but it fails, then they
      // try to enter again - we need to remove the first entry request.
      forEach(stateCopy, (entryRequest, key) => {
        if (entryRequest.lineupId === action.lineupId) {
          log.debug('Deleting already-existing edit request for this entry.', key);
          delete stateCopy[key];
        }
      });

      stateCopy[action.taskId] = {
        status: 'PENDING',
        lineupId: action.lineupId,
        maxAttempts: action.maxAttempts,
        attempt: action.attempt,
      };

      return stateCopy;


    case ActionTypes.FETCHING_LINEUP_EDIT_REQUEST_STATUS: {
      // Add 1 to the attempt count
      let attemptCount = parseInt(stateCopy[action.taskId].attempt, 10) + 1;

      if (typeof attemptCount !== 'number') {
        log.error(`${stateCopy[action.taskId].attempt} is not a number.`);
        attemptCount = 1;
      }

      stateCopy[action.taskId].status = 'FETCHING';
      stateCopy[action.taskId].attempt = attemptCount;

      return stateCopy;
    }


    case ActionTypes.LINEUP_EDIT_REQUEST_RECIEVED:
      if (action.status === 'FAILURE' || action.status === 'POLLING_TIMEOUT') {
        log.debug('Edit failed, deleting task from store.', action.taskId);
        delete stateCopy[action.taskId];
        return stateCopy;
      }

      // Update the status and merge states
      stateCopy[action.taskId].status = action.status;

      return stateCopy;


    case ActionTypes.DELETE_LINEUP_EDIT_REQUEST:
      delete stateCopy[action.taskId];
      log.debug('deleting task from store.', action.taskId);
      return stateCopy;


    default:
      return state;
  }
};
