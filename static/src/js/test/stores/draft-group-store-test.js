'use strict';

require('../test-dom')();
var request = require("superagent");
var fixtures = require('../../fixtures/draft-group-nba.js');
require('superagent-mock')(request, fixtures);
var expect = require('chai').expect;
var sinon = require('sinon');
var DraftGroupStore = require('../../stores/draft-group-store.js');
var DraftActions = require('../../actions/draft-actions');


describe("DraftGroupStore", function() {
  var sortBySalarySpy = sinon.spy(DraftGroupStore, "sort");


  /**
   * Before the test are run, test that store is initialized empty, then load it up with the
   * data fixtures.
   */
  before(function() {
    expect(DraftGroupStore.allPlayers.length).to.equal(
      0, "data.players is not initially empty"
    );
    expect(DraftGroupStore.data.sport).to.equal(
      null, "data.sport is not initially null"
    );
    expect(DraftGroupStore.data.filteredPlayers.length).to.equal(
      0, "data.filteredPlayers is not initially empty"
    );

    // Load in some fixture data.
    DraftActions.loadDraftGroup.trigger(1);
  });


  it("should have populated the store on DraftActions.loadDraftGroup()", function() {
    // Ensure that the player list is sorted after data is fetched.
    expect(sortBySalarySpy.callCount).to.equal(1,
      "Players do not get sorted after being fetched."
    );

    expect(DraftGroupStore.allPlayers.length).to.be.above(0,
      "data.players does not populate after data is fetched"
    );

    expect(DraftGroupStore.data.filteredPlayers.length).to.be.above(0,
      "data.filteredPlayers does not populate after data is fetched"
    );
  });


  // it("should set the playerFocused property when the setFocusedPlayer() action is called", function() {
  //   var setFocusedPlayerSpy = sinon.spy(DraftGroupStore, "setFocusedPlayer");
  //   expect(DraftGroupStore.data.focusedPlayerId).to.equal(null);
  //
  //   DraftActions.playerFocused(666).then(function() {
  //     expect(setFocusedPlayerSpy.callCount).to.equal(1);
  //     expect(DraftGroupStore.data.focusedPlayerId).to.equal(666);
  //   });
  // });


  // it("should sort players by salary with sortBySalary()", function() {
  //   /**
  //    * Start with a list of unordered salaries and run them through the sort function, then
  //    * test for sort.
  //    */
  //   var unorderedPlayers = [
  //     {salary: 10},
  //     {salary: 20},
  //     {salary: 50},
  //     {salary: 10}
  //   ];
  //
  //   var orderedPlayers = DraftGroupStore.sortBySalary(unorderedPlayers);
  //
  //   // Go through each player and check if their salary is greater than or equal to the next.
  //   for (var i = 1; i < orderedPlayers.length; i++) {
  //     expect(
  //       orderedPlayers[i-1].salary
  //     ).to.be.at.least(
  //       orderedPlayers[i].salary
  //     );
  //   }
  // });

});
