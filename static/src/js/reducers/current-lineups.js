import update from 'react-addons-update';
import * as ActionTypes from '../action-types';


module.exports = (state = {
  isFetching: false,
  items: {},
}, action = {}) => {
  switch (action.type) {
    case ActionTypes.SET_CURRENT_LINEUPS:
      return update(state, {
        $set: {
          updatedAt: action.updatedAt,
          items: action.lineups,
        },
      });

    default:
      return state;
  }
};
