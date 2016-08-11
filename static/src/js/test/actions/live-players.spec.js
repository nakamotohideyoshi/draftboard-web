import { dateNow } from '../../lib/utils';
import assert from 'assert';
import mockStore from '../mock-store-with-middleware';
import nock from 'nock';

import * as ActionTypes from '../../action-types';
import * as actions from '../../actions/live-players';
import reducer from '../../reducers/live-players';


describe('actions.livePlayers', () => {
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
      currentLineups: {
        items: {
          1: {
            // in the future
            start: dateNow() + 10000,
          },
        },
      },
      livePlayers: reducer(undefined, {}),
    });

    nock('http://localhost')
      .get('/api/contest/lineup/1/')
      .reply(200, { body: [
        {
          i: 0,
          started: true,
          data: [
            {
              pk: 27110,
              model: 'mlb.playerstatspitcher',
              fields: {
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
            },
          ],
        },
      ] });

    // data coming out
    const expectedActions = [{
      payload: [
        {
          type: ActionTypes.RECEIVE_LIVE_PLAYERS_STATS,
        },
      ],
      type: ActionTypes.RECEIVE_LIVE_PLAYERS_STATS,
    }];

    store.dispatch(actions.fetchPlayersStatsIfNeeded(1))
      .then(() => {
        assert.deepEqual(store.getActions(), expectedActions);
      });
  });

  it('should correctly update live players stats', () => {
    // initial store, state
    const store = mockStore({
      livePlayers: {
        relevantPlayers: {
          playerId: {
            foo: 'bar',
          },
        },
      },
    });

    store.dispatch(actions.updateLivePlayersStats('playerId', { newField: 'hi' }));
    assert.deepEqual(store.getActions()[0].type, ActionTypes.UPDATE_LIVE_PLAYER_STATS);
  });
});
