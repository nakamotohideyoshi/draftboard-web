import { createSelector } from 'reselect';
import { stringSearchFilter, matchFilter, inArrayFilter } from './filters';
import { orderBy } from './order-by.js';
import { mapValues as _mapValues } from 'lodash';


// All the players in the state.
const allPlayersSelector = (state) => state.draftGroupPlayers.allPlayers;
const injuriesSelector = (state) => state.injuries;
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
  (players, injuries, histories, sport, sportInfo,
    activeDraftGroupId, boxScoreGames
  ) => _mapValues(players, (player) => {
    // Duplicate the player so we don't mutate the state.
    const playerWithInfo = Object.assign({}, player);
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
    }

    return playerWithInfo;
  })

);


// Filter players based on the search filter
const filterPropertySelector = (state) => state.draftGroupPlayers.filters.playerSearchFilter.filterProperty;
const filterMatchSelector = (state) => state.draftGroupPlayers.filters.playerSearchFilter.match;

const playerNameSelector = createSelector(
  [playersWithInfo, filterPropertySelector, filterMatchSelector],
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

const positionSelector = createSelector(
  [teamSelector, positionFilterPropertySelector, positionFilterMatchSelector],
  (collection, filterProperty, searchString) => matchFilter(collection, filterProperty, searchString)
);


/**
 * Sort the contests.
 */
const sortDirection = (state) => state.draftGroupPlayers.filters.orderBy.direction;
const sortProperty = (state) => state.draftGroupPlayers.filters.orderBy.property;

export const draftGroupPlayerSelector = createSelector(
  [positionSelector, sortProperty, sortDirection],
  (collection, sortProp, sortDir) => orderBy(collection, sortProp, sortDir)
);
