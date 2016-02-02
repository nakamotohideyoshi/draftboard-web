import update from 'react-addons-update';
import * as ActionTypes from '../action-types';


// Reducer for the live section, stores what mode the app is in
module.exports = (state = {
  mode: {},
}, action) => {
  switch (action.type) {
    case ActionTypes.LIVE_MODE_CHANGED:
      return update(state, {
        mode: {
          $merge: action.mode,
        },
      });

    default:
      return state;
  }
};
