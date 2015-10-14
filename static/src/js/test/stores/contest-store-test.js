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
    ContestActions.contestFocused.trigger(666);
    expect(this.ContestStore.data.focusedContestId).to.equal(666);
  });


  it("setFocusedContest() should set focusedContestId", function() {
    this.ContestStore.setFocusedContest(999);
    expect(this.ContestStore.data.focusedContestId).to.equal(999);
  });


  it("getFocusedContest() should get the focused contest object", function() {
    // Get contest fixtures by triggering the load action.
    ContestActions.load.trigger();
    // Grab any old contest.
    var focusedContest = this.ContestStore.allContests[0];
    // set it as active.
    this.ContestStore.data.focusedContestId = focusedContest.id;
    // make sure getFocusedContest() gets the one we set.
    expect(this.ContestStore.getFocusedContest()).to.equal(focusedContest);
  });


  it(
  "getCurrentfocusedContestIndex() should get the index of the contest in the allContests array",
  function ()  {
    // Get contest fixtures.
    // Trigger the load action
    ContestActions.load.trigger();

    var index = 2;
    // grab a contest.
    var focusedContest = this.ContestStore.allContests[index];
    // set it as active.
    this.ContestStore.data.focusedContestId = focusedContest.id;
    // make sure getFocusedContest() gets the one we set.
    expect(this.ContestStore.getCurrentfocusedContestIndex()).to.equal(index);
  });



  it('should get the next row with getNextVisibleRowId()', function() {
    ContestActions.load.trigger();

    var index = 0;
    // grab a contest.
    var focusedContest = this.ContestStore.data.filteredContests[index];
    // set it as focused.
    this.ContestStore.data.focusedContestId = focusedContest.id;

    expect(
      this.ContestStore.getNextVisibleRowId()).to.equal(
      this.ContestStore.data.filteredContests[index + 1].id
    );

    expect(
      this.ContestStore.getCurrentfocusedContestIndex()
    ).to.equal(index);

  });


  it('should get the prev row with getPreviousVisibleRowId()', function() {
    ContestActions.load.trigger();

    var index = 1;
    // grab a contest.
    var focusedContest = this.ContestStore.data.filteredContests[index];
    // set it as focused.
    this.ContestStore.data.focusedContestId = focusedContest.id;

    expect(
      this.ContestStore.getPreviousVisibleRowId()).to.equal(
      this.ContestStore.data.filteredContests[index - 1].id
    );

    expect(
      this.ContestStore.getCurrentfocusedContestIndex()
    ).to.equal(index);

  });



  it("should run the sortable mixin's sort method on sortableUpdated()", function() {
    this.ContestStore.sort = function(){};
    var sortSpy = sinon.spy(this.ContestStore, 'sort');
    this.ContestStore.sortableUpdated();
    expect(sortSpy.callCount).to.equal(1);
  });


  it("should run the sortable mixin's sort method on filterUpdated()", function() {
    this.ContestStore.runFilters = function(){};
    var filterSpy = sinon.spy(this.ContestStore, 'runFilters');
    this.ContestStore.sort = function(){};
    var sortSpy = sinon.spy(this.ContestStore, 'sort');

    this.ContestStore.filterUpdated();
    expect(filterSpy.callCount).to.equal(1);
    expect(sortSpy.callCount).to.equal(1);

  });


});
