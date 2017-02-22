import { assert } from 'chai';
import reducer from '../../reducers/results';
import * as types from '../../action-types';


describe('reducers.results', () => {
  const defaultState = reducer(undefined, {});

  it('should return state if invalid action type used', () => {
    const newState = reducer(defaultState, { type: 'foo' });
    assert.deepEqual(defaultState, newState);
  });

  it('should return state if no action type used', () => {
    const newState = reducer(defaultState);
    assert.deepEqual(defaultState, newState);
  });

  it('should handle RECEIVE_RESULTS', () => {
    const response = {
      response: {
        when: '2015-6-15',
        response: { foo: 'bar' },
      },
      type: types.RECEIVE_RESULTS,
      expiresAt: 'myDate',
    };

    const newState = reducer(defaultState, response);

    assert.deepEqual(
      newState['2015-6-15'],
      response.response.response  // yuck
    );
  });
});
