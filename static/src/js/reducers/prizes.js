import update from 'react-addons-update';
import * as ActionTypes from '../action-types';


module.exports = (state = {}, action = {}) => {
  switch (action.type) {

    case ActionTypes.REQUEST_PRIZE: {
      const newProps = {
        id: action.id,
        expiresAt: action.expiresAt,
      };

      return update(state, {
        $merge: {
          [action.id]: newProps,
        },
      });
    }


    case ActionTypes.RECEIVE_PRIZE:
      return update(state, {
        [action.response.id]: {
          $set: {
            info: action.response.info,
            expiresAt: action.expiresAt,
          },
        },
      });


    default:
      return state;
  }
};
