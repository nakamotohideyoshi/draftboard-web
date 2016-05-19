import { assert, expect } from 'chai';
import reducer from '../../reducers/events-multipart';
import * as types from '../../action-types';


describe('reducers.eventsMultipart', () => {
  it('should return the initial state', () => {
    assert.deepEqual(
      reducer(undefined, {}),
      {
        events: {},
        watchablePlayers: {},
      }
    );
  });

  it('should handle EVENT_MULTIPART_SET', () => {
    assert.deepEqual(
      reducer(undefined, {
        type: types.EVENT_MULTIPART_SET,
        key: '123',
        value: { foo: 'bar' },
      }),
      {
        events: {
          123: { foo: 'bar' },
        },
        watchablePlayers: {},
      }
    );

    assert.deepEqual(
      reducer({
        events: {
          123: { foo: 'bar' },
        },
        watchablePlayers: {},
      }, {
        type: types.EVENT_MULTIPART_SET,
        key: '123',
        value: { bar: 'baz' },
      }),
      {
        events: {
          123: { bar: 'baz' },
        },
        watchablePlayers: {},
      }
    );
  });

  it('should handle EVENT_MULTIPART_DELETE', () => {
    // should fail if there is no event to add to
    expect(
      // expect needs a function not a result, so wrap in an anonymous func
      () => reducer(undefined, {
        type: types.EVENT_MULTIPART_DELETE,
        key: '456',
      })
    ).to.throw(Error);

    // should work normally
    assert.deepEqual(
      reducer({
        events: {
          123: { foo: 'bar' },
        },
      }, {
        type: types.EVENT_MULTIPART_DELETE,
        key: '123',
      }),
      {
        events: {},
      }
    );
  });

  it('should handle EVENT_MULTIPART_OMIT_PLAYERS', () => {
    // should return no players if they don't exist
    assert.deepEqual(
      reducer(undefined, {
        type: types.EVENT_MULTIPART_OMIT_PLAYERS,
        players: ['foo', 'bar'],
      }),
      {
        events: {},
        watchablePlayers: {},
      }
    );

    // should work normally
    assert.deepEqual(
      reducer({
        events: {},
        watchablePlayers: {
          foo: 'baz',
          bar: 'qux',
        },
      }, {
        type: types.EVENT_MULTIPART_OMIT_PLAYERS,
        players: ['bar'],
      }),
      {
        events: {},
        watchablePlayers: { foo: 'baz' },
      }
    );
  });

  it('should handle EVENT_MULTIPART_MERGE_PLAYERS', () => {
    // should work normally
    assert.deepEqual(
      reducer({
        events: {},
        watchablePlayers: {
          foo: 'baz',
        },
      }, {
        type: types.EVENT_MULTIPART_MERGE_PLAYERS,
        eventId: 'qux',
        players: ['bar', 'baz'],
      }),
      {
        events: {},
        watchablePlayers: {
          foo: 'baz',
          bar: 'qux',
          baz: 'qux',
        },
      }
    );

    // overrides what existed
    assert.deepEqual(
      reducer({
        events: {},
        watchablePlayers: {
          foo: 'baz',
          bar: 'baz',
        },
      }, {
        type: types.EVENT_MULTIPART_MERGE_PLAYERS,
        eventId: 'qux',
        players: ['bar'],
      }),
      {
        events: {},
        watchablePlayers: {
          foo: 'baz',
          bar: 'qux',
        },
      }
    );
  });
});
