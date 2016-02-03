import { sortByOrder } from 'lodash';


/**
 * A reusable Selector function that will sort a collection of stuff based on a property.
 * @param  {array} collection         A list of stuff.
 * @param  {string} sortProperty      The property to sort by.
 * @param  {string} direction         The sort direction ['asc' or 'desc']
 * @return {array}                    The sorted collection
 */
export const orderBy = (collection, sortProperty, direction = 'desc') => {
  let sorted = sortByOrder(collection, sortProperty);

  if (direction === 'asc') {
    sorted = sorted.reverse();
  }

  // Due to how lodash sorts, these columns should be reverse-sorted.
  if (['buyin', 'start', 'prize_pool'].indexOf(sortProperty) > -1) {
    sorted = sorted.reverse();
  }

  return sorted;
};
