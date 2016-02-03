import { createSelector } from 'reselect';
import { upcomingLineupsInfo } from './upcoming-lineups-info.js';


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
  (upcomingContests, focusedContestId, focusedLineupId, boxScores, prizes, entrants, lineupsInfo) => {
    // Default return data.
    const contestInfo = {
      contest: {
        id: null,
      },
      prizeStructure: {},
      entrants: [],
      isEntered: false,
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
        contestInfo.isEntered = (lineupsInfo[focusedLineupId].contests.indexOf(contestInfo.contest.id) !== -1);
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
