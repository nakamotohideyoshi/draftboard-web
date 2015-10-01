'use strict';

var log = require("../../lib/logging");


/**
 * If you want to use any of our filter components, you'll need to add this mixin to the store.
 */
var FilterableMixin = {

  filters: [],
  // activeFilters: [],


  /**
   * Register a filter with this component.
   *
   * @param {Object} filterComponent - The react filter comonent.
   */
  registerFilter: function(filterComponent) {
    log.debug('FilterableMixin.registerFilter()', filterComponent.props.filterName);
    // Push the filter into the state filter stack.
    this.filters = this.filters.concat(filterComponent);
  },


  /**
   * Determine if a row should be dislayed by running the filter() method on all of
   * the component's registered filters.
   *
   * @param {Object} row - A row of data from the state.data array.
   * @return {boolean} Should the row be displayed?
   */
  shouldDisplayRow: function(row) {
    // Default to showing the row.
    var show = true;
    // Run through each registered filter and determine if the row should be displayed.
    for (var i in this.filters) {
      show = this.filters[i].filter(row);
      // As soon as we get a false, stop running filters and return;
      if (show === false) {
        break;
      }
    }

    return show;
  },


  /**
   * For each row in the collection, run all filters on it to determine if it should be displayed.
   */
  runFilters: function(collection) {
    log.debug('FilterableMixin.runFilters()');
    var rows = [];

    // Loop through all sorted data rows, determine if they should be displayed and build a list
    // of visible data rows,
    // TODO: This can be replaced with the cleaner Array.map()
    for (var i = 0; i < collection.length; i++) {
      if(this.shouldDisplayRow(collection[i])) {
        rows.push(collection[i]);
      }
    }

    return rows;
  }

};


module.exports = FilterableMixin;
