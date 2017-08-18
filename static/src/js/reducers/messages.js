import ActionTypes from '../action-types.js';
import merge from 'lodash/merge';
import log from '../lib/logging.js';

const initialState = {};


/**
 * Messages provide a channel for the app to notify the user of something.
 *
 * There are 3 types of messages: warning, info, and success. These simply correspond with pre-set
 * CSS styles that will dictate the color of the message the user sees.
 */
module.exports = (state = initialState, action) => {
  const nextState = merge({}, state);

  switch (action.type) {

    case ActionTypes.ADD_MESSAGE:

      if (state[action.id] && !action.replace) {
        log.warn('not displaying user message, message.id already exists.', action.id);
        return state;
      }

      nextState[action.id] = {
        level: action.level,
        header: action.header,
        content: action.content,
        ttl: action.ttl,
      };
      return nextState;


    case ActionTypes.REMOVE_MESSAGE:
      delete nextState[action.id];
      return nextState;


    case ActionTypes.CLEAR_MESSAGES:
      return {};


    default:
      return state;
  }
};
