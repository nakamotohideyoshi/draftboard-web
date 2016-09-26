import { assert } from 'chai';
import { testLineup } from './current-lineups.spec';
import {
  rankContestLineups,
} from '../../selectors/live-contests';
import { dateNow } from '../../lib/utils';


// default lineup usernames
export const testUsersByLineup = {
  5: {
    user: {
      username: 'exampleUsername',
    },
  },
};

describe('selectors.liveContests.rankContestLineups', () => {
  it('should return empty object if the contest has not started', () => {
    assert.deepEqual(rankContestLineups({}, { start: dateNow() + 1000 }), {});
  });

  it('should return empty object if the draft group has no info', () => {
    assert.deepEqual(rankContestLineups({}, { start: dateNow() - 1000 }, { hasAllInfo: false }), {});
  });

  it('should return shell if we do not have lineups yet', () => {
    assert.deepEqual(rankContestLineups(
      {},
      { start: dateNow() - 1000, lineups: {} },
      { hasAllInfo: true }
    ), {
      hasLineupsUsernames: false,
      lineups: {},
      rankedLineups: [],
    });
  });

  it('should return shell if we do not have prize ranks yet', () => {
    assert.deepEqual(rankContestLineups(
      {
        lineups: {
          5: testLineup,
        },
      },
      {
        start: dateNow() - 1000,
      },
      {
        hasAllInfo: true,
        boxScores: {},
        playersInfo: {},
        playersStats: {},
        infoExpiresAt: 1458255600000,
        fpExpiresAt: 1458255600000,
        boxscoresExpiresAt: 1458255600000,
      }
    ), {
      hasLineupsUsernames: false,
      lineups: {},
      rankedLineups: [],
    });
  });
});
