import {matchFilter} from './filters'
import { createSelector } from 'reselect'


// All the upcoming lineups in the state.
const allLineupsSelector = (state) => state.upcomingLineups.lineups


/**
 * Filter the list by the sport selection dropdown...
 */
const sportSelectorProperty = () => 'sport'
const sportSelectorMatch = (state) => state.upcomingContests.filters.sportFilter.match


// filter the contests by sport.
export const LineupsBySportSelector = createSelector(
  [allLineupsSelector, sportSelectorProperty, sportSelectorMatch],
  (collection, filterProperty, searchString) => {
    return matchFilter(collection, filterProperty, searchString)
  }
)
