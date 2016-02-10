import { createSelector } from 'reselect';
import { countBy as _countBy, filter as _filter } from 'lodash';
import { mapValues as _mapValues } from 'lodash';


// Input Selectors
const draftGroupsFilterSelector = (state) => state.upcomingDraftGroups.draftGroups;
const contestsFilterSelector = (state) => state.upcomingContests.allContests;


/**
 * A memoized selector that finds derived data from the list of upcoming contests and upcoming
 * draftgroups. We need this for the draft group selection modal in the lobby.
 *
 * End result is something like:
 *
 {
   draftGroups [
     {pk: 1, sport: 'nba', start: '2016-03-20T20:56:25Z'},
     {pk: 2, sport: 'nfl', start: '2016-03-20T20:56:25Z'},
     {pk: 3, sport: 'nfl', start: '2016-03-20T20:56:25Z'}
   ],
   sportContestCounts: [
     'nba': 1,
     'nfl': 2
   ]
 }
*/
export const draftGroupInfoSelector = createSelector(
  [draftGroupsFilterSelector, contestsFilterSelector],
  (draftGroups, contests) => {
    //  Get a group listing of each sport with counts.
    const sportContestCounts = _countBy(contests, (contest) => contest.sport);
    // For each draft group, figure out how many contests are available to enter.
    const draftGrupsExtra = _mapValues(draftGroups, (group) => {
      const groupExtra = Object.assign({}, group);
      groupExtra.contestCount = _filter(contests, 'draft_group', group.pk).length;
      return groupExtra;
    });

    return {
      sportContestCounts,
      draftGroups: draftGrupsExtra,
    };
  }
);


/**
 * Build up a bunch of data related to the currently active draft group. This is used in the draft
 * section for the team filter.
 */
const activeDraftGroupIdSelector = (state) => state.upcomingDraftGroups.activeDraftGroupId;
const boxScoresSelector = (state) => state.upcomingDraftGroups.boxScores;
// const boxScoreGamesSelector = (state) => state.upcomingDraftGroups.boxScoreGames

export const activeDraftGroupBoxScoresSelector = createSelector(
  [activeDraftGroupIdSelector, draftGroupsFilterSelector, boxScoresSelector],
  (activeDraftGroupId, draftGroups, boxScores) => {
    let response = {};

    if (activeDraftGroupId) {
      if (boxScores.hasOwnProperty(activeDraftGroupId)) {
        response = boxScores[activeDraftGroupId];
      }
    }

    return response;
  }
);
