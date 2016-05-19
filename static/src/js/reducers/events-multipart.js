import update from 'react-addons-update';
import * as ActionTypes from '../action-types';
import omit from 'lodash/omit';
import merge from 'lodash/merge';
import map from 'lodash/map';
import zipObject from 'lodash/zipObject';


const initialState = {
  // object of current multipart events that exist
  // key is `at_bat__id` for mlb
  events: {},
  // object of players with the eventID as their value
  watchablePlayers: {},
};

// Reducer for multipart events, such as mlb at bats, and nfl drives
module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.EVENT_MULTIPART_SET:
      return update(state, {
        events: {
          $merge: {
            [action.key]: action.value,
          },
        },
      });

    case ActionTypes.EVENT_MULTIPART_DELETE: {
      if (state.events.hasOwnProperty(action.key) === false) {
        throw new Error(`Cannot delete a multievent that does not exist, key ${action.key}`);
      }

      const events = merge({}, state.events);
      delete events[action.key];

      return update(state, {
        events: {
          $set: events,
        },
      });
    }

    case ActionTypes.EVENT_MULTIPART_OMIT_PLAYERS: {
      return update(state, {
        watchablePlayers: {
          $set: omit(state.watchablePlayers, action.players),
        },
      });
    }

    case ActionTypes.EVENT_MULTIPART_MERGE_PLAYERS: {
      return update(state, {
        watchablePlayers: {
          $merge: zipObject(action.players, map(action.players, () => action.eventId)),
        },
      });
    }

    default:
      return state;
  }
};
