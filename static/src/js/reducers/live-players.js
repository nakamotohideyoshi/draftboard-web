import update from 'react-addons-update';
import * as ActionTypes from '../action-types';
import { dateNow } from '../lib/utils';


module.exports = (state = {
  isFetching: [],
  relevantPlayers: {},
  fetched: [],
  expiresAt: dateNow(),
}, action) => {
  switch (action.type) {
    case ActionTypes.REQUEST_LIVE_PLAYERS_STATS:
      return update(state, {
        $merge: {
          expiresAt: action.expiresAt,
        },
      });

    case ActionTypes.RECEIVE_LIVE_PLAYERS_STATS:
      const newState = update(state, {
        // add in players
        relevantPlayers: {
          $merge: action.players,
        },
        // add to fetched list
        fetched: {
          $push: [action.lineupId],
        },
      });

      newState.isFetching = newState.isFetching.filter(item => item !== action.lineupId);
      newState.expiresAt = action.expiresAt;

      return newState;


    case ActionTypes.UPDATE_LIVE_PLAYER_STATS:
      return update(state, {
        relevantPlayers: {
          $merge: {
            [action.playerSRID]: action.fields,
          },
        },
      });

    default:
      return state;
  }
};
