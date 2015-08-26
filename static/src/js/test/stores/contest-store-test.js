"use strict";

require("../test-dom")();
var request = require("superagent");
var fixtures = require("../../fixtures/contests.js");
require("superagent-mock")(request, fixtures);
var expect = require("chai").expect;
var sinon = require("sinon");
var ContestActions = require("../../actions/contest-actions");
var MatchFilter = require('../../components/contest-list/contest-store-property-match-filter.jsx');

describe("ContestStore", function() {

  beforeEach(function() {
    this.ContestStore = require("../../stores/contest-store.js");
  });


  it("should connect contestFocused action to setFocusedContest()", function() {
    sinon.spy(ContestActions, "contestFocused");

    ContestActions.contestFocused(666).then(function() {
      sinon.assert.calledOnce(ContestActions.contestFocused);
      expect(this.ContestStore.data.focusedContestId).to.equal(666);
    });
  });


  it("should return a collection of contests", function() {
    var self = this;
    // Trigger the load action
    return ContestActions.load.triggerPromise().then(function() {
      // This is dumb to statically set '6', but we know there are 10 contests in the
      // fixtures, so make sure they get retrieved.
      expect(self.ContestStore.data.contests.length).to.equal(10);
    });
  });


  it("should register a filter", function() {
    // Empty filters, register one, check that it was added.
    this.ContestStore.filters = [];
    expect(this.ContestStore.filters.length).to.equal(0);
    this.ContestStore.registerFilter(MatchFilter);
    expect(this.ContestStore.filters.length).to.equal(1);
  });

});
