import map from 'lodash/map';
import merge from 'lodash/merge';
import uniqBy from 'lodash/uniqBy';
import zipObject from 'lodash/zipObject';
import { createSelector } from 'reselect';
import { dateNow } from '../lib/utils';


const entriesItemsSelector = (state) => state.entries.items;
const entriesSelector = (state) => state.entries;

/**
 * Simple selector to return unique entries and if they are finished loading.
 * Used by the opening window in /live/ to choose a sport -> lineup
 */
export const uniqueEntriesSelector = createSelector(
  [entriesSelector],
  (entries) => {
    const uniqueEntriesArray = uniqBy(map(entries.items, (entry) => entry), 'lineup');
    const uniqueEntries = zipObject(
      map(uniqueEntriesArray, 'lineup'),
      // add in hasStarted to values
      map(uniqueEntriesArray, (entry) => merge({}, entry, {
        hasStarted: new Date(entry.start).getTime() < dateNow(),
        start: new Date(entry.start).getTime(),
      }))
    );

    return {
      entries: uniqueEntriesArray,  // for choosing lineup in live
      entriesObj: uniqueEntries,  // for showing countdown before lineup is loaded in
      haveLoaded: entries.isFetching === false,  // to know when to show entries to choose from
    };
  }
);

export const entriesHaveRelatedInfoSelector = createSelector(
  [entriesSelector], (entries) => entries.hasRelatedInfo
);

export const entriesContestLineupSelector = createSelector(
  [entriesItemsSelector], (entries) => map(entries, (entry) => ({
    contest: entry.contest,
    lineup: entry.lineup,
  }))
);
