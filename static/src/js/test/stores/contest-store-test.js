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
    this.ContestStore = require("../../stores/contest-store");
  });

  it("should connect contestFocused action to setFocusedContest()", function() {
    sinon.spy(ContestActions, "contestFocused");
    ContestActions.contestFocused(666);
    sinon.assert.calledOnce(ContestActions.contestFocused);
    this.ContestStore.setFocusedContest(666);
    expect(this.ContestStore.data.focusedContestId).to.equal(666);
  });

  it("should return a collection of contests", function() {
    var self = this;

    // Trigger the load action
    ContestActions.load.triggerPromise().then(function(body) {
      // This is dumb to statically set '7', but we know there are 7 contests in the fixtures, so make sure they get
      // retrieved and set when the action is fired.
      expect(self.ContestStore.data.length).to.equal(7);
    }).catch(function(err) {
      expect(self.ContestStore.data.length).to.equal(7);
      console.log(err);
    });
  });

});
