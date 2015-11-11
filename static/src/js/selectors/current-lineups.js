import { countBy as _countBy } from 'lodash'
import { createSelector } from 'reselect'
import { filter as _filter } from 'lodash'
import { map as _map } from 'lodash'
import { reduce as _reduce } from 'lodash'

import log from '../lib/logging'


// Input Selectors
import { liveContestsStatsSelector } from './live-contests'


// Crazy selector that
// - loops through the entries per lineup and calculates potential earnings
// - loops through the players per lineup and calculates PMR
export const currentLineupsStatsSelector = createSelector(
  liveContestsStatsSelector,
  state => state.liveDraftGroups,
  state => state.entries.items,
  state => state.currentLineups.items,
  state => state.entries.hasRelatedInfo,

  (contestStats, boxScores, entries, lineups, hasRelatedInfo) => {
    log.debug('selectors.currentLineupsStatsSelector')

    if (hasRelatedInfo === false) {
      return {}
    }

    const liveLineups = _filter(lineups, function(lineup) {
      return lineup.start < Date.now()
    })

    return _map(liveLineups, (lineup) => {
      let boxScores = liveDraftGroups[lineup.draft_group].boxScores

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