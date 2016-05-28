import { createSelector } from 'reselect';
import { mapValues as _mapValues } from 'lodash';
import { merge as _merge } from 'lodash';
import { orderByProperty } from './order-by-property.js';
import { stringSearchFilter, matchFilter, inArrayFilter } from './filters';
import { isPlayerInLineup } from '../components/draft/draft-utils.js';


// All the players in the state.
const allPlayersSelector = (state) => state.draftGroupPlayers.allPlayers;
const injuriesSelector = (state) => state.injuries;
const historiesSelector = (state) => state.fantasyHistory;
const sportInfoSelector = (state) => state.sports;
const boxScoreGamesSelector = (state) => state.upcomingDraftGroups.boxScores;
const activeDraftGroupIdSelector = (state) => state.upcomingDraftGroups.activeDraftGroupId;
const sportSelector = (state) => state.draftGroupPlayers.sport;
const availablePositionSelector = (state) => state.createLineup.availablePositions;
const newLineupSelector = (state) => state.createLineup.lineup;
const remainingSalarySelector = (state) => state.createLineup.remainingSalary;


// Add injury information to each player.
const playersWithInfo = createSelector(
  allPlayersSelector,
  injuriesSelector,
  historiesSelector,
  sportSelector,
  sportInfoSelector,
  activeDraftGroupIdSelector,
  boxScoreGamesSelector,
  availablePositionSelector,
  newLineupSelector,
  remainingSalarySelector,
  (players, injuries, histories, sport, sportInfo,
    activeDraftGroupId, boxScoreGames, availablePositions, newLineup, remainingSalary
  ) => _mapValues(players, (player) => {
    // Duplicate the player so we don't mutate the state.
    const playerWithInfo = _merge({}, player);
    // Add injury status if we have it.
    if (injuries.hasOwnProperty(player.player_id)) {
      playerWithInfo.status = injuries[player.player_id].status;
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
    }


    return playerWithInfo;
  })

);


/**
 * Sort the players.
 */
const sortDirection = (state) => state.draftGroupPlayers.filters.orderBy.direction;
const sortProperty = (state) => state.draftGroupPlayers.filters.orderBy.filterProperty;

export const draftGroupPlayerSelector = createSelector(
  [playersWithInfo, sortProperty, sortDirection],
  (collection, sortProp, sortDir) => orderByProperty(collection, sortProp, sortDir)
);


/**
 * The folloiwng selectors are used to filter the state.draftGroups.filteredPlayers
 */

// Filter players based on the search filter
const filterPropertySelector = (state) => state.draftGroupPlayers.filters.playerSearchFilter.filterProperty;
const filterMatchSelector = (state) => state.draftGroupPlayers.filters.playerSearchFilter.match;

const playerNameSelector = createSelector(
  [allPlayersSelector, filterPropertySelector, filterMatchSelector],
  (collection, filterProperty, searchString) => stringSearchFilter(collection, filterProperty, searchString)
);


// Filter players based on the team filter
const teamFilterPropertySelector = (state) => state.draftGroupPlayers.filters.teamFilter.filterProperty;
const teamFilterMatchSelector = (state) => state.draftGroupPlayers.filters.teamFilter.match;

const teamSelector = createSelector(
  [playerNameSelector, teamFilterPropertySelector, teamFilterMatchSelector],
  (collection, filterProperty, teamArray) => inArrayFilter(collection, filterProperty, teamArray)
);


// Filter players based on the position filter
const positionFilterPropertySelector = (state) => state.draftGroupPlayers.filters.positionFilter.filterProperty;
const positionFilterMatchSelector = (state) => state.draftGroupPlayers.filters.positionFilter.match;

export const filteredPlayersSelector = createSelector(
  [teamSelector, positionFilterPropertySelector, positionFilterMatchSelector],
  (collection, filterProperty, searchString) => matchFilter(collection, filterProperty, searchString)
);
