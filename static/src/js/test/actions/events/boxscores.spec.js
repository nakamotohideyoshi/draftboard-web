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
  const itRan = { type: 'ran' };
  const properMessage = { id: 'foo', outcome__list: {}, status: 'inprogress' };

  // use proxyquire to mock in responses
  const actions = proxyquire('../../../actions/events/boxscores', {
    '../events': {
      addEventAndStartQueue: () => itRan,
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

  it('should return false if game has not started', () => {
    const newState = merge({}, state);
    newState.sports.games.foo = {
      boxscore: {},
    };
    const store = mockStore(newState);

    // key here is the status of `scheduled`, see possible statuses in docs https://git.io/votCh
    const message = { id: 'foo', outcome__list: {}, status: 'scheduled' };
    assert.equal(
      store.dispatch(actions.onBoxscoreGameReceived(message)),
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
      store.dispatch(actions.onBoxscoreGameReceived(properMessage)),
      itRan
    );
  });
});
