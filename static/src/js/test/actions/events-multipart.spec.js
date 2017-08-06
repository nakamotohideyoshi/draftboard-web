import * as actions from '../../actions/events-multipart';
import * as types from '../../action-types';
import mockStore from '../mock-store-with-middleware';
import reducer from '../../reducers/events-multipart';
import { assert } from 'chai';

const key = '73e40c5f-c690-4936-8853-339ed43dcc76';
const value = { 1: 'foo' };
const players = ['13b40c5f-c690-4936-8853-339ed43dcc70'];

describe('actions.eventsMultipart.storeEventMultipart', () => {
  it('should correctly set a multievent', () => {
    // initial store, state
    const store = mockStore({
      eventsMultipart: reducer(undefined, {}),
    });

    // data coming out
    const expectedActions = [{
      type: 'BATCHING_REDUCER.BATCH',
      meta: { batch: true },
      payload: [
        {
          type: types.EVENT_MULTIPART_SET,
          key,
          value,
        },
      ],
    }];

    store.dispatch(actions.storeEventMultipart(key, value));
    assert.deepEqual(store.getActions(), expectedActions);
  });

  it('should include mergeWatchablePlayers if there are players', () => {
    // initial store, state
    const store = mockStore({
      eventsMultipart: reducer(undefined, {}),
    });

    // data coming out
    const expectedActions = [{
      type: 'BATCHING_REDUCER.BATCH',
      meta: { batch: true },
      payload: [
        {
          type: types.EVENT_MULTIPART_SET,
          key,
          value,
        },
        {
          type: types.EVENT_MULTIPART_MERGE_PLAYERS,
          players,
          eventId: key,
        },
      ],
    }];

    store.dispatch(actions.storeEventMultipart(key, value, players));
    assert.deepEqual(store.getActions(), expectedActions);
  });
});

describe('actions.eventsMultipart.removeEventMultipart', () => {
  it('should correctly remove an existing multievent with players', () => {
    // initial store, state
    const store = mockStore({
      eventsMultipart: {
        events: {
          [key]: [{ 1: 'foo' }],
        },
        watchablePlayers: players,
      },
    });

    // data coming out
    const expectedActions = [{
      type: 'BATCHING_REDUCER.BATCH',
      meta: { batch: true },
      payload: [
        {
          type: types.EVENT_MULTIPART_OMIT_PLAYERS,
          players,
        },
        {
          type: types.EVENT_MULTIPART_DELETE,
          key,
        },
      ],
    }];

    store.dispatch(actions.removeEventMultipart(key, players));
    assert.deepEqual(store.getActions(), expectedActions);
  });

  it('should correctly remove an existing multievent without players', () => {
    // initial store, state
    const store = mockStore({
      eventsMultipart: {
        events: {
          [key]: [{ 1: 'foo' }],
        },
        watchablePlayers: players,
      },
    });

    // data coming out
    const expectedActions = [{
      type: 'BATCHING_REDUCER.BATCH',
      meta: { batch: true },
      payload: [
        {
          type: types.EVENT_MULTIPART_DELETE,
          key,
        },
      ],
    }];

    store.dispatch(actions.removeEventMultipart(key));
    assert.deepEqual(store.getActions(), expectedActions);
  });

  it('should remove nothing if event is not in store', () => {
    // initial store, state
    const store = mockStore({
      eventsMultipart: reducer(undefined, {}),
    });

    // data coming out
    const expectedActions = [{
      type: 'BATCHING_REDUCER.BATCH',
      meta: { batch: true },
      payload: [],
    }];

    store.dispatch(actions.removeEventMultipart(key));
    assert.deepEqual(store.getActions(), expectedActions);
  });
});
