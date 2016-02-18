import { matchFilter } from './filters';
import { createSelector } from 'reselect';
import { sortByOrder as _sortByOrder } from 'lodash';


/**
 * Filter the list by the sport selection dropdown...
 */
const sportSelectorProperty = () => 'sport';
const sportSelectorMatch = (state) => state.upcomingContests.filters.sportFilter.match;
// All the upcoming lineups in the state.
const allLineupsSelector = (state) => state.upcomingLineups.lineups;


// filter the lineups by sport.
export const lineupsBySportSelector = createSelector(
  allLineupsSelector,
  sportSelectorProperty,
  sportSelectorMatch,
  (collection, filterProperty, searchString) => (
    // Sort + filter them.
    _sortByOrder(matchFilter(collection, filterProperty, searchString), 'id').reverse()
  )
);
