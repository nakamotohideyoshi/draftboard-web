'use strict';

require('../test-dom')();
var request = require("superagent");
var fixtures = require('../../fixtures/draft-group-nba.js');
require('superagent-mock')(request, fixtures);
var expect = require('chai').expect;
// var sinon = require('sinon');
var DraftActions = require('../../actions/draft-actions');
var DraftGroupStore = require('../../stores/draft-group-store.js');
var DraftNewLineupStore = require('../../stores/draft-new-lineup-store.js');


describe("DraftNewLineupStore", function() {

  /**
   * Before the test are run, test that store is initialized empty, then load it up with the
   * data fixtures.
   */
  before(function() {
    expect(DraftNewLineupStore.data.errorMessage).to.equal(
      "", "data.errorMessage is not empty on initialization."
    );

    // Load in some fixture data into the draft group.
    DraftActions.loadDraftGroup.trigger(1);
    // Since the DraftNewLineupStore is listening for the DraftGroupStore to update, we'll just
    // manually jam the fixtures in there.
    DraftNewLineupStore.draftGroupUpdated(fixtures[0].fixtures());
  });


  beforeEach(function() {
    // Empty the lineup before each test.
    DraftNewLineupStore.resetLineup();
  });


  it("getPlayerCount() should return a count of lineup players", function() {
    expect(DraftNewLineupStore.getPlayerCount()).to.equal(
      0, "either getPlayerCount() doesn't seem to be counting correctly or the lineup is not"
      + "starting out empty"
    );

    // add a player
    DraftNewLineupStore.data.lineup[2].player = {name: "fake player"};
    expect(DraftNewLineupStore.getPlayerCount()).to.equal(
      1, "getPlayerCount() doesn't seem to be counting correctly"
    );

    // add another player
    DraftNewLineupStore.data.lineup[6].player = {name: "another fake player"};
    expect(DraftNewLineupStore.getPlayerCount()).to.equal(
      2, "getPlayerCount() doesn't seem to be counting correctly"
    );
  });


  it("addPlayer() should add a player to the lineup", function() {
    expect(DraftNewLineupStore.getPlayerCount()).to.equal(
      0, "Lineup is not starting out empty"
    );

    // add a player
    DraftNewLineupStore.addPlayer(DraftGroupStore.allPlayers[0].player_id);
    expect(DraftNewLineupStore.getPlayerCount()).to.equal(
      1, "addPlayer() is not increasing the player count."
    );

    // add another player
    DraftNewLineupStore.addPlayer(DraftGroupStore.allPlayers[2].player_id);
    expect(DraftNewLineupStore.getPlayerCount()).to.equal(
      2, "addPlayer() is not increasing the player count."
    );
  });


  it("addPlayer() should not allow a player to be in the lineup twice.", function() {
    DraftNewLineupStore.addPlayer(DraftGroupStore.allPlayers[0].player_id);
    DraftNewLineupStore.addPlayer(DraftGroupStore.allPlayers[0].player_id);

    expect(DraftNewLineupStore.getPlayerCount()).to.equal(
      1, "addPlayer() is allowing the a player to be in the lineup more than once."
    );
  });


  it("getTotalSalary() should accurately sum the current salary of the lineup.", function() {
    expect(DraftNewLineupStore.getTotalSalary()).to.equal(0,
      "Lineup salary is not startingout at $0"
    );

    // add any player and keep track of their salary.
    DraftNewLineupStore.addPlayer(DraftGroupStore.allPlayers[0].player_id);
    var playerSalary = DraftGroupStore.allPlayers[0].salary;

    expect(DraftNewLineupStore.getTotalSalary()).to.be.above(0,
      "Lineup salary does not increase when a player is added"
    );

    expect(DraftNewLineupStore.getTotalSalary()).to.equal(playerSalary,
      "Lineup.salary does not match salary of players."
    );

    // add another player. + salary
    DraftNewLineupStore.addPlayer(DraftGroupStore.allPlayers[2].player_id);
    playerSalary += DraftGroupStore.allPlayers[2].salary;

    expect(DraftNewLineupStore.getTotalSalary()).to.equal(playerSalary,
      "Lineup.salary does not match salary of 2 players."
    );
  });


  it('getAvgPlayerSalary() should return 0 if lineup is empty', function() {
    expect(DraftNewLineupStore.getAvgPlayerSalary()).to.equal(0);
  });


  it('getAvgPlayerSalary() should return the mean of player salaries.', function() {
    var player1Salary = DraftGroupStore.allPlayers[1].salary;
    var player2Salary = DraftGroupStore.allPlayers[2].salary;

    // are we starting at 0?
    expect(DraftNewLineupStore.getAvgPlayerSalary()).to.equal(0);

    // add a player + calculate.
    DraftNewLineupStore.addPlayer(DraftGroupStore.allPlayers[1].player_id);
    expect(DraftNewLineupStore.getAvgPlayerSalary()).to.equal(player1Salary);

    // add player2 + calculate.
    DraftNewLineupStore.addPlayer(DraftGroupStore.allPlayers[2].player_id);
    expect(DraftNewLineupStore.getAvgPlayerSalary()).to.equal(
      (player1Salary + player2Salary) / 2
    );
  });


  it('isPlayerInLineup() should detect players already in the lineup', function() {
    var player = DraftGroupStore.allPlayers[2];

    // should not be in the lineup.
    expect(
      DraftNewLineupStore.isPlayerInLineup(player)
    ).to.equal(false);

    // add player.
    DraftNewLineupStore.addPlayer(player.player_id);

    // should now be in the lineup.
    expect(
      DraftNewLineupStore.isPlayerInLineup(player)
    ).to.equal(true);
  });


  it("findAvailablePositions() should find available positions", function() {
    // First do a simple count to make sure that it's adding all of the positions.
    var positionCount = 0;

     DraftNewLineupStore.rosterTemplates.nba.forEach(function(slot) {
        positionCount +=  slot.positions.length;

        // Make sure each of the positions in the template are in
        // DraftNewLineupStore.data.availablePositions.
        slot.positions.forEach(function(position) {
          expect(
            DraftNewLineupStore.data.availablePositions.indexOf(position)
          ).to.not.equal(-1);
        });
    });

    expect(DraftNewLineupStore.data.availablePositions.length).to.equal(positionCount);

    // Next fill up a slot and re-check the count.
    DraftNewLineupStore.addPlayer(DraftGroupStore.allPlayers[1].player_id);
    DraftNewLineupStore.findAvailablePositions();
    expect(DraftNewLineupStore.data.availablePositions.length).to.equal(positionCount - 1);
  });


  it('removePlayer() should remove a player from the lineup', function() {
    var player0 = DraftGroupStore.allPlayers[0];
    var player1 = DraftGroupStore.allPlayers[DraftGroupStore.allPlayers.length - 3];
    var player2 = DraftGroupStore.allPlayers[DraftGroupStore.allPlayers.length - 2];
    var player3 = DraftGroupStore.allPlayers[DraftGroupStore.allPlayers.length - 4];

    /**
      Test with one player in the lineup.
     */

    // make sure we're starting off with all slots open.
    expect(
      DraftNewLineupStore.getAvailableLineupSlots().length).to.equal(
      DraftNewLineupStore.data.lineup.length
    );

    // add a player
    DraftNewLineupStore.addPlayer(player0.player_id);
    expect(DraftNewLineupStore.getPlayerCount()).to.equal(
      1, "addPlayer() is not increasing the player count."
    );

    // Make sure that one of the slots is filled.
    expect(
      DraftNewLineupStore.getAvailableLineupSlots().length).to.equal(
      DraftNewLineupStore.data.lineup.length - 1
    );

    // remove that player
    DraftNewLineupStore.removePlayer(player0.player_id);

    // do we have an extra slot open now?
    expect(
      DraftNewLineupStore.getAvailableLineupSlots().length).to.equal(
      DraftNewLineupStore.data.lineup.length
    );


    /**
      Test with multiple players in the lineup.
    */

    // make sure we're starting off with all slots open.
    expect(
      DraftNewLineupStore.getAvailableLineupSlots().length).to.equal(
      DraftNewLineupStore.data.lineup.length
    );

    // add three  players
    DraftNewLineupStore.addPlayer(player1.player_id);
    DraftNewLineupStore.addPlayer(player2.player_id);
    DraftNewLineupStore.addPlayer(player3.player_id);

    expect(DraftNewLineupStore.getPlayerCount()).to.equal(
      3, "addPlayer() is not increasing the player count."
    );

    // remove one.
    DraftNewLineupStore.removePlayer(
      player1.player_id
    );

    // Make sure that two of the slots are still filled.
    expect(
      DraftNewLineupStore.getAvailableLineupSlots().length
    ).to.equal(
      DraftNewLineupStore.data.lineup.length - 2,
      "removePlayer is not reducing the number of available lineup slots."
    );

    // ensure that we removed the correct player.
    expect(
      DraftNewLineupStore.isPlayerInLineup(player2)
    ).to.equal(
      true,
      "removePlayer is not removing the specified player."
    );

    expect(
      DraftNewLineupStore.isPlayerInLineup(player3)
    ).to.equal(
      true,
      "removePlayer is not removing the specified player."
    );
  });


});
