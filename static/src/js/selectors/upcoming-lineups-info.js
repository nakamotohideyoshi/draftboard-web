import {matchFilter} from './filters'
import {createSelector} from 'reselect'
import {forEach as _forEach, countBy as _countBy, where as _where} from 'lodash'


/**
This selector will give us entry count and fee information about a user's upcoming lineups.

Exampe of output:
{
  // lineup ID
  34: {
    entries: 6, // number of entries
    contests: [3, 34, 2, 34 ,25, 34],
    fees: 135 // fee total
  },
  78: {
    entries: 1,
    contests: [3],
    fees: 10
  }
  ...
}
*/

// All the upcoming lineups in the state.
const lineups = (state) => state.upcomingLineups.lineups
const entries = (state) => state.entries.items
const contests = (state) => state.upcomingContests.allContests


// filter the contests by sport.
export const upcomingLineupsInfo = createSelector(
  [lineups, entries, contests],
  (lineups, entries, contests) => {
    let info = {}
    let feeMap = {}
    let contestMap = {}

    // Count the entries for each lineup.
    let entryMap = _countBy(entries, function(entry) {
      return entry.lineup
    })

    // Determine fees.
    _forEach(lineups, function(lineup) {
      // Find all entries for the lineup.
      let lineupEntries = _where(entries, {'lineup': lineup.id})
      let lineupFeeTotal = 0
      let lineupContests = []

      // for each entry, look up the contest it's entered into, then add up the fees.
      _forEach(lineupEntries, function(lineupEntry) {
        lineupFeeTotal = lineupFeeTotal + contests[lineupEntry.contest].buyin
        lineupContests.push(contests[lineupEntry.contest].id)
      })
      // Add it to our feeMap + contesetMap
      feeMap[lineup.id] = lineupFeeTotal
      contestMap[lineup.id] = lineupContests
    })

    // Add each lineup entry to the final info object
    _forEach(lineups, function(lineup) {
      info[lineup.id] = {
        entries: entryMap[lineup.id] || 0,
        contests: contestMap[lineup.id],
        fees: feeMap[lineup.id]
      }
    })

    return info
  }
)
