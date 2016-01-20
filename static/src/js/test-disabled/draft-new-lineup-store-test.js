'use strict';

require('../test-dom')();
var request = require("superagent");
var fixtures = require('../../fixtures/draft-group-nba.js');
var expect = require('chai').expect;
var DraftActions = require('../../actions/draft-actions');


describe("DraftNewLineupStore", function() {

  /**
   * Before the test are run, test that store is initialized empty, then load it up with the
   * data fixtures.
   */
  before(function() {
    this.DraftGroupStore = require('../../stores/draft-group-store.js');
    this.DraftNewLineupStore = require('../../stores/draft-new-lineup-store.js');
    this.requestMock = require('superagent-mock')(request, fixtures);
  });


  beforeEach(function() {
    expect(this.DraftNewLineupStore.data.errorMessage).to.equal(
      "", "data.errorMessage is not empty on initialization."
    );

    // Load in some fixture data into the draft group.
    DraftActions.loadDraftGroup.trigger(1);
    // Since the this.DraftNewLineupStore is listening for the this.DraftGroupStore to update, we'll just
    // manually jam the fixtures in there.
    this.DraftNewLineupStore.draftGroupUpdated(fixtures[0].fixtures());
    // Empty the lineup before each test.
    this.DraftNewLineupStore.resetLineup();
  });


  after(function() {
    this.requestMock.unset();
  });


  afterEach(function() {
    this.DraftNewLineupStore.resetState();
  });


  it("getPlayerCount() should return a count of lineup players", function() {
    expect(this.DraftNewLineupStore.getPlayerCount()).to.equal(
      0, "either getPlayerCount() doesn't seem to be counting correctly or the lineup is not"
      + "starting out empty"
    );

    // add a player
    this.DraftNewLineupStore.data.lineup[2].player = {name: "fake player"};
    expect(this.DraftNewLineupStore.getPlayerCount()).to.equal(
      1, "getPlayerCount() doesn't seem to be counting correctly"
    );

    // add another player
    this.DraftNewLineupStore.data.lineup[6].player = {name: "another fake player"};
    expect(this.DraftNewLineupStore.getPlayerCount()).to.equal(
      2, "getPlayerCount() doesn't seem to be counting correctly"
    );
  });


  it("addPlayer() should add a player to the lineup", function() {
    expect(this.DraftNewLineupStore.getPlayerCount()).to.equal(
      0, "Lineup is not starting out empty"
    );

    // add a player
    this.DraftNewLineupStore.addPlayer(this.DraftGroupStore.allPlayers[0].player_id);
    expect(this.DraftNewLineupStore.getPlayerCount()).to.equal(
      1, "addPlayer() is not increasing the player count."
    );

    // add another player
    this.DraftNewLineupStore.addPlayer(this.DraftGroupStore.allPlayers[2].player_id);
    expect(this.DraftNewLineupStore.getPlayerCount()).to.equal(
      2, "addPlayer() is not increasing the player count."
    );
  });


  it("addPlayer() should not allow a player to be in the lineup twice.", function() {
    this.DraftNewLineupStore.addPlayer(this.DraftGroupStore.allPlayers[0].player_id);
    this.DraftNewLineupStore.addPlayer(this.DraftGroupStore.allPlayers[0].player_id);

    expect(this.DraftNewLineupStore.getPlayerCount()).to.equal(
      1, "addPlayer() is allowing the a player to be in the lineup more than once."
    );
  });


  it("getTotalSalary() should accurately sum the current salary of the lineup.", function() {
    expect(this.DraftNewLineupStore.getTotalSalary()).to.equal(0,
      "Lineup salary is not startingout at $0"
    );

    // add any player and keep track of their salary.
    this.DraftNewLineupStore.addPlayer(this.DraftGroupStore.allPlayers[0].player_id);
    var playerSalary = this.DraftGroupStore.allPlayers[0].salary;

    expect(this.DraftNewLineupStore.getTotalSalary()).to.be.above(0,
      "Lineup salary does not increase when a player is added"
    );

    expect(this.DraftNewLineupStore.getTotalSalary()).to.equal(playerSalary,
      "Lineup.salary does not match salary of players."
    );

    // add another player. + salary
    this.DraftNewLineupStore.addPlayer(this.DraftGroupStore.allPlayers[2].player_id);
    playerSalary += this.DraftGroupStore.allPlayers[2].salary;

    expect(this.DraftNewLineupStore.getTotalSalary()).to.equal(playerSalary,
      "Lineup.salary does not match salary of 2 players."
    );
  });


  it('getAvgRemainingPlayerSalary() should return 0 if lineup is empty', function() {
    expect(this.DraftNewLineupStore.getAvgRemainingPlayerSalary()).to.equal(0);
  });


  it('getAvgRemainingPlayerSalary() should return the mean of player salaries.', function() {
    var player1Salary = this.DraftGroupStore.allPlayers[1].salary;
    var player2Salary = this.DraftGroupStore.allPlayers[2].salary;

    // are we starting at 0?
    expect(this.DraftNewLineupStore.getAvgRemainingPlayerSalary()).to.equal(0);

    // add a player + calculate.
    this.DraftNewLineupStore.addPlayer(this.DraftGroupStore.allPlayers[1].player_id);
    expect(this.DraftNewLineupStore.getAvgRemainingPlayerSalary()).to.equal(player1Salary);

    // add player2 + calculate.
    this.DraftNewLineupStore.addPlayer(this.DraftGroupStore.allPlayers[2].player_id);
    expect(this.DraftNewLineupStore.getAvgRemainingPlayerSalary()).to.equal(
      (player1Salary + player2Salary) / 2
    );
  });


  it('isPlayerInLineup() should detect players already in the lineup', function() {
    var player = this.DraftGroupStore.allPlayers[2];

    // should not be in the lineup.
    expect(
      this.DraftNewLineupStore.isPlayerInLineup(player)
    ).to.equal(false);

    // add player.
    this.DraftNewLineupStore.addPlayer(player.player_id);

    // should now be in the lineup.
    expect(
      this.DraftNewLineupStore.isPlayerInLineup(player)
    ).to.equal(true);
  });


  it("findAvailablePositions() should find available positions", function() {
    // First do a simple count to make sure that it's adding all of the positions.
    var positionCount = 0;

     this.DraftNewLineupStore.rosterTemplates.nba.forEach(function(slot) {
        positionCount +=  slot.positions.length;

        // Make sure each of the positions in the template are in
        // this.DraftNewLineupStore.data.availablePositions.
        slot.positions.forEach(function(position) {
          expect(
            this.DraftNewLineupStore.data.availablePositions.indexOf(position)
          ).to.not.equal(-1);
        }.bind(this));
    }.bind(this));

    expect(this.DraftNewLineupStore.data.availablePositions.length).to.equal(positionCount);

    // Next fill up a slot and re-check the count.
    this.DraftNewLineupStore.addPlayer(this.DraftGroupStore.allPlayers[1].player_id);
    this.DraftNewLineupStore.findAvailablePositions();
    expect(this.DraftNewLineupStore.data.availablePositions.length).to.equal(positionCount - 1);
  });


  it('removePlayer() should remove a player from the lineup', function() {
    var player0 = this.DraftGroupStore.allPlayers[0];
    var player1 = this.DraftGroupStore.allPlayers[this.DraftGroupStore.allPlayers.length - 3];
    var player2 = this.DraftGroupStore.allPlayers[this.DraftGroupStore.allPlayers.length - 2];
    var player3 = this.DraftGroupStore.allPlayers[this.DraftGroupStore.allPlayers.length - 4];

    /**
      Test with one player in the lineup.
     */

    // make sure we're starting off with all slots open.
    expect(
      this.DraftNewLineupStore.getAvailableLineupSlots().length).to.equal(
      this.DraftNewLineupStore.data.lineup.length
    );

    // add a player
    this.DraftNewLineupStore.addPlayer(player0.player_id);
    expect(this.DraftNewLineupStore.getPlayerCount()).to.equal(
      1, "addPlayer() is not increasing the player count."
    );

    // Make sure that one of the slots is filled.
    expect(
      this.DraftNewLineupStore.getAvailableLineupSlots().length).to.equal(
      this.DraftNewLineupStore.data.lineup.length - 1
    );

    // remove that player
    this.DraftNewLineupStore.removePlayer(player0.player_id);

    // do we have an extra slot open now?
    expect(
      this.DraftNewLineupStore.getAvailableLineupSlots().length).to.equal(
      this.DraftNewLineupStore.data.lineup.length
    );


    /**
      Test with multiple players in the lineup.
    */

    // make sure we're starting off with all slots open.
    expect(
      this.DraftNewLineupStore.getAvailableLineupSlots().length).to.equal(
      this.DraftNewLineupStore.data.lineup.length
    );

    // add three  players
    this.DraftNewLineupStore.addPlayer(player1.player_id);
    this.DraftNewLineupStore.addPlayer(player2.player_id);
    this.DraftNewLineupStore.addPlayer(player3.player_id);

    expect(this.DraftNewLineupStore.getPlayerCount()).to.equal(
      3, "addPlayer() is not increasing the player count."
    );

    // remove one.
    this.DraftNewLineupStore.removePlayer(
      player1.player_id
    );

    // Make sure that two of the slots are still filled.
    expect(
      this.DraftNewLineupStore.getAvailableLineupSlots().length
    ).to.equal(
      this.DraftNewLineupStore.data.lineup.length - 2,
      "removePlayer is not reducing the number of available lineup slots."
    );

    // ensure that we removed the correct player.
    expect(
      this.DraftNewLineupStore.isPlayerInLineup(player2)
    ).to.equal(
      true,
      "removePlayer is not removing the specified player."
    );

    expect(
      this.DraftNewLineupStore.isPlayerInLineup(player3)
    ).to.equal(
      true,
      "removePlayer is not removing the specified player."
    );
  });


});
