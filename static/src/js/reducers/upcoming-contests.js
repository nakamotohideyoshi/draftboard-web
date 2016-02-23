import { merge as _merge } from 'lodash';
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
      return _merge({}, state, {
        allContests: action.body.contests,
        filteredContests: action.body.contests,
      });


    case ActionTypes.UPCOMING_CONTESTS_FILTER_CHANGED:
      const newFilter = {};

      newFilter[action.filter.filterName] = {
        filterProperty: action.filter.filterProperty,
        match: action.filter.match,
      };

      return _merge({}, state, {
        filters: _merge({}, state.filters, newFilter),
      });


    case ActionTypes.SET_FOCUSED_CONTEST:
      return _merge({}, state, {
        focusedContestId: action.contestId,
      });


    case ActionTypes.UPCOMING_CONTESTS_ORDER_CHANGED:
      newState = _merge({}, state);
      newState.filters.orderBy = action.orderBy;
      return newState;


    case ActionTypes.FETCHING_CONTEST_ENTRANTS:
      return _merge({}, state, {
        isFetchingEntrants: true,
      });


    case ActionTypes.FETCH_CONTEST_ENTRANTS_FAIL:
      return _merge({}, state, {
        isFetchingEntrants: false,
      });


    case ActionTypes.FETCH_CONTEST_ENTRANTS_SUCCESS:
      const newEntrants = _merge({}, state.entrants);
      newEntrants[action.contestId] = action.entrants;

      return _merge({}, state, {
        isFetchingEntrants: false,
        entrants: newEntrants,
      });


    case ActionTypes.UPCOMING_CONTESTS_UPDATE_RECEIVED:
      const stateCopy = _merge({}, state);

      stateCopy.allContests[action.contest.id] = action.contest;
      if (stateCopy.filteredContests.hasOwnProperty(action.contest.id)) {
        stateCopy.filteredContests[action.contest.id] = action.contest;
      }

      return stateCopy;


    default:
      return state;
  }
};
