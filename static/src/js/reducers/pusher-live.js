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

    case ActionTypes.PUSHER_ADD_ANIMATION_EVENT:
      return update(state, {
        animationEvents: {
          $merge: {
            [action.key]: action.value,
          },
        },
      });

    case ActionTypes.PUSHER_ADD_GAME_QUEUE_EVENT:
      // update if already running
      if (state.gamesQueue.hasOwnProperty(action.gameId)) {
        return update(state, {
          gamesQueue: {
            [action.gameId]: {
              queue: {
                $push: [action.gameQueueEvent],
              },
            },
          },
        });
      }

      // otherwise make a new queue
      return update(state, {
        gamesQueue: {
          $set: {
            [action.gameId]: {
              queue: [action.gameQueueEvent],
            },
          },
        },
      });

    case ActionTypes.PUSHER_ADD_PLAYER_EVENT_DESCRIPTION:
      return update(state, {
        playerEventDescriptions: {
          $merge: {
            [action.key]: action.value,
          },
        },
      });

    case ActionTypes.PUSHER_DIFFERENCE_PLAYERS_PLAYING:
      return update(state, {
        $merge: {
          playersPlaying: _difference(state.playersPlaying, action.players),
        },
      });

    case ActionTypes.PUSHER_REMOVE_ANIMATION_EVENT: {
      const animationEvents = _merge({}, state.animationEvents);
      delete animationEvents[action.key];

      return update(state, {
        $merge: {
          animationEvents,
        },
      });
    }

    case ActionTypes.PUSHER_REMOVE_PLAYER_EVENT_DESCRIPTION: {
      const playerEventDescriptions = _merge({}, state.playerEventDescriptions);
      delete playerEventDescriptions[action.key];

      return update(state, {
        $merge: {
          playerEventDescriptions,
        },
      });
    }

    case ActionTypes.PUSHER_SHIFT_GAME_QUEUE_EVENT: {
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

    case ActionTypes.PUSHER_UNION_PLAYERS_PLAYING:
      return update(state, {
        $merge: {
          playersPlaying: _union(state.playersPlaying, action.players),
        },
      });

    case ActionTypes.PUSHER_UNSHIFT_PLAYER_HISTORY: {
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
