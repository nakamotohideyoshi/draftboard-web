import assert from 'assert';
import merge from 'lodash/merge';
import mockStore from '../../mock-store-with-middleware';
import proxyquire from 'proxyquire';

import eventsReducer from '../../../reducers/events';
import sportsReducer from '../../../reducers/sports';


describe('actions.events.pbp.onPBPReceived (mlb)', () => {
  // scope the state we reset in beforeEach
  let state;
  let store;

  // mock responses, answers to make sure it ran correctly
  const addEventRan = { type: 'addEventAndStartQueue ran' };

  // use proxyquire to mock in responses
  const actions = proxyquire('../../../actions/events/pbp', {
    '../events': {
      addEventAndStartQueue: (gameId, message) => merge({}, addEventRan, { message }),
    },
  });

  const defaultMessage = {
    at_bat: {
      stats_str: 'This happened',
      srid_hitter: 'player4',
      srid_team: 'team1',
    },
    stats: [],
    pbp: {
      count: {
        pc: 3,
        outs: 2,
        k: 1,
        b: 1,
      },
      flags: {
        is_ab_over: false,
      },
      srid: 'pbp1',
      srid_at_bat: 'atbat1',
      srid_game: 'game1',  // in state.sports.games
      srid_pitcher: 'player1',
    },
    zone_pitches: [],
  };


  beforeEach(() => {
    // initial state to mock the store with
    state = {
      events: eventsReducer(undefined, {}),
      sports: sportsReducer(undefined, {}),
    };

    // add in example games to make sure game is ready
    state.sports.games = {
      game1: { boxscore: {} },
      game2: { boxscore: {} },
    };

    store = mockStore(state);
  });

  // it('should return false if game is not ready', () => {
  //   // key here is that `game3` is not in state.sports.games
  //   const message = {
  //     at_bat: {
  //       srid_hitter: 'hitter1',
  //     },
  //     pbp: {
  //       srid_game: 'game3',
  //       flags: {},
  //     },
  //     stats: {},
  //   };

  //   assert.equal(
  //     store.dispatch(actions.onPBPReceived(message, 'mlb')),
  //     false
  //   );
  // });

  it('should properly find pitcher, hitter IDs and include in message', () => {
    const response = store.dispatch(actions.onPBPReceived(defaultMessage, 'mlb'));
    assert.deepEqual(
      response.message.eventPlayers,
      ['player1', 'player4']
    );
  });

  it('should properly find runners if in message', () => {
    const message = merge({}, defaultMessage, {
      runners: [
        { srid: 'player5' },
        { srid: 'player6' },
      ],
    });

    const response = store.dispatch(actions.onPBPReceived(message, 'mlb'));
    assert.deepEqual(
      response.message.eventPlayers,
      ['player1', 'player4', 'player5', 'player6']
    );
  });

  // it('should fail if at bat is over but has no description', () => {
  //   const message = merge({}, defaultMessage, {
  //     pbp: {
  //       flags: {
  //         is_ab_over: true,
  //       },
  //     },
  //   });
  //   const response = store.dispatch(actions.onPBPReceived(message, 'mlb'));
  //   assert.deepEqual(
  //     response,
  //     false
  //   );
  // });

  it('should add event if valid', () => {
    const response = store.dispatch(actions.onPBPReceived(defaultMessage, 'mlb'));
    assert.deepEqual(
      response.message,
      {
        description: '',
        eventPlayers: ['player1', 'player4'],
        gameId: 'game1',
        hitter: {
          atBatStats: 'This happened',
          name: ' ',
          sridPlayer: 'player4',
          sridTeam: 'team1',
          outcomeFp: null,
        },
        id: 'pbp1',
        isAtBatOver: false,
        pitcher: {
          outcomeFp: null,
          sridPlayer: 'player1',
        },
        pitchCount: '1B/1S - 2 Outs',
        runnerIds: [],
        runners: [],
        playersStats: {},
        sport: 'mlb',
        sridAtBat: 'atbat1',
        when: { half: false, inning: false, humanized: false },
        zonePitches: [],
      }
    );
    assert.equal(
      response.type,
      addEventRan.type
    );
  });

  it('should generate zone pitches', () => {
    const message = merge({}, defaultMessage, {
      zone_pitches: [
        {
          z: 11,
          t: 'CT',
          pc: 1,
          mph: 93,
        },
        {
          z: 3,
          t: 'SL',
          pc: 2,
          mph: 88,
        },
        {
          z: 8,
          t: 'SL',
          pc: 3,
          mph: 89,
        },
      ],
    });

    const response = store.dispatch(actions.onPBPReceived(message, 'mlb'));
    assert.equal(response.message.zonePitches[0].count, 1);
    assert.equal(response.message.zonePitches[0].outcome, 'ball');
  });
});
