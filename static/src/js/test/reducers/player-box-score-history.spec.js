import { assert } from 'chai';
import reducer from '../../reducers/player-box-score-history';
import * as types from '../../action-types';


describe('reducers.playerBoxScoreHistory', () => {
  const defaultState = reducer(undefined, {});

  it('should return the initial state', () => {
    assert.deepEqual(defaultState.nfl, {});
    assert.deepEqual(defaultState.mlb, {});
    assert.deepEqual(defaultState.nba, {});
  });

  it('should return state if invalid action type used', () => {
    const newState = reducer(defaultState, { type: 'foo' });
    assert.deepEqual(defaultState, newState);
  });

  it('should return state if no action type used', () => {
    const newState = reducer(defaultState);
    assert.deepEqual(defaultState, newState);
  });

  it('should handle PLAYER_HISTORY_SINGLE__RECEIVE', () => {
    const defaultResponse = {
      type: types.PLAYER_HISTORY_SINGLE__RECEIVE,
      response: {
        id: 2200,
        sport: 'nfl',
        fields: {
          foo: 'bar',
        },
      },
    };
    const newState = reducer(defaultState, defaultResponse);
    assert.deepEqual(
      newState.nfl['2200'],
      defaultResponse.response.fields
    );
  });
});
