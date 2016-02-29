import { forEach as _forEach } from 'lodash';
import { filter as _filter } from 'lodash';
import { groupBy as _groupBy } from 'lodash';
import { map as _map } from 'lodash';
import { merge as _merge } from 'lodash';
import { reduce as _reduce } from 'lodash';
import { sortBy as _sortBy } from 'lodash';
import { compileLineupStats } from './current-lineups';
import { createSelector } from 'reselect';
import { dateNow } from '../lib/utils';
import log from '../lib/logging';


/*
 * Takes the contest lineups, converts each out of bytes, then adds up fantasy total
 *
 * @param {Object} (required) Original set of players from API
 * @param {Object} (required) Final, centralized associative array of players
 * @param {String} (required) Which lineup, mine or opponent?
 *
 * @return {Object, Object} Return the lineups, sorted highest to lowest points
 */
export const rankContestLineups = (contest, draftGroup, games, prizeStructure, relevantPlayers) => {
  const lineups = contest.lineups;
  const lineupsUsernames = contest.lineupsUsernames || {};

  const lineupsStats = {};
  const lineupsWithValue = [];
  let rankedLineups = [];

  _forEach(lineups, (lineup, id) => {
    const stats = compileLineupStats(lineup, draftGroup, games, relevantPlayers);

    if (id in lineupsUsernames) {
      stats.user = lineupsUsernames[id].user;
    }

    rankedLineups.push(stats);
    lineupsStats[id] = stats;
  });

  // sort then make just ID
  rankedLineups = _sortBy(rankedLineups, 'points').reverse();
  rankedLineups = _map(rankedLineups, (lineup) => lineup.id);

  // set standings for use in contests pane
  _forEach(rankedLineups, (lineupId, index) => {
    const lineupStats = lineupsStats[lineupId];

    lineupStats.rank = parseInt(index, 10) + 1;
    lineupStats.potentialEarnings = 0;

    if ('ranks' in prizeStructure && parseInt(index, 10) in prizeStructure.ranks) {
      lineupStats.potentialEarnings = prizeStructure.ranks[index].value;
    }

    lineupsWithValue.push({
      lineupId,
      rankValue: lineupStats.potentialEarnings,
      points: lineupStats.points,
    });
  });

  // group by points
  const groupedByValue = _filter(
    _groupBy(
      lineupsWithValue, (i) => i.points
    ),
    (group) => group.length > 1
  );

  // loop through each tie and split the sum
  _forEach(groupedByValue, (group) => {
    // sum up the entries potential earnings
    const total = _reduce(group, (sum, entry) => sum + entry.rankValue, 0);

    // if they are actually making money
    if (total > 0) {
      // then we split out to three decimal points
      let split = total / group.length;

      // round down to the nearest cent, then set values
      split = Math.floor(split * 100) / 100;

      _forEach(group, (entry) => {
        lineupsStats[entry.lineupId].potentialEarnings = split;
      });
    }
  });

  return {
    rankedLineups,
    lineups: lineupsStats,
    hasLineupsUsernames: 'lineupsUsernames' in contest,
  };
};

/**
 * Redux reselect selector to compile all relevant information for contests
 */
export const liveContestsSelector = createSelector(
  state => state.liveContests,
  state => state.liveDraftGroups,
  state => state.sports.games,
  state => state.prizes,
  state => state.entries.hasRelatedInfo,
  state => state.livePlayers.relevantPlayers,

  (contests, draftGroups, games, prizes, hasRelatedInfo, relevantPlayers) => {
    // do not show if we don't have data yet
    if (hasRelatedInfo === false) {
      return {};
    }

    const contestsStats = {};
    let prizeStructure = {};

    _forEach(contests, (contest, id) => {
      // This seems to be a recurring issue. I believe it has something to do with the logged-in
      // user not having any lineups. For now we'll skip things if we don't have any contest.info.
      if (!contest.info) {
        return;
      }

      const draftGroup = draftGroups[contest.info.draft_group];

      // Make sure we have the prize structure before adding it.
      if (prizes.hasOwnProperty(contest.info.prize_structure)) {
        prizeStructure = prizes[contest.info.prize_structure].info;
      }

      const stats = {
        buyin: contest.info.buyin,
        entriesCount: contest.info.entries,
        id: contest.id,
        name: contest.info.name,
        percentageCanWin: prizeStructure.payout_spots / contest.info.entries * 100,
        start: contest.info.start,
      };

      // if we haven't started, then don't bother ranking
      if (new Date(contest.start) > dateNow()) {
        log.trace('liveContestsSelector() - Contest has not started', id, new Date(contest.start), dateNow());
        contestsStats[id] = stats;
        return;
      }

      // if undefined and we're still trying, then return. occurs when cached for days
      if (draftGroup === undefined) {
        log.trace('liveContestsSelector() - draftGroup is undefined for contest', id);
        contestsStats[id] = stats;
        return;
      }

      contestsStats[id] = _merge(
        stats,
        rankContestLineups(contest, draftGroup, games, prizeStructure, relevantPlayers)
      );
    });

    return contestsStats;
  }
);
