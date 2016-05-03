import { createSelector } from 'reselect';
import { upcomingLineupsInfo } from './upcoming-lineups-info.js';
import sortBy from 'lodash/sortBy';
import filter from 'lodash/filter';


/**
 * Get the currently focused contest object based on state.upcomingContests.focusedContestId
 * Add it's prize structure and entrant usernames.
 */
export const focusedContestInfoSelector = createSelector(
  (state) => state.upcomingContests.allContests,
  (state) => state.upcomingContests.focusedContestId,
  (state) => state.upcomingLineups.focusedLineupId,
  (state) => state.upcomingDraftGroups.boxScores,
  (state) => state.prizes,
  (state) => state.upcomingContests.entrants,
  (state) => upcomingLineupsInfo(state),
  (state) => state.contestPoolEntries.entries,
  (upcomingContests, focusedContestId, focusedLineupId, boxScores, prizes, entrants, lineupsInfo,
    contestPoolEntries
  ) => {
    // Default return data.
    const contestInfo = {
      contest: {
        id: null,
      },
      prizeStructure: {},
      entrants: [],
      isEntered: false,
      entries: [],
    };

    // Add additional info if available.
    if (upcomingContests.hasOwnProperty(focusedContestId)) {
      contestInfo.contest = upcomingContests[focusedContestId];

      // Add the boxscore if it's available.
      if (boxScores.hasOwnProperty(contestInfo.contest.draft_group)) {
        contestInfo.boxScores = boxScores[contestInfo.contest.draft_group];
      }

      // Add the usernames of anyone who has entered the contest
      if (entrants.hasOwnProperty(focusedContestId)) {
        contestInfo.entrants = entrants[focusedContestId];
      }

      // Add 'isEntered' attribute if the focused lineup has been entered into this contest
      if (focusedLineupId && lineupsInfo.hasOwnProperty(focusedLineupId)) {
        contestInfo.isEntered = (
          lineupsInfo[focusedLineupId].contestPoolEntries.indexOf(contestInfo.contest.id) !== -1
        );
      }

      // Add contestPool entries for the current lineup.
      if (focusedLineupId && contestPoolEntries) {
        contestInfo.entries = filter(contestPoolEntries, (entry) =>
           entry.contest_pool.toString() === focusedContestId.toString()
          && entry.lineup.toString() === focusedLineupId.toString()
        );
      }

      // Add the prize payout structure.
      if (
          contestInfo.contest.prize_structure &&
          prizes.hasOwnProperty(contestInfo.contest.prize_structure)
        ) {
        contestInfo.prizeStructure = prizes[contestInfo.contest.prize_structure];
      }
    }

    return contestInfo;
  }
);


/**
 * Return the upcomingLineupsInfo item for the currently focused lineup.
 */
export const focusedLineupSelector = createSelector(
  (state) => upcomingLineupsInfo(state),
  (state) => state.upcomingLineups.focusedLineupId,
  (lineupsInfo, focusedLineupId) => lineupsInfo[focusedLineupId]
);


/**
 * Find the highest buyin for a contest - this is used for contest filters.
 */
export const highestContestBuyin = createSelector(
  (state) => state.upcomingContests.allContests,
  (contests) => {
    const sortedContests = sortBy(contests, ['buyin']);

    if (sortedContests.length) {
      return parseFloat(sortedContests[0].buyin);
    }

    // If we don't have any contests, don't return anything. This is important.
    // if we set it to a default value, the RangeSlider will get rendered with
    // that default, and when we get contests with actual values, it will force
    // a re-render and because that is a jquery plugin, we only want to render
    // it once.
    return null;
  }
);
