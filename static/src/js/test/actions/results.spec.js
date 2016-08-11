import assert from 'assert';
import mockStore from '../mock-store-with-middleware';
import nock from 'nock';

import * as ActionTypes from '../../action-types';
import * as actions from '../../actions/results';
import reducer from '../../reducers/results';


describe('actions.results', () => {
  before(() => {
    nock.disableNetConnect();
  });

  after(() => {
    nock.enableNetConnect();
  });

  afterEach(() => {
    nock.cleanAll();
  });

  it('should not fetch if the result already exists', () => {
    // initial store, state
    const store = mockStore({
      results: reducer({
        '2016-6-15': {},
      }, {}),
    });

    store.dispatch(actions.fetchResultsIfNeeded('2016-6-15'));
    assert.equal(store.getActions(), '');
  });

  it('should correctly fetch results for a day', () => {
    // initial store, state
    const store = mockStore({
      results: reducer(undefined, {}),
    });

    nock('http://localhost')
      .get('/api/contest/play-history/2016/06/15/')
      .reply(200, { body: {
        lineups: [
          {
            id: 319,
            players: [
              {
                player_id: 918,
                full_name: 'Tyler Wilson',
                roster_spot: 'SP',
                idx: 0,
                player_meta: {
                  first_name: 'Tyler',
                  last_name: 'Wilson',
                  status: 'A',
                  srid: '1d7c554a-84a7-4796-9bcd-9162e961a01a',
                  team: {
                    id: 3,
                    alias: 'BAL',
                    market: 'Baltimore',
                    name: 'Orioles',
                  },
                },
                fppg: 16.3333333333333,
                salary: 6100,
                fantasy_points: 0,
              },
            ],
            entries: [
              {
                id: 1191,
                final_rank: -1,
                contest: null,
                payout: null,
              },
            ],
            name: '',
            sport: 'mlb',
          },
        ],
        overall: {
          buyins: '711.00',
          entries: 28,
          possible: '1693.40',
          contests: 28,
          winnings: '534.40',
        },
      } });

    // data coming out
    const expectedActions = [{
      payload: [
        {
          type: ActionTypes.RECEIVE_RESULTS,
        },
      ],
      type: ActionTypes.RECEIVE_RESULTS,
    }];

    store.dispatch(actions.fetchResultsIfNeeded('2016-06-15'))
      .then(() => {
        assert.deepEqual(store.getActions(), expectedActions);
      });
  });
});
