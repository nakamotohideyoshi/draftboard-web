import { assert } from 'chai';
import merge from 'lodash/merge';
import reducer from '../../reducers/live-players';
import * as types from '../../action-types';


describe('reducers.live-players', () => {
  const defaultState = reducer(undefined, {});

  it('should return the initial state', () => {
    assert.deepEqual(defaultState.relevantPlayers, {});
    assert.deepEqual(defaultState.fetched, []);
    assert.deepEqual(defaultState.expiresAt, {});
  });

  it('should return state if invalid action type used', () => {
    const newState = reducer(defaultState, { type: 'foo' });
    assert.deepEqual(defaultState, newState);
  });

  it('should return state if no action type used', () => {
    const newState = reducer(defaultState);
    assert.deepEqual(defaultState, newState);
  });

  it('should handle REQUEST_LIVE_PLAYERS_STATS', () => {
    const newState = reducer(defaultState, {
      lineupId: 2,
      type: types.REQUEST_LIVE_PLAYERS_STATS,
      expiresAt: 'myDate',
    });
    assert.equal(
      newState.expiresAt[2],
      'myDate'
    );
  });

  it('should handle UPDATE_LIVE_PLAYER_STATS', () => {
    const newStats = {
      type: types.UPDATE_LIVE_PLAYER_STATS,
      playerSRID: 'myPlayerId',
      fields: { foo: 'bar' },
    };

    const newState = reducer({
      relevantPlayers: {
        myPlayerId: {
          bar: 'baz',
        },
      },
    },
    newStats);

    // make sure fields are overwritten w new
    assert.deepEqual(
      newState.relevantPlayers.myPlayerId,
      { foo: 'bar' }
    );
  });

  it('should handle RECEIVE_LIVE_PLAYERS_STATS', () => {
    const defaultResponse = {
      type: types.RECEIVE_LIVE_PLAYERS_STATS,
      expiresAt: 1466031908348,
      response: {
        lineupId: 324,
        players: {
          '9760f1d6-9560-45ed-bc73-5ec2205905a2': {
            lineupId: 324,
            sport: 'mlb',
            id: 1054,
          },
          '3da24e28-741c-4978-bdba-52de51975820': {
            lineupId: 324,
            sport: 'mlb',
            id: 920,
          },
          '36d8674c-0ff2-468a-b284-6dc338c6a13a': {
            lineupId: 324,
            sport: 'mlb',
            id: 1512,
          },
          '029ba09e-9965-4497-b141-5bd8dedbad6a': {
            lineupId: 324,
            sport: 'mlb',
            id: 927,
          },
          '267c9cd7-a2e2-4f88-8b9b-b7389b1a9ccd': {
            lineupId: 324,
            sport: 'mlb',
            id: 925,
          },
          '8540822b-75bd-424d-ba88-5e60c80b6c30': {
            lineupId: 324,
            sport: 'mlb',
            id: 114,
          },
          '78bbb2e3-487a-4f14-ad95-22dfae998a98': {
            lineupId: 324,
            sport: 'mlb',
            id: 933,
          },
          '7335e54f-cc2f-422c-808e-c19a267827a5': {
            lineupId: 324,
            sport: 'mlb',
            id: 935,
          },
          '5a82d6e0-6981-4eab-85ed-c4bc55b951ca': {
            lineupId: 324,
            sport: 'mlb',
            id: 123,
          },
        },
      },
    };

    // return new players, lineup to fetched list
    const state = reducer(undefined, defaultResponse);
    assert.deepEqual(
      state.relevantPlayers,
      defaultResponse.response.players
    );
    assert.deepEqual(
      state.fetched[0],
      defaultResponse.response.lineupId
    );

    // if there is a lineup item, then add the roster to it
    const modifiedState = merge({}, defaultState, {
      relevantPlayers: {
        // matches defaultResponse player
        '9760f1d6-9560-45ed-bc73-5ec2205905a2': { sport: 'nfl' },
      },
      // make sure that expires at gets merged
      expiresAt: {
        324: 'oldDate',
      },
    });
    const newState = reducer(modifiedState, defaultResponse);
    assert.deepEqual(
      state.relevantPlayers,
      defaultResponse.response.players
    );

    // check that expiration was updated
    assert.notEqual(
      'oldDate',
      newState.expiresAt[324]
    );
  });
});
