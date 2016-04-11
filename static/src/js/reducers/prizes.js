import update from 'react-addons-update';
import * as ActionTypes from '../action-types';


module.exports = (state = {}, action) => {
  switch (action.type) {

    case ActionTypes.REQUEST_PRIZE: {
      const newProps = {
        id: action.id,
        isFetching: true,
      };

      return update(state, {
        $set: {
          [action.id]: newProps,
        },
      });
    }


    case ActionTypes.RECEIVE_PRIZE:
      return update(state, {
        [action.id]: {
          $set: {
            info: action.info,
            isFetching: false,
          },
        },
      });


    default:
      return state;
  }
};
