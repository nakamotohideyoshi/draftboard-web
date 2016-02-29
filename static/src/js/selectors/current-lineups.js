import { forEach as _forEach } from 'lodash';
import { map as _map } from 'lodash';
import { merge as _merge } from 'lodash';
import { reduce as _reduce } from 'lodash';
import moment from 'moment';
import { createSelector } from 'reselect';
import { dateNow } from '../lib/utils';
import { GAME_DURATIONS } from '../actions/sports';
import { liveContestsSelector } from './live-contests';
import log from '../lib/logging';


/**
 * Calculate the amount of time remaining in decimal between 0 and 1, where 1 is 100% of the time remaining
 * @param  {number} minutesRemaining Number of minutes remaining
 * @param  {number} totalMinutes     Total number of minutes for all of the player's games combined
 * @return {number}                  Remaining time in decimal form
 */
const calcDecimalRemaining = (minutesRemaining, totalMinutes) => {
  const decimalRemaining = minutesRemaining / totalMinutes;

  // we don't want 1 exactly, as that messes with the calculations, 0.99 looks full
  if (decimalRemaining === 1) return 0.9999;

  return decimalRemaining;
};

/**
 * Loop through all contests a lineup is in and return pertinent information on them if they're live
 * @param  {integer} lineupId      Lineup ID
 * @param  {object} lineupContests List of contests the lineup is in to loop through
 * @param  {object} contestsStats  Contest stats generated by the contest selector
 * @param  {object} liveContests   List of live contests from the server
 * @return {object}                List of contests with new stats
 */
const calcEntryContestStats = (lineupId, lineupContests, contestsStats, liveContests) => {
  const stats = {};

  // loop through each of the lineup's entered contests
  _forEach(lineupContests, (contestId) => {
    // Make sure we have lineups.
    if (!contestsStats[contestId].hasOwnProperty('lineups')) {
      return;
    }

    const liveContest = liveContests[contestId];
    const contestStats = contestsStats[contestId];
    const entryStats = contestStats.lineups[lineupId];

    // if stats exist (aka the lineup has started playing), then modify the given contest stats with some additional
    // information, such as our entry's rank and position, since we don't need to calculate for everyone yet
    if (entryStats && contestStats && liveContest) {
      stats[contestId] = _merge(
        contestStats,
        {
          myPercentagePosition: (entryStats.rank - 1) / liveContest.info.entries * 100,
          myEntryRank: entryStats.rank,
          potentialEarnings: entryStats.potentialEarnings,
        }
      );
    }
  });

  return stats;
};

/**
 * Shortcut method to loop through all lineup entries and their associated contests to sum potential earnings
 * @param  {object} entries       List of entries the lineup is in
 * @param  {object} contestsStats List of contests with their associated stats
 * @return {number}               Total potential earnings for the lineup
 */
const calcLineupPotentialEarnings = (entries, contestsStats) =>
  _reduce(entries, (sum, entry) => {
    // Make sure we have entries.
    if (contestsStats.hasOwnProperty(entry.contest)) {
      const contestLineups = contestsStats[entry.contest].lineups;

      if (entry.lineup in contestLineups === true) {
        return sum + contestsStats[entry.contest].lineups[entry.lineup].potentialEarnings;
      }
    }

    return sum;
  },
0);

/**
 * Add relevant player information to each player in the roster
 * @param  {list} roster          List of player IDs
 * @param  {object} draftGroup    The lineup's draft group
 * @param  {object} games         Object of all relevant games, used to get boxscore time remaining
 * @param  {list} relevantPlayers List of relevant player IDs
 * @return {object}               List of the players and all of their pertinent information
 */
export const compileRosterStats = (roster, draftGroup, games, relevantPlayers) => {
  const currentPlayers = {};

  _forEach(roster, (playerId) => {
    // exit if we don't have any player info.
    if (draftGroup.playersInfo.hasOwnProperty(playerId) === false) return;

    const player = {
      id: playerId,
      info: draftGroup.playersInfo[playerId],
      stats: _merge(
        {
          // default to no points and no minutes remaining
          fp: 0,
          minutesRemaining: 0,
          decimalRemaining: 0,
        },
        draftGroup.playersStats[playerId] || {}
      ),
    };
    player.liveStats = relevantPlayers[player.info.player_srid];

    // pull in accurate data from related game
    const game = games[player.info.game_srid];
    if (game) {
      // if playing then get the live amount remaining
      if (game.hasOwnProperty('boxscore')) {
        player.stats.minutesRemaining = game.boxscore.timeRemaining || 0;
        player.stats.decimalRemaining = calcDecimalRemaining(
          player.stats.minutesRemaining,
          GAME_DURATIONS.nba.gameMinutes
        );
      // otherwise this means the game is scheduled, so show as full
      } else {
        player.stats.minutesRemaining = GAME_DURATIONS.nba.gameMinutes;
        player.stats.decimalRemaining = 0.99;
      }
    }

    currentPlayers[playerId] = player;
  });

  return currentPlayers;
};

/**
 * Compile all relevant stats for a lineup
 * @param  {object} lineup          The original lineup object from the server
 * @param  {object} draftGroup      The lineup's draft group, used to get player stats and info for the roster
 * @param  {object} games           All relevant games for that sport, used for boxscore time remaining
 * @param  {list} relevantPlayers All relevant players, which will add live stats to said player
 * @return {object}                 Super loaded lineup with all relevant information
 */
export const compileLineupStats = (lineup, draftGroup, games, relevantPlayers) => {
  const stats = {
    id: lineup.id,
    name: lineup.name || 'Example Lineup Name',
    roster: lineup.roster,
    start: lineup.start,
    totalMinutes: GAME_DURATIONS.nba.gameMinutes * GAME_DURATIONS.nba.players,
  };

  // return if the lineup hasn't started yet
  if (lineup.roster === undefined) return stats;

  stats.rosterDetails = compileRosterStats(lineup.roster, draftGroup, games, relevantPlayers);

  // determine total fantasy points for the lineup
  // only add if they have fantasy points
  stats.points = _reduce(stats.rosterDetails, (fp, player) =>
    (isNaN(player.stats.fp)) ? fp : fp + player.stats.fp,
  0);

  // calculate minutes
  stats.minutesRemaining = _reduce(stats.rosterDetails, (timeRemaining, player) =>
    (player.stats.minutesRemaining) ? player.stats.minutesRemaining + timeRemaining : timeRemaining,
  0);
  stats.decimalRemaining = calcDecimalRemaining(stats.minutesRemaining, stats.totalMinutes);

  return stats;
};

/**
 * When you choose to watch the top players, we need to make a fake lineup based on that roster
 * @param  {list} roster     Fake roster of top owned player IDs
 * @param  {object} draftGroup Draft group associated to the contest the user is in
 * @param  {string} sport      Sport to determine game related constants
 * @param  {object} games      Games to calculate PMR for roster
 * @return {object}            Lineup stats, similar to what comes out of compileLineupStats
 */
export const compileVillianLineup = (roster, draftGroup, sport, games) => {
  const sportConst = GAME_DURATIONS[sport];

  const stats = {
    id: 1,
    name: 'Top Owned',
    roster,
    start: draftGroup.start,
    totalMinutes: sportConst.gameMinutes * sportConst.players,
  };

  stats.rosterDetails = compileRosterStats(roster, draftGroup, games, roster);

  // determine total fantasy points for the lineup
  // only add if they have fantasy points
  stats.points = _reduce(stats.rosterDetails, (fp, player) =>
    (isNaN(player.stats.fp)) ? fp : fp + player.stats.fp,
  0);

  // calculate minutes
  stats.minutesRemaining = _reduce(stats.rosterDetails, (timeRemaining, player) =>
    (player.stats.minutesRemaining) ? player.stats.minutesRemaining + timeRemaining : timeRemaining,
  0);
  stats.decimalRemaining = calcDecimalRemaining(stats.minutesRemaining, stats.totalMinutes);

  return stats;
};


// Crazy selector that
// - loops through the entries per lineup and calculates potential earnings
// - loops through the players per lineup and calculates PMR
export const currentLineupsSelector = createSelector(
  liveContestsSelector,
  state => state.liveContests,
  state => state.liveDraftGroups,
  state => state.sports,
  state => state.entries.items,
  state => state.currentLineups.items,
  state => state.entries.hasRelatedInfo,
  state => state.livePlayers.relevantPlayers || [],

  (contestsStats, liveContests, liveDraftGroups, sports, entries, lineups, hasRelatedInfo, relevantPlayers) => {
    // do not show if we don't have data yet
    if (hasRelatedInfo === false) {
      log.trace('currentLineupsSelector() - entries have not finished loading yet');
      return {};
    }

    const stats = {};
    _forEach(lineups, (lineup) => {
      const draftGroup = liveDraftGroups[lineup.draft_group];

      // send back a default lineup if it has not started playing yet
      if (new Date(lineup.start) > dateNow() || lineup.roster === undefined) {
        log.trace('currentLineupsSelector() - lineup has not started yet', lineup.id);

        stats[lineup.id] = {
          decimalRemaining: 0.99,
          draftGroup,
          formattedStart: moment(lineup.start).format('ha'),
          id: lineup.id,
          minutesRemaining: 384,
          name: lineup.name || 'Example Lineup Name',
          points: 0,
          roster: lineup.roster,
          start: lineup.start,
        };

        return;
      }

      // combine the normal lineup stats (that are used in the contests selector), with additional stats that are only
      // used for the lineups you're watching
      stats[lineup.id] = _merge(
        compileLineupStats(lineup, draftGroup, sports.games, relevantPlayers),
        {
          draftGroup,
          formattedStart: moment(lineup.start).format('ha'),
          // used for animations to determine which side
          rosterBySRID: _map(stats.rosterDetails, (player) => player.info.player_srid),
          // used by LiveOverallStats to show potential earnings
          totalPotentialEarnings: calcLineupPotentialEarnings(entries, contestsStats),
          // used by LiveContestsPane to view contests for a lineup
          contestsStats: calcEntryContestStats(lineup.id, lineup.contests, contestsStats, liveContests),
        }
      );
    });

    return stats;
  }
);
