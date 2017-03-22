import Raven from 'raven-js';
import log from '../lib/logging';
import map from 'lodash/map';
import mapValues from 'lodash/mapValues';
import merge from 'lodash/merge';
import reduce from 'lodash/reduce';
import size from 'lodash/size';
import uniqBy from 'lodash/uniqBy';
import zipObject from 'lodash/zipObject';
import { assembleCurrentPlayer } from './live-draft-groups';
import { calcDecimalRemaining, SPORT_CONST } from '../actions/sports';
import { createSelector } from 'reselect';
import { dateNow } from '../lib/utils';
import { gamesTimeRemainingSelector } from './sports';

// get custom logger for actions
const logSelector = log.getLogger('selector');

const lineupsItemsSelector = (state) => state.currentLineups.items;
const lineupsSelector = (state) => state.currentLineups;

/**
 * Simple selector to return unique lineups and if they are finished loading.
 * Used by the opening window in /live/ to choose a sport -> lineup
 */
export const uniqueLineupsSelector = createSelector(
  [lineupsSelector],
  (lineups) => {
    const uniqueLineupsArray = uniqBy(map(lineups.items, (lineup) => lineup), 'id');
    const uniqueLineups = zipObject(
      map(uniqueLineupsArray, 'id'),
      // add in hasStarted to values
      map(uniqueLineupsArray, (lineup) => merge({}, lineup, {
        hasStarted: new Date(lineup.start).getTime() < dateNow(),
        start: new Date(lineup.start).getTime(),
      }))
    );

    return {
      lineups: uniqueLineupsArray,  // for choosing lineup in live
      lineupsObj: uniqueLineups,  // for showing countdown before lineup is loaded in
      haveLoaded: lineups.isFetching === false,  // to know when to show lineups to choose from
    };
  }
);

export const lineupsHaveRelatedInfoSelector = createSelector(
  [lineupsSelector], (lineups) => lineups.hasRelatedInfo
);

export const contestsLineupsSelector = createSelector(
  [lineupsItemsSelector], (lineups) => map(lineups, (lineup) => ({
    contest: lineup.contest,
    lineup: lineup.id,
  }))
);


/**
 * Helper method to calculate FP for a lineup roster.
 * This is exported for testing purposes, important to make sure this works correctly!
 * @param  {object} roster  List of players with fp, comes from lineup.rosterDetails
 * @return {object}         Return FP
 */
export const calcRosterFP = (roster) => reduce(roster || {}, (sum, player) => (sum + player.fp), 0);

/**
 * Helper method to calculate timeRemaining stats for a lineup
 * This is exported for testing purposes, important to make sure this works correctly!
 * @param  {string} sport   Sport to determine game duration -> lineup duration
 * @param  {object} roster  (optional) List of players with duration, comes from lineup.rosterDetails
 * @return {object}         Return timeRemaining in decimal and quantity
 */
export const calcRosterTimeRemaining = (sport, roster = {}) => {
  // logSelector.info('selectors.calcRosterTimeRemaining', { sport, roster });

  const sportConst = SPORT_CONST[sport] || null;

  // if not valid sport, return default of no time left
  if (sportConst === null) {
    Raven.captureException(`selectors.currentLineups.calcRosterTimeRemaining - sport does not exist: "${sport}"`);
    return { duration: 0, decimal: 0.00001 };
  }

  const lineupDuration = sportConst.gameDuration * sportConst.players;

  // if no roster, default to full time remaining
  const duration = (size(roster) === 0) ?
    lineupDuration :
    reduce(roster, (sum, player) => sum + player.timeRemaining.duration, 0);

  return {
    duration,
    decimal: calcDecimalRemaining(duration, lineupDuration),
  };
};

/**
 * Helper method to add relevant player information to each player in the roster
 * @param  {list}   roster             List of player IDs
 * @param  {object} draftGroup         The lineup's draft group
 * @param  {object} gamesTimeRemaining Games to calculate PMR for roster
 * @return {object}                    List of the players and all of their pertinent information
 */
export const compileRosterDetails = (roster, draftGroup, gamesTimeRemaining) =>
  zipObject(roster,
    map(roster, (playerId) => assembleCurrentPlayer(playerId, draftGroup, gamesTimeRemaining))
  );

/**
 * Helper method to compile all relevant stats for a lineup
 * @param  {object} lineup          The original lineup object from the server
 * @param  {object} draftGroup      The lineup's draft group, used to get player stats and info for the roster
 * @param  {object} games           All relevant games for that sport, used for boxscore time remaining
 * @return {object}                 Lineup with all relevant information
 */
export const compileLineupStats = (lineup = {}, draftGroup = {}, gamesTimeRemaining) => {
  logSelector.info('selectors.compileLineupStats', lineup.id);

  // check that enough is loaded in to return stats
  const hasAllInfo = draftGroup.hasAllInfo || false;
  if (hasAllInfo === false) return {};

  const stats = {
    draftGroupId: draftGroup.id,  // when we watch a lineup, this is used to pull in extra information
    id: lineup.id,
    name: lineup.name || '',
    roster: lineup.roster || [],  // default to empty list while we wait for lineup to be received
    rosterDetails: compileRosterDetails(lineup.roster, draftGroup, gamesTimeRemaining),
    sport: draftGroup.sport,  // used in nav
    start: new Date(lineup.start).getTime() || undefined,
  };

  const all = merge(
    stats,
    {
      fp: calcRosterFP(stats.rosterDetails),
      timeRemaining: calcRosterTimeRemaining(draftGroup.sport, stats.rosterDetails),
    }
  );

  logSelector.info('selectors.compileLineupStats - DONE', all);

  return all;
};

/**
 * When you choose to watch the top players, we need to make a fake lineup based on that roster
 * @param  {list}   roster             Fake roster of top owned player IDs
 * @param  {object} draftGroup         Draft group associated to the contest the user is in
 * @param  {object} gamesTimeRemaining Games to calculate PMR for roster
 * @return {object}                    Lineup with all relevant information
 */
export const compileVillianLineup = (roster = [], draftGroup = {}, gamesTimeRemaining = {}) => {
  // check that enough is loaded in to return stats
  const hasAllInfo = draftGroup.hasAllInfo || false;
  if (hasAllInfo === false) return {};

  if (roster.length === 0) {
    Raven.captureException('selectors.currentLineups.compileVillianLineup - roster is empty');
  }

  const stats = {
    id: 1,
    name: 'Top Owned',
    roster,
    rosterDetails: compileRosterDetails(roster, draftGroup, gamesTimeRemaining, roster),
  };

  return merge(
    stats,
    {
      fp: calcRosterFP(stats.rosterDetails),
      timeRemaining: calcRosterTimeRemaining(draftGroup.sport, stats.rosterDetails),
    }
  );
};

const currentLineupsItemsSelector = (state) => state.currentLineups.items;
const liveDraftGroupsSelector = (state) => state.liveDraftGroups;

/**
 * Selector to take our current lineups for a user, generate all fields needed for components
 * Note that this is everything in compileLineupStats, and then totalBuyin for the cmp.liveContestsPane
 */
export const myCurrentLineupsSelector = createSelector(
  [currentLineupsItemsSelector, liveDraftGroupsSelector, gamesTimeRemainingSelector],
  (lineups, draftGroups, gamesTimeRemaining) =>
    mapValues(lineups, (lineup) =>
      compileLineupStats(lineup, draftGroups[lineup.draftGroup], gamesTimeRemaining)
    )
);
