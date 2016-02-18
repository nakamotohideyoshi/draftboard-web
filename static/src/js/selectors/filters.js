import { filter as _filter } from 'lodash';
import log from '../lib/logging.js';


/**
 * [function description]
 * @param  {array} collection     A list of things to filter.
 * @param  {string} property      The property to match against.
 * @param  {string} searchString  A String to match the property.
 * @return {array}                A filtered list of items.
 */
export const stringSearchFilter = (collection, filterProperty, searchString) =>
  _filter(collection, (item) => {
    // Show the row if there is no search query.
    if (!searchString) {
      return true;
    }

    // We can account for nested resources here. so if we want to search for the row.player.name
    // property, just set 'row.player.name' as the search property, this will drill down into the
    // nested properties for it's search target.
    const nestedProps = filterProperty.split('.');
    let searchTarget = item;

    nestedProps.forEach((property) => {
      if (item.hasOwnProperty(property)) {
        searchTarget = item[property];
      }
    });

    // Search in the row's scpecified property for the search string.
    if (searchTarget.toLowerCase().indexOf(searchString.toLowerCase()) === -1) {
      return false;
    }

    // Default to show.
    return true;
  });


/**
 * This filter performs a string match on the specified row property (this.props.filterProperty).
 * @param  {Object} row The single collection row.
 * @return {boolean} Should the row be displayed in the filtered collection list?
 */
export const matchFilter = (collection, filterProperty, match) => _filter(collection, (item) => {
  // If there's nothing to match against, show the item.
  if (!match) {
    return true;
  }

  if (!item.hasOwnProperty(filterProperty)) {
    log.warn('CollectionMatchFilter.filter() Row does not contain property',
      filterProperty);
    return true;
  }

  // If we have a string, just check for equality.
  // We will have a string as a match for sport matching in the lobby. ex: 'nba'
  if (typeof match === 'string') {
    return match.toLowerCase() === item[filterProperty].toLowerCase();
  }

  // If we have an array as a match, check each element for equality individually and return an
  // array of matches.
  //
  // We will have an array as a match for position matching in the draft section ex: ['pg', 'sg']
  const matches = _filter(
    match,
    (matchItem) => matchItem.toLowerCase() === item[filterProperty].toLowerCase()
  );

  // If the array contains a match, return true.
  return matches.length > 0;
});


/**
 * This filter performs a range match on the specified row property (this.props.filterProperty).
 * @param  {Object} row The single collection row.
 * @return {boolean} Should the row be displayed in the filtered collection list?
 */
export const rangeFilter = (collection, filterProperty, minVal, maxVal) => _filter(collection, (item) => {
  // Is the property value less than the minimum range value, or greater than the biggest?
  if (item[filterProperty] < minVal || item[filterProperty] > maxVal) {
    return false;
  }

  return true;
});


/**
 * This filter will determine if a contest is one of [GPP, H2H, or double-up]
 */
export const gameTypeFilter = (collection, gameType) => _filter(collection, (item) => {
  switch (gameType) {
    case 'gpp':
      return item.gpp;

    case 'double-up':
      return item.doubleup;

    case 'h2h':
      return (item.entries === 2);

    default:
      return true;
  }
});


// Given an array of matches (matchList), look at each collection item's [filterProperty] for
// matches. This is used on the game filter in the drafting section for filtering players based
// on a list of team IDs... basically, is this player's team in the list of team IDs?
export const inArrayFilter = (collection, filterProperty, matchList) => {
  if (!matchList || !filterProperty || !matchList.length) {
    return collection;
  }

  const matches = _filter(collection, (item) => matchList.indexOf(item[filterProperty]) !== -1);

  return matches;
};
