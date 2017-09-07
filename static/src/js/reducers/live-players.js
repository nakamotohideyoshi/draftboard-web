import update from 'react-addons-update';
import * as ActionTypes from '../action-types';


module.exports = (state = {
  relevantPlayers: {},
  fetched: [],
  expiresAt: {},
}, action = {}) => {
  switch (action.type) {
    case ActionTypes.REQUEST_LIVE_PLAYERS_STATS:
      return update(state, {
        expiresAt: {
          $merge: {
            [action.lineupId]: action.expiresAt,
          },
        },
      });

    case ActionTypes.RECEIVE_LIVE_PLAYERS_STATS: {
      const { lineupId, players } = action.response;
      const newState = update(state, {
        // add in players
        relevantPlayers: {
          $merge: players,
        },
        // add to fetched list
        fetched: {
          $push: [lineupId],
        },
      });

      newState.expiresAt[lineupId] = action.expiresAt;

      return newState;
    }


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
