import * as ActionTypes from '../action-types';
import update from 'react-addons-update';
import { dateNow } from '../lib/utils';
import { forEach as _forEach } from 'lodash';
import { map as _map } from 'lodash';
import { merge as _merge } from 'lodash';


module.exports = (state = {
  isFetching: false,
  hasRelatedInfo: false,
  expiresAt: dateNow(),
  items: [],
}, action = {}) => {
  const newState = _merge({}, state);

  switch (action.type) {
    case ActionTypes.ENTRIES__ADD_PLAYERS:
      _forEach(action.entriesPlayers, (roster, entryId) => {
        newState.items[entryId].roster = roster;
      });

      return newState;

    case ActionTypes.ENTRIES_ROSTERS__RECEIVE:
      _forEach(newState.items, (entry, index) => {
        const lineup = action.response.entriesRosters[entry.lineup] || {};
        if (lineup.hasOwnProperty('players')) {
          newState.items[index].roster = _map(lineup.players, player => player.playerId);
        }
      });

      return newState;

    case ActionTypes.ENTRIES__RELATED_INFO_SUCCESS:
      return update(state, {
        $merge: {
          hasRelatedInfo: true,
        },
      });

    case ActionTypes.ENTRIES__REQUEST:
      return update(state, {
        $merge: {
          isFetching: true,
          expiresAt: action.expiresAt,
        },
      });

    case ActionTypes.ENTRIES__RECEIVE:
      return update(state, {
        $set: {
          isFetching: false,
          hasRelatedInfo: false,
          // items: action.items,
          items: action.response.entries,
          expiresAt: action.expiresAt,
        },
      });

    default:
      return state;
  }
};
