import update from 'react-addons-update';
import * as ActionTypes from '../action-types';


// Reducer for the live section, stores what you're watching
module.exports = (state = {
  myLineupId: null,
  sport: null,
  contestId: null,
  opponentLineupId: null,
}, action = {}) => {
  switch (action.type) {
    case ActionTypes.WATCHING_UPDATE:
      return update(state, {
        $merge: action.watching,
      });

    default:
      return state;
  }
};
