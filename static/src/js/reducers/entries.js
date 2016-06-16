import * as ActionTypes from '../action-types';
import update from 'react-addons-update';
import { dateNow } from '../lib/utils';
import forEach from 'lodash/forEach';
import map from 'lodash/map';
import merge from 'lodash/merge';


module.exports = (state = {
  isFetching: false,
  isFetchingRosters: false,
  hasRelatedInfo: false,
  expiresAt: dateNow(),
  items: [],
}, action = {}) => {
  const newState = merge({}, state);

  switch (action.type) {
    case ActionTypes.ENTRIES__ADD_PLAYERS:
      forEach(action.entriesPlayers, (roster, entryId) => {
        newState.items[entryId].roster = roster;
      });

      return newState;

    case ActionTypes.ENTRIES_ROSTERS__REQUEST:
      return update(state, {
        $merge: {
          isFetchingRosters: true,
          rostersExpireAt: action.expiresAt,
        },
      });

    case ActionTypes.ENTRIES_ROSTERS__RECEIVE:
      forEach(newState.items, (entry, index) => {
        const lineup = action.response.entriesRosters[entry.lineup] || {};
        if (lineup.hasOwnProperty('players')) {
          newState.items[index].roster = map(lineup.players, player => player.playerId);
        }
      });

      newState.isFetchingRosters = false;
      newState.rostersExpireAt = action.expiresAt;

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
