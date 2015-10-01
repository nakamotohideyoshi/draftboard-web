"use strict";

require("../test-dom")();
var request = require("superagent");
var fixtures = require("../../fixtures/contests.js");
require("superagent-mock")(request, fixtures);
var expect = require("chai").expect;
var sinon = require("sinon");
var ContestActions = require("../../actions/contest-actions");


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


  it("setFocusedContest() should set focusedContestId", function() {
    this.ContestStore.setFocusedContest(999);
    expect(this.ContestStore.data.focusedContestId).to.equal(999);
  });


  it("getFocusedContest() should get the focused contest object", function() {
    // Get contest fixtures.
    // Trigger the load action
    return ContestActions.load.triggerPromise().then(function() {
      // grab a contest.
      var focusedContest = this.ContestStore.allContests[0];
      // set it as active.
      this.ContestStore.data.focusedContestId = focusedContest.id;
      // make sure getFocusedContest() gets the one we set.
      expect(this.ContestStore.getFocusedContest()).to.equal(focusedContest);
    }.bind(this));
  });


  it(
  "getCurrentfocusedContestIndex() should get the index of the contest in the allContests array",
  function ()  {
    // Get contest fixtures.
    // Trigger the load action
    return ContestActions.load.triggerPromise().then(function() {
      var index = 2;
      // grab a contest.
      var focusedContest = this.ContestStore.allContests[index];
      // set it as active.
      this.ContestStore.data.focusedContestId = focusedContest.id;
      // make sure getFocusedContest() gets the one we set.
      expect(this.ContestStore.getCurrentfocusedContestIndex()).to.equal(index);
    }.bind(this));

  });


  // TODO: This is intermittently not working on codeship, ignore it until I figure it out.
  // it("should return a collection of contests", function() {
  //   var self = this;
  //   // Trigger the load action
  //   return ContestActions.load.triggerPromise().then(function() {
  //     // This is dumb to statically set '6', but we know there are 10 contests in the
  //     // fixtures, so make sure they get retrieved.
  //     expect(self.ContestStore.data.contests.length).to.equal(10);
  //   });
  // });


  // it("should register a filter", function() {
  //   // Empty filters, register one, check that it was added.
  //   this.ContestStore.filters = [];
  //   expect(this.ContestStore.filters.length).to.equal(0);
  //   this.ContestStore.registerFilter(MatchFilter);
  //   expect(this.ContestStore.filters.length).to.equal(1);
  // });

});
