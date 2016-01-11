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
      direction: 'desc'
    },
    contestTypeFilter: {},
    contestFeeFilter: {
      match: {minVal: 0, maxVal: null}
    },
    contestSearchFilter: {},
    sportFilter: {}
  }
}

module.exports = function(state = initialState, action) {
  switch (action.type) {

    case ActionTypes.FETCH_UPCOMING_CONTESTS_SUCCESS:
      // Return a copy of the previous state with our new things added to it.
      return Object.assign({}, state, {
        allContests: action.body.contests,
        filteredContests: action.body.contests
      });


    case ActionTypes.UPCOMING_CONTESTS_FILTER_CHANGED:
      let newFilter = {};

      newFilter[action.filter.filterName] = {
        filterProperty: action.filter.filterProperty,
        match: action.filter.match
      }

      return Object.assign({}, state, {
        filters: Object.assign({}, state.filters, newFilter)
      });


    case ActionTypes.SET_FOCUSED_CONTEST:
      return Object.assign({}, state, {
        focusedContestId: action.contestId
      });


    case ActionTypes.UPCOMING_CONTESTS_ORDER_CHANGED:
      let newState = Object.assign({}, state)
      newState.filters.orderBy = action.orderBy
      return newState


    case ActionTypes.FETCHING_CONTEST_ENTRANTS:
      return Object.assign({}, state, {
        isFetchingEntrants: true
      })


    case ActionTypes.FETCH_CONTEST_ENTRANTS_FAIL:
      return Object.assign({}, state, {
        isFetchingEntrants: false
      })


    case ActionTypes.FETCH_CONTEST_ENTRANTS_SUCCESS:
      let newEntrants = Object.assign({}, state.entrants)
      newEntrants[action.contestId] = action.entrants

      return Object.assign({}, state, {
        isFetchingEntrants: false,
        entrants: newEntrants
      })


    default:
      return state;
  }
};
