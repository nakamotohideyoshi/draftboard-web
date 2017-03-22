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
      .reply(200, {
        'lineups': [
          {
            'id': 322,
            'players': [
              {
                'player_id': 447,
                'full_name': 'Derrick Favors',
                'roster_spot': 'FX',
                'idx': 7,
                'player_meta': {
                  'first_name': 'Derrick',
                  'last_name': 'Favors',
                  'status': 'ACT',
                  'srid': 'ad354ebb-88e5-46e4-ad79-f7188ee1f6c2',
                  'team': {
                    'id': 17,
                    'alias': 'UTA',
                    'market': 'Utah',
                    'name': 'Jazz'
                  }
                },
                'fppg': 25.81137,
                'salary': 5200,
                'fantasy_points': 0
              },
              {
                'player_id': 147,
                'full_name': 'Tony Parker',
                'roster_spot': 'FX',
                'idx': 6,
                'player_meta': {
                  'first_name': 'Tony',
                  'last_name': 'Parker',
                  'status': 'ACT',
                  'srid': 'b1b2d578-44df-4e05-9884-31dd89e82cf0',
                  'team': {
                    'id': 24,
                    'alias': 'SAS',
                    'market': 'San Antonio',
                    'name': 'Spurs'
                  }
                },
                'fppg': 21.2916275,
                'salary': 3400,
                'fantasy_points': 6.75
              },
              {
                'player_id': 454,
                'full_name': 'Jamal Murray',
                'roster_spot': 'FX',
                'idx': 5,
                'player_meta': {
                  'first_name': 'Jamal',
                  'last_name': 'Murray',
                  'status': 'ACT',
                  'srid': '685576ef-ea6c-4ccf-affd-18916baf4e60',
                  'team': {
                    'id': 20,
                    'alias': 'DEN',
                    'market': 'Denver',
                    'name': 'Nuggets'
                  }
                },
                'fppg': 21.905315,
                'salary': 4000,
                'fantasy_points': 27.75
              },
              {
                'player_id': 232,
                'full_name': 'Nikola Jokic',
                'roster_spot': 'C',
                'idx': 4,
                'player_meta': {
                  'first_name': 'Nikola',
                  'last_name': 'Jokic',
                  'status': 'ACT',
                  'srid': 'f2625432-3903-4f90-9b0b-2e4f63856bb0',
                  'team': {
                    'id': 20,
                    'alias': 'DEN',
                    'market': 'Denver',
                    'name': 'Nuggets'
                  }
                },
                'fppg': 42.551595,
                'salary': 9200,
                'fantasy_points': 0
              },
              {
                'player_id': 575,
                'full_name': 'Okaro White',
                'roster_spot': 'F',
                'idx': 3,
                'player_meta': {
                  'first_name': 'Okaro',
                  'last_name': 'White',
                  'status': 'ACT',
                  'srid': 'bd0e96ba-6f67-43f2-ac8c-04a313d0a32f',
                  'team': {
                    'id': 4,
                    'alias': 'MIA',
                    'market': 'Miami',
                    'name': 'Heat'
                  }
                },
                'fppg': 1.5018025,
                'salary': 3000,
                'fantasy_points': 0
              },
              {
                'player_id': 381,
                'full_name': 'Giannis Antetokounmpo',
                'roster_spot': 'F',
                'idx': 2,
                'player_meta': {
                  'first_name': 'Giannis',
                  'last_name': 'Antetokounmpo',
                  'status': 'ACT',
                  'srid': '6c60282d-165a-4cba-8e5a-4f2d9d4c5905',
                  'team': {
                    'id': 15,
                    'alias': 'MIL',
                    'market': 'Milwaukee',
                    'name': 'Bucks'
                  }
                },
                'fppg': 46.759455,
                'salary': 9900,
                'fantasy_points': 70.25
              },
              {
                'player_id': 331,
                'full_name': 'Ish Smith',
                'roster_spot': 'G',
                'idx': 1,
                'player_meta': {
                  'first_name': 'Ish',
                  'last_name': 'Smith',
                  'status': 'ACT',
                  'srid': '05a90cd6-73de-43d5-9d30-bc2588d03262',
                  'team': {
                    'id': 14,
                    'alias': 'DET',
                    'market': 'Detroit',
                    'name': 'Pistons'
                  }
                },
                'fppg': 19.6051225,
                'salary': 4000,
                'fantasy_points': 17
              },
              {
                'player_id': 25,
                'full_name': 'James Harden',
                'roster_spot': 'G',
                'idx': 0,
                'player_meta': {
                  'first_name': 'James',
                  'last_name': 'Harden',
                  'status': 'ACT',
                  'srid': 'a52b2c84-9c3d-4d6e-8a3b-10e75d11c2bc',
                  'team': {
                    'id': 22,
                    'alias': 'HOU',
                    'market': 'Houston',
                    'name': 'Rockets'
                  }
                },
                'fppg': 48.6541725,
                'salary': 11200,
                'fantasy_points': 52
              }
            ],
            'entries': [
              {
                'id': 1616,
                'final_rank': 2,
                'contest': {
                  'id': 502,
                  'name': '$1 NBA H2H',
                  'status': 'closed'
                },
                'payout': null
              },
              {
                'id': 1617,
                'final_rank': 9,
                'contest': {
                  'id': 499,
                  'name': '$1 NBA Tourney',
                  'status': 'closed'
                },
                'payout': null
              },
              {
                'id': 1619,
                'final_rank': 7,
                'contest': {
                  'id': 498,
                  'name': '$2 NBA Tourney',
                  'status': 'closed'
                },
                'payout': null
              },
              {
                'id': 1618,
                'final_rank': 2,
                'contest': {
                  'id': 496,
                  'name': '$2 NBA H2H',
                  'status': 'closed'
                },
                'payout': null
              },
              {
                'id': 1621,
                'final_rank': 6,
                'contest': {
                  'id': 493,
                  'name': '$5 NBA Tourney',
                  'status': 'closed'
                },
                'payout': null
              },
              {
                'id': 1620,
                'final_rank': 2,
                'contest': {
                  'id': 490,
                  'name': '$5 NBA H2H',
                  'status': 'closed'
                },
                'payout': null
              },
              {
                'id': 1624,
                'final_rank': 6,
                'contest': {
                  'id': 489,
                  'name': '$5 NBA 50/50',
                  'status': 'closed'
                },
                'payout': null
              },
              {
                'id': 1623,
                'final_rank': 5,
                'contest': {
                  'id': 488,
                  'name': '$2 NBA 50/50',
                  'status': 'closed'
                },
                'payout': {
                  'amount': 3.6
                }
              },
              {
                'id': 1622,
                'final_rank': 7,
                'contest': {
                  'id': 487,
                  'name': '$1 NBA 50/50',
                  'status': 'closed'
                },
                'payout': null
              }
            ],
            'name': 'Fear the Beard',
            'sport': 'nba'
          }
        ],
        'overall': {
          'contests': 9,
          'buyins': '24.00',
          'winnings': '3.60',
          'possible': '60.80',
          'entries': 9
        },
      });

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
