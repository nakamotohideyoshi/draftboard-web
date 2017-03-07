import filter from 'lodash/filter';
import forEach from 'lodash/forEach';
import groupBy from 'lodash/groupBy';
import log from '../lib/logging';
import map from 'lodash/map';
import mapValues from 'lodash/mapValues';
import merge from 'lodash/merge';
import orderBy from 'lodash/orderBy';
import reduce from 'lodash/reduce';
import values from 'lodash/values';
import zipObject from 'lodash/zipObject';
import { compileLineupStats } from './current-lineups';
import { createSelector } from 'reselect';
import { dateNow } from '../lib/utils';
import { gamesTimeRemainingSelector } from './sports';

// get custom logger for actions
const logSelector = log.getLogger('selector');

/**
 * Calculate potential earnings based on rank and prize structure
 * @param  {object} lineups         Lineups made from compileLineupStats
 * @param  {array}  rankedLineupIDs List of lineup IDs, ranked by desc fp
 * @param  {object} prizeRanks      Object with key of rank, value of how much you win
 * @return {object}                 Returns an object with key of lineup ID, value is potential winnings
 */
const calcContestLineupsValues = (lineups, rankedLineupIDs, prizeRanks) => {
  // generate rank, winnings for all entries in contest
  const lineupsValues = zipObject(rankedLineupIDs, map(rankedLineupIDs, (lineupId, index) => {
    const rankInfo = prizeRanks[index] || {};
    const lineup = lineups[lineupId] || {};
    return {
      fp: lineup.fp || 0,  // default to 0 while loading
      lineupId,
      potentialWinnings: rankInfo.value || 0,  // default winnings to 0
      rank: index + 1,  // since index starts at 0 we have to bump up by 1
    };
  }));

  // group by points
  const groupedByFP = groupBy(lineupsValues, (lineup) => lineup.fp);
  const tiedLineups = filter(groupedByFP, (group) => group.length > 1);

  // loop through each tie and split the sum
  forEach(tiedLineups, (group) => {
    // sum up the entries potential earnings
    const total = reduce(group, (sum, entry) => sum + entry.potentialWinnings, 0);

    // if they are actually making money
    if (total > 0) {
      // then we split out to two decimal points
      let split = total / group.length;
      split = Math.floor(split * 100) / 100;

      forEach(group, (entry) => {
        lineupsValues[entry.lineupId].potentialWinnings = split;
      });
    }
  });

  // only return the two fields we need
  return mapValues(lineupsValues, (lineup) => ({
    potentialWinnings: lineup.potentialWinnings,
    rank: lineup.rank,
  }));
};

/*
 * Takes the contest lineups, converts each out of bytes, then adds up fantasy total
 *
 * @param {Object} (required) Original set of players from API
 * @param {Object} (required) Final, centralized associative array of players
 * @param {String} (required) Which lineup, mine or opponent?
 *
 * @return {Object, Object} Return the lineups, sorted highest to lowest points
 */
export const rankContestLineups = (contest, contestPool, draftGroup, gamesTimeRemaining, prizeStructure = {}) => {
  logSelector.info('rankContestLineups', contest.id, {
    info: { contest, contestPool, draftGroup, gamesTimeRemaining, prizeStructure },
  });

  // return nothing if the contest hasn't started or we don't have info yet
  if (
    new Date(contestPool.start).getTime() > dateNow() ||
    draftGroup.hasAllInfo === false
  ) return {};

  // return shell if no prize structures yet
  if (prizeStructure.hasOwnProperty('ranks') === false) {
    return {
      hasLineupsUsernames: false,
      lineups: {},
      rankedLineups: [],
    };
  }

  // return basic lineup information
  const lineupsStats = mapValues(contest.lineups, (lineup) =>
    compileLineupStats(lineup, draftGroup, gamesTimeRemaining)
  );

  // sort ID by descending fp
  const rankedLineupIDs = map(
    orderBy(values(lineupsStats), 'fp', 'desc'), // sort by descending fp
    (lineup) => lineup.id
  );

  const lineupsValues = calcContestLineupsValues(lineupsStats, rankedLineupIDs, prizeStructure.ranks || {});

  const lineups = mapValues(lineupsStats, (lineup) =>
    merge(
      {},
      lineup,
      lineupsValues[lineup.id]
    )
  );

  return {
    rankedLineups: rankedLineupIDs,
    lineups,
    hasLineupsUsernames: contest.hasOwnProperty('lineupsUsernames'),
  };
};

const onlyLiveContestsSelector = (state) => state.liveContests;
const liveDraftGroupsSelector = (state) => state.liveDraftGroups;
const liveContestPoolsSelector = (state) => state.liveContestPools;
const prizesSelector = (state) => state.prizes;

/**
 * Redux reselect selector to compile all relevant information for contests
 */
export const liveContestsSelector = createSelector(
  [
    onlyLiveContestsSelector,
    liveContestPoolsSelector,
    liveDraftGroupsSelector,
    gamesTimeRemainingSelector,
    prizesSelector,
  ],
  (liveContests, liveContestPools, liveDraftGroups, gamesTimeRemaining, prizes) =>
    mapValues(liveContests, (contest) => {
      logSelector.info('selectors.liveContestsSelector', contest.id);

      // if the contest has not started, return nothing
      if (!(contest.contestPoolId in liveContestPools)) return {};
      const contestPool = liveContestPools[contest.contestPoolId];

      // if draft groups have not loaded yet, return nothing
      if (liveDraftGroups.hasOwnProperty(contestPool.draft_group) === false) return {};

      logSelector.info('selectors.liveContestsSelector - IN', contest, contestPool);

      // default prize structure so we can still return stats
      const prize = prizes[contestPool.prize_structure.id] || {};
      const prizeStructure = prize.info || {};

      const entriesCount = Object.keys(contest.lineups).length;
      let percentageCanWin = prizeStructure.payout_spots / entriesCount * 100 || 100;

      if (percentageCanWin > 100) {
        percentageCanWin = 100;
      }

      const stats = {
        buyin: contestPool.buyin,
        entriesCount,
        id: contest.id,
        name: contestPool.name,
        percentageCanWin,
        start: contestPool.start,
        prizeStructure,
      };

      const rankedLineups = rankContestLineups(
        contest,
        contestPool,
        liveDraftGroups[contestPool.draft_group],
        gamesTimeRemaining,
        prizeStructure
      );

      const all = merge(
        stats,
        rankedLineups
      );

      logSelector.info('selectors.liveContestsSelector - DONE', contest.id, { rankedLineups, all });

      return all;
    })
);
