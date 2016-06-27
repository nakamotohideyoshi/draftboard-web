import merge from 'lodash/merge';
const actionTypes = require('../action-types');

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
      // Default sport filter is set here.
      match: 'mlb',
      filterProperty: 'sport',
    },
  },
};


module.exports = (state = initialState, action) => {
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
      });


    case actionTypes.FETCH_CONTEST_POOLS_FAIL:
      return merge({}, state, {
        isFetchingContestPools: false,
      });


    case actionTypes.UPCOMING_CONTESTS_FILTER_CHANGED: {
      const newFilter = {};

      newFilter[action.filter.filterName] = {
        filterProperty: action.filter.filterProperty,
        match: action.filter.match,
      };

      return merge({}, state, {
        filters: merge({}, state.filters, newFilter),
      });
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
