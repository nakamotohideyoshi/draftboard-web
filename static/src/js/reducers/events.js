import update from 'react-addons-update';
import * as ActionTypes from '../action-types';
import { difference as _difference } from 'lodash';
import { merge as _merge } from 'lodash';
import { union as _union } from 'lodash';

const initialState = {
  animationEvents: {},
  gamesQueue: {},
  playerEventDescriptions: {},
  playerHistories: {},
  playersPlaying: [],
};

// Reducer for the live section, stores what mode the app is in
module.exports = (state = initialState, action) => {
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
          playersPlaying: _difference(state.playersPlaying, action.players),
        },
      });

    case ActionTypes.EVENT_REMOVE_ANIMATION: {
      const animationEvents = _merge({}, state.animationEvents);
      delete animationEvents[action.key];

      return update(state, {
        $merge: {
          animationEvents,
        },
      });
    }

    case ActionTypes.EVENT_PLAYER_REMOVE_DESCRIPTION: {
      const playerEventDescriptions = _merge({}, state.playerEventDescriptions);
      delete playerEventDescriptions[action.key];

      return update(state, {
        $merge: {
          playerEventDescriptions,
        },
      });
    }

    case ActionTypes.EVENT_SHIFT_GAME_QUEUE: {
      const queue = [...state.gamesQueue[action.gameId].queue];
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
          playersPlaying: _union(state.playersPlaying, action.players),
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
