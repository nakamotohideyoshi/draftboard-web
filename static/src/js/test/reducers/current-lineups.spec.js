import { assert } from 'chai';
import merge from 'lodash/merge';
import reducer from '../../reducers/current-lineups';
import * as types from '../../action-types';


describe('reducers.current-lineups', () => {
  const defaultState = reducer(undefined, {});

  it('should return the initial state', () => {
    assert.equal(defaultState.isFetching, false);
    assert.equal(defaultState.hasRelatedInfo, false);
    assert.equal(typeof defaultState.expiresAt, 'number');
    assert.equal(typeof defaultState.rostersExpireAt, 'number');
    assert.deepEqual(defaultState.items, {});
  });

  it('should return state if invalid action type used', () => {
    const newState = reducer(defaultState, { type: 'foo' });
    assert.deepEqual(defaultState, newState);
  });

  it('should return state if no action type used', () => {
    const newState = reducer(defaultState);
    assert.deepEqual(defaultState, newState);
  });

  it('should handle SET_CURRENT_LINEUPS', () => {
    const state = reducer(undefined, {
      type: types.SET_CURRENT_LINEUPS,
      lineups: { lineup1: {} },
    });
    assert.deepEqual(
      state.items,
      { lineup1: {} }
    );

    const newState = reducer(state, {
      type: types.SET_CURRENT_LINEUPS,
      lineups: { lineup2: {} },
    });
    assert.deepEqual(
      newState.items,
      { lineup2: {} }
    );
  });

  it('should handle CURRENT_LINEUPS__ADD_PLAYERS', () => {
    // return same state if there is no current lineup to associate players with
    const state = reducer(undefined, {
      type: types.CURRENT_LINEUPS__ADD_PLAYERS,
      lineupsPlayers: { lineup2: ['player1'], lineup5: ['player23'] },
    });
    assert.deepEqual(
      state.items,
      {}
    );

    // if there is a lineup item, then add the roster to it
    const modifiedState = merge({}, defaultState, {
      items: { lineup2: {} },
    });
    const newState = reducer(modifiedState, {
      type: types.CURRENT_LINEUPS__ADD_PLAYERS,
      lineupsPlayers: { lineup2: ['player1'], lineup5: ['player23'] },
    });
    assert.deepEqual(
      newState.items,
      { lineup2: { roster: ['player1'] } }
    );
  });

  it('should handle CURRENT_LINEUPS_ROSTERS__REQUEST', () => {
    const newState = reducer(defaultState, {
      type: types.CURRENT_LINEUPS_ROSTERS__REQUEST,
      expiresAt: 'myDate',
    });
    assert.equal(
      newState.rostersExpireAt,
      'myDate'
    );
  });

  it('should handle CURRENT_LINEUPS_ROSTERS__RECEIVE', () => {
    const defaultResponse = {
      type: types.CURRENT_LINEUPS_ROSTERS__RECEIVE,
      expiresAt: 1466031908348,
      response: {
        lineupsRosters: {
          2: {
            id: 2,
            user: 3,
            name: 'My Lineup 123',
            sport: 'mlb',
            fantasyPoints: 0,
            draftGroup: 4,
            players: [{ playerId: 'player1' }, { playerId: 'player2' }],
          },
          // no players for 3, important
          3: {
            id: 2,
            user: 3,
            name: 'My Lineup 123',
            sport: 'mlb',
            fantasyPoints: 0,
            draftGroup: 4,
          },
        },
      },
    };

    // return nothing if there is no current lineup to associate rosters with
    const state = reducer(undefined, defaultResponse);
    assert.deepEqual(
      state.items,
      {}
    );

    // if there is a lineup item, then add the roster to it
    const modifiedState = merge({}, defaultState, {
      items: {
        2: { id: 2 },  // matches the defaultResponse lineups
        3: { id: 3 },  // no players in defaultResponse lineup
        4: { id: 4 },  // no match in defaultResponse lineups
      },
    });
    const newState = reducer(modifiedState, defaultResponse);
    assert.deepEqual(
      newState.items[2].roster,
      ['player1', 'player2']
    );
    assert.equal(
      newState.items[3].roster,
      undefined
    );
    assert.equal(
      newState.items[4].roster,
      undefined
    );

    // check that expiration was updated
    assert.notEqual(
      modifiedState.rostersExpireAt,
      newState.rostersExpireAt
    );
  });

  it('should handle CURRENT_LINEUPS__RELATED_INFO_SUCCESS', () => {
    const newState = reducer(defaultState, {
      type: types.CURRENT_LINEUPS__RELATED_INFO_SUCCESS,
    });
    assert.deepEqual(
      newState.hasRelatedInfo,
      true
    );
  });

  it('should handle CURRENT_LINEUPS__REQUEST', () => {
    const newState = reducer(defaultState, {
      type: types.CURRENT_LINEUPS__REQUEST,
      expiresAt: 'myDate',
    });
    assert.equal(
      newState.expiresAt,
      'myDate'
    );
    assert.equal(
      newState.isFetching,
      true
    );
  });

  it('should handle CURRENT_LINEUPS__RECEIVE', () => {
    const defaultResponse = {
      type: types.CURRENT_LINEUPS__RECEIVE,
      expiresAt: 1466031908348,
      response: {
        lineups: {
          2: {
            id: 2,
            contests: [3, 4],
            name: 'My Lineup',
            sport: 'mlb',
            draftGroup: 3,
            start: '2016-06-15T23:05:00Z',
          },
        },
      },
    };

    // return nothing if there is no current lineup to associate rosters with
    const state = reducer(undefined, defaultResponse);
    assert.deepEqual(
      state.items[2],
      defaultResponse.response.lineups[2]
    );
    assert.equal(
      state.isFetching,
      false
    );

    // return nothing if there is no current lineup to associate rosters with
    const noLineupsState = reducer(undefined, {
      type: types.CURRENT_LINEUPS__RECEIVE,
      expiresAt: 1466031908348,
      response: {
        lineups: undefined,
      },
    });
    assert.deepEqual(
      noLineupsState.items,
      {}
    );

    // if there is a lineup item, then add the roster to it
    const modifiedState = merge({}, defaultState, {
      items: { 2: { id: 2, contests: [1] } },
    });
    const newState = reducer(modifiedState, defaultResponse);
    assert.deepEqual(
      newState.items[2].contests,
      [3, 4]
    );
    // check that expiration was updated
    assert.notEqual(
      modifiedState.expiresAt,
      newState.expiresAt
    );
  });
});
