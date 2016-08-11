import update from 'react-addons-update';
import ActionTypes from '../action-types';


module.exports = (state = {}, action = {}) => {
  switch (action.type) {
    case ActionTypes.RECEIVE_RESULTS: {
      const { when, response } = action.response;
      return update(state, {
        $set: {
          [when]: response,
        },
      });
    }

    default:
      return state;
  }
};
