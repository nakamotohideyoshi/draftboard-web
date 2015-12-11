import { createSelector } from 'reselect'
import { stringSearchFilter, matchFilter } from './filters'
import {forEach as _forEach} from 'lodash'

// All the players in the state.

const allPlayersSelector = (state) => state.draftDraftGroup.allPlayers


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


const filterPropertySelector = (state) => state.draftDraftGroup.filters.playerSearchFilter.filterProperty
const filterMatchSelector = (state) => state.draftDraftGroup.filters.playerSearchFilter.match

const playerNameSelector = createSelector(
  [playersWithInjuryInfo, filterPropertySelector, filterMatchSelector],
  (collection, filterProperty, searchString) => {
    return  stringSearchFilter(collection, filterProperty, searchString)
  }
)


const positionFilterPropertySelector = (state) => state.draftDraftGroup.filters.positionFilter.filterProperty
const positionFilterMatchSelector = (state) => state.draftDraftGroup.filters.positionFilter.match

export const draftGroupPlayerSelector = createSelector(
  [playerNameSelector, positionFilterPropertySelector, positionFilterMatchSelector],
  (collection, filterProperty, searchString) => {
    return matchFilter(collection, filterProperty, searchString)
  }
)
