import { assert } from 'chai';
import merge from 'lodash/merge';
import reducer from '../../reducers/events';
import * as types from '../../action-types';


describe('reducers.events', () => {
  const defaultState = reducer(undefined, {});

  it('should return the initial state', () => {
    assert.deepEqual(defaultState, {
      currentEvent: null,
      bigEvents: [],
      queue: [],
      playerEventDescriptions: {},
      playerHistories: {},
      playersPlaying: [],
      showEventResult: false,
    });
  });

  it('should return state if invalid action type used', () => {
    const newState = reducer(defaultState, { type: 'foo' });
    assert.deepEqual(defaultState, newState);
  });

  it('should return state if no action type used', () => {
    const newState = reducer(defaultState);
    assert.deepEqual(defaultState, newState);
  });


  it('should handle EVENT__SET_CURRENT', () => {
    let newState = reducer(defaultState, {
      type: types.EVENT__SET_CURRENT,
      value: { foo: 'bar' },
    });
    assert.deepEqual(
      newState.currentEvent,
      { foo: 'bar' }
    );

    // should replace existing animation event
    newState = merge({}, defaultState, {
      currentEvent: { oldKey: 'oldValue' },
    });
    newState = reducer(newState, {
      type: types.EVENT__SET_CURRENT,
      value: { foo: 'bar' },
    });
    assert.deepEqual(
      newState.currentEvent,
      { foo: 'bar' }
    );
  });

  it('should handle EVENT_ADD_TO_BIG_QUEUE', () => {
    // should work normally
    assert.deepEqual(
      reducer({
        currentEvent: null,
        bigEvents: [{ foo: 'bar' }],
        queue: [],
        playerEventDescriptions: {},
        playerHistories: {},
        playersPlaying: [],
        showEventResult: false,
      }, {
        type: types.EVENT_ADD_TO_BIG_QUEUE,
        value: { bar: 'baz' },
      }),
      {
        currentEvent: null,
        bigEvents: [{ foo: 'bar' }, { bar: 'baz' }],
        queue: [],
        playerEventDescriptions: {},
        playerHistories: {},
        playersPlaying: [],
        showEventResult: false,
      }
    );

    const bigEvents = [];
    for (let i = 1; i <= 50; i++) {
      bigEvents.push(i);
    }

    const initialState = reducer({
      currentEvent: null,
      bigEvents,
      queue: [],
      playerEventDescriptions: {},
      playerHistories: {},
      playersPlaying: [],
      showEventResult: false,
    }, {
      type: types.EVENT_ADD_TO_BIG_QUEUE,
      value: 51,
    });

    assert.equal(50, initialState.bigEvents.length);
  });

  it('should handle EVENT_GAME_QUEUE_PUSH', () => {
    // should work normally
    assert.deepEqual(
      reducer({
        currentEvent: null,
        queue: [{ foo: 'bar' }],
        playerEventDescriptions: {},
        playerHistories: {},
        playersPlaying: [],
        showEventResult: false,
      }, {
        type: types.EVENT_GAME_QUEUE_PUSH,
        gameId: '123',
        event: { bar: 'baz' },
      }),
      {
        currentEvent: null,
        queue: [{ foo: 'bar' }, { bar: 'baz' }],
        playerEventDescriptions: {},
        playerHistories: {},
        playersPlaying: [],
        showEventResult: false,
      }
    );
  });


  it('should handle EVENT_PLAYER_ADD_DESCRIPTION', () => {
    let newState = reducer(defaultState, {
      type: types.EVENT_PLAYER_ADD_DESCRIPTION,
      key: 'myKey',
      value: { foo: 'bar' },
    });
    assert.deepEqual(
      newState.playerEventDescriptions.myKey,
      { foo: 'bar' }
    );

    // should replace existing animation event
    newState = merge({}, defaultState, {
      playerEventDescriptions: {
        myKey: { oldKey: 'oldValue' },
      },
    });
    newState = reducer(newState, {
      type: types.EVENT_PLAYER_ADD_DESCRIPTION,
      key: 'myKey',
      value: { foo: 'bar' },
    });
    assert.deepEqual(
      newState.playerEventDescriptions.myKey,
      { foo: 'bar' }
    );
  });


  it('should handle EVENT_REMOVE_PLAYERS_PLAYING', () => {
    // should return no players when none exist
    let state = reducer(defaultState, {
      type: types.EVENT_REMOVE_PLAYERS_PLAYING,
      players: ['player1', 'player2'],
    });
    assert.deepEqual(state.playersPlaying, []);

    // should diff when they exist
    state = merge({}, defaultState, {
      playersPlaying: ['player1', 'player3'],
    });
    state = reducer(state, {
      type: types.EVENT_REMOVE_PLAYERS_PLAYING,
      players: ['player1', 'player2'],
    });
    assert.deepEqual(state.playersPlaying, []);
  });


  it('should handle EVENT_PLAYER_REMOVE_DESCRIPTION', () => {
    // don't bother deleting if nothing is there
    let newState = reducer(defaultState, {
      type: types.EVENT_PLAYER_REMOVE_DESCRIPTION,
      key: 'myKey',
    });
    assert.deepEqual(newState.playerEventDescriptions, {});

    // should delete existing description
    newState = merge({}, defaultState, {
      playerEventDescriptions: {
        myKey: { oldKey: 'oldValue' },
      },
    });
    newState = reducer(newState, {
      type: types.EVENT_PLAYER_REMOVE_DESCRIPTION,
      key: 'myKey',
    });
    assert.deepEqual(newState.playerEventDescriptions, {});
  });


  it('should handle EVENT_SHIFT_GAME_QUEUE', () => {
    // don't bother if nothing in the queue
    let newState = reducer(defaultState, {
      type: types.EVENT_SHIFT_GAME_QUEUE,
    });
    assert.deepEqual(newState.queue, []);

    // should shift if exists
    newState = merge({}, defaultState, {
      queue: ['history1', 'history2'],
    });
    newState = reducer(newState, {
      type: types.EVENT_SHIFT_GAME_QUEUE,
    });
    assert.deepEqual(newState.queue, ['history2']);
  });


  it('should handle EVENT_UNION_PLAYERS_PLAYING', () => {
    let state = reducer(defaultState, {
      type: types.EVENT_UNION_PLAYERS_PLAYING,
      players: ['player1'],
    });
    assert.deepEqual(state.playersPlaying, ['player1']);

    state = merge({}, defaultState, {
      playersPlaying: ['player1', 'player2'],
    });
    state = reducer(state, {
      type: types.EVENT_UNION_PLAYERS_PLAYING,
      players: ['player1'],
    });
    assert.deepEqual(state.playersPlaying, ['player1', 'player2']);
  });


  it('should handle EVENT_UNSHIFT_PLAYER_HISTORY', () => {
    // should create history array if doesn't exist
    let newState = reducer(defaultState, {
      type: types.EVENT_UNSHIFT_PLAYER_HISTORY,
      key: 'myKey',
      value: 'myHistoryValue1',
    });
    assert.equal(
      newState.playerHistories.myKey[0],
      'myHistoryValue1'
    );

    // should unshift
    newState = merge({}, defaultState, {
      playerHistories: {
        myKey: 'myHistoryValue1',
      },
    });
    newState = reducer(newState, {
      type: types.EVENT_UNSHIFT_PLAYER_HISTORY,
      key: 'myKey',
      value: 'myHistoryValue2',
    });
    assert.equal(
      newState.playerHistories.myKey[0],
      'myHistoryValue2'
    );
  });
});
