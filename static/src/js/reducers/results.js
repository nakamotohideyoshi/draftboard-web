import update from 'react-addons-update';
import ActionTypes from '../action-types';


module.exports = (state = {}, action) => {
  switch (action.type) {
    case ActionTypes.RECEIVE_RESULTS:
      return update(state, {
        $set: {
          [action.when]: action.response,
        },
      });

    default:
      return state;
  }
};
