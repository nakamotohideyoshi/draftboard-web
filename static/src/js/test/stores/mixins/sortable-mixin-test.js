'use strict';

var expect = require("chai").expect;
var mixin = require('../../../stores/mixins/sortable-mixin.js');

var collection = [
  {order: 2},
  {order: 5},
  {order: 1},
  {order: 4},
  {order: 3}
];


describe('SortableMixin', function() {

  before(function() {
    // override the sortableUpdated method to prevent warnings.
    mixin.sortableUpdated = function(){};
  });


  it("setSortDirection() should set the sortDirection property.", function() {
    // should default to descending.
    expect(mixin.sortDirection).to.be.equal('desc');
    mixin.setSortDirection('asc');
    expect(mixin.sortDirection).to.be.equal('asc');
  });


  it("setSortProperty() should set the sortProperty property.", function() {
    // should default to null.
    expect(mixin.sortProperty).to.be.equal(null);
    mixin.setSortProperty('order');
    expect(mixin.sortProperty).to.be.equal('order');
  });


  it("should sort the collection by the specified property.", function() {
    // Set the sort property.
    mixin.setSortProperty('order');
    // Sort it.
    var sortedCollection = mixin.sort(collection);
    // Check order of collection to make sure it actually is sorted.
    sortedCollection.reduce(function(previousValue, currentValue) {
      if (previousValue) {
        expect(currentValue.order).to.be.below(previousValue.order);
      }
    });

    // reverse the sortDirection.
    mixin.setSortDirection('asc');
    sortedCollection = mixin.sort(collection);
    // Check order of collection to make sure it actually is sorted.
    sortedCollection.reduce(function(previousValue, currentValue) {
      if (previousValue) {
        expect(currentValue.order).to.be.above(previousValue.order);
      }
    });
  });


  it("should default to descending sort if a bogus value is provided.", function() {
    mixin.sortDirection = 'bogus';
    mixin.sort([]);
    expect(mixin.sortDirection).to.equal('desc');
  });

});
