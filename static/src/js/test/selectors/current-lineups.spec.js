import { assert } from 'chai';
import size from 'lodash/size';
import { testDraftGroup, testGamesTimeRemaining } from './live-draft-groups.spec';
import {
  calcRosterFP,
  calcRosterTimeRemaining,
  compileRosterDetails,
  compileLineupStats,
  compileVillianLineup,
  myCurrentLineupsSelector,
} from '../../selectors/current-lineups';
import reducerLiveDraftGroups from '../../reducers/live-draft-groups';
import reducerSports from '../../reducers/sports';
import reducerCurrentLineups from '../../reducers/current-lineups';


// default lineup info
export const testLineup = {
  id: 5,
  contests: [1, 2, 3],
  name: 'Ultimate',
  roster: [200],
  draftGroup: 52,
  start: 1458255600000,
};

describe('selectors.currentLineups.calcRosterFP', () => {
  it('should return 0 when it does not exist', () => {
    assert.equal(calcRosterFP(), 0);
  });

  it('should return correct sum', () => {
    const roster = {
      0: { fp: 1 },
      1: { fp: 3 },
      2: { fp: 5 },
    };

    assert.equal(calcRosterFP(roster), 9);
  });
});

describe('selectors.currentLineups.calcRosterTimeRemaining', () => {
  it('should return no time remaining with invalid sport', () => {
    assert.deepEqual(calcRosterTimeRemaining(), { duration: 0, decimal: 0.00001 });
  });

  it('should return full time remaining with no roster', () => {
    assert.deepEqual(calcRosterTimeRemaining('nba'), { duration: 384, decimal: 0.9999 });
  });

  it('should return proper time with roster', () => {
    const roster = {
      0: { timeRemaining: { duration: 10 } },
      1: { timeRemaining: { duration: 20 } },
      2: { timeRemaining: { duration: 30 } },
    };
    assert.deepEqual(calcRosterTimeRemaining('nba', roster), { duration: 60, decimal: 0.1563 });
  });
});

describe('selectors.currentLineups.compileRosterDetails', () => {
  it('should return empty object if there is no roster', () => {
    assert.deepEqual(compileRosterDetails(), {});
  });

  it('should return same length as roster', () => {
    const rosterDetails = compileRosterDetails([200], testDraftGroup, testGamesTimeRemaining);
    assert.equal(size(rosterDetails), 1);
  });
});

describe('selectors.currentLineups.compileLineupStats', () => {
  it('should return empty object if draftGroup has not loaded yet', () => {
    assert.deepEqual(compileLineupStats(), {});
  });

  it('should return empty object if there is no draftGroup info yet', () => {
    assert.deepEqual(compileLineupStats({}, { hasAllInfo: false }), {});
  });

  it('should return basic info if there is no roster yet', () => {
    const lineup = {
      id: 5,
      name: 'Ultimate',
    };

    assert.deepEqual(compileLineupStats(lineup, testDraftGroup, testGamesTimeRemaining), {
      draftGroupId: 52,
      fp: 0,
      id: 5,
      name: 'Ultimate',
      roster: [],
      rosterDetails: {},
      sport: 'nba',
      start: undefined,
      timeRemaining: {
        decimal: 0.9999,
        duration: 384,
      },
    });
  });

  // note that we don't need to check contents of rosterDetails, already tested in live-draft-groups.spec.js
  it('should return correctly sized rosterDetails, roster if there is a roster', () => {
    const stats = compileLineupStats(testLineup, testDraftGroup, testGamesTimeRemaining);

    assert.equal(stats.roster.length, 1);
    assert.equal(size(stats.rosterDetails), 1);
  });
});

describe('selectors.currentLineups.compileVillianLineup', () => {
  it('should return empty object if draftGroup has not loaded yet', () => {
    assert.deepEqual(compileVillianLineup(), {});
  });

  it('should return empty object if there is no draftGroup info yet', () => {
    assert.deepEqual(compileVillianLineup({}, { hasAllInfo: false }), {});
  });

  // this should never happen
  // TODO check that Raven message worked here
  it('should return basic info if there is no roster yet', () => {
    assert.deepEqual(compileVillianLineup([], testDraftGroup, testGamesTimeRemaining), {
      fp: 0,
      id: 1,
      name: 'Top Owned',
      roster: [],
      rosterDetails: {},
      timeRemaining: {
        decimal: 0.9999,
        duration: 384,
      },
    });
  });

  // note that we don't need to check contents of rosterDetails, already tested in live-draft-groups.spec.js
  it('should return correctly sized rosterDetails, roster if there is a roster', () => {
    const stats = compileVillianLineup([200], testDraftGroup, testGamesTimeRemaining);

    assert.equal(stats.roster.length, 1);
    assert.equal(size(stats.rosterDetails), 1);
  });
});

// note how we don't need to test every situation of data coming in because we already did with compileLineupStats
describe('selectors.currentLineups.myCurrentLineupsSelector', () => {
  it('should return empty object if there are no lineups yet', () => {
    const state = {
      currentLineups: reducerCurrentLineups({}, { type: '' }),
      liveDraftGroups: reducerLiveDraftGroups({}, { type: '' }),
      sports: reducerSports({}, { type: '' }),
    };
    assert.deepEqual(myCurrentLineupsSelector(state), {});
  });

  it('should return mapped lineups', () => {
    const state = {
      currentLineups: { items: { 5: testLineup } },
      liveDraftGroups: { 52: testDraftGroup },
      sports: {
        games: {
          '47dcf0e0-f141-458e-8ef2-31d8f5f4a357': {
            timeRemaining: {
              decimal: 0.6,
              duration: 25,
            },
          },
        },
      },
    };

    assert.deepEqual(myCurrentLineupsSelector(state), {
      5: {
        draftGroupId: 52,
        fp: 4.25,
        id: 5,
        name: 'Ultimate',
        roster: [
          200,
        ],
        rosterDetails: {
          200: {
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
          },
        },
        sport: 'nba',
        start: 1458255600000,
        timeRemaining: {
          decimal: 0.0652,
          duration: 25,
        },
      },
    });
  });
});
