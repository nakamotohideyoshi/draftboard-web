import { createSelector } from 'reselect'
import { countBy as _countBy, forEach as _forEach } from 'lodash'
import {filter as _filter} from 'lodash'

// Input Selectors
const draftGroupsFilterSelector = (state) => state.upcomingDraftGroups.draftGroups
const contestsFilterSelector = (state) => state.upcomingContests.allContests


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
    let sportContestCounts = _countBy(contests, function(contest) {
      return contest.sport
    })
    // For each draft group, figure out how many contests are available to enter.
    _forEach(draftGroups, function(group) {
      group.contestCount = _filter(contests, 'draft_group', group.pk).length
    })

    return {
      sportContestCounts,
      draftGroups: draftGroups
    }
  }
)
