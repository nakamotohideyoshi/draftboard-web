import assert from 'assert';
import mockStore from '../mock-store-with-middleware';
import nock from 'nock';

import * as ActionTypes from '../../action-types';
import * as actions from '../../actions/current-lineups';
import reducer from '../../reducers/current-lineups';


describe('actions.currentLineups', () => {
  afterEach(() => {
    nock.cleanAll();
  });

  it('should correctly fetch current lineups', () => {
    // initial store, state
    const store = mockStore({
      lineups: reducer(undefined, {}),
    });

    nock('http://example.com/')
      .get('/api/lineups/current/')
      .reply(200, { body: [
        {
          id: 1,
          contest_pool: 2,
          contests: [3],
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
          type: ActionTypes.CURRENT_LINEUPS__RECEIVE,
        },
      ],
      type: ActionTypes.CURRENT_LINEUPS__RECEIVE,
    }];

    store.dispatch(actions.fetchCurrentLineups())
      .then(() => {
        assert.deepEqual(store.getActions(), expectedActions);
      });
  });

  it('should correctly fetch lineups rosters', () => {
    // initial store, state
    const store = mockStore({
      lineups: reducer(undefined, {}),
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
          type: ActionTypes.CURRENT_LINEUPS_ROSTERS__RECEIVE,
        },
      ],
      type: ActionTypes.CURRENT_LINEUPS_ROSTERS__RECEIVE,
    }];

    store.dispatch(actions.fetchLineupsRosters())
      .then(() => {
        assert.deepEqual(store.getActions(), expectedActions);
      });
  });
});
