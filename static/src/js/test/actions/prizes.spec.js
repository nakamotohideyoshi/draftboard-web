import assert from 'assert';
import mockStore from '../mock-store-with-middleware';
import nock from 'nock';

import { dateNow } from '../../lib/utils';
import * as ActionTypes from '../../action-types';
import * as actions from '../../actions/prizes';
import reducer from '../../reducers/prizes';


describe('actions.prizes', () => {
  before(() => {
    nock.disableNetConnect();
  });

  after(() => {
    nock.enableNetConnect();
  });

  beforeEach(() => {
    nock('http://localhost')
      .get('/api/prize/1/')
      .reply(200, { body: {
        pk: 1,
        name: '$100 H2H',
        prize_pool: 180,
        payout_spots: 1,
        buyin: 100,
        ranks: [
          {
            rank: 1,
            value: 180,
            category: 'cash',
          },
        ],
      } });
  });

  afterEach(() => {
    nock.cleanAll();
  });

  it('should correctly fetch prize if no prize exists', () => {
    // initial store, state
    const store = mockStore({
      prizes: reducer(undefined, {}),
    });

    // data coming out
    const expectedActions = [{
      payload: [
        {
          type: ActionTypes.RECEIVE_PRIZE,
        },
      ],
      type: ActionTypes.RECEIVE_PRIZE,
    }];

    store.dispatch(actions.fetchPrizeIfNeeded(1))
      .then(() => {
        assert.deepEqual(store.getActions(), expectedActions);
      });
  });

  it('should fetch prize if expired', () => {
    // initial store, state
    const store = mockStore({
      prizes: {
        1: {
          info: {},
          expiresAt: dateNow() - 1000 * 60,  // 1 minute ago, definitely in the past
        },
      },
    });

    // data coming out
    const expectedActions = [{
      payload: [
        {
          type: ActionTypes.RECEIVE_PRIZE,
        },
      ],
      type: ActionTypes.RECEIVE_PRIZE,
    }];

    store.dispatch(actions.fetchPrizeIfNeeded(1))
      .then(() => {
        assert.deepEqual(store.getActions(), expectedActions);
      });
  });

  it('should not fetch prize otherwise', () => {
    // initial store, state
    const store = mockStore({
      prizes: {
        1: {
          info: {},
          expiresAt: dateNow() + 1000 * 60,  // 1 minute in future
        },
      },
    });

    store.dispatch(actions.fetchPrizeIfNeeded(1))
      .then((reason) => {
        assert.equal(reason, 'Prize already exists');
      });
  });
});
