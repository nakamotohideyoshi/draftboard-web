import merge from 'lodash/merge';
import mergeWith from 'lodash/mergeWith';
import isArray from 'lodash/isArray';
import intersection from 'lodash/intersection';
import map from 'lodash/map';
import uniq from 'lodash/uniq';
const actionTypes = require('../action-types');
import Cookies from 'js-cookie';

// If the user has a previously stored skill level selection in their browser
// cookies, default to that. It gets set on UPCOMING_CONTESTS_FILTER_CHANGED.
const savedSkillLevel = Cookies.get('skillLevel') || 'rookie';

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
    contestSearchFilter: {},
    sportFilter: {
      match: '',
      filterProperty: 'sport',
    },
    // Default to Rookie.
    // TODO: Store a cookie to default to the one the user last chose.
    skillLevelFilter: {
      match: [savedSkillLevel, 'all'],
      filterProperty: 'skill_level.name',
    },
  },
};


module.exports = (state = initialState, action = {}) => {
  let newState;

  switch (action.type) {

    case actionTypes.FETCH_CONTEST_POOLS: {
      return merge({}, state, {
        isFetchingContestPools: true,
      });
    }


    case actionTypes.FETCH_CONTEST_POOLS_SUCCESS: {
      let activeSport = state.filters.sportFilter.match;

      if (state.filters.sportFilter.match === '') {
        activeSport = findPreselectedSport(action.response, preselectedSportFilterOrder);
      }
      // Return a copy of the previous state with our new things added to it.
      return merge({}, state, {
        allContests: action.response,
        filteredContests: action.response,
        isFetchingContestPools: false,
        filters: {
          sportFilter: {
            match: activeSport,
          },
        },
      });
    }


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

        // If the skill level filter was changed, save it as a cookie for
        // retrieval when the user comes back to the page.
        if (action.filter.filterName === 'skillLevelFilter') {
          Cookies.set('skillLevel', action.filter.match[0]);
        }

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
      newEntrants[action.response.contestId] = action.response.entrants;
      // we use mergeWith cause of merge don't replace array by array
      return mergeWith({}, state, {
        isFetchingEntrants: false,
        entrants: newEntrants,
      }, (object, key) => {
        if (isArray(key)) {
          return key;
        }
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


    case actionTypes.LINEUP_FOCUSED: {
      // When a lineup is focused, select that sport.
      // This is used when a lineup is saved and the user is redirected back to the lobby page.
      if (action.sport) {
        const stateCopy = merge({}, state);
        stateCopy.filters.sportFilter.match = action.sport;
        return stateCopy;
      }
      return state;
    }


    default:
      return state;
  }
};
