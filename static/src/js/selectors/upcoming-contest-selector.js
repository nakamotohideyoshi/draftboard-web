import { stringSearchFilter, matchFilter, rangeFilter } from './filters'
import { createSelector } from 'reselect'

/**
 * This selector will return all upcoming contests that match the user-selected filter properties
 *  on the lobby page.
 */

// All the upcoming contests in the state.
const allContestsSelector = (state) => state.upcomingContests.allContests


/**
 * First, filter the contests by the title search field...
 */
const searchFilterPropertySelector = (state) => state.upcomingContests.filters.contestSearchFilter.filterProperty
const searchFilterMatchSelector = (state) => state.upcomingContests.filters.contestSearchFilter.match

// Search the contest's name.
const contestsWithMatchingTitles = createSelector(
  [allContestsSelector, searchFilterPropertySelector, searchFilterMatchSelector],
  (collection, filterProperty, searchString) => {
    return  stringSearchFilter(collection, filterProperty, searchString)
  }
)


/**
 * Then filter that list by the sport selection dropdown...
 */
const sportSelectorProperty = (state) => state.upcomingContests.filters.sportFilter.filterProperty
const sportSelectorMatch = (state) => state.upcomingContests.filters.sportFilter.match

// filter the contests by sport.
const contestsWithMatchingSport = createSelector(
  [contestsWithMatchingTitles, sportSelectorProperty, sportSelectorMatch],
  (collection, filterProperty, searchString) => {
    return matchFilter(collection, filterProperty, searchString)
  }
)


/**
 * Then filter that list by the sport selection dropdown...
 */
const feeSelectorProperty = (state) => state.upcomingContests.filters.contestFeeFilter.filterProperty
const feeSelectorMatch = (state) => state.upcomingContests.filters.contestFeeFilter.match

// filter the contests by sport.
const contestsWithMatchingFee = createSelector(
  [contestsWithMatchingSport, feeSelectorProperty, feeSelectorMatch],
  (collection, filterProperty, feeSelectorMatch) => {
    return rangeFilter(collection, filterProperty, feeSelectorMatch.minVal, feeSelectorMatch.maxVal)
  }
)


/**
 * Finally, filter them by the contest type [GPP, H2H, etc..].
 */
const typeFilterPropertySelector = (state) => state.upcomingContests.filters.contestTypeFilter.filterProperty
const typeFilterMatchSelector = (state) => state.upcomingContests.filters.contestTypeFilter.match

export const upcomingContestSelector = createSelector(
  [contestsWithMatchingFee, typeFilterPropertySelector, typeFilterMatchSelector],
  (collection, filterProperty, searchString) => {
    return matchFilter(collection, filterProperty, searchString)
  }
)
