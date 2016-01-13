import { createSelector } from 'reselect'
import { stringSearchFilter, matchFilter, inArrayFilter } from './filters'
import {orderBy} from './order-by.js'
import {forEach as _forEach} from 'lodash'


// All the players in the state.
const allPlayersSelector = (state) => state.draftGroupPlayers.allPlayers


// Add injury information to each player.
const injuries = (state) => state.injuries

const playersWithInjuryInfo = createSelector(
  [allPlayersSelector, injuries],
  (players, injuries) => {
    // Loop through each player and find any matching injuries.
    return _forEach(players, function(player) {
      if (injuries.hasOwnProperty(player.player_id)) {
        player.status = injuries[player.player_id].status
      }
    })
  }
)


// Add fantasy history information to each player.
const histories = (state) => state.fantasyHistory

const playersWithHistory = createSelector(
  [playersWithInjuryInfo, histories],
  (players, histories) => {
    // Loop through each player and attach their FP histories.
    return _forEach(players, function(player) {
      if (histories.hasOwnProperty(player.player_id)) {
        player.history = histories[player.player_id].fantasy_points
      }
    })
  }
)


// Filter players based on the search filter
const filterPropertySelector = (state) => state.draftGroupPlayers.filters.playerSearchFilter.filterProperty
const filterMatchSelector = (state) => state.draftGroupPlayers.filters.playerSearchFilter.match

const playerNameSelector = createSelector(
  [playersWithHistory, filterPropertySelector, filterMatchSelector],
  (collection, filterProperty, searchString) => {
    return  stringSearchFilter(collection, filterProperty, searchString)
  }
)


// Filter players based on the team filter
const teamFilterPropertySelector = (state) => state.draftGroupPlayers.filters.teamFilter.filterProperty
const teamFilterMatchSelector = (state) => state.draftGroupPlayers.filters.teamFilter.match

const teamSelector = createSelector(
  [playerNameSelector, teamFilterPropertySelector, teamFilterMatchSelector],
  (collection, filterProperty, teamArray) => {

    return  inArrayFilter(collection, filterProperty, teamArray)
  }
)


// Filter players based on the position filter
const positionFilterPropertySelector = (state) => state.draftGroupPlayers.filters.positionFilter.filterProperty
const positionFilterMatchSelector = (state) => state.draftGroupPlayers.filters.positionFilter.match

const positionSelector = createSelector(
  [teamSelector, positionFilterPropertySelector, positionFilterMatchSelector],
  (collection, filterProperty, searchString) => {
    return matchFilter(collection, filterProperty, searchString)
  }
)


/**
 * Sort the contests.
 */
const sortDirection = (state) => state.draftGroupPlayers.filters.orderBy.direction
const sortProperty = (state) => state.draftGroupPlayers.filters.orderBy.property

export const draftGroupPlayerSelector = createSelector(
  [positionSelector, sortProperty, sortDirection],
  (collection, sortProperty, sortDirection) => {
    return orderBy(collection, sortProperty, sortDirection)
  }
)
