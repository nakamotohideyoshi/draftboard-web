import { createSelector } from 'reselect';
import { myCurrentLineupsSelector } from './current-lineups';
import { liveContestsSelector } from './live-contests';
import map from 'lodash/map';
import merge from 'lodash/merge';
import reduce from 'lodash/reduce';
import size from 'lodash/size';
import { dateNow } from '../lib/utils';
import { calcTotalPotentialEarnings, calcEntryContestStats } from './watching';
import log from '../lib/logging.js';


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
    if (
        !currentLineups ||
        !currentLineups.hasRelatedInfo === true ||
        !contestsStats ||
        !Object.keys(contestsStats).length > 0 ||
        !currentLineupsStats
    ) {
      log.info('returning empty resultswitlive');
      return {};
    }

    const lineups = map(currentLineups.items, (lineup) => {
      let lineupInfo = {
        id: lineup.id,
        name: lineup.name,
        sport: lineup.sport,
        players: [],
        entries: [],
        hasNotEnded: true,
      };

      // hack, need to find better way to know when contests are loaded
      const firstContestsStats = contestsStats[Object.keys(contestsStats)[0]];

      if (
        currentLineups.hasRelatedInfo === true &&
        firstContestsStats &&
        Object.keys(firstContestsStats).length > 0 &&
        currentLineupsStats.hasOwnProperty(lineup.id)
      ) {
        const lineupSelector = currentLineupsStats[lineup.id];
        const draftGroup = liveDraftGroups[lineup.draftGroup] || {};
        const hasEnded = draftGroup.closed !== null && draftGroup.closed < dateNow();

        let lineupEntriesInfo = [];
        if (lineupSelector.upcomingContestsStats) {
          lineupEntriesInfo = lineupSelector.upcomingContestsStats;
        } else {
          const contestsStatsWithRank = calcEntryContestStats(lineupSelector, lineup.contests, contestsStats);

          lineupEntriesInfo = map(lineup.contests, (contestId) => {
            const contestInfo = contestsStatsWithRank[contestId];

            return {
              contest: {
                id: contestInfo.id,
                name: contestInfo.name,
              },
              final_rank: contestInfo.myEntryRank,
              payout: {
                amount: contestInfo.potentialWinnings,
              },
              sport: lineup.sport,
              hasNotEnded: hasEnded === false,
            };
          });
        }

        lineupInfo = merge(lineupInfo, {
          players: map(lineupSelector.roster, (playerId) => {
            const player = lineupSelector.rosterDetails[playerId];

            return {
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
              salary: draftGroup.playersInfo && draftGroup.playersInfo[player.id].salary,
            };
          }),
          entries: lineupEntriesInfo,
          start: lineup.start,
          draftGroupId: draftGroup.id,
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

        return lineupInfo;
      }

      // otherwise don't return anything
    });

    log.info('succesfully returning resultswitlive');
    return {
      overall: {
        winnings: 0,
        possible: 0,
        buyins: 0,
        entries: size(lineups),
        contests: 0,
      },
      lineups,
      hasRelatedInfo: currentLineups.hasRelatedInfo,
    };
  }
);
