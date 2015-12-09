import _ from 'lodash'
import { createSelector } from 'reselect'

import { currentLineupsStatsSelector } from './current-lineups'

/**
 * Returns hours for provided timestamp with format like: 7pm
 * @param {Number} timestamp
 * @return {String}
 */
function getFormattedTime(timestamp) {
  let hours = new Date(timestamp).getHours()
  let time = (hours % 12 || 12) + (hours > 12 ? 'pm' : 'am')
  if(time == '12pm') time = '0am'

  return time
}

/**
 * The big scoreboard navigation selector that selects current lineups,
 * current draft groups, current user and some addition data for them.
 */
export const navScoreboardSelector = createSelector(
  currentLineupsStatsSelector,
  state => state.liveDraftGroups,
  state => state.currentBoxScores,
  state => state.user,

  (lineups, draftGroups, boxScores, user) => {
    const resultLineups = _.map(lineups, (lineup) => {
      return {
        id: lineup.id,
        name: lineup.name,
        time: getFormattedTime(lineup.start),
        contest: 'NBA', // TODO:
        points:  89,    // TODO:
        pmr:     lineup.totalMinutes,
        balance: "$" + lineup.potentialEarnings
      }
    })

    const loadedDraftGroups = _.filter(draftGroups, (dg) => {
      return dg.hasAllInfo === true
    })

    const resultDraftGroups = _.mapValues(loadedDraftGroups, (dg) => {
      return {
        id: dg.id,
        time: dg.start,  // TODO replace with start
        sport: dg.sport,
        start: dg.start,
        end: dg.end,
        boxScores: _.mapValues(dg.boxScores, (boxScore, id) => {
          return boxScores[id]
        })
      }
    })

    return {
      // TODO: No user data.
      user: {
        name: user.name       || '-',
        balance: user.balance || '-'
      },
      gamesByDraftGroup: resultDraftGroups, // TODO:
      lineups: resultLineups
    }
  }
)
