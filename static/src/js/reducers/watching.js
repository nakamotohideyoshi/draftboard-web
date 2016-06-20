import update from 'react-addons-update';
import * as ActionTypes from '../action-types';


const initialState = {
  contestId: null,
  myLineupId: null,
  myPlayerSRID: null,
  opponentLineupId: null,
  opponentPlayerSRID: null,
  sport: null,
};

// Reducer for the live section, stores what you're watching
module.exports = (state = initialState, action) => {
  switch (action.type) {
    case ActionTypes.WATCHING_UPDATE:
      return update(state, {
        $merge: action.watching,
      });

    case ActionTypes.WATCHING__RESET:
      return initialState;

    default:
      return state;
  }
};
