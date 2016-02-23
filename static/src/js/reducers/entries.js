import * as ActionTypes from '../action-types';
import update from 'react-addons-update';
import { dateNow } from '../lib/utils';
import { forEach as _forEach } from 'lodash';
import { merge as _merge } from 'lodash';


module.exports = (state = {
  isFetching: false,
  hasRelatedInfo: false,
  expiresAt: dateNow(),
  items: [],
}, action) => {
  switch (action.type) {
    case ActionTypes.ADD_ENTRIES_PLAYERS:
      const newState = _merge({}, state);

      _forEach(action.entriesPlayers, (roster, entryId) => {
        newState.items[entryId].roster = roster;
      });

      return newState;

    case ActionTypes.CONFIRM_RELATED_ENTRIES_INFO:
      return update(state, {
        $merge: {
          hasRelatedInfo: true,
        },
      });

    case ActionTypes.REQUEST_ENTRIES:
      return update(state, {
        $merge: {
          isFetching: true,
          expiresAt: action.expiresAt,
        },
      });


    case ActionTypes.RECEIVE_ENTRIES:
      return update(state, {
        $set: {
          isFetching: false,
          hasRelatedInfo: false,
          items: action.items,
          expiresAt: action.expiresAt,
        },
      });


    default:
      return state;
  }
};
