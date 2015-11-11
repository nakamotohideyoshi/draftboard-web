'use strict';

require('../test-dom')();
var request = require("superagent");
var expect = require('chai').expect;
var sinon = require('sinon');
var DraftActions = require('../../actions/draft-actions');


describe("DraftGroupStore", function() {

  /**
   * Before the test are run, test that store is initialized empty, then load it up with the
   * data fixtures.
   */
  before(function() {
    var fixtures = require('../../fixtures/draft-group-nba.js');
    this.requestMock = require('superagent-mock')(request, fixtures);
    this.DraftGroupStore = require('../../stores/draft-group-store.js');
    this.sortBySalarySpy = sinon.spy(this.DraftGroupStore, "sort");

    expect(this.DraftGroupStore.allPlayers.length).to.equal(
      0, "data.players is not initially empty"
    );
    expect(this.DraftGroupStore.data.sport).to.equal(
      null, "data.sport is not initially null"
    );
    expect(this.DraftGroupStore.data.filteredPlayers.length).to.equal(
      0, "data.filteredPlayers is not initially empty"
    );

    // Load in some fixture data.
    DraftActions.loadDraftGroup.trigger(1);
  });


  after(function() {
    this.requestMock.unset();
    this.DraftGroupStore.resetState();
  });


  it("should have populated the store on DraftActions.loadDraftGroup()", function() {
    // Ensure that the player list is sorted after data is fetched.
    expect(this.sortBySalarySpy.callCount).to.equal(1,
      "Players do not get sorted after being fetched."
    );

    expect(this.DraftGroupStore.allPlayers.length).to.be.above(0,
      "data.players does not populate after data is fetched"
    );

    expect(this.DraftGroupStore.data.filteredPlayers.length).to.be.above(0,
      "data.filteredPlayers does not populate after data is fetched"
    );
  });

});
