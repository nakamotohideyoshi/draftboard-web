import {createSelector} from 'reselect';
import {forEach as _forEach} from 'lodash';
import {countBy as _countBy} from 'lodash';
import {where as _where} from 'lodash';
import {filter as _filter} from 'lodash';

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

// All the upcoming lineups in the state.
const lineups = (state) => state.upcomingLineups.lineups;
const entries = (state) => state.entries.items;
const contests = (state) => state.upcomingContests.allContests;
const entryRequests = (state) => state.entryRequests;

// filter the contests by sport.
export const upcomingLineupsInfo = createSelector(
  [lineups, entries, contests, entryRequests],
  (lineups, entries, contests, entryRequests) => {
    let info = {};
    let feeMap = {};
    let contestMap = {};
    let lineupEntryRequestMap = {};

    // Count the entries for each lineup.
    let entryMap = _countBy(entries, function(entry) {
      return entry.lineup;
    });


    // Determine fees.
    _forEach(lineups, function(lineup) {
      // Attach entryRequests for each lineup & contest.
      if (entryRequests) {
        // Find all contest entry requests for this lineup.
        let lineupEntryRequests = _filter(entryRequests, {lineupId: lineup.id});
        lineupEntryRequestMap[lineup.id] = {};
        // Insert each of the lineup's entry requests, grouped by contestId,
        _forEach(lineupEntryRequests, function(entryRequest) {
          lineupEntryRequestMap[lineup.id][entryRequest.contestId] = entryRequest;
        })
      }


      // Find all entries for the lineup.
      let lineupEntries = _where(entries, {'lineup': lineup.id});
      let lineupFeeTotal = 0;
      let lineupContests = [];

      // for each entry, look up the contest it's entered into, then add up the fees.
      _forEach(lineupEntries, function(lineupEntry) {
        if (contests.hasOwnProperty(lineupEntry.contest)) {
          lineupFeeTotal = lineupFeeTotal + contests[lineupEntry.contest].buyin;
          lineupContests.push(contests[lineupEntry.contest].id);
        }
      });
      // Add it to our feeMap + contesetMap
      feeMap[lineup.id] = lineupFeeTotal;
      contestMap[lineup.id] = lineupContests;
    });

    // Add each lineup entry to the final info object
    _forEach(lineups, function(lineup) {
      info[lineup.id] = {
        id: lineup.id,
        draft_group: lineup.draft_group,
        fantasy_points: lineup.fantasy_points,
        sport: lineup.sport,
        name: lineup.name,
        entries: entryMap[lineup.id] || 0,
        contests: contestMap[lineup.id],
        fees: feeMap[lineup.id],
        entryRequests: lineupEntryRequestMap[lineup.id] || {}
      };
    });


    return info;
  }
);
