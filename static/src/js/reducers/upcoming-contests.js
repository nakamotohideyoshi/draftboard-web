import merge from 'lodash/merge';
const ActionTypes = require('../action-types');

const initialState = {
  allContests: {},
  filteredContests: {},
  focusedContestId: null,
  isFetchingEntrants: false,
  entrants: {},
  filters: {
    orderBy: {
      property: 'start',
      direction: 'asc',
    },
    contestTypeFilter: {},
    contestFeeFilter: {
      match: { minVal: 0, maxVal: null },
    },
    contestSearchFilter: {},
    sportFilter: {},
  },
};


module.exports = (state = initialState, action) => {
  let newState;

  switch (action.type) {

    case ActionTypes.FETCH_UPCOMING_CONTESTS_SUCCESS:
      // Return a copy of the previous state with our new things added to it.
      return merge({}, state, {
        allContests: action.body.contests,
        filteredContests: action.body.contests,
      });


    case ActionTypes.UPCOMING_CONTESTS_FILTER_CHANGED: {
      const newFilter = {};

      newFilter[action.filter.filterName] = {
        filterProperty: action.filter.filterProperty,
        match: action.filter.match,
      };

      return merge({}, state, {
        filters: merge({}, state.filters, newFilter),
      });
    }


    case ActionTypes.SET_FOCUSED_CONTEST:
      return merge({}, state, {
        focusedContestId: action.contestId,
      });


    case ActionTypes.UPCOMING_CONTESTS_ORDER_CHANGED:
      newState = merge({}, state);
      newState.filters.orderBy = action.orderBy;
      return newState;


    case ActionTypes.FETCHING_CONTEST_ENTRANTS:
      return merge({}, state, {
        isFetchingEntrants: true,
      });


    case ActionTypes.FETCH_CONTEST_ENTRANTS_FAIL:
      return merge({}, state, {
        isFetchingEntrants: false,
      });


    case ActionTypes.FETCH_CONTEST_ENTRANTS_SUCCESS: {
      const newEntrants = merge({}, state.entrants);
      newEntrants[action.contestId] = action.entrants;

      return merge({}, state, {
        isFetchingEntrants: false,
        entrants: newEntrants,
      });
    }


    case ActionTypes.UPCOMING_CONTESTS_UPDATE_RECEIVED: {
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
