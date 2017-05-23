import { createSelector } from 'reselect';
import mapValues from 'lodash/mapValues';
import merge from 'lodash/merge';
import filter from 'lodash/filter';
import { orderByProperty } from './order-by-property.js';
import { stringSearchFilter, matchFilter, inArrayFilter } from './filters';
import { isPlayerInLineup } from '../components/draft/draft-utils.js';


// All the players in the state.
const allPlayersSelector = (state) => state.draftGroupPlayers.allPlayers;
const injuriesSelector = (state) => state.draftGroupUpdates;
const historiesSelector = (state) => state.fantasyHistory;
const sportInfoSelector = (state) => state.sports;
const boxScoreGamesSelector = (state) => state.upcomingDraftGroups.boxScores;
const activeDraftGroupIdSelector = (state) => state.upcomingDraftGroups.activeDraftGroupId;
const sportSelector = (state) => state.draftGroupPlayers.sport;


// Add injury information to each player.
const playersWithInfo = createSelector(
  allPlayersSelector,
  injuriesSelector,
  historiesSelector,
  sportSelector,
  sportInfoSelector,
  activeDraftGroupIdSelector,
  boxScoreGamesSelector,
  (players, injuries, histories, sport, sportInfo, activeDraftGroupId, boxScoreGames
  ) => mapValues(players, (player) => {
    // Duplicate the player so we don't mutate the state.
    const playerWithInfo = merge({}, player);
    // Add injury status if we have it.
    if (injuries.sports[sport].hasOwnProperty('playerUpdates')) {
      if (injuries.sports[sport].playerUpdates.playerStatus.hasOwnProperty(player.player_srid)) {
        playerWithInfo.status = injuries.sports[sport].playerUpdates.playerStatus[player.player_srid][0].status;
      }
    }

    // Add FP history.
    if (histories.hasOwnProperty(player.player_id)) {
      playerWithInfo.history = histories[player.player_id].fantasy_points;
    }

    // Attach the player's team info.
    if (sportInfo.hasOwnProperty(sport) && sportInfo[sport].teams[player.team_srid]) {
      playerWithInfo.teamCity = sportInfo[sport].teams[player.team_srid].city;
      playerWithInfo.teamName = sportInfo[sport].teams[player.team_srid].name;
    }

    // attach next game info.
    if (activeDraftGroupId && boxScoreGames.hasOwnProperty(activeDraftGroupId)) {
      // Grab info about the player's next game.
      playerWithInfo.nextGame = boxScoreGames[activeDraftGroupId][player.game_srid];

      // If we have team info, attach the next teams in the next game.
      if (sportInfo.hasOwnProperty(sport) && playerWithInfo.nextGame) {
        // Add home team info
        if (sportInfo[sport].teams.hasOwnProperty(playerWithInfo.nextGame.srid_home)) {
          playerWithInfo.nextGame.homeTeam = sportInfo[sport].teams[playerWithInfo.nextGame.srid_home];
        }
        // Add away team info.
        if (sportInfo[sport].teams.hasOwnProperty(playerWithInfo.nextGame.srid_away)) {
          playerWithInfo.nextGame.awayTeam = sportInfo[sport].teams[playerWithInfo.nextGame.srid_away];
        }
      }
    }

    return playerWithInfo;
  })

);


const remainingSalarySelector = (state) => state.createLineup.remainingSalary;
const availablePositionSelector = (state) => state.createLineup.availablePositions;
const newLineupSelector = (state) => state.createLineup.lineup;


/**
 * Add affordability + draftability meta info.
 */
const playersWithDraftabilityInfo = createSelector(
  [playersWithInfo, remainingSalarySelector, availablePositionSelector, newLineupSelector],
  (players, remainingSalary, availablePositions, newLineup) => mapValues(players, (player) => {
    const playerWithInfo = merge({}, player);

    // add affordability.
    playerWithInfo.canAfford = remainingSalary >= player.salary;

    // Add draft status.
    let draftable = true;
    let drafted = false;
    // Is there a slot available?
    if (availablePositions.indexOf(player.position) === -1) {
      draftable = false;
    }
    // Is the player already drafted?
    if (isPlayerInLineup(newLineup, player)) {
      draftable = false;
      drafted = true;
    }
    playerWithInfo.drafted = drafted;
    playerWithInfo.draftable = draftable;

    return playerWithInfo;
  })
);


/**
 * Sort the players.
 */
const sortDirectionSelector = (state) => state.draftGroupPlayersFilters.filters.orderBy.direction;
const sortPropertySelector = (state) => state.draftGroupPlayersFilters.filters.orderBy.property;

export const draftGroupPlayerSelector = createSelector(
  [playersWithDraftabilityInfo, sortPropertySelector, sortDirectionSelector],
  (collection, sortProperty, direction) => orderByProperty(collection, sortProperty, direction)
);


/**
 * The following selectors are used to filter the state.draftGroups.filteredPlayers
 */

 // Filter players based on the probable pitchers filter.
const probablePitchersFilter = (state) => state.draftGroupPlayersFilters.filters.probablePitchersFilter.match;
const draftGroupUpdatesSelector = (state) => state.draftGroupUpdates;

const probablePitchersSelector = createSelector(
    [allPlayersSelector, probablePitchersFilter, draftGroupUpdatesSelector, sportSelector, activeDraftGroupIdSelector],
    (players, showOnlyProbablePitchers, draftGroupUpdates, sport, draftGroupId) => {
      // Ignore this for any non-mlb sports.
      if (sport !== 'mlb') {
        return players;
      }

      // If we are showing all pitchers, just return them all.
      if (!showOnlyProbablePitchers) {
        return players;
      }

      // Make sure the draftgroup with pitchers exists in the store.
      if (
        draftGroupId &&
        draftGroupUpdates &&
        draftGroupUpdates.sports &&
        sport in draftGroupUpdates.sports &&
        draftGroupUpdates.sports[sport].probablePitchers &&
        draftGroupUpdates.sports[sport].probablePitchers.length
      ) {
        //  Filter out any non-probable pitchers.
        const pp = filter(players, (player) => {
          // Hide all non pitchers
          if (player.position !== 'SP') {
            return true;
          }

          // Filter out any pitchers that are not found in the probablePitchers list.
          return draftGroupUpdates.sports[sport].probablePitchers.indexOf(player.player_srid) > -1;
        });

        return pp;
      }

      return players;
    }
 );


// Filter players based on the search filter
const searchFilterPropertySelector = (state) =>
  state.draftGroupPlayersFilters.filters.playerSearchFilter.filterProperty;
const searchFilterMatchSelector = (state) => state.draftGroupPlayersFilters.filters.playerSearchFilter.match;

const playerNameSelector = createSelector(
  [probablePitchersSelector, searchFilterPropertySelector, searchFilterMatchSelector],
  (collection, filterProperty, searchString) => stringSearchFilter(collection, filterProperty, searchString)
);


// Filter players based on the team filter
const teamFilterPropertySelector = (state) => state.draftGroupPlayersFilters.filters.teamFilter.filterProperty;
const teamFilterMatchSelector = (state) => state.draftGroupPlayersFilters.filters.teamFilter.match;

const teamSelector = createSelector(
  [playerNameSelector, teamFilterPropertySelector, teamFilterMatchSelector, searchFilterMatchSelector],
  (collection, filterProperty, teamArray, searchFilterMatch) => {
    // If the user is searching via player name, ignore any other filters.
    if (searchFilterMatch !== '') {
      return collection;
    }
    return inArrayFilter(collection, filterProperty, teamArray);
  }
);


// Filter players based on the position filter
const positionFilterPropertySelector = (state) => state.draftGroupPlayersFilters.filters.positionFilter.filterProperty;
const positionFilterMatchSelector = (state) => state.draftGroupPlayersFilters.filters.positionFilter.match;

export const filteredPlayersSelector = createSelector(
  [teamSelector, positionFilterPropertySelector, positionFilterMatchSelector, searchFilterMatchSelector],
  (collection, filterProperty, searchString, searchFilterMatch) => {
    // If the user is searching via player name, ignore any other filters.
    if (searchFilterMatch !== '') {
      return collection;
    }

    return matchFilter(collection, filterProperty, searchString);
  }
);
