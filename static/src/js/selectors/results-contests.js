import { createSelector } from 'reselect';

//
// const focusedEntryIdSelector = (state) => state.results.focusedEntryId;
// const entryResultsSelector = (state) => state.results.entryResults;
//
// export const focusedEntryResultSelector = createSelector(
//   [focusedEntryIdSelector, entryResultsSelector],
//   (focusedEntry, entryResults) => {
//     if (focusedEntry in entryResults) {
//       return entryResults[focusedEntry];
//     }
//
//     return {};
//   }
// );


const focusedContestIdSelector = (state) => state.results.focusedContestId;
const entryContestSelector = (state) => state.results.contestResults;

export const focusedContestResultSelector = createSelector(
  [focusedContestIdSelector, entryContestSelector],
  (focusedContest, contestResults) => {
    if (focusedContest in contestResults) {
      return contestResults[focusedContest];
    }

    return {};
  }
);


// const liveDraftGroupsSelector = (state) => state.liveDraftGroups;
// const onlyLiveContestsSelector = (state) => state.liveContestPools;
// const prizesSelector = (state) => state.prizes;
// const sportsSelector = (state) => state.sports;

/**
 * Redux reselect selector to compile all relevant information for results contest pane
 */
// export const resultsContestsSelector = createSelector(
//   [onlyLiveContestsSelector, liveDraftGroupsSelector, sportsSelector, prizesSelector],
//   (contests, draftGroups, sports, prizes) => {
//     const contestsStats = {};
//     console.warn('contestsStats update');
//     forEach(contests, (contest, id) => {
//       console.log(contest);
//       // if we don't have contest information yet, then return
//       if (!contest.hasRelatedInfo) return;
//
//       console.log('contest has info, adding ot list');
//       const draftGroup = draftGroups[contest.draft_group];
//       // const prizeStructure = prizes[contest.prize_structure];
//
//       const stats = {
//         boxScores: null,
//         buyin: contest.buyin,
//         draftGroupId: contest.draft_group,
//         entriesCount: contest.entries,
//         id: contest.id,
//         name: contest.name,
//         prizeStructure: contest.prize_structure,
//         sport: contest.sport,
//         teams: sports[contest.sport],
//       };
//
//       // if undefined and we're still trying, then return. occurs when cached for days
//       if (draftGroup !== undefined) {
//         stats.boxScores = draftGroup.boxScores;
//
//         contestsStats[id] = merge(
//           stats,
//           rankContestLineups(contest, draftGroup, {}, contest.prize_structure, [])
//         );
//       } else {
//         contestsStats[id] = stats;
//       }
//     });
//
//
//     console.log(contestsStats);
//     return contestsStats;
//   }
// );
