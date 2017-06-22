import countBy from 'lodash/countBy';
import { createSelector } from 'reselect';
import filter from 'lodash/filter';
import mapValues from 'lodash/mapValues';
import merge from 'lodash/merge';
import sortBy from 'lodash/sortBy';
import forEach from 'lodash/forEach';


// Input Selectors
const draftGroupsFilterSelector = (state) => state.upcomingDraftGroups.draftGroups;
const contestsFilterSelector = (state) => state.contestPools.allContests;
const draftGroupBoxScoresSelector = (state) => state.upcomingDraftGroups.boxScores;

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
   // How many contets each sport has
   sportContestCounts: [
     'nba': 1,
     'nfl': 2
   ],
   // How many draft groups each sport has.
   sportDraftGroupCounts: [
     'nfl': 3
   ],
 }
*/
export const draftGroupInfoSelector = createSelector(
  [draftGroupsFilterSelector, contestsFilterSelector, draftGroupBoxScoresSelector],
  (draftGroups, contests, draftGroupBoxScores) => {
    //  Get a group listing of each sport with counts.
    const sportContestCounts = countBy(contests, (contest) => contest.sport);
    const sportDraftGroupCounts = countBy(draftGroups, (draftGroup) => draftGroup.sport);
    // For each draft group, figure out how many contests are available to enter.
    let draftGrupsExtra = mapValues(draftGroups, (group) => {
      const groupExtra = merge({}, group);
      groupExtra.contestCount = filter(contests, 'draft_group', group.pk).length;
      return groupExtra;
    });
    // Sort the draftgroups by start time.
    draftGrupsExtra = sortBy(draftGrupsExtra, 'start');

    const data = Object.assign({}, {
      sportContestCounts,
      draftGroups: draftGrupsExtra,
      sportDraftGroupCounts,
    });
    /* eslint-disable no-param-reassign */
    forEach(data.draftGroups, group => {
      group.boxScores = draftGroupBoxScores[group.pk];
    });
    /* eslint-enable no-param-reassign */
    return data;
  }
);


/**
 * Build up a bunch of data related to the currently active draft group. This is used in the draft
 * section for the team filter.
 */
const activeDraftGroupIdSelector = (state) => state.upcomingDraftGroups.activeDraftGroupId;
// const boxScoreGamesSelector = (state) => state.upcomingDraftGroups.boxScoreGames

export const activeDraftGroupBoxScoresSelector = createSelector(
  [activeDraftGroupIdSelector, draftGroupsFilterSelector, draftGroupBoxScoresSelector],
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
