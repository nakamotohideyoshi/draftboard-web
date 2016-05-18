import update from 'react-addons-update';
import * as ActionTypes from '../action-types';


// Reducer for the live section, stores what you're watching
module.exports = (state = {
  contestId: null,
  myLineupId: null,
  myPlayerSRID: null,
  opponentLineupId: null,
  opponentPlayerSRID: null,
  sport: null,
}, action) => {
  switch (action.type) {
    case ActionTypes.WATCHING_UPDATE:
      return update(state, {
        $merge: action.watching,
      });

    default:
      return state;
  }
};
