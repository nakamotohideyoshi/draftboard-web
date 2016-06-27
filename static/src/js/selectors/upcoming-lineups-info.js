import { createSelector } from 'reselect';
import forEach from 'lodash/forEach';
import countBy from 'lodash/countBy';
import filter from 'lodash/filter';

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
  (state) => state.contestPools.allContests,
  (state) => state.pollingTasks,
  (lineups, entries, contests, pollingTasks) => {
    const info = {};
    const feeMap = {};
    // The contest pools the lineup is entered into
    const contestMap = {};
    const lineupEntryRequestMap = {};
    const unregisterRequestMap = {};

    // Count the entries for each lineup.
    const entryMap = countBy(entries, (entry) => entry.lineup);


    // Determine fees.
    forEach(lineups, (lineup) => {
      // Attach entryRequests and unregister requests for each lineup & contest.
      if (pollingTasks) {
        // Find all contest entry requests for this lineup.
        const lineupEntryRequests = filter(pollingTasks, { lineupId: lineup.id, requestType: 'entry' });
        lineupEntryRequestMap[lineup.id] = {};
        // Insert each of the lineup's entry requests, grouped by contestPoolId,
        forEach(lineupEntryRequests, (entryRequest) => {
          lineupEntryRequestMap[lineup.id][entryRequest.contestPoolId] = entryRequest;
        });

        // Find all entry unregister requests for this lineup.
        const unregisterRequests = filter(pollingTasks, { lineupId: lineup.id, requestType: 'unregister' });
        unregisterRequestMap[lineup.id] = {};
        // Insert each of the lineup's unregister requests, grouped by contestPoolId,
        forEach(unregisterRequests, (request) => {
          unregisterRequestMap[lineup.id][request.entryId] = request;
        });
      }


      // Find all entries for the lineup.
      const lineupEntries = filter(entries, (entry) => entry.lineup === lineup.id);
      let lineupFeeTotal = 0;
      const lineupContestPools = {};

      // for each entry, look up the contest it's entered into, then add up the fees.
      forEach(lineupEntries, (lineupEntry) => {
        if (contests.hasOwnProperty(lineupEntry.contest_pool)) {
          lineupFeeTotal = lineupFeeTotal + contests[lineupEntry.contest_pool].buyin;
          // Grab all of the entries for this lineup & contest pool combo.
          const lineupContestPoolEntries = filter(entries, { contest_pool: lineupEntry.contest_pool });

          lineupContestPools[lineupEntry.contest_pool] = {
            entryCount: Object.keys(lineupContestPoolEntries).length,
            entries: lineupContestPoolEntries,
            contest: contests[lineupEntry.contest_pool] || {},
          };
        }
      });

      // Add it to our feeMap + contesetMap
      feeMap[lineup.id] = lineupFeeTotal;
      contestMap[lineup.id] = lineupContestPools;
    });

    // Add each lineup entry to the final info object
    forEach(lineups, (lineup) => {
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
        unregisterRequests: unregisterRequestMap[lineup.id] || {},
      };
    });


    return info;
  }
);
