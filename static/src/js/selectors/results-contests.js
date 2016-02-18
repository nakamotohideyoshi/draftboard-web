import _ from 'lodash';
import { createSelector } from 'reselect';
import { rankContestLineups } from './live-contests';


/**
 * Redux reselect selector to compile all relevant information for results contest pane
 */
export const resultsContestsSelector = createSelector(
  state => state.liveContests,
  state => state.liveDraftGroups,
  state => state.prizes,
  state => state.sports,

  (contests, draftGroups, prizes, sports) => {
    const contestsStats = {};

    _.forEach(contests, (contest, id) => {
      // if we don't have contest information yet, then return
      if (!contest.info || contest.hasRelatedInfo === false) {
        return;
      }

      const draftGroup = draftGroups[contest.info.draft_group];
      const prizeStructure = prizes[contest.info.prize_structure];

      // if undefined and we're still trying, then return. occurs when cached for days
      if (draftGroup === undefined) {
        return;
      }

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


      contestsStats[id] = Object.assign(
        stats,
        rankContestLineups(contest, draftGroup, {}, prizeStructure.info, [])
      );
    });

    return contestsStats;
  }
);
