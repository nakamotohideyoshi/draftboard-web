import * as actions from '../../actions/events';
import * as types from '../../action-types';
import mockStore from '../mock-store-with-middleware';
import reducer from '../../reducers/events';
import { assert } from 'chai';

const gameId = '73e40c5f-c690-4936-8853-339ed43dcc76';
const event = { 1: 'foo' };

describe('actions.events.storeEvent', () => {
  it('should correctly save a new event', () => {
    // initial store, state
    const store = mockStore({
      events: reducer(undefined, {}),
    });

    // data coming out
    const expectedActions = [{
      type: 'BATCHING_REDUCER.BATCH',
      payload: [
        {
          gameId,
          type: types.EVENT_ADD_GAME_QUEUE,
        },
        {
          type: types.EVENT_GAME_QUEUE_PUSH,
          gameId,
          event,
        },
      ],
    }];

    store.dispatch(actions.storeEvent(gameId, event));
    assert.deepEqual(store.getActions(), expectedActions);
  });

  it('should correctly add an event to existing game queue', () => {
    // initial store, state
    const store = mockStore({
      events: {
        gamesQueue: {
          [gameId]: [{}],
        },
      },
    });

    // data coming out
    const expectedActions = [{
      type: 'BATCHING_REDUCER.BATCH',
      payload: [
        {
          type: types.EVENT_GAME_QUEUE_PUSH,
          gameId,
          event,
        },
      ],
    }];

    store.dispatch(actions.storeEvent(gameId, event));
    assert.deepEqual(store.getActions(), expectedActions);
  });
});
