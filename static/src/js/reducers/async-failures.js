import ActionTypes from '../action-types.js';

const initialState = [];


/**
 * Store async failures
 * Pass through the ActionType as `failedType`
 *
 * We check on failure if it already exists, and if so, then we addMessage() and tell Sentry
 */
module.exports = (state = initialState, action) => {
  const nextState = state.slice(0);

  switch (action.type) {

    case ActionTypes.ADD_ASYNC_FAILURE:
      nextState.push(action.requestType);
      return nextState;


    case ActionTypes.REMOVE_ASYNC_FAILURE:
      delete nextState[action.requestType];
      return nextState;


    default:
      return state;
  }
};
