import { assert } from 'chai';
import merge from 'lodash/merge';
import reducer from '../../reducers/sports';
import * as types from '../../action-types';


describe('reducers.sports', () => {
  const defaultState = reducer(undefined, {});

  it('should return the initial state', () => {
    const sportTypes = ['nba', 'nhl', 'mlb', 'nfl'];

    assert.deepEqual(defaultState.games, {});
    assert.deepEqual(defaultState.types, sportTypes);

    sportTypes.forEach((sport) => {
      const defaultSport = defaultState[sport];
      assert.equal(typeof defaultSport.gamesExpireAt, 'number');
      assert.equal(typeof defaultSport.teamsExpireAt, 'number');
      assert.deepEqual(defaultSport.gameIds, []);
    });
  });

  it('should return state if invalid action type used', () => {
    const newState = reducer(defaultState, { type: 'foo' });
    assert.deepEqual(defaultState, newState);
  });

  it('should return state if no action type used', () => {
    const newState = reducer(defaultState);
    assert.deepEqual(defaultState, newState);
  });

  it('should handle REQUEST_TEAMS', () => {
    const newState = reducer(defaultState, {
      type: types.REQUEST_TEAMS,
      sport: 'mlb',
      expiresAt: 'myDate',
    });
    assert.equal(
      newState.mlb.teamsExpireAt,
      'myDate'
    );
  });

  it('should handle RECEIVE_TEAMS', () => {
    const defaultResponse = {
      type: types.RECEIVE_TEAMS,
      expiresAt: 1466031908348,
      response: {
        sport: 'mlb',
        teams: {},
      },
    };

    // return nothing if there is no current lineup to associate rosters with
    const oldState = reducer(defaultState, defaultResponse);
    assert.deepEqual(
      defaultState.mlb.teams,
      {}
    );

    const responseWithTeams = merge({}, defaultResponse, {
      response: {
        teams: {
          '833a51a9-0d84-410f-bd77-da08c3e5e26e': {
            id: 6,
            srid: '833a51a9-0d84-410f-bd77-da08c3e5e26e',
            name: 'Royals',
            alias: 'KC',
            city: 'Kansas City',
          },
          'bdc11650-6f74-49c4-875e-778aeb7632d9': {
            id: 2,
            srid: 'bdc11650-6f74-49c4-875e-778aeb7632d9',
            name: 'Rays',
            alias: 'TB',
            city: 'Tampa Bay',
          },
        },
      },
    });

    const state = reducer(defaultState, responseWithTeams);
    assert.deepEqual(
      state.mlb.teams,
      responseWithTeams.response.teams
    );

    // check that expiration was updated
    assert.notEqual(
      oldState.mlb.teamsExpireAt,
      state.mlb.teamsExpireAt
    );
  });


  it('should handle REQUEST_GAMES', () => {
    const newState = reducer(defaultState, {
      type: types.REQUEST_GAMES,
      sport: 'mlb',
      expiresAt: 'myDate',
    });
    assert.equal(
      newState.mlb.gamesExpireAt,
      'myDate'
    );
  });

  it('should handle RECEIVE_GAMES', () => {
    const defaultResponse = {
      type: types.RECEIVE_GAMES,
      expiresAt: 1466031908348,
      response: {
        sport: 'mlb',
        games: {},
        gameIds: [],
      },
    };

    // return nothing if there is no current lineup to associate rosters with
    const oldState = reducer(defaultState, defaultResponse);
    assert.deepEqual(defaultState.games, {});
    assert.deepEqual(defaultState.mlb.gameIds, []);

    const responseWithTeams = merge({}, defaultResponse, {
      response: {
        games: {
          'c6742f5c-2270-4cff-b29e-bc2528fb7182': {
            srid: 'c6742f5c-2270-4cff-b29e-bc2528fb7182',
            status: 'scheduled',
            start: '2016-06-17T02:10:00Z',
            srid_away: 'dcfd5266-00ce-442c-bc09-264cd20cf455',
            srid_home: 'ef64da7f-cfaf-4300-87b0-9313386b977c',
            title: '',
            game_number: 1,
            day_night: 'N',
            sport: 'mlb',
            timeRemaining: { duration: 18, decimal: 0.9999 },
          },
        },
        gameIds: ['c6742f5c-2270-4cff-b29e-bc2528fb7182'],
      },
    });

    const state = reducer(defaultState, responseWithTeams);
    assert.deepEqual(
      state.games,
      responseWithTeams.response.games
    );
    assert.deepEqual(
      state.mlb.gameIds,
      responseWithTeams.response.gameIds
    );

    // check that expiration was updated
    assert.notEqual(
      oldState.mlb.gamesExpireAt,
      state.mlb.gamesExpireAt
    );
  });

  it('should handle UPDATE_GAME', () => {
    const defaultResponse = {
      type: types.UPDATE_GAME,
      gameId: '30fba042-9c84-43ff-850d-06574ac05ab4',
      updatedFields: {
        status: 'inprogress',
        boxscore: {
          attendance: 0,
          weather: 'Indoor Temp:  F, Wind:   mph',
          srid_game: '30fba042-9c84-43ff-850d-06574ac05ab4',
          ts: 1470958010613,
          clock: '4:10',
          scheduled: '2016-08-11T23:00:00+00:00',
          summary: {
            venue: '216de6bf-bce0-409a-a9e7-90db8df1f7b9',
            week: '1d810a06-3f3b-4865-a0ba-f28091dd8d6f',
            season: '659d2bd0-c43e-4bb0-8503-9d576911d029',
            away: '22052ff7-c065-42ee-bc8f-c4691c50e624',
            home: 'e6aa13a4-0055-48a9-bc41-be28dc106929',
          },
          status: 'inprogress',
          quarter: 1,
        },
        timeRemaining: {
          duration: 49,
          decimal: 0.8167,
        },
      },
    };

    // return nothing if there is no current lineup to associate rosters with
    let oldState = reducer(defaultState, defaultResponse);
    assert.deepEqual(oldState.games, {});
    assert.deepEqual(oldState.mlb.gameIds, []);

    // check updatedFields merged in
    oldState = merge({}, defaultState, {
      games: {
        '30fba042-9c84-43ff-850d-06574ac05ab4': {
          srid: '30fba042-9c84-43ff-850d-06574ac05ab4',
          status: 'scheduled',
          start: '2016-06-17T02:10:00Z',
          srid_away: 'dcfd5266-00ce-442c-bc09-264cd20cf455',
          srid_home: 'ef64da7f-cfaf-4300-87b0-9313386b977c',
          title: '',
          game_number: 1,
          day_night: 'N',
          sport: 'mlb',
          timeRemaining: { duration: 18, decimal: 0.9999 },
        },
      },
    });

    oldState = reducer(oldState, defaultResponse);
    const game = oldState.games['30fba042-9c84-43ff-850d-06574ac05ab4'];

    assert.deepEqual(
      game.boxscore,
      defaultResponse.updatedFields.boxscore
    );
    assert.deepEqual(
      game.timeRemaining,
      defaultResponse.updatedFields.timeRemaining
    );
    assert.deepEqual(
      game.status,
      defaultResponse.updatedFields.status
    );
  });
});
