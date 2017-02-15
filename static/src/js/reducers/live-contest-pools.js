import * as ActionTypes from '../action-types';
import merge from 'lodash/merge';


module.exports = (state = {}, action = {}) => {
  switch (action.type) {
    case ActionTypes.REQUEST_CONTEST_POOL_INFO: {
      const newState = merge({}, state);
      const pool = merge(
        {},
        newState[action.id] || {},
        {
          id: action.id,
          expiresAt: action.expiresAt,
          isFetchingInfo: true,
        }
      );

      newState[action.id] = pool;
      return newState;
    }

    case ActionTypes.RECEIVE_CONTEST_POOL_INFO: {
      const newState = merge({}, state);
      const { id, info } = action.response;
      const pool = merge(
        {},
        newState[id] || {},
        {
          expiresAt: action.expiresAt,
          isFetchingInfo: false,
          hasRelatedInfo: true,
        },
        info
      );

      newState[id] = pool;
      return newState;
    }

    default:
      return state;
  }
};
