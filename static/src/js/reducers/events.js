import update from 'react-addons-update';
import * as ActionTypes from '../action-types';
import merge from 'lodash/merge';
import union from 'lodash/union';

const initialState = {
  currentEvent: null,
  history: [],
  queue: [],
  playerEventDescriptions: {},
  playerHistories: {},
  playersPlaying: [],
};

// Reducer for the pusher events coming through
module.exports = (state = initialState, action = {}) => {
  switch (action.type) {
    case ActionTypes.EVENT_ADD_TO_HISTORY: {
      const newState = merge({}, state);
      newState.history.push(action.value);

      // limit the size of the queue to 50
      if (newState.history.length > 50) newState.history.shift();

      return newState;
    }

    case ActionTypes.EVENT_PLAYER_ADD_DESCRIPTION:
      return update(state, {
        playerEventDescriptions: {
          $merge: {
            [action.key]: action.value,
          },
        },
      });

    case ActionTypes.EVENT_REMOVE_PLAYERS_PLAYING: {
      const newState = merge({}, state);
      newState.playersPlaying = [];

      return newState;
    }

    case ActionTypes.EVENT__SET_CURRENT: {
      const newState = merge({}, state);
      newState.currentEvent = action.value;
      return newState;
    }

    case ActionTypes.EVENT__REMOVE_CURRENT:
      // perf optimization, memoization
      if (state.currentEvent === null) return state;

      return merge({}, state, {
        currentEvent: null,
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
