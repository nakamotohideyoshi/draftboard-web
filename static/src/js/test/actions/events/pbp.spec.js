import assert from 'assert';
import merge from 'lodash/merge';
import mockStore from '../../mock-store-with-middleware';
import proxyquire from 'proxyquire';

import eventsReducer from '../../../reducers/events';
import sportsReducer from '../../../reducers/sports';


describe('actions.events.pbp.onPBPReceived', () => {
  // scope the state we reset in beforeEach
  let state;
  let store;

  // mock responses, answers to make sure it ran correctly
  const addEventRan = { type: 'addEventAndStartQueue ran' };
  const playerStatsRan = { type: 'updatePBPPlayersStats ran' };

  // use proxyquire to mock in responses
  const actions = proxyquire('../../../actions/events/pbp', {
    '../events': {
      addEventAndStartQueue: (gameId, message) =>
        merge({}, addEventRan, {
          message,
        }),
      updatePBPPlayersStats: () => playerStatsRan,
    },
  });

  // default which games matter for testing
  const relevantPlayers = ['player1', 'player2'];

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

  it('should return false if game is not ready', () => {
    // key here is that `game3` is not in state.sports.games
    const message = { stats: {}, pbp: { game__id: 'game3' } };

    assert.equal(
      store.dispatch(actions.onPBPReceived(message, 'mlb', 'myDraftGroupId', [])),
      false
    );
  });

  it('should properly find pitcher, hitter IDs and include in message', () => {
    const message = {
      at_bat_stats: { id: 'player4' },
      pbp: {
        game__id: 'game1',  // in state.sports.games
        pitcher: 'player1',  // this IS IN relevantPlayers
      },
      stats: {},
    };
    const response = store.dispatch(actions.onPBPReceived(message, 'mlb', 'myDraftGroupId', relevantPlayers));
    assert.deepEqual(
      response.message.addedData.eventPlayers,
      ['player1', 'player4']
    );
  });

  it('should properly find runners if in message', () => {
    const message = {
      at_bat_stats: { id: 'player4' },
      pbp: {
        game__id: 'game1',  // in state.sports.games
        pitcher: 'player1',  // this IS IN relevantPlayers
      },
      runners: [
        { id: 'player5' },
        { id: 'player6' },
      ],
      stats: {},
    };
    const response = store.dispatch(actions.onPBPReceived(message, 'mlb', 'myDraftGroupId', relevantPlayers));
    assert.deepEqual(
      response.message.addedData.eventPlayers,
      ['player1', 'player4', 'player5', 'player6']
    );
  });

  it('should update player stats if player is not in a game that involves a player in our lineup', () => {
    const message = {
      at_bat_stats: { id: 'player4' },
      pbp: {
        game__id: 'game1',  // in state.sports.games
        pitcher: 'player3',  // important, this is NOT in relevantPlayers
      },
      stats: {},
    };
    assert.equal(
      store.dispatch(actions.onPBPReceived(message, 'mlb', 'myDraftGroupId', relevantPlayers)),
      playerStatsRan
    );
  });

  it('should add event if one of the players is in one of the watched lineups', () => {
    const message = {
      at_bat_stats: { id: 'player4' },
      pbp: {
        game__id: 'game1',  // in state.sports.games
        pitcher: 'player1',  // important, this IS IN relevantPlayers
      },
      stats: {},
    };
    assert.equal(
      store.dispatch(actions.onPBPReceived(message, 'mlb', 'myDraftGroupId', relevantPlayers)).type,
      addEventRan.type
    );
  });
});
