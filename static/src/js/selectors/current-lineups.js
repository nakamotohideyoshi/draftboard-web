import { countBy as _countBy } from 'lodash'
import { createSelector } from 'reselect'
import { filter as _filter } from 'lodash'
import { map as _map } from 'lodash'
import { reduce as _reduce } from 'lodash'
import { forEach as _forEach } from 'lodash'

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

  (contestStats, liveDraftGroups, entries, lineups, hasRelatedInfo) => {
    log.debug('selectors.currentLineupsStatsSelector')

    if (hasRelatedInfo === false) {
      return {}
    }

    const liveLineups = _filter(lineups, function(lineup) {
      return lineup.start < Date.now()
    })

    let liveLineupsStats = {}
    _forEach(liveLineups, (lineup) => {
      const liveDraftGroup = liveDraftGroups[lineup.draft_group]

      let stats = {
        id: lineup.id,
        name: lineup.name,
        start: lineup.start,
        totalMinutes: lineup.roster.length * 48
      }

      if (lineup.start >= Date.now()) {
        liveLineupsStats[lineup.id] = stats
        return
      }

      stats.minutesRemaining = _reduce(lineup.roster, (timeRemaining, playerId) => {
        const player = liveDraftGroup.playersInfo[playerId]
        const game = liveDraftGroup.boxScores[player.game_srid]

        // if the game hasn't started, then give full minutes remaining
        if (game === undefined) {
          return timeRemaining + 48
        }

        return timeRemaining + game.timeRemaining
      }, 0)

      let potentialEarnings = 0
      _forEach(entries, (entry) => {
        potentialEarnings += contestStats[entry.contest].entriesStats[entry.lineup].potentialEarnings
      })
      stats.potentialEarnings = potentialEarnings

      liveLineupsStats[lineup.id] = stats
    })

    return liveLineupsStats
  }
)