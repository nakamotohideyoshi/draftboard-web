import assert from 'assert';
import mockStore from '../mock-store-with-middleware';
import nock from 'nock';

import * as ActionTypes from '../../action-types';
import * as actions from '../../actions/entries';
import reducer from '../../reducers/entries';


describe('actions.entries', () => {
  afterEach(() => {
    nock.cleanAll();
  });

  it('should correctly fetch current entries', () => {
    // initial store, state
    const store = mockStore({
      entries: reducer(undefined, {}),
    });

    nock('http://example.com/')
      .get('/api/contest/contest-pools/current-entries/')
      .reply(200, { body: [
        {
          id: 1,
          contest_pool: 2,
          contest: 3,
          lineup: 4,
          draft_group: 5,
          start: '2016-05-11T23:05:00Z',
          lineup_name: 'Foo',
          sport: 'mlb',
        },
      ] });

    // data coming out
    const expectedActions = [{
      payload: [
        {
          type: ActionTypes.ENTRIES__RECEIVE,
        },
      ],
      type: ActionTypes.ENTRIES__RECEIVE,
    }];

    store.dispatch(actions.fetchCurrentEntries())
      .then(() => {
        assert.deepEqual(store.getActions(), expectedActions);
      });
  });

  it('should correctly fetch entries rosters', () => {
    // initial store, state
    const store = mockStore({
      entries: reducer(undefined, {}),
    });

    nock('http://example.com/')
      .get('/api/lineup/upcoming/')
      .reply(200, { body: [
        {
          id: 1,
          user: 2,
          name: 'My Lineup 1',
          sport: 'mlb',
          fantasy_points: 0.0,
          draft_group: 3,
          players: [
            { player_id: 1 },
            { player_id: 2 },
          ],
        },
      ] });

    // data coming out
    const expectedActions = [{
      payload: [
        {
          type: ActionTypes.ENTRIES_ROSTERS__RECEIVE,
        },
      ],
      type: ActionTypes.ENTRIES_ROSTERS__RECEIVE,
    }];

    store.dispatch(actions.fetchEntriesRosters())
      .then(() => {
        assert.deepEqual(store.getActions(), expectedActions);
      });
  });
});
