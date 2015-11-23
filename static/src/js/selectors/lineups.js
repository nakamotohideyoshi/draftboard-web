import { countBy as _countBy } from 'lodash'
import { createSelector } from 'reselect'
import { filter as _filter } from 'lodash'
import { reduce as _reduce } from 'lodash'


// Input Selectors
import { contestsStatsSelector } from './contests'
const boxScoresSelector = (state) => state.boxScores.items
const entriesSelector = (state) => state.entries.items
const lineupsSelector = (state) => state.lineups.items
const entriesHasRelatedInfoSelector = (state) => state.entries.hasRelatedInfo


// Crazy selector that
// - loops through the entries per lineup and calculates potential earnings
// - loops through the players per lineup and calculates PMR
export const lineupsStatsSelector = createSelector(
  [boxScoresSelector, entriesSelector, contestsStatsSelector, lineupsSelector, entriesHasRelatedInfoSelector],
  (boxScores, entries, contestStats, lineups, hasRelatedInfo) => {
    if (hasRelatedInfo === false) {
      return {}
    }

    const liveLineups = _filter(lineups, function(lineup) {
      return lineup.start < Date.now()
    })

    return _map(liveLineups, (lineup) => {
      let info = {
        id: lineup.id,
        name: lineup.name,
        start: lineup.start,
        totalMinutes: lineup.totalMinutes
      }

      if (lineup.start >= Date.now()) {
        return info
      }

      info.minutesRemaining = _reduce(players, (player) => {
        return boxScores[player.match].timeRemaining
      })

      info.potentialEarnings = _reduce(entries, (total, id) => {
        return total + contestStats[id].potentialEarnings
      })

      return info
    })
  }
)