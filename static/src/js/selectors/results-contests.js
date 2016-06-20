import forEach from 'lodash/forEach';
import merge from 'lodash/merge';
import { createSelector } from 'reselect';
import { rankContestLineups } from './live-contests';


const liveDraftGroupsSelector = (state) => state.liveDraftGroups;
const onlyLiveContestsSelector = (state) => state.liveContests;
const prizesSelector = (state) => state.prizes;
const sportsSelector = (state) => state.sports;

/**
 * Redux reselect selector to compile all relevant information for results contest pane
 */
export const resultsContestsSelector = createSelector(
  [onlyLiveContestsSelector, liveDraftGroupsSelector, sportsSelector, prizesSelector],
  (contests, draftGroups, sports, prizes) => {
    const contestsStats = {};

    forEach(contests, (contest, id) => {
      // if we don't have contest information yet, then return
      if (!contest.info || contest.hasRelatedInfo === false) return;

      const draftGroup = draftGroups[contest.info.draft_group];
      const prizeStructure = prizes[contest.info.prize_structure];

      const stats = {
        boxScores: null,
        buyin: contest.info.buyin,
        draftGroupId: contest.info.draft_group,
        entriesCount: contest.info.entries,
        id: contest.id,
        name: contest.info.name,
        prizeStructure,
        sport: contest.info.sport,
        teams: sports[contest.info.sport],
      };

      // if undefined and we're still trying, then return. occurs when cached for days
      if (draftGroup !== undefined) {
        stats.boxScores = draftGroup.boxScores;

        contestsStats[id] = merge(
          stats,
          rankContestLineups(contest, draftGroup, {}, prizeStructure.info, [])
        );
      } else {
        contestsStats[id] = stats;
      }
    });

    return contestsStats;
  }
);
