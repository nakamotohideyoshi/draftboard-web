import assert from 'assert';
import mockStore from '../mock-store-with-middleware';
import nock from 'nock';

import * as ActionTypes from '../../action-types';
import * as actions from '../../actions/sports';
import reducer from '../../reducers/sports';


describe('actions.sports', () => {
  before(() => {
    nock.disableNetConnect();
  });

  after(() => {
    nock.enableNetConnect();
  });

  afterEach(() => {
    nock.cleanAll();
  });

  it('should correctly fetch games', () => {
    // initial store, state
    const store = mockStore({
      sports: reducer(undefined, {}),
    });

    nock('http://localhost')
      .get('/api/sports/scoreboard-games/mlb/')
      .reply(200, { body: {
        'c6742f5c-2270-4cff-b29e-bc2528fb7182': {
          srid: 'c6742f5c-2270-4cff-b29e-bc2528fb7182',
          status: 'scheduled',
          start: '2016-06-17T02:10:00Z',
          srid_away: 'dcfd5266-00ce-442c-bc09-264cd20cf455',
          srid_home: 'ef64da7f-cfaf-4300-87b0-9313386b977c',
          title: '',
          game_number: 1,
          day_night: 'N',
        },
      } });

    // data coming out
    const expectedActions = [{
      payload: [
        {
          type: ActionTypes.RECEIVE_GAMES,
        },
      ],
      type: ActionTypes.RECEIVE_GAMES,
    }];

    store.dispatch(actions.fetchGamesIfNeeded('mlb', true))
      .then(() => {
        assert.deepEqual(store.getActions(), expectedActions);
      });
  });

  it('should correctly fetch teams', () => {
    // initial store, state
    const store = mockStore({
      sports: reducer(undefined, {}),
    });

    nock('http://localhost')
      .get('/api/sports/teams/mlb/')
      .reply(200, { body: [
        {
          id: 6,
          srid: '833a51a9-0d84-410f-bd77-da08c3e5e26e',
          name: 'Royals',
          alias: 'KC',
          city: 'Kansas City',
        },
        {
          id: 2,
          srid: 'bdc11650-6f74-49c4-875e-778aeb7632d9',
          name: 'Rays',
          alias: 'TB',
          city: 'Tampa Bay',
        },
      ] });

    // data coming out
    const expectedActions = [{
      payload: [
        {
          type: ActionTypes.RECEIVE_TEAMS,
        },
      ],
      type: ActionTypes.RECEIVE_TEAMS,
    }];

    store.dispatch(actions.fetchTeamsIfNeeded('mlb', true))
      .then(() => {
        assert.deepEqual(store.getActions(), expectedActions);
      });
  });
});
