import { assert } from 'chai';
import merge from 'lodash/merge';
import reducer from '../../reducers/live-draft-groups';
import * as types from '../../action-types';


describe('reducers.live-draft-groups', () => {
  const defaultState = reducer(undefined, {});

  it('should return the initial state', () => {
    assert.deepEqual(defaultState, {});
  });

  it('should return state if invalid action type used', () => {
    const newState = reducer(defaultState, { type: 'foo' });
    assert.deepEqual(defaultState, newState);
  });

  it('should return state if no action type used', () => {
    const newState = reducer(defaultState);
    assert.deepEqual(defaultState, newState);
  });


  it('should handle CONFIRM_LIVE_DRAFT_GROUP_STORED', () => {
    // no draft group, no change
    let state = reducer(defaultState, {
      type: types.CONFIRM_LIVE_DRAFT_GROUP_STORED,
      id: 2,
    });
    assert.deepEqual(defaultState, state);

    // works
    state = merge({}, defaultState, {
      2: {
        hasAllInfo: false,
        id: 2,
      },
    });
    state = reducer(state, {
      type: types.CONFIRM_LIVE_DRAFT_GROUP_STORED,
      id: 2,
    });
    assert.equal(state[2].hasAllInfo, true);
  });


  it('should handle LIVE_DRAFT_GROUP__INFO__REQUEST', () => {
    const newState = reducer(defaultState, {
      type: types.LIVE_DRAFT_GROUP__INFO__REQUEST,
      id: 2,
      expiresAt: 'myDate',
    });
    assert.equal(newState[2].infoExpiresAt, 'myDate');
    assert.equal(newState[2].hasAllInfo, false);
  });


  it('should handle LIVE_DRAFT_GROUP__INFO__RECEIVE', () => {
    const defaultResponse = {
      type: types.LIVE_DRAFT_GROUP__INFO__RECEIVE,
      expiresAt: 'myDate2',
      response: {
        id: 2,
        players: {},
        start: 'isADate',
        end: 'isADate',
        sport: 'mlb',
      },
    };

    let state = merge({}, defaultState, {
      2: {
        hasAllInfo: false,
        infoExpiresAt: 'myDate1',
        id: 2,
      },
    });
    state = reducer(state, defaultResponse);
    assert.equal(state[2].infoExpiresAt, defaultResponse.expiresAt);
    assert.equal(state[2].hasAllInfo, false);
    assert.equal(state[2].id, defaultResponse.response.id);
    assert.deepEqual(state[2].playersInfo, defaultResponse.response.players);
    assert.equal(state[2].start, defaultResponse.response.start);
    assert.equal(state[2].end, defaultResponse.response.end);
    assert.equal(state[2].sport, defaultResponse.response.sport);

    // check it works if we didn't make draft group yet
    state = reducer(undefined, defaultResponse);
    assert.equal(state[2].infoExpiresAt, defaultResponse.expiresAt);
    assert.equal(state[2].hasAllInfo, false);
    assert.equal(state[2].id, defaultResponse.response.id);
    assert.deepEqual(state[2].playersInfo, defaultResponse.response.players);
    assert.equal(state[2].start, defaultResponse.response.start);
    assert.equal(state[2].end, defaultResponse.response.end);
    assert.equal(state[2].sport, defaultResponse.response.sport);
  });


  it('should handle REQUEST_LIVE_DRAFT_GROUP_FP', () => {
    const newState = reducer(defaultState, {
      type: types.REQUEST_LIVE_DRAFT_GROUP_FP,
      id: 2,
      expiresAt: 'myDate',
    });
    assert.equal(newState[2].fpExpiresAt, 'myDate');
    assert.equal(newState[2].hasAllInfo, false);
  });


  it('should handle RECEIVE_LIVE_DRAFT_GROUP_FP', () => {
    const defaultResponse = {
      type: types.RECEIVE_LIVE_DRAFT_GROUP_FP,
      expiresAt: 'myDate2',
      response: {
        id: 2,
        players: {},
      },
    };

    let state = merge({}, defaultState, {
      2: {
        hasAllInfo: false,
        fpExpiresAt: 'myDate1',
        id: 2,
      },
    });
    state = reducer(state, defaultResponse);
    assert.equal(state[2].fpExpiresAt, defaultResponse.expiresAt);
    assert.equal(state[2].hasAllInfo, false);
    assert.equal(state[2].id, defaultResponse.response.id);
    assert.deepEqual(state[2].playersStats, defaultResponse.response.players);

    // check it works if we didn't make draft group yet
    state = reducer(undefined, defaultResponse);
    assert.equal(state[2].fpExpiresAt, defaultResponse.expiresAt);
    assert.equal(state[2].hasAllInfo, false);
    assert.equal(state[2].id, defaultResponse.response.id);
    assert.deepEqual(state[2].playersStats, defaultResponse.response.players);
  });


  it('should handle REQUEST_DRAFT_GROUP_BOXSCORES', () => {
    const newState = reducer(defaultState, {
      type: types.REQUEST_DRAFT_GROUP_BOXSCORES,
      id: 2,
      expiresAt: 'myDate',
    });
    assert.equal(newState[2].boxscoresExpiresAt, 'myDate');
    assert.equal(newState[2].hasAllInfo, false);
  });


  it('should handle RECEIVE_DRAFT_GROUP_BOXSCORES', () => {
    const defaultResponse = {
      type: types.RECEIVE_DRAFT_GROUP_BOXSCORES,
      expiresAt: 'myDate2',
      response: {
        id: 2,
        boxscores: {},
      },
    };

    let state = merge({}, defaultState, {
      2: {
        hasAllInfo: false,
        boxscoresExpiresAt: 'myDate1',
        id: 2,
      },
    });
    state = reducer(state, defaultResponse);
    assert.equal(state[2].boxscoresExpiresAt, defaultResponse.expiresAt);
    assert.equal(state[2].hasAllInfo, false);
    assert.equal(state[2].id, defaultResponse.response.id);
    assert.deepEqual(state[2].boxScores, defaultResponse.response.boxscores);

    // check it works if we didn't make draft group yet
    state = reducer(undefined, defaultResponse);
    assert.equal(state[2].boxscoresExpiresAt, defaultResponse.expiresAt);
    assert.equal(state[2].hasAllInfo, false);
    assert.equal(state[2].id, defaultResponse.response.id);
    assert.deepEqual(state[2].boxScores, defaultResponse.response.boxscores);
  });


  it('should handle REMOVE_LIVE_DRAFT_GROUPS', () => {
    let state = merge({}, defaultState, {
      1: { id: 1 },
      2: { id: 2 },
      3: { id: 3 },
    });

    state = reducer(state, {
      type: types.REMOVE_LIVE_DRAFT_GROUPS,
      ids: [2, 3],
    });
    assert.deepEqual(state, { 1: { id: 1 } });
  });


  it('should handle UPDATE_LIVE_DRAFT_GROUP_PLAYER_FP', () => {
    const state = merge({}, defaultState, {
      1: {
        playersStats: {
          2: {
            fp: 10,
          },
        },
      },
    });

    let newState = reducer(state, {
      type: types.UPDATE_LIVE_DRAFT_GROUP_PLAYER_FP,
      id: 1,
      playerId: 2,
      fp: 30,
    });
    assert.equal(newState[1].playersStats[2].fp, 30);


    newState = reducer(state, {
      type: types.UPDATE_LIVE_DRAFT_GROUP_PLAYER_FP,
      id: 1,
      playerId: 20,  // does not exist
      fp: 30,
    });
    assert.equal(state, newState);


    newState = reducer(defaultState, {
      type: types.UPDATE_LIVE_DRAFT_GROUP_PLAYER_FP,
      id: 1,  // does not exist
      playerId: 20,  // does not exist
      fp: 30,
    });
    assert.equal(defaultState, newState);
  });
});
