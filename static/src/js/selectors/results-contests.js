import { forEach as _forEach } from 'lodash';
import { merge as _merge } from 'lodash';
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

    _forEach(contests, (contest, id) => {
      // if we don't have contest information yet, then return
      if (!contest.info || contest.hasRelatedInfo === false) return;

      const draftGroup = draftGroups[contest.info.draft_group];
      const prizeStructure = prizes[contest.info.prize_structure];

      // if undefined and we're still trying, then return. occurs when cached for days
      if (draftGroup === undefined) return;

      const stats = {
        boxScores: draftGroup.boxScores || null,
        buyin: contest.info.buyin,
        draftGroupId: contest.info.draft_group,
        entriesCount: contest.info.entries,
        id: contest.id,
        name: contest.info.name,
        prizeStructure,
        sport: contest.info.sport,
        teams: sports[contest.info.sport],
      };

      contestsStats[id] = _merge(
        stats,
        rankContestLineups(contest, draftGroup, {}, prizeStructure.info, [])
      );
    });

    return contestsStats;
  }
);
