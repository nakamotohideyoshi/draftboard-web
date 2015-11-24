import _ from 'lodash';
import { createSelector } from 'reselect'

import { currentLineupsStatsSelector } from './current-lineups';

/**
 * Returns hours for provided timestamp with format like: 7pm
 * @param {Number} timestamp
 * @return {String}
 */
function getFormattedTime(timestamp) {
  let hours = new Date(timestamp).getHours();
  let time = (hours % 12 || 12) + (hours > 12 ? 'pm' : 'am')
  if(time == '12pm') time = '0am';

  return time;
}

/**
 * The big scoreboard navigation selector that selects current lineups,
 * current draft groups, current user and some addition data for them.
 */
export const navScoreboardSelector = createSelector(
  currentLineupsStatsSelector,
  state => state.liveDraftGroups,
  state => state.user,

  (lineups, draftGroups, user) => {
    const resultLineups = _.map(lineups, (lineup) => {
      return {
        id: lineup.id,
        name: lineup.name,
        time: getFormattedTime(lineup.start),
        contest: 'NBA', // TODO:
        points:  89,    // TODO:
        pmr:     lineup.totalMinutes,
        balance: "$" + lineup.potentialEarnings
      };
    });

    const resultDraftGroups = _.map(draftGroups, (dg) => {
      return {
        id:      dg.id,
        time:    getFormattedTime(dg.expiresAt),     // TODO:
        players: _.map(dg.boxScores, bs => bs.model) // TODO:
      }
    });

    return {
      // TODO: No user data.
      user: {
        name: user.name       || '-',
        balance: user.balance || '-'
      },
      games: {
        "NBA": resultDraftGroups // TODO:
      },
      lineups: resultLineups
    };
  }
)
