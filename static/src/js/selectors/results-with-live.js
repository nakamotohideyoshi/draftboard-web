import { createSelector } from 'reselect';
import { currentLineupsSelector } from './current-lineups';
import { liveContestsSelector } from './live-contests';
import { map as _map } from 'lodash';
import { merge as _merge } from 'lodash';
import { size as _size } from 'lodash';
import { uniq as _uniq } from 'lodash';
import { values as _values } from 'lodash';
import { dateNow } from '../lib/utils';


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
  liveContestsSelector,
  currentLineupsSelector,
  state => state.live.mode,
  state => state.entries,

  (contestStats, currentLineupsStats, mode, entries) => {
    const uniqueEntries = _uniq(_values(entries.items), 'lineup');

    const lineups = _map(uniqueEntries, (entry) => {
      let lineupInfo = {
        id: entry.lineup,
        name: entry.lineup_name,
        sport: entry.sport,
        players: [],
        entries: [],
        hasNotEnded: true,
      };

      if (entries.hasRelatedInfo === true) {
        const lineupSelector = currentLineupsStats[entry.lineup];
        const hasEnded = lineupSelector.draftGroup.closed !== null && lineupSelector.draftGroup.closed < dateNow();

        const lineupEntriesInfo = lineupSelector.upcomingContestsStats ||
          _map(lineupSelector.contestsStats, (contestEntry) => ({
            contest: {
              id: contestEntry.id,
              name: contestEntry.name,
            },
            final_rank: contestEntry.myEntryRank,
            payout: {
              amount: contestEntry.potentialEarnings,
            },
            hasNotEnded: hasEnded === false,
          })
        );

        lineupInfo = _merge(lineupInfo, {
          players: _map(lineupSelector.rosterDetails, (player) => ({
            player_id: player.id,
            full_name: player.info.name,
            fantasy_points: player.stats.fp,
            roster_spot: player.info.position,
            decimalRemaining: player.stats.decimalRemaining,
            player_meta: {
              srid: player.info.player_srid,
            },
          })),
          entries: lineupEntriesInfo,
          start: lineupSelector.start,
          liveStats: {
            entries: lineupSelector.entriesSize,
            points: lineupSelector.points,
            fees: lineupSelector.totalFees,
            winning: lineupSelector.totalPotentialEarnings,
          },
        });
      }

      return lineupInfo;
    });

    return {
      overall: {
        winnings: '0',
        possible: '0',
        buyins: '0',
        entries: _size(entries.items),
        contests: 0,
      },
      lineups,
      hasRelatedInfo: entries.hasRelatedInfo,
    };
  }
);
