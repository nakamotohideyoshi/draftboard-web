import { createSelector } from 'reselect';
import { upcomingLineupsInfo } from './upcoming-lineups-info';
import filter from 'lodash/filter';
import reduce from 'lodash/reduce';
import log from '../lib/logging';


/**
 * Get the currently focused contest object based on state.contestPools.focusedContestId
 * Add it's prize structure and entrant usernames.
 */
export const focusedContestInfoSelector = createSelector(
  (state) => state.contestPools.allContests,
  (state) => state.contestPools.focusedContestId,
  (state) => state.upcomingLineups.focusedLineupId,
  (state) => state.upcomingDraftGroups.boxScores,
  (state) => state.prizes,
  (state) => state.contestPools.entrants,
  (state) => upcomingLineupsInfo(state),
  (state) => state.contestPoolEntries.entries,
  (upcomingContests,
    focusedContestId,
    focusedLineupId,
    boxScores,
    prizes,
    entrants,
    lineupsInfo,
    contestPoolEntries
  ) => {
    // Default return data.
    const contestInfo = {
      contest: {
        id: null,
        entryInfo: [],
      },
      prizeStructure: {},
      entrants: [],
      isEntered: false,
      focusedLineupEntries: [],

    };

    // Add additional info if a contest is focused.
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
          lineupsInfo[focusedLineupId].contestPoolEntries.hasOwnProperty(contestInfo.contest.id)
        );
      }

      // Add contestPool entries for the current lineup.
      if (focusedLineupId && contestPoolEntries) {
        contestInfo.focusedLineupEntries = filter(contestPoolEntries, (entry) =>
           entry.contest_pool.toString() === focusedContestId.toString()
          && entry.lineup.toString() === focusedLineupId.toString()
        );
      }

      // Add info about ALL lineups entered into this contest pool, not just the focused one.
      contestInfo.contest.entryInfo = filter(
        contestPoolEntries, (entry) => entry.contest_pool === contestInfo.contest.id
      );
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
 * Skill Level Map.
 *
 * A user may only enter into 1 skill level per sport. This keeps track of which
 * skill levels they have chosen to enter for each sport.
 *
 * example output:
 * {
 * 	nba: 'veteran',
 * 	nfl: 'rookie',
 * 	nhl: 'rookie',
 * }
 */
export const entrySkillLevelsSelector = createSelector(
  (state) => state.contestPoolEntries.entries,
  (state) => state.contestPools.allContests,
  (entries, contestPools) => {
    if (!entries || !contestPools) {
      return {};
    }

    if (!Object.keys(entries).length || !Object.keys(contestPools).length) {
      log.info('Either entries or contest pools don\'t exist.');
      return {};
    }

    // Create a map for each sport's skill level.
    const skillLevelsMap = reduce(entries, (previousValue, entry) => {
      // Make sure we have the contest pool the entry is in.
      if (!(entry.contest_pool in contestPools)) {
        log.error(`Contest #${entry.contest_pool} not found. - referenced from entry #${entry.id}.`);
        return;
      }

      // Ignore any contest pools that allow 'all' skill levels.
      if (contestPools[entry.contest_pool].skill_level.name === 'all') {
        return;
      }

      // If we already have an skill level set for this sport, ignore this one.
      // TODO: do a check to make sure we have no skill level conflicts.
      if (previousValue && entry.sport in previousValue) {
        return previousValue;
      }

      const newValue = Object.assign({}, previousValue);
      newValue[entry.sport] = contestPools[entry.contest_pool].skill_level.name;
      return newValue;
    }, {});

    return skillLevelsMap || {};
  }
);
