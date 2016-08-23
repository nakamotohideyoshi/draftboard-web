import assert from 'assert';
import mockStore from '../mock-store-with-middleware';
import nock from 'nock';

import * as ActionTypes from '../../action-types';
import * as actions from '../../actions/player-box-score-history-actions';
import reducer from '../../reducers/player-box-score-history';


describe('actions.playerBoxScoreHistory', () => {
  before(() => {
    nock.disableNetConnect();
  });

  after(() => {
    nock.enableNetConnect();
  });

  afterEach(() => {
    nock.cleanAll();
  });

  it('should correctly fetch live players stats for a lineup', () => {
    // initial store, state
    const store = mockStore({
      playerBoxScoreHistory: reducer(undefined, {}),
    });

    nock('http://localhost')
      .get('/api/sports/player/history/nfl/20/2200/')
      .reply(200, { body: [
        {
          i: 0,
          started: true,
          data: [
            {
              ip_2: 0.2,
              fantasy_points: 5,
              started: false,
              hbp: 0,
              ktotal: 1,
              game_id: 4624,
              win: false,
              cg: false,
              nono: false,
              position: 18,
              bb: 0,
              srid_game: '81a368a2-6d20-455b-8a11-022b4426f05d',
              loss: false,
              qstart: false,
              game_type: 55,
              ip_1: 2,
              r_total: 0,
              player_id: 1054,
              played: false,
              er: 0,
              created: '2016-06-16T23:00:47.156Z',
              fp_change: 0,
              cgso: false,
              srid_player: '9760f1d6-9560-45ed-bc73-5ec2205905a2',
              player_type: 57,
              updated: '2016-06-16T23:24:36.545Z',
              h: 0,
            },
          ],
        },
      ] });

    // data coming out
    const expectedActions = [{
      payload: [
        {
          type: ActionTypes.PLAYER_HISTORY_SINGLE__RECEIVE,
        },
      ],
      type: ActionTypes.PLAYER_HISTORY_SINGLE__RECEIVE,
    }];

    store.dispatch(actions.fetchSinglePlayerBoxScoreHistoryIfNeeded('nfl', 2200))
      .then(() => {
        assert.deepEqual(store.getActions(), expectedActions);
      });
  });
});
