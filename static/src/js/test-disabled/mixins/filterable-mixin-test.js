'use strict';

var expect = require("chai").expect;
var sinon = require("sinon");
var mixin = require('../../../stores/mixins/filterable-mixin.js');

var fakeFilter = {
  props: {filterName: 'fakeName'},
  filter: function(row){
    return row.shouldPass;
  }
};

var collection = [
  {shouldPass: true},
  {shouldPass: true},
  {shouldPass: true},
  {shouldPass: false},
  {shouldPass: false}
];


describe('FilterableMixin', function() {

  it("registerFilter() should add a filterComponent to the filters array.", function() {
    expect(mixin.filters.length).to.be.equal(0);
    mixin.registerFilter(fakeFilter);
    expect(mixin.filters.length).to.be.equal(1);
  });


  it("runFilters() should run shouldDisplayRow on every item in the collection", function() {
    var spy = sinon.spy(mixin, 'shouldDisplayRow');
    mixin.runFilters(collection);
    sinon.assert.callCount(spy, collection.length);
  });


  it("runFilters() should return rows that pass the filter's filter() function", function() {
    // Because there are 3 rows in the collection that will pass our fakefilter, we expect
    // this to return 3.
    expect(mixin.runFilters(collection).length).to.equal(3);
  });

});
