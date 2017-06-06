import assert from 'assert';
import mockStore from '../../mock-store-with-middleware';
import proxyquire from 'proxyquire';

import eventsReducer from '../../../reducers/events';
import sportsReducer from '../../../reducers/sports';


describe('actions.events.stats.onPlayerStatsReceived', () => {
  // scope the state, store we reset in beforeEach
  let state;
  let store;

  // mock answers to make sure it ran correctly
  const addEventRan = { type: 'addEventRan' };
  const playerStatsRan = { type: 'playerStatsRan' };

  // use proxyquire to mock in responses
  const actions = proxyquire('../../../actions/events/stats', {
    '../events': {
      addEventAndStartQueue: () => addEventRan,
    },
    '../live-draft-groups': {
      updatePlayerStats: () => playerStatsRan,
    },
  });

  // default which games matter for testing
  const relevantGames = ['game1'];

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
    // key here is that game3 is NOT in state.sports.games
    const message = { fields: { srid_game: 'game3' } };
    assert.equal(
      store.dispatch(actions.onPlayerStatsReceived(message)),
      false
    );
  });

  it('should update player stats if player is not in a game that involves a player in our lineup', () => {
    // key here is that srid_game value `game2` is NOT in relevantGamesPlayers above
    const message = {
      srid_game: 'game2',
    };
    assert.equal(
      store.dispatch(actions.onPlayerStatsReceived(message, 'mlb', relevantGames)),
      playerStatsRan
    );
  });

  it('should add event if player is in one of the watched lineups', () => {
    // key here is that srid_game value `game1` is THE SAME AS `game1` in relevantGames above
    const message = {
      srid_game: 'game1',
    };
    assert.equal(
      store.dispatch(actions.onPlayerStatsReceived(message, 'mlb', relevantGames)),
      addEventRan
    );
  });
});
