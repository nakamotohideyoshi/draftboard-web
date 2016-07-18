import { matchFilter } from './filters';
import { orderByProperty } from './order-by-property.js';
import { createSelector } from 'reselect';
import filter from 'lodash/filter';
// import forEach from 'lodash/forEach';


/**
 * This selector will return all upcoming contests that match the user-selected filter properties
 *  on the lobby page.
 */

// All the upcoming contests in the state.
const allContestsSelector = (state) => state.contestPools.allContests;


/**
 * Then filter that list by the sport selection dropdown...
 */
const sportSelectorProperty = (state) => state.contestPools.filters.sportFilter.filterProperty;
const sportSelectorMatch = (state) => state.contestPools.filters.sportFilter.match;

// filter the contests by sport.
const contestsWithMatchingSport = createSelector(
  [allContestsSelector, sportSelectorProperty, sportSelectorMatch],
  (collection, filterProperty, searchString) => matchFilter(collection, filterProperty, searchString)
);


/**
 * Then filter that list by the FEE selection dropdown...
 */
// const feeSelectorProperty = (state) => state.contestPools.filters.contestFeeFilter.filterProperty;
// const feeSelectorMatch = (state) => state.contestPools.filters.contestFeeFilter.match;

// filter the contests by skill level.
const contestsWithMatchingSkillLevel = createSelector(
  [contestsWithMatchingSport],
  (collection) => collection
);


const contestPoolEntriesSelector = (state) => state.contestPoolEntries.entries;

/**
 * Add ContestPoolEntry info to each contest.
 */
const contestsWithEntryInfoSelector = createSelector(
  [contestsWithMatchingSkillLevel, contestPoolEntriesSelector],
  (contests, entries) => contests.map((contest) => {
    const contestWithEntries = Object.assign({}, contest);

    contestWithEntries.entryInfo = filter(
      entries, (entry) => entry.contest_pool === contest.id
    );

    return contestWithEntries;
  })
);

/**
 * Sort the contests.
 */
const sortDirection = (state) => state.contestPools.filters.orderBy.direction;
const sortProperty = (state) => state.contestPools.filters.orderBy.property;

export const contestPoolsSelector = createSelector(
  [contestsWithEntryInfoSelector, sortProperty, sortDirection],
  (collection, sortProp, sortDir) => orderByProperty(collection, sortProp, sortDir)
);
