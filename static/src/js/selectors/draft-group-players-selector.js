import { createSelector } from 'reselect'
import { stringSearchFilter, matchFilter } from './filters'


// All the players in the state.
const allPlayersSelector = (state) => state.draftDraftGroup.allPlayers
const filterPropertySelector = (state) => state.draftDraftGroup.filters.playerSearchFilter.filterProperty
const filterMatchSelector = (state) => state.draftDraftGroup.filters.playerSearchFilter.match

const playerNameSelector = createSelector(
  [allPlayersSelector, filterPropertySelector, filterMatchSelector],
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
