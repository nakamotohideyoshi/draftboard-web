import {createSelector} from 'reselect';
import {upcomingLineupsInfo} from './upcoming-lineups-info.js';



/**
 * Get the currently focused contest object based on state.upcomingContests.focusedContestId
 * Add it's prize structure and entrant usernames.
 */
let upcomingContests = (state) => state.upcomingContests.allContests;
let focusedContestId = (state) => state.upcomingContests.focusedContestId;
let focusedLineupId = (state) => state.upcomingLineups.focusedLineupId;
let boxScores = (state) => state.upcomingDraftGroups.boxScores;
let prizes = (state) => state.prizes;
let entrants = (state) => state.upcomingContests.entrants;
let lineupsInfo = (state) => upcomingLineupsInfo(state);

export const focusedContestInfoSelector = createSelector(
  [upcomingContests, focusedContestId, focusedLineupId, boxScores, prizes, entrants, lineupsInfo],
  (upcomingContests, focusedContestId, focusedLineupId, boxScores, prizes, entrants, lineupsInfo) => {
    // Default return data.
    let contestInfo = {
      contest: {
        id: null
      },
      prizeStructure: {},
      entrants: [],
      isEntered: false
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
        contestInfo.isEntered = (lineupsInfo[focusedLineupId].contests.indexOf(contestInfo.contest.id) != -1);
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
  [lineupsInfo, focusedLineupId],
  (lineupsInfo, focusedLineupId) => {
    // To add fields to this, you'll probably want to do it in the upcomingLineupsInfo selector.
    return lineupsInfo[focusedLineupId];
  }
);
