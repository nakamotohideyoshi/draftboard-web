import assert from 'assert';
import merge from 'lodash/merge';
import mockStore from '../../mock-store-with-middleware';
import proxyquire from 'proxyquire';

import eventsReducer from '../../../reducers/events';
import sportsReducer from '../../../reducers/sports';


describe('actions.events.pbp.onPBPReceived (nfl)', () => {
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

  const defaultPassReceptionMessage = {
    pbp: {
      end_situation: {
        down: 3,
        location: {
          yardline: 29,
        },
      },
      clock: '14:30',
      ts: 1464841517401,
      type: 'pass',
      statistics: {
        receive__list: {
          yards_after_catch: 2,
          player: 'player2-receiver',
        },
        pass__list: {
          att_yards: 2,
          complete: 1,
          player: 'player1-quarterback',
        },
        defense__list: {
          team: 'team1',
        },
      },
      start_situation: {
        down: 2,
        clock: '14:30',
        location: {
          yardline: 25,
        },
      },
      description: '(14:30) (Shotgun) K.Cousins pass short right to A.Roberts to WAS 29 for 4 yards (B.Grimes).',
      srid_game: 'game1',  // matches state
      id: '7e49db54-68d0-444d-b244-690f3930b77b',
      extra_info: {
        pass: {
          distance: 'short',
          side: 'right',
        },
        intercepted: false,
        fumbles: false,
        touchdown: false,
        formation: 'shotgun',
      },
    },
    stats: [],
  };

  const defaultRushMessage = {
    pbp: {
      end_situation: {
        down: 2,
        location: {
          yardline: 25,
        },
      },
      clock: '15:00',
      ts: 1464841517401,
      type: 'rush',
      statistics: {
        rush__list: {
          yards: 5,
          player: 'player1-rb',
        },
        defense__list: {
          team: 'team1',
        },
      },
      start_situation: {
        down: 1,
        clock: '15:00',
        location: {
          yardline: 20,
        },
      },
      description: '(15:00) A.Morris left tackle to WAS 25 for 5 yards (K.Sheppard).',
      srid_game: 'game1',  // matches state
      id: '7e49db54-68d0-444d-b244-690f3930b77b',
      extra_info: {
        rush: {
          side: 'left',
          scramble: false,
        },
        intercepted: false,
        fumbles: false,
        touchdown: false,
        formation: 'default',
      },
    },
    stats: [],
  };

  const defaultKickoffMessage = {
    pbp: {
      end_situation: {
        down: 1,
        location: {
          yardline: 25,
        },
      },
      clock: '7:29',
      ts: 1464841517401,
      type: 'kickoff',
      statistics: {
        return__list: {
          yards: 29,
          player: 'player1-rb',
        },
        defense__list: {
          team: 'team1',
        },
      },
      start_situation: {
        down: 0,
        clock: '7:35',
        location: {
          yardline: 35,
        },
      },
      description: 'M.Bosher kicks 69 yards from ATL 35 to TEN -4. T.McBride to TEN 25 for 29 yards (K.White).',
      srid_game: 'game1',  // matches state
      id: '7e49db54-68d0-444d-b244-690f3930b77b',
      extra_info: {
        intercepted: false,
        fumbles: false,
        touchdown: false,
        formation: 'default',
      },
    },
    stats: [],
  };


  beforeEach(() => {
    // initial state to mock the store with
    state = {
      events: eventsReducer(undefined, {}),
      sports: sportsReducer(undefined, {}),
    };

    // add in example games to make sure game is ready
    state.sports.games = {
      game1: {
        boxscore: {
          quarter: 1,  // needed
        },
        srid_away: 'team1',  // to determine driveDirection
      },
      game2: { boxscore: {} },
    };

    store = mockStore(state);
  });

  it('should return false if game is not ready', () => {
    // key here is that `game3` is not in state.sports.games
    const message = {
      pbp: {
        srid_game: 'game3',
      },
      stats: {},
    };

    assert.equal(
      store.dispatch(actions.onPBPReceived(message, 'nfl')),
      false
    );
  });

  // it('should properly find quarterback, receiver IDs and include in pass message', () => {
  //   const response = store.dispatch(actions.onPBPReceived(defaultPassReceptionMessage, 'nfl'));
  //   assert.deepEqual(
  //     response.message.eventPlayers,
  //     ['player2-receiver', 'player1-quarterback']
  //   );
  // });

  it('should add pass pbp event if valid', () => {
    const response = store.dispatch(actions.onPBPReceived(defaultPassReceptionMessage, 'nfl'));
    const testAgainst = {
      description: '(14:30) (Shotgun) K.Cousins pass short right to A.Roberts to WAS 29 for 4 yards (B.Grimes).',
      driveDirection: 'leftToRight',
      eventPlayers: ['player2-receiver', 'player1-quarterback'],
      formation: 'shotgun',
      fumbles: false,
      gameId: 'game1',
      playersStats: [],
      side: 'middle',
      sport: 'nfl',
      touchdown: false,
      type: 'pass',
      when: { clock: '14:30', quarter: 1 },
      yardlineEnd: 0.29,
      yardlineStart: 0.25,
      pass: {
        attemptedYards: 2,
        completed: true,
        distance: 'short',
        intercepted: false,
        sack: false,
        sackYards: 0,
        side: 'right',
        yardsAfterCatch: 2,
      },
    };

    // is a timestamp, remove to compare
    delete(response.message.id);

    assert.deepEqual(
      response.message,
      testAgainst
    );
    assert.equal(
      response.type,
      addEventRan.type
    );
  });

  it('should properly find rb ID and include in rush message', () => {
    const response = store.dispatch(actions.onPBPReceived(defaultRushMessage, 'nfl'));
    assert.deepEqual(
      response.message.eventPlayers,
      ['player1-rb']
    );
  });

  it('should add rush pbp event if valid', () => {
    const response = store.dispatch(actions.onPBPReceived(defaultRushMessage, 'nfl'));
    const testAgainst = {
      description: '(15:00) A.Morris left tackle to WAS 25 for 5 yards (K.Sheppard).',
      driveDirection: 'leftToRight',
      eventPlayers: ['player1-rb'],
      fumbles: false,
      formation: 'default',
      gameId: 'game1',
      playersStats: [],
      side: 'middle',
      sport: 'nfl',
      touchdown: false,
      type: 'rush',
      when: { clock: '15:00', quarter: 1 },
      yardlineEnd: 0.25,
      yardlineStart: 0.2,
      rush: {
        side: 'left',
        scramble: false,
      },
    };

    // is a timestamp, remove to compare
    delete(response.message.id);

    assert.deepEqual(
      response.message,
      testAgainst
    );
    assert.equal(
      response.type,
      addEventRan.type
    );
  });

  it('should properly find rb ID and include in kickoff return message', () => {
    const response = store.dispatch(actions.onPBPReceived(defaultKickoffMessage, 'nfl'));
    assert.deepEqual(
      response.message.eventPlayers,
      ['player1-rb']
    );
  });

  it('should add kickoff pbp event if valid', () => {
    const response = store.dispatch(actions.onPBPReceived(defaultKickoffMessage, 'nfl'));
    const testAgainst = {
      description: 'M.Bosher kicks 69 yards from ATL 35 to TEN -4. T.McBride to TEN 25 for 29 yards (K.White).',
      driveDirection: 'leftToRight',
      eventPlayers: ['player1-rb'],
      formation: 'default',
      fumbles: false,
      gameId: 'game1',
      playersStats: [],
      side: 'middle',
      sport: 'nfl',
      touchdown: false,
      type: 'kickoff',
      when: { clock: '7:29', quarter: 1 },
      yardlineEnd: 0.25,
      yardlineStart: 0.35,
      kickoff: {
        returnYards: 29,
      },
    };

    // is a timestamp, remove to compare
    delete(response.message.id);

    assert.deepEqual(
      response.message,
      testAgainst
    );
    assert.equal(
      response.type,
      addEventRan.type
    );
  });

  it('should add sack information if available in pass pbp event', () => {
    const message = merge({}, defaultPassReceptionMessage, {
      pbp: {
        statistics: {
          pass__list: {
            sack_yards: -8,
            sack: true,
          },
        },
      },
    });
    delete(message.pbp.statistics.receive__list);

    const response = store.dispatch(actions.onPBPReceived(message, 'nfl'));

    const testAgainst = {
      description: '(14:30) (Shotgun) K.Cousins pass short right to A.Roberts to WAS 29 for 4 yards (B.Grimes).',
      driveDirection: 'leftToRight',
      eventPlayers: ['player1-quarterback'],
      formation: 'shotgun',
      fumbles: false,
      gameId: 'game1',
      playersStats: [],
      side: 'middle',
      sport: 'nfl',
      touchdown: false,
      type: 'pass',
      when: { clock: '14:30', quarter: 1 },
      yardlineEnd: 0.29,
      yardlineStart: 0.25,
      pass: {
        attemptedYards: 2,
        completed: true,
        distance: 'short',
        intercepted: false,
        sack: true,
        sackYards: -8,
        side: 'right',
        yardsAfterCatch: 0,
      },
    };

    // is a timestamp, remove to compare
    delete(response.message.id);

    assert.deepEqual(
      response.message,
      testAgainst
    );
    assert.equal(
      response.type,
      addEventRan.type
    );
  });
});
