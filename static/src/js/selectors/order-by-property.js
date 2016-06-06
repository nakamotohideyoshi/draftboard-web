import orderBy from 'lodash/orderBy';


/**
 * A reusable Selector function that will sort a collection of stuff based on a property.
 * @param  {array} collection         A list of stuff.
 * @param  {string} sortProperty      The property to sort by.
 * @param  {string} direction         The sort direction ['asc' or 'desc']
 * @return {array}                    The sorted collection
 */
export const orderByProperty = (collection, sortProperty, direction = 'desc') => {
  let sorted = orderBy(collection, [sortProperty]);

  if (direction === 'asc') {
    sorted = sorted.reverse();
  }

  // Due to how lodash sorts, these columns should be reverse-sorted.
  if (['buyin', 'start', 'prize_pool', 'fppg', 'salary'].indexOf(sortProperty) > -1) {
    sorted = sorted.reverse();
  }

  return sorted;
};
