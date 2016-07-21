import assert from 'assert';
import mockStore from '../mock-store-with-middleware';
import nock from 'nock';
import merge from 'lodash/merge';

import * as ActionTypes from '../../action-types';
import * as actions from '../../actions/sports';
import reducer from '../../reducers/sports';


describe('actions.sports.calcDecimalRemaining', () => {
  it('should return correct amount', () => {
    assert.equal(actions.calcDecimalRemaining(1, 1), 0.9999);
    assert.equal(actions.calcDecimalRemaining(0, 1), 0);
    assert.equal(actions.calcDecimalRemaining(1, 3), 0.3334);
  });
});

describe('actions.sports.calculateTimeRemaining', () => {
  it('should return full duration if game has not started', () => {
    assert.equal(actions.calculateTimeRemaining('mlb', {}), 18);
  });

  it('should return appropriate amounts for mlb', () => {
    assert.equal(actions.calculateTimeRemaining('mlb', {
      boxscore: {},
      status: 'complete',
    }), 0);

    // bottom of 9th
    assert.equal(actions.calculateTimeRemaining('mlb', {
      status: 'inprogress',
      boxscore: {
        inning: 1,
        inning_half: 'T',
      },
    }), 18);

    // bottom of 9th
    assert.equal(actions.calculateTimeRemaining('mlb', {
      status: 'inprogress',
      boxscore: {
        inning: 9,
        inning_half: 'B',
      },
    }), 1);
  });

  it('should return appropriate amounts for nba', () => {
    assert.equal(actions.calculateTimeRemaining('nba', {
      boxscore: {},
      status: 'complete',
    }), 0);

    // no quarter yet, give full time
    assert.equal(actions.calculateTimeRemaining('nba', {
      status: 'inprogress',
      boxscore: {
        clock: '12:00',
        quarter: '',
      },
    }), 48);

    // bottom of 9th
    assert.equal(actions.calculateTimeRemaining('nba', {
      status: 'inprogress',
      boxscore: {
        clock: '2:00',
        quarter: '2',
      },
    }), 26);

    // bottom of 9th
    assert.equal(actions.calculateTimeRemaining('nba', {
      status: 'inprogress',
      boxscore: {
        clock: '0:00',
        quarter: '4',
      },
    }), 0);
  });
});

describe('actions.sports.isGameReady', () => {
  before(() => {
    nock.disableNetConnect();
  });

  after(() => {
    nock.enableNetConnect();
  });

  afterEach(() => {
    nock.cleanAll();
  });

  it('should return false if game does not exist', () => {
    // initial store, state
    const store = mockStore({
      sports: reducer(undefined, {}),
    });

    assert.equal(
      actions.isGameReady(store.getState(), store.dispatch, 'mlb', 'foo'),
      false
    );
  });

  it('should return false if boxscore does not exist', () => {
    // store with no boxscore
    const store = mockStore({
      sports: merge({}, reducer(undefined, {}), {
        games: {
          foo: {},
        },
      }),
    });

    nock('http://localhost')
      .get('/api/sports/scoreboard-games/mlb/')
      .reply(200, {
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
      });

    const itRan = nock('http://localhost')
      .get('/api/sports/teams/mlb/')
      .reply(200, [
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
      ]);

    assert.equal(
      actions.isGameReady(store.getState(), store.dispatch, 'mlb', 'foo'),
      false
    );

    assert.equal(
      itRan.isDone(),
      true
    );
  });

  it('should return true otherwise', () => {
    // initial store, state
    const store = mockStore({
      sports: merge({}, reducer(undefined, {}), {
        games: {
          foo: {
            boxscore: {},
          },
        },
      }),
    });
    assert.equal(actions.isGameReady(store.getState(), store.dispatch, 'mlb', 'foo'), true);
  });
});

describe('actions.sports.fetch', () => {
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
      .reply(200, {
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
      });

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
      .reply(200, [
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
      ]);

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
