import update from 'react-addons-update';
import * as ActionTypes from '../action-types';
import { merge as _merge } from 'lodash';


const initialState = {
  // object of current multipart events that exist
  // key is `at_bat__id` for mlb
  events: {},
  // list of players that user can choose to watch, aka see updates with corresponding multipart event
  watchablePlayers: [],
};

// Reducer for multipart events, such as mlb at bats, and nfl drives
module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.EVENT_MULTIPART_ADD:
      return update(state, {
        events: {
          $merge: {
            [action.id]: [action.event],
          },
        },
      });

    case ActionTypes.EVENT_MULTIPART_UPDATE:
      return update(state, {
        events: {
          [action.id]: {
            $push: [action.event],
          },
        },
      });

    case ActionTypes.EVENT_MULTIPART_REMOVE: {
      const events = _merge({}, state.events[action.sport]);
      delete events[action.id];

      return update(state, {
        events: {
          $set: events,
        },
      });
    }

    default:
      return state;
  }
};
