import { createSelector } from 'reselect';
import { myCurrentLineupsSelector } from './current-lineups';
import { liveContestsSelector } from './live-contests';
import map from 'lodash/map';
import merge from 'lodash/merge';
import reduce from 'lodash/reduce';
import size from 'lodash/size';
import { dateNow } from '../lib/utils';
import { calcTotalPotentialEarnings } from './watching';


/**
 * Fancy Redux reselect selector that compiles together relevant live information.
 * Returns an object with an architecture of:
 *
 * lineups
 *   mine
 *   opponent (optional)
 * contest
 */
export const resultsWithLive = createSelector(
  state => state.liveDraftGroups,
  state => liveContestsSelector(state),
  state => myCurrentLineupsSelector(state),
  state => state.currentLineups,

  (liveDraftGroups, contestsStats, currentLineupsStats, currentLineups) => {
    const lineups = map(currentLineups.items, (lineup) => {
      let lineupInfo = {
        id: lineup.id,
        name: lineup.name,
        sport: lineup.sport,
        players: [],
        entries: [],
        hasNotEnded: true,
      };

      if (currentLineups.hasRelatedInfo === true) {
        const lineupSelector = currentLineupsStats[lineup.id];
        const draftGroup = liveDraftGroups[lineup.draftGroupId] || {};
        const hasEnded = draftGroup.closed !== null && draftGroup.closed < dateNow();

        const lineupEntriesInfo = lineupSelector.upcomingContestsStats ||
          map(lineupSelector.contestsStats, (contestEntry) => ({
            contest: {
              id: contestEntry.id,
              name: contestEntry.name,
            },
            final_rank: contestEntry.myEntryRank,
            payout: {
              amount: contestEntry.potentialWinnings,
            },
            sport: lineup.sport,
            hasNotEnded: hasEnded === false,
          })
        );

        lineupInfo = merge(lineupInfo, {
          players: map(lineupSelector.rosterDetails, (player) => ({
            player_id: player.id,
            full_name: player.name,
            fantasy_points: player.fp,
            roster_spot: player.position,
            timeRemaining: {
              decimal: player.timeRemaining.decimal,
            },
            player_meta: {
              srid: player.srid,
            },
          })),
          entries: lineupEntriesInfo,
          start: lineup.start,
          liveStats: {
            entries: size(lineup.contests),
            points: lineupSelector.fp,
            totalBuyin: reduce(lineup.contests || {}, (sum, id) => {
              if (!contestsStats[id]) return sum;
              return sum + contestsStats[id].buyin;
            }, 0),
            potentialWinnings: {
              amount: 0,
              percentage: 100,
            },
          },
        });

        if (lineupSelector.hasOwnProperty('contestsStats')) {
          lineupInfo.potentialWinnings = calcTotalPotentialEarnings(currentLineups, lineupSelector.contestsStats);
        }
      }

      return lineupInfo;
    });

    return {
      overall: {
        winnings: '0',
        possible: '0',
        buyins: '0',
        entries: size(lineups),
        contests: 0,
      },
      lineups,
      hasRelatedInfo: currentLineups.hasRelatedInfo,
    };
  }
);
