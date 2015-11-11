import { stringSearchFilter, matchFilter } from './filters'
import { createSelector } from 'reselect'


// All the players in the state.
const allContestsSelector = (state) => state.upcomingContests.allContests
const searchFilterPropertySelector = (state) => state.upcomingContests.filters.contestSearchFilter.filterProperty
const searchFilterMatchSelector = (state) => state.upcomingContests.filters.contestSearchFilter.match

// Search the contest's name.
const contestNameSelector = createSelector(
  [allContestsSelector, searchFilterPropertySelector, searchFilterMatchSelector],
  (collection, filterProperty, searchString) => {
    return  stringSearchFilter(collection, filterProperty, searchString)
  }
)


const typeFilterPropertySelector = (state) => state.upcomingContests.filters.contestTypeFilter.filterProperty
const typeFilterMatchSelector = (state) => state.upcomingContests.filters.contestTypeFilter.match

export const upcomingContestSelector = createSelector(
  [contestNameSelector, typeFilterPropertySelector, typeFilterMatchSelector],
  (collection, filterProperty, searchString) => {
    return matchFilter(collection, filterProperty, searchString)
  }
)
