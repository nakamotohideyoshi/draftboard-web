import { assert, expect } from 'chai';
import reducer from '../../reducers/events';
import * as types from '../../action-types';


describe('reducers.events', () => {
  it('should return the initial state', () => {
    assert.deepEqual(
      reducer(undefined, {}),
      {
        animationEvents: {},
        gamesQueue: {},
        playerEventDescriptions: {},
        playerHistories: {},
        playersPlaying: [],
      }
    );
  });

  it('should handle EVENT_ADD_GAME_QUEUE', () => {
    assert.deepEqual(
      reducer(undefined, {
        type: types.EVENT_ADD_GAME_QUEUE,
        gameId: '123',
      }),
      {
        animationEvents: {},
        gamesQueue: {
          123: {
            queue: [],
          },
        },
        playerEventDescriptions: {},
        playerHistories: {},
        playersPlaying: [],
      }
    );

    // should not be called if already added, but allow overwriting for now
    assert.deepEqual(
      reducer({
        animationEvents: {},
        gamesQueue: {
          123: {
            queue: [],
          },
        },
        playerEventDescriptions: {},
        playerHistories: {},
        playersPlaying: [],
      }, {
        type: types.EVENT_ADD_GAME_QUEUE,
        gameId: '123',
      }),
      {
        animationEvents: {},
        gamesQueue: {
          123: {
            queue: [],
          },
        },
        playerEventDescriptions: {},
        playerHistories: {},
        playersPlaying: [],
      }
    );
  });

  it('should handle EVENT_GAME_QUEUE_PUSH', () => {
    // should fail if there is no game to add to
    expect(
      // expect needs a function not a result, so wrap in an anonymous func
      () => reducer(undefined, {
        type: types.EVENT_GAME_QUEUE_PUSH,
        gameId: '123',
        event: { foo: 'bar' },
      })
    ).to.throw(Error);

    // should work normally
    assert.deepEqual(
      reducer({
        animationEvents: {},
        gamesQueue: {
          123: {
            queue: [{ foo: 'bar' }],
          },
        },
        playerEventDescriptions: {},
        playerHistories: {},
        playersPlaying: [],
      }, {
        type: types.EVENT_GAME_QUEUE_PUSH,
        gameId: '123',
        event: { bar: 'baz' },
      }),
      {
        animationEvents: {},
        gamesQueue: {
          123: {
            queue: [{ foo: 'bar' }, { bar: 'baz' }],
          },
        },
        playerEventDescriptions: {},
        playerHistories: {},
        playersPlaying: [],
      }
    );
  });
});
