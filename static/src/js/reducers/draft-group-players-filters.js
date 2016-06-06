import { merge as _merge } from 'lodash';
import * as ActionTypes from '../action-types.js';
import log from '../lib/logging.js';


const initialState = {
  filters: {
    orderBy: {
      property: 'salary',
      direction: 'desc',
    },
    playerSearchFilter: {
      filterProperty: 'player.name',
      match: '',
    },
    probablePitchersFilter: {
      // match == true means to only show probably pitchers.
      match: true,
      // this doesn't matter.
      filterProperty: 'srid',
    },
    positionFilter: {},
    teamFilter: {
      match: [],
      count: 0,
    },
  },
  focusedPlayerId: null,
};


/**
 * Reducer for the players of a single draft group - used in the draft section.
 */
module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.SET_FOCUSED_PLAYER:
      // Grab the focused player from our list of players.
      return _merge({}, state, {
        focusedPlayerId: action.playerId,
      });


    case ActionTypes.DRAFTGROUP_FILTER_CHANGED: {
      // Override any previous filters with what has been passed.
      const filters = _merge({}, state.filters);

      if (!filters[action.filter.filterName]) {
        log.error('No matching filter was found in the store.', action);
        return state;
      }

      // If nothing has changed, ignore the DRAFTGROUP_FILTER_CHANGED action.
      if (
        filters[action.filter.filterName].filterProperty === action.filter.filterProperty &&
        filters[action.filter.filterName].match === action.filter.match
      ) {
        log.info(`${action.filter.filterProperty} filter has not changed, ignoring DRAFTGROUP_FILTER_CHANGED action.`);
        return state;
      }

      filters[action.filter.filterName] = {
        filterProperty: action.filter.filterProperty,
        match: action.filter.match,
        count: action.filter.match.length,
      };

      const newFilterState = _merge({}, state, {
        filters,
      });
      // Since a merge won't replace the `match` array, do it manually, otherwise the previous
      // filter matches will still remain in the array.
      newFilterState.filters[action.filter.filterName].match = action.filter.match;

      return newFilterState;
    }


    case ActionTypes.DRAFTGROUP_ORDER_CHANGED: {
      const newState = _merge({}, state);
      newState.filters.orderBy = action.orderBy;
      return newState;
    }


    default:
      return state;
  }
};
