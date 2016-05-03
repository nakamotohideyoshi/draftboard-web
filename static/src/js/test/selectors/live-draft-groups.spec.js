import { assert, expect } from 'chai';
import { assembleCurrentPlayer } from '../../selectors/live-draft-groups';


// default player info
export const testPlayerInfo = {
  game_srid: '47dcf0e0-f141-458e-8ef2-31d8f5f4a357',
  name: 'Foo Bar',
  position: 'SG',
  player_srid: '2733be7a-cfc6-4787-8405-371db5af0399',
  team_alias: 'MEM',
  team_srid: '583ec8d4-fb46-11e1-82cb-f4ce4684ea4c',
};
export const testGamesTimeRemaining = {
  '47dcf0e0-f141-458e-8ef2-31d8f5f4a357': {
    decimal: 0.6,
    duration: 25,
  },
};
export const testDraftGroup = {
  playersInfo: {
    200: testPlayerInfo,
  },
  playersStats: {
    200: {
      fp: 4.25,
    },
  },
  sport: 'nba',

  // used in compileLineupStats and higher
  id: 52,
  hasAllInfo: true,
};


describe('selectors.liveDraftGroups.assembleCurrentPlayer', () => {
  it('should return nothing when it does not exist', () => {
    const draftGroup = {
      playersInfo: {},
    };

    assert.deepEqual(assembleCurrentPlayer(200, draftGroup, {}), {});
  });

  it('should return fp of 0 when there is no fp in stats', () => {
    const draftGroup = {
      playersInfo: {
        200: testPlayerInfo,
      },
      playersStats: {},
      sport: 'nba',
    };

    const player = assembleCurrentPlayer(200, draftGroup, {});
    expect(player.fp).to.equal(0);
  });

  it('should return full timeRemaining when the game has not started', () => {
    const draftGroup = {
      playersInfo: {
        200: testPlayerInfo,
      },
      playersStats: {},
      sport: 'nba',
    };

    const player = assembleCurrentPlayer(200, draftGroup, {});
    assert.deepEqual(player.timeRemaining, {
      decimal: 0.9999,
      duration: 48,
    });
  });

  it('should return expected fields', () => {
    assert.deepEqual(assembleCurrentPlayer(200, testDraftGroup, testGamesTimeRemaining), {
      fp: 4.25,
      gameSRID: '47dcf0e0-f141-458e-8ef2-31d8f5f4a357',
      id: 200,
      name: 'Foo Bar',
      position: 'SG',
      srid: '2733be7a-cfc6-4787-8405-371db5af0399',
      teamAlias: 'MEM',
      teamSRID: '583ec8d4-fb46-11e1-82cb-f4ce4684ea4c',
      timeRemaining: {
        decimal: 0.6,
        duration: 25,
      },
    });
  });
});
