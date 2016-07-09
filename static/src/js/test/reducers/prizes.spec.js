import { assert } from 'chai';
import merge from 'lodash/merge';
import reducer from '../../reducers/prizes';
import * as types from '../../action-types';


describe('reducers.prizes', () => {
  const defaultState = reducer(undefined, {});

  it('should return the initial state', () => {
    assert.deepEqual(defaultState, {});
  });

  it('should return state if invalid action type used', () => {
    const newState = reducer(defaultState, { type: 'foo' });
    assert.deepEqual(defaultState, newState);
  });

  it('should return state if no action type used', () => {
    const newState = reducer(defaultState);
    assert.deepEqual(defaultState, newState);
  });

  it('should handle REQUEST_PRIZE', () => {
    let newState = reducer(defaultState, {
      type: types.REQUEST_PRIZE,
      expiresAt: 'myDate',
      id: 1,
    });
    assert.equal(
      newState[1].expiresAt,
      'myDate'
    );

    // make sure that we aren't overwriting the state
    newState = reducer(newState, {
      type: types.REQUEST_PRIZE,
      expiresAt: 'myDate',
      id: 2,
    });
    assert.equal(Object.keys(newState).length, 2);
  });

  it('should handle RECEIVE_PRIZE', () => {
    const defaultResponse = {
      type: types.RECEIVE_PRIZE,
      expiresAt: 1466031908348,
      response: {
        id: 1,
        info: {
          pk: 1,
          name: '$1 H2H',
          prize_pool: 1.8,
          payout_spots: 1,
          buyin: 1,
          ranks: [
            {
              rank: 1,
              value: 1.8,
              category: 'cash',
            },
          ],
        },
      },
    };

    const stateWithRequest = reducer(defaultState, {
      type: types.REQUEST_PRIZE,
      expiresAt: 'myDate',
      id: 1,
    });


    // check that the prize was added
    const state = reducer(stateWithRequest, defaultResponse);
    assert.deepEqual(
      state[1].info,
      defaultResponse.response.info
    );
    // check that expiration was updated
    assert.notEqual(
      stateWithRequest[1].expiresAt,
      state[1].expiresAt
    );

    // check that updating prize overwrites it
    const modifiedState = merge({}, defaultState, {
      1: {
        info: { name: 'Old Name' },
      },
    });
    const overwrittenState = reducer(modifiedState, defaultResponse);
    assert.notEqual(
      modifiedState[1].info.name,
      overwrittenState[1].info.name
    );
  });
});
