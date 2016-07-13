import merge from 'lodash/merge';
import intersection from 'lodash/intersection';
import map from 'lodash/map';
import uniq from 'lodash/uniq';
const actionTypes = require('../action-types');

// This is the order in which sports should be pre-selected.  If we don't have
// any contests, it will walk the array looking for the first sport which has
// contests.
// To change the order that the filters appear on the page, look in
// contest-list-sport-filter.jsx.
const preselectedSportFilterOrder = ['mlb', 'nfl', 'nba', 'nhl'];

const findPreselectedSport = (contests, presetOrder) => {
  const contestSports = uniq(map(contests, (contest) => contest.sport));
  const defaultSportList = intersection(presetOrder, contestSports);

  if (defaultSportList.length) {
    return defaultSportList[0];
  }

  return '';
};


const initialState = {
  allContests: {},
  filteredContests: {},
  focusedContestId: null,
  isFetchingEntrants: false,
  isFetchingContestPools: false,
  entrants: {},
  filters: {
    orderBy: {
      property: 'start',
      direction: 'asc',
    },
    // Default to 'all' contest type matches.
    contestTypeFilter: {
      filterProperty: 'contestType',
      match: '',
    },
    contestFeeFilter: {
      match: { minVal: 0, maxVal: null },
    },
    contestSearchFilter: {},
    sportFilter: {
      match: '',
      filterProperty: 'sport',
    },
  },
};


module.exports = (state = initialState, action = {}) => {
  let newState;

  switch (action.type) {

    case actionTypes.FETCH_CONTEST_POOLS:
      return merge({}, state, {
        isFetchingContestPools: true,
      });


    case actionTypes.FETCH_CONTEST_POOLS_SUCCESS:
      // Return a copy of the previous state with our new things added to it.
      return merge({}, state, {
        allContests: action.response,
        filteredContests: action.response,
        isFetchingContestPools: false,
        filters: {
          sportFilter: {
            match: findPreselectedSport(action.response, preselectedSportFilterOrder),
          },
        },
      });


    case actionTypes.FETCH_CONTEST_POOLS_FAIL:
      return merge({}, state, {
        isFetchingContestPools: false,
      });


    case actionTypes.UPCOMING_CONTESTS_FILTER_CHANGED: {
      const newFilter = {};

      if (action.filter) {
        newFilter[action.filter.filterName] = {
          filterProperty: action.filter.filterProperty,
          match: action.filter.match,
        };

        return merge({}, state, {
          filters: merge({}, state.filters, newFilter),
        });
      }

      // If no filter was supplied, return the original state.
      return state;
    }


    case actionTypes.SET_FOCUSED_CONTEST:
      return merge({}, state, {
        focusedContestId: action.contestId,
      });


    case actionTypes.UPCOMING_CONTESTS_ORDER_CHANGED:
      newState = merge({}, state);
      newState.filters.orderBy = action.orderBy;
      return newState;


    case actionTypes.FETCHING_CONTEST_ENTRANTS:
      return merge({}, state, {
        isFetchingEntrants: true,
      });


    case actionTypes.FETCH_CONTEST_ENTRANTS_FAIL:
      return merge({}, state, {
        isFetchingEntrants: false,
      });


    case actionTypes.FETCH_CONTEST_ENTRANTS_SUCCESS: {
      const newEntrants = merge({}, state.entrants);
      newEntrants[action.contestId] = action.entrants;

      return merge({}, state, {
        isFetchingEntrants: false,
        entrants: newEntrants,
      });
    }


    case actionTypes.UPCOMING_CONTESTS_UPDATE_RECEIVED: {
      const stateCopy = merge({}, state);

      stateCopy.allContests[action.contest.id] = action.contest;
      if (stateCopy.filteredContests.hasOwnProperty(action.contest.id)) {
        stateCopy.filteredContests[action.contest.id] = action.contest;
      }

      return stateCopy;
    }


    default:
      return state;
  }
};
