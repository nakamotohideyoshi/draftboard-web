import { assert } from 'chai';
import reducer from '../../reducers/contest-pools.js';
import * as actionTypes from '../../action-types';
import contestPools from '../../fixtures/json/contest-pools.js';
// This is an example of a data payload from a pusher contest_pool.upate event.
import contestPoolUpdate from
  '../../fixtures/json/pusher-event-data/contest-pool-update.js';
import Cookies from 'js-cookie';


describe('reducers.contest-pools', () => {
  const defaultState = reducer(undefined, {});


  it('should return the initial state', () => {
    assert.equal(defaultState.isFetchingEntrants, false);
    assert.equal(defaultState.isFetchingContestPools, false);
    assert.typeOf(defaultState.filters.orderBy, 'object');
    assert.typeOf(defaultState.filters.sportFilter, 'object');
    assert.typeOf(defaultState.filters.skillLevelFilter, 'object');
    assert.equal(defaultState.filters.skillLevelFilter.filterProperty, 'skill_level.name');
    assert.deepEqual(defaultState.allContests, {});
    assert.deepEqual(defaultState.filteredContests, {});
    assert.deepEqual(defaultState.entrants, {});
  });


  it('should return state if invalid action type used', () => {
    const newState = reducer(defaultState, { type: 'nonexistent' });
    assert.deepEqual(defaultState, newState);
  });


  it('should return state if no action type used', () => {
    const newState = reducer(defaultState);
    assert.deepEqual(defaultState, newState);
  });


  it('should handle FETCH_CONTEST_POOLS', () => {
    const state = reducer(defaultState, {
      type: actionTypes.FETCH_CONTEST_POOLS,
    });

    assert.equal(
      state.isFetchingContestPools,
      true
    );
  });


  it('should handle FETCH_CONTEST_POOLS_SUCCESS', () => {
    const state = reducer(defaultState, {
      type: actionTypes.FETCH_CONTEST_POOLS_SUCCESS,
      response: contestPools,
    });

    assert.deepEqual(state.allContests, contestPools);
    assert.deepEqual(state.allContests, contestPools);
    assert.equal(state.isFetchingContestPools, false);
  });


  it('should handle FETCH_CONTEST_POOLS_FAIL', () => {
    const state = reducer(defaultState, {
      type: actionTypes.FETCH_CONTEST_POOLS_FAIL,
    });

    assert.equal(
      state.isFetchingContestPools,
      false
    );
  });


  it('should handle UPCOMING_CONTESTS_FILTER_CHANGED', () => {
    const filterInfo = {
      filterName: 'MyFilterName',
      filterProperty: 'MyFilterProperty',
      match: 'match',
    };

    const state = reducer(defaultState, {
      type: actionTypes.UPCOMING_CONTESTS_FILTER_CHANGED,
      filter: filterInfo,
    });

    assert.deepEqual(
      state.filters[filterInfo.filterName],
      {
        filterProperty: filterInfo.filterProperty,
        match: filterInfo.match,
      }
    );
  });


  it('should set a cookie when the skillLevel filter changes', () => {
    const filterInfo = {
      filterName: 'skillLevelFilter',
      filterProperty: 'skill_level.name',
      match: ['veteran', 'all'],
    };

    assert.deepEqual(
      defaultState.filters.skillLevelFilter.match,
      ['rookie', 'all'],
      'Initial skill level is not set to rookie.'
    );

    assert.isUndefined(
      Cookies.get('skillLevel'),
      'skillLevel cookie has been set before test started.'
    );

    const state = reducer(defaultState, {
      type: actionTypes.UPCOMING_CONTESTS_FILTER_CHANGED,
      filter: filterInfo,
    });

    assert.deepEqual(
      state.filters.skillLevelFilter.match,
      ['veteran', 'all'],
      'filter not being set to veteran'
    );

    assert.equal(
      Cookies.get('skillLevel'),
      'veteran',
      'skillLevel cookie is not being set.'
    );
  });


  it('should handle SET_FOCUSED_CONTEST', () => {
    const state = reducer(defaultState, {
      type: actionTypes.SET_FOCUSED_CONTEST,
      contestId: 1337,
    });

    assert.equal(state.focusedContestId, 1337);
  });


  it('should handle UPCOMING_CONTESTS_ORDER_CHANGED', () => {
    const state = reducer(defaultState, {
      type: actionTypes.UPCOMING_CONTESTS_ORDER_CHANGED,
      orderBy: 'myProp',
    });

    assert.equal(state.filters.orderBy, 'myProp');
  });


  it('should handle FETCHING_CONTEST_ENTRANTS', () => {
    const state = reducer(defaultState, {
      type: actionTypes.FETCHING_CONTEST_ENTRANTS,
    });

    assert.equal(state.isFetchingEntrants, true);
  });


  it('should handle FETCH_CONTEST_ENTRANTS_FAIL', () => {
    const state = reducer(defaultState, {
      type: actionTypes.FETCH_CONTEST_ENTRANTS_FAIL,
    });

    assert.equal(state.isFetchingEntrants, false);
  });


  it('should handle UPCOMING_CONTESTS_UPDATE_RECEIVED', () => {
    const state = reducer(defaultState, {
      type: actionTypes.UPCOMING_CONTESTS_UPDATE_RECEIVED,
      contest: contestPoolUpdate,
    });

    assert.equal(state.allContests[contestPoolUpdate.id], contestPoolUpdate);
  });


  it('should handle LINEUP_FOCUSED', () => {
    const state = reducer(defaultState, {
      type: actionTypes.LINEUP_FOCUSED,
      sport: 'sport_acronym',
    });

    assert.equal(
      state.filters.sportFilter.match,
      'sport_acronym',
      'Focusing a lineup does not select that sport in the sport filter.'
    );
  });
});
