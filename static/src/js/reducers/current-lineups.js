import * as ActionTypes from '../action-types';
import forEach from 'lodash/forEach';
import merge from 'lodash/merge';
import update from 'react-addons-update';
import { dateNow } from '../lib/utils';


module.exports = (state = {
  hasRelatedInfo: false,
  expiresAt: dateNow(),
  isFetching: false,
  rostersExpireAt: dateNow(),
  items: {},
}, action = {}) => {
  const newState = merge({}, state);

  switch (action.type) {
    case ActionTypes.SET_CURRENT_LINEUPS:
      return update(state, {
        $merge: {
          items: action.lineups,
        },
      });

    case ActionTypes.CURRENT_LINEUPS__ADD_PLAYERS:
      forEach(action.lineupsPlayers, (roster, entryId) => {
        if (entryId in newState.items) {
          newState.items[entryId].roster = roster;
        }
      });

      return newState;

    case ActionTypes.CURRENT_LINEUPS_ROSTERS__REQUEST:
      return update(state, {
        $merge: {
          rostersExpireAt: action.expiresAt,
        },
      });

    case ActionTypes.CURRENT_LINEUPS_ROSTERS__RECEIVE:
      forEach(newState.items, (lineup, index) => {
        const withRoster = action.response.lineupsRosters[lineup.id] || {};
        if (withRoster.hasOwnProperty('players')) {
          newState.items[index].roster = withRoster.players.map(player => player.playerId);
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
          hasRelatedInfo: false,
          isFetching: false,
          items: action.response.lineups || {},
          expiresAt: action.expiresAt,
        },
      });

    default:
      return state;
  }
};
