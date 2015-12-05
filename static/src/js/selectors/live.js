import { countBy as _countBy } from 'lodash'
import { createSelector } from 'reselect'
import { filter as _filter } from 'lodash'
import { map as _map } from 'lodash'
import { reduce as _reduce } from 'lodash'
import { forEach as _forEach } from 'lodash'

import log from '../lib/logging'


// Input Selectors
import { liveContestsStatsSelector } from './live-contests'
import { currentLineupsStatsSelector } from './current-lineups'


// returns:
// - If lineup mode:
//   - myLineup
//     - name
//     - points
//     - potential earnings
//     - pmr
//     - tmr
//
// - If contest mode:
//   - contestInfo
//     - title
//     - prize structure
//   - myLineup
//     - name
//     - contest title
//     - points (from lineup)
//     - standing
//       - find lineup in contest ranked lineups
//     - potential earnings
//       - use prize structure and standing
//     - pmr (from lineup)
//     - tmr (from lineup)
//   - opponentLineup
//     - points
//     - standing
//       - find lineup in contest ranked lineups
//     - potential earnings
//       - use prize structure and standing
//     - pmr
//     - tmr
export const liveSelector = createSelector(
  liveContestsStatsSelector,
  currentLineupsStatsSelector,
  state => state.live.mode,
  state => state.entries.hasRelatedInfo,

  (contestStats, currentLineupsStats, mode, hasRelatedInfo) => {
    log.debug('selectors.liveStatsSelector')

    let stats = {
      lineups: {}
    }

    // return if the data hasn't loaded yet
    if (hasRelatedInfo === false) {
      return {}
    }

    if (mode.myLineupId) {
      stats.lineups.mine = currentLineupsStats[mode.myLineupId]
    }

    if (mode.opponentLineupId) {
      stats.lineups.opponent = currentLineupsStats[mode.opponentLineupId]
    }

    if (mode.contestId) {
      stats.contest = contestStats[mode.contestId]
    }

    return stats
  }
)

