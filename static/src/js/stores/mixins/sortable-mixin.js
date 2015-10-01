'use strict';

var log = require("../../lib/logging");
var _sortByOrder = require("lodash/collection/sortByOrder");


/**
 * Add this mixin to a data store for sorting functionality on a collection.
 * @type {Object}
 */
var SortableMixin = {

  sortProperty: null,
  sortDirection: 'desc',


  // Dummy method if not implemented on store..
  sortableUpdated: function() {
    log.warn("Stores implementing 'SortableMixin' require a 'sortableUpdated' method.");
  },


  sort: function(collection) {
    log.debug('SortableMixin.sort()', this.sortProperty, this.sortDirection);
    if (this.sortDirection !== 'desc' && this.sortDirection !== 'asc') {
      log.warn('SortableMixin.sort() - Sort direction was not provided, defaulting to desc.');
      this.sortDirection = 'desc';
    }

    // Sort the rows by the currently active filter.
    if (this.sortDirection === 'desc') {
      collection = _sortByOrder(collection, this.sortProperty).reverse();
    } else {
      collection = _sortByOrder(collection, this.sortProperty);
    }

    return collection;
  },


  setSortDirection: function(direction) {
    this.sortDirection = direction;
    this.sortableUpdated();
  },


  setSortProperty: function(property) {
    // If the requested sort property is the current property, flip the order.
    if (property === this.sortProperty) {
      this.sortDirection = (this.sortDirection === 'asc') ? 'desc' : 'asc';
    } else {
      this.sortProperty = property;
    }

    this.sortableUpdated();
  }

};


module.exports = SortableMixin;
