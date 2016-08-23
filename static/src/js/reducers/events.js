import update from 'react-addons-update';
import * as ActionTypes from '../action-types';
import difference from 'lodash/difference';
import merge from 'lodash/merge';
import union from 'lodash/union';

const initialState = {
  animationEvent: null,
  queue: [],
  playerEventDescriptions: {},
  playerHistories: {},
  playersPlaying: [],
};

// Reducer for the pusher events coming through
module.exports = (state = initialState, action = {}) => {
  switch (action.type) {

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

    case ActionTypes.EVENT__SET_CURRENT: {
      const newState = merge({}, state);
      newState.animationEvent = action.value;
      return newState;
    }

    case ActionTypes.EVENT__REMOVE_CURRENT:
      // perf optimization, memoization
      if (state.animationEvent === null) return state;

      return merge({}, state, {
        animationEvent: null,
      });

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

    case ActionTypes.EVENT_GAME_QUEUE_PUSH: {
      const newState = merge({}, state);
      newState.queue.push(action.event);
      return newState;
    }

    case ActionTypes.EVENT_SHIFT_GAME_QUEUE: {
      const newState = merge({}, state);

      // if queue empty, return for performance optimizations
      if (newState.queue.length === 0) return state;

      newState.queue.shift();
      return newState;
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
