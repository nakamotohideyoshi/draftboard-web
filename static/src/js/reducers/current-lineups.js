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
  rostersExpireAt: dateNow(),
  items: {},
}, action = {}) => {
  const newState = _merge({}, state);

  switch (action.type) {
    case ActionTypes.SET_CURRENT_LINEUPS:
      return update(state, {
        $merge: {
          items: action.lineups,
        },
      });

    case ActionTypes.CURRENT_LINEUPS__ADD_PLAYERS:
      _forEach(action.lineupsPlayers, (roster, entryId) => {
        newState.items[entryId].roster = roster;
      });

      return newState;

    case ActionTypes.CURRENT_LINEUPS_ROSTERS__REQUEST:
      return update(state, {
        $merge: {
          rostersExpireAt: action.expiresAt,
        },
      });

    case ActionTypes.CURRENT_LINEUPS_ROSTERS__RECEIVE:
      _forEach(newState.items, (lineup, index) => {
        const withRoster = action.response.lineupsRosters[lineup.id] || {};
        if (withRoster.hasOwnProperty('players')) {
          newState.items[index].roster = _map(withRoster.players, player => player.playerId);
        }
      });

      newState.rostersExpireAt = action.expiresAt;

      return newState;

    case ActionTypes.CURRENT_LINEUPS__RELATED_INFO_SUCCESS:
      return update(state, {
        $merge: {
          hasRelatedInfo: true,
        },
      });

    case ActionTypes.CURRENT_LINEUPS__REQUEST:
      return update(state, {
        $merge: {
          isFetching: true,
          expiresAt: action.expiresAt,
        },
      });

    case ActionTypes.CURRENT_LINEUPS__RECEIVE:
      return update(state, {
        $set: {
          isFetching: false,
          hasRelatedInfo: false,
          // items: action.items,
          items: action.response.lineups || {},
          expiresAt: action.expiresAt,
        },
      });

    default:
      return state;
  }
};
