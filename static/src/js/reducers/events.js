import update from 'react-addons-update';
import * as ActionTypes from '../action-types';
import difference from 'lodash/difference';
import merge from 'lodash/merge';
import union from 'lodash/union';

const initialState = {
  animationEvents: {},
  gamesQueue: {},
  playerEventDescriptions: {},
  playerHistories: {},
  playersPlaying: [],
};

// Reducer for the pusher events coming through
module.exports = (state = initialState, action = {}) => {
  switch (action.type) {

    case ActionTypes.EVENT_ADD_ANIMATION:
      return update(state, {
        animationEvents: {
          $merge: {
            [action.key]: action.value,
          },
        },
      });

    case ActionTypes.EVENT_ADD_GAME_QUEUE:
      return update(state, {
        gamesQueue: {
          $merge: {
            [action.gameId]: {
              queue: [],
            },
          },
        },
      });

    case ActionTypes.EVENT_GAME_QUEUE_PUSH:
      if (state.gamesQueue.hasOwnProperty(action.gameId) === false) {
        throw new Error(`Cannot push an event to a game that does not exist, gameId ${action.gameId}`);
      }

      return update(state, {
        gamesQueue: {
          [action.gameId]: {
            queue: {
              $push: [action.event],
            },
          },
        },
      });

    case ActionTypes.EVENT_PLAYER_ADD_DESCRIPTION:
      return update(state, {
        playerEventDescriptions: {
          $merge: {
            [action.key]: action.value,
          },
        },
      });

    case ActionTypes.EVENT_DIFFERENCE_PLAYERS_PLAYING:
      return update(state, {
        $merge: {
          playersPlaying: difference(state.playersPlaying, action.players),
        },
      });

    case ActionTypes.EVENT_REMOVE_ANIMATION: {
      const animationEvents = merge({}, state.animationEvents);
      delete animationEvents[action.key];

      return update(state, {
        $merge: {
          animationEvents,
        },
      });
    }

    case ActionTypes.EVENT_PLAYER_REMOVE_DESCRIPTION: {
      const playerEventDescriptions = merge({}, state.playerEventDescriptions);

      // don't bother if it isn't there
      if (!(action.key in playerEventDescriptions)) return state;

      delete playerEventDescriptions[action.key];

      return update(state, {
        $merge: {
          playerEventDescriptions,
        },
      });
    }

    case ActionTypes.EVENT_SHIFT_GAME_QUEUE: {
      // if no queue, return
      if (!(action.gameId in state.gamesQueue)) return state;

      const queue = [...state.gamesQueue[action.gameId].queue];

      // if queue empty, return
      if (queue.length === 0) return state;

      queue.shift();

      return update(state, {
        gamesQueue: {
          [action.gameId]: {
            $set: {
              queue,
            },
          },
        },
      });
    }

    case ActionTypes.EVENT_UNION_PLAYERS_PLAYING:
      return update(state, {
        $merge: {
          playersPlaying: union(state.playersPlaying, action.players),
        },
      });

    case ActionTypes.EVENT_UNSHIFT_PLAYER_HISTORY: {
      const playerHistory = state.playerHistories[action.key] || [];
      const newHistory = [...playerHistory];
      newHistory.unshift(action.value);

      return update(state, {
        playerHistories: {
          $set: {
            [action.key]: newHistory,
          },
        },
      });
    }

    default:
      return state;
  }
};
