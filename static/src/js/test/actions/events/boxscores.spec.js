import assert from 'assert';
import merge from 'lodash/merge';
import mockStore from '../../mock-store-with-middleware';
import proxyquire from 'proxyquire';

import eventsReducer from '../../../reducers/events';
import sportsReducer from '../../../reducers/sports';


describe('actions.events.boxscores.onBoxscoreGameReceived', () => {
  // scope the state we reset in beforeEach
  let state;

  // mock responses, answers to make sure it ran correctly
  const properMessage = { id: 'foo', outcome__list: {}, status: 'inprogress' };

  // use proxyquire to mock in responses
  const actions = proxyquire('../../../actions/events/boxscores', {
    '../events': {
      addEventAndStartQueue: (gameId, relevantData) => ({
        type: 'ran',
        relevantData,
      }),
    },
  });

  beforeEach(() => {
    // initial state to mock the store with
    state = {
      events: eventsReducer(undefined, {}),
      sports: sportsReducer(undefined, {}),
    };
  });

  it('should return false if `outcome__list` is missing, no sport', () => {
    const newState = merge({}, state);
    newState.sports.games.foo = {
      boxscore: {},
    };
    const store = mockStore(newState);

    const message = { id: 'foo', status: 'inprogress' };
    assert.equal(
      store.dispatch(actions.onBoxscoreGameReceived(message)),
      false
    );
  });

  it('should return false if game is not ready', () => {
    // note that we are not adding a game, which means it's not ready
    const store = mockStore(state);

    assert.equal(
      store.dispatch(actions.onBoxscoreGameReceived(properMessage)),
      false
    );
  });

  it('should fail if message invalid', () => {
    const newState = merge({}, state);
    newState.sports.games.foo = {
      boxscore: {},
    };

    let store = mockStore(newState);
    let message = { id: 'foo', outcome__list: {}, status: 'closed' };
    assert.equal(store.dispatch(actions.onBoxscoreGameReceived(message)), false);

    store = mockStore(newState);
    message = { id: 'foo', status: 'scheduled' };
    assert.equal(store.dispatch(actions.onBoxscoreGameReceived(message)), false);

    store = mockStore(newState);
    message = { id: 'foo', final__list: {}, status: 'inprogress' };
    assert.equal(store.dispatch(actions.onBoxscoreGameReceived(message)), false);
  });

  it('should correctly create mlb inprogress relevant data', () => {
    const newState = merge({}, state);
    newState.sports.games.foo = {
      boxscore: {},
    };

    const store = mockStore(newState);
    const message = merge({}, properMessage, {
      outcome__list: {
        current_inning: 4,
        current_inning_half: 'B',
      },
    });

    assert.deepEqual(
      store.dispatch(actions.onBoxscoreGameReceived(message)).relevantData,
      {
        gameId: 'foo',
        updatedFields: {
          status: 'inprogress',
          boxscore: {
            inning: 4,
            inning_half: 'B',
          },
        },
      }
    );
  });

  it('should correctly create mlb closed relevant data', () => {
    const newState = merge({}, state);
    newState.sports.games.foo = {
      boxscore: {},
    };

    const store = mockStore(newState);
    const message = merge({}, properMessage, {
      final__list: {
        inning: 9,
        inning_half: 'B',
      },
      status: 'closed',
    });

    assert.deepEqual(
      store.dispatch(actions.onBoxscoreGameReceived(message)).relevantData,
      {
        gameId: 'foo',
        updatedFields: {
          status: 'closed',
          boxscore: {
            inning: 9,
            inning_half: 'B',
          },
        },
      }
    );
  });

  it('should correctly store event', () => {
    const newState = merge({}, state);
    newState.sports.games.foo = {
      boxscore: {},
    };

    const store = mockStore(newState);

    assert.equal(
      store.dispatch(actions.onBoxscoreGameReceived(properMessage)).type,
      'ran'
    );
  });
});


describe('actions.events.boxscores.onBoxscoreTeamReceived', () => {
  // scope the state we reset in beforeEach
  let state;

  // mock responses, answers to make sure it ran correctly
  const properMessage = { game__id: 'foo', points: 23 };

  // use proxyquire to mock in responses
  const actions = proxyquire('../../../actions/events/boxscores', {
    '../events': {
      addEventAndStartQueue: (gameId, relevantData) => ({
        type: 'ran',
        relevantData,
      }),
    },
  });

  beforeEach(() => {
    // initial state to mock the store with
    state = {
      events: eventsReducer(undefined, {}),
      sports: sportsReducer(undefined, {}),
    };
  });

  it('should return false if points are missing, no sport', () => {
    const newState = merge({}, state);
    newState.sports.games.foo = {
      boxscore: {},
    };
    const store = mockStore(newState);

    const message = { game__id: 'foo' };
    assert.equal(
      store.dispatch(actions.onBoxscoreTeamReceived(message)),
      false
    );
  });

  it('should return false if game is not ready', () => {
    // note that we are not adding a game, which means it's not ready
    const store = mockStore(state);

    assert.equal(
      store.dispatch(actions.onBoxscoreTeamReceived(properMessage)),
      false
    );
  });

  it('should correctly store event', () => {
    const newState = merge({}, state);
    newState.sports.games.foo = {
      boxscore: {},
    };

    const store = mockStore(newState);

    assert.equal(
      store.dispatch(actions.onBoxscoreTeamReceived(properMessage)).type,
      'ran'
    );
  });
});
