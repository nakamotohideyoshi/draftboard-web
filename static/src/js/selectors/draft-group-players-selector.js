import { createSelector } from 'reselect';
import { stringSearchFilter, matchFilter, inArrayFilter } from './filters';
import { orderBy } from './order-by.js';
import { mapValues as _mapValues } from 'lodash';


// All the players in the state.
const allPlayersSelector = (state) => state.draftGroupPlayers.allPlayers;

// Add injury information to each player.
const playersWithInjuryInfo = createSelector(
  allPlayersSelector,
  (state) => state.injuries,
  (players, injuries) => _mapValues(players, (player) => {
    // Duplicate the player so we don't mutate the state.
    const playerWithStatus = Object.assign({}, player);
    // Add status if we have it.
    if (injuries.hasOwnProperty(player.player_id)) {
      playerWithStatus.status = injuries[player.player_id].status;
    }
    return playerWithStatus;
  })
);


// Add fantasy history information to each player.
const histories = (state) => state.fantasyHistory;

const playersWithHistory = createSelector(
  [playersWithInjuryInfo, histories],
  (players, playerHistories) => _mapValues(players, (player) => {
    // Duplicate the player so we don't mutate the state.
    const playerWithHistory = Object.assign({}, player);
    // Add status if we have it.
    if (playerHistories.hasOwnProperty(player.player_id)) {
      playerWithHistory.history = playerHistories[player.player_id].fantasy_points;
    }
    return playerWithHistory;
  })
);


// Filter players based on the search filter
const filterPropertySelector = (state) => state.draftGroupPlayers.filters.playerSearchFilter.filterProperty;
const filterMatchSelector = (state) => state.draftGroupPlayers.filters.playerSearchFilter.match;

const playerNameSelector = createSelector(
  [playersWithHistory, filterPropertySelector, filterMatchSelector],
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
