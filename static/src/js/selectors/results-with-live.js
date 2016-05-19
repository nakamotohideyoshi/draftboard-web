import { createSelector } from 'reselect';
import { myCurrentLineupsSelector } from './current-lineups';
import { liveContestsSelector } from './live-contests';
import { map as _map } from 'lodash';
import { merge as _merge } from 'lodash';
import reduce from 'lodash/reduce';
import { size as _size } from 'lodash';
import { uniqBy as _uniqBy } from 'lodash';
import { values as _values } from 'lodash';
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
  state => state.currentLineups.items,
  state => state.watching,
  state => state.entries,

  (liveDraftGroups, contestsStats, currentLineupsStats, currentLineups, watching, entries) => {
    const uniqueEntries = _uniqBy(_values(entries.items), 'lineup');

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
        const lineup = currentLineups[entry.lineup];
        const draftGroup = liveDraftGroups[lineup.draftGroupId] || {};
        const hasEnded = draftGroup.closed !== null && draftGroup.closed < dateNow();

        const lineupEntriesInfo = lineupSelector.upcomingContestsStats ||
          _map(lineupSelector.contestsStats, (contestEntry) => ({
            contest: {
              id: contestEntry.id,
              name: contestEntry.name,
            },
            final_rank: contestEntry.myEntryRank,
            payout: {
              amount: contestEntry.potentialWinnings,
            },
            sport: entry.sport,
            hasNotEnded: hasEnded === false,
          })
        );

        lineupInfo = _merge(lineupInfo, {
          players: _map(lineupSelector.rosterDetails, (player) => ({
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
            entries: _size(lineup.contests),
            points: lineupSelector.points,
            totalBuyin: reduce(lineup.contests || {}, (sum, id) => sum + contestsStats[id].buyin, 0),
            potentialWinnings: {
              amount: 0,
              percentage: 100,
            },
          },
        });

        if (lineupSelector.hasOwnProperty('contestsStats')) {
          lineupInfo.potentialWinnings = calcTotalPotentialEarnings(entries, lineupSelector.contestsStats);
        }
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
