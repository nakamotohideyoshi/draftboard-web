import { createSelector } from 'reselect';
import { forEach as _forEach } from 'lodash';
import { countBy as _countBy } from 'lodash';
import { filter as _filter } from 'lodash';

/**
This selector will give us entry count and fee information about a user's upcoming lineups.

Exampe of output:
{
  // lineup ID
  34: {
    entries: 6, // total number of entries
    contests: {
      3: 1, // contestId: number of entries.
      34: 2,
      2: 3,
    },
    fees: 135 // fee total
  },
  78: {
    entries: 1,
    contests: {3: 1},
    fees: 10
  }
  ...
}
*/


// filter the contests by sport.
export const upcomingLineupsInfo = createSelector(
  (state) => state.upcomingLineups.lineups,
  (state) => state.contestPoolEntries.entries,
  (state) => state.upcomingContests.allContests,
  (state) => state.pollingTasks,
  (lineups, entries, contests, entryRequests) => {
    const info = {};
    const feeMap = {};
    // The contest pools the lineup is entered into
    const contestMap = {};
    const lineupEntryRequestMap = {};

    // Count the entries for each lineup.
    const entryMap = _countBy(entries, (entry) => entry.lineup);


    // Determine fees.
    _forEach(lineups, (lineup) => {
      // Attach entryRequests for each lineup & contest.
      if (entryRequests) {
        // Find all contest entry requests for this lineup.
        const lineupEntryRequests = _filter(entryRequests, { lineupId: lineup.id });
        lineupEntryRequestMap[lineup.id] = {};
        // Insert each of the lineup's entry requests, grouped by contestPoolId,
        _forEach(lineupEntryRequests, (entryRequest) => {
          lineupEntryRequestMap[lineup.id][entryRequest.contestPoolId] = entryRequest;
        });
      }


      // Find all entries for the lineup.
      const lineupEntries = _filter(entries, (entry) => entry.lineup === lineup.id);
      let lineupFeeTotal = 0;
      const lineupContestPools = [];

      // for each entry, look up the contest it's entered into, then add up the fees.
      _forEach(lineupEntries, (lineupEntry) => {
        if (contests.hasOwnProperty(lineupEntry.contest_pool)) {
          lineupFeeTotal = lineupFeeTotal + contests[lineupEntry.contest_pool].buyin;
          // Take a tally to count up all of the contest pool entries this lineup has.
          let currentEntryCount = 0;

          if (
            lineupContestPools[contests[lineupEntry.contest_pool].id] &&
            lineupContestPools[contests[lineupEntry.contest_pool].id].hasOwnProperty('entryCount')
          ) {
            currentEntryCount = lineupContestPools[contests[lineupEntry.contest_pool].id].entryCount;
          }

          lineupContestPools[contests[lineupEntry.contest_pool].id] = {
            entryCount: currentEntryCount + 1,
            entry: lineupEntry,
            contest: contests[lineupEntry.contest_pool] || {},
          };
        }
      });
      // Add it to our feeMap + contesetMap
      feeMap[lineup.id] = lineupFeeTotal;
      contestMap[lineup.id] = lineupContestPools;
    });

    // Add each lineup entry to the final info object
    _forEach(lineups, (lineup) => {
      info[lineup.id] = {
        id: lineup.id,
        draft_group: lineup.draft_group,
        fantasy_points: lineup.fantasy_points,
        sport: lineup.sport,
        name: lineup.name,
        totalEntryCount: entryMap[lineup.id] || 0,
        contestPoolEntries: contestMap[lineup.id],
        fees: feeMap[lineup.id],
        entryRequests: lineupEntryRequestMap[lineup.id] || {},
      };
    });

    return info;
  }
);
