import { filter as _filter } from 'lodash'

/**
 * [function description]
 * @param  {array} collection     A list of things to filter.
 * @param  {string} property      The property to match against.
 * @param  {string} searchString  A String to match the property.
 * @return {array}                A filtered list of items.
 */
export const stringSearchFilter = function (collection, filterProperty, searchString) {
  return _filter(collection, function(item) {

    // Show the row if there is no search query.
    if (!searchString) {
      return true;
    }

    // We can account for nested resources here. so if we want to search for the row.player.name
    // property, just set 'row.player.name' as the search property, this will drill down into the
    // nested properties for it's search target.
    var nestedProps = filterProperty.split('.');
    var searchTarget = item;

    nestedProps.forEach(function(filterProperty) {
      if (item.hasOwnProperty(filterProperty)) {
        searchTarget = item[filterProperty];
      }
    });

    // Search in the row's scpecified property for the search string.
    if (searchTarget.toLowerCase().indexOf(searchString.toLowerCase()) === -1) {
      return false;
    }
    // Default to show.
    return true;
  })
}


/**
 * This filter performs a string match on the specified row property (this.props.filterProperty).
 * @param  {Object} row The single collection row.
 * @return {boolean} Should the row be displayed in the filtered collection list?
 */
export const matchFilter = function(collection, filterProperty, match) {
  return _filter(collection, function(item) {
    // If there's nothing to match against, show the item.
    if (!match) {
        return true
    }

    if(!item.hasOwnProperty(filterProperty)) {
        console.warn('CollectionMatchFilter.filter() Row does not contain property',
        filterProperty);
        return true;
    } else {
      // Check if the row's property matches this filter's match value.
      if (match === '' || item[filterProperty].toLowerCase() === match.toLowerCase()) {
        return true;
      }

      return false;
    }
  })
}



/**
 * This filter performs a range match on the specified row property (this.props.filterProperty).
 * @param  {Object} row The single collection row.
 * @return {boolean} Should the row be displayed in the filtered collection list?
 */
export const rangeFilter = function(collection, filterProperty, minVal, maxVal) {
  return _filter(collection, function(item) {
    // Is the property value less than the minimum range value, or greater than the biggest?
    if (item[filterProperty] < minVal || item[filterProperty] > maxVal) {
      return false;
    }

    return true;
  })
}


/**
 * This filter will determine if a contest is one of [GPP, H2H, or double-up]
 */
export const gameTypeFilter = function(collection, gameType) {
  return _filter(collection, function(item) {
    switch (gameType) {
      case 'gpp':
        return item.gpp

      case 'double-up':
        return item.doubleup

      case 'h2h':
        return (item.entries === 2)

      default:
        return true;
    }
  })
}
