'use strict';

var Reflux = require('reflux');
var DraftActions = require('../actions/draft-actions');
var log = require('../lib/logging');
// var _sortByOrder = require('lodash/collection/sortByOrder');
var DraftGroupStore = require('./draft-group-store.js');
var _find = require("lodash/collection/find");
var request = require('superagent');
require('superagent-django-csrf');


/**
 * A store to hold a new lineup as it's being created. The empty lineup  (this.data.lineup) is
 * created from one of the rosterTemplates. Players are added to each lineup slot by adding them to
 * this.data.lineup[slotIndex].player.
 */
var DraftNewLineupStore = Reflux.createStore({

  data: {},

  rosterTemplates: {
    'nfl': [
      {idx: 0, name: 'QB', positions: ['QB'], player: null},
      {idx: 1, name: 'RB', positions: ['RB', 'FB'], player: null},
      {idx: 2, name: 'RB', positions: ['RB', 'FB'], player: null},
      {idx: 3, name: 'WR', positions: ['WR'], player: null},
      {idx: 4, name: 'WR', positions: ['WR'], player: null},
      {idx: 5, name: 'TE', positions: ['TE'], player: null},
      {idx: 6, name: 'FLEX', positions: ['RB','FB','WR','TE'], player: null},
      {idx: 7, name: 'FLEX', positions: ['RB','FB','WR','TE'], player: null},
      {idx: 8, name: 'DST', positions: ['DST'], player: null}
    ]
  },


  init: function() {
    this.listenTo(DraftActions.addPlayerToLineup, this.addPlayer);
    this.listenTo(DraftActions.removePlayerToLineup, this.removePlayer);
    this.listenTo(DraftActions.saveLineup, this.save);
    this.listenTo(DraftGroupStore, this.DraftGroupUpdated);

    this.data = {
      lineup: [],
      remainingSalary: 150000,
      avgPlayerSalary: 0,
      contestSalaryLimit: 150000,
      availablePositions: []
    };

    this.findAvailablePositions();

    this.trigger(this.data);
    log.debug('DraftNewLineupStore.init()');
  },


  /**
   * Save the lineup.
   */
  save: function() {
    if(this.isValid()) {
      // Build an array of player_ids.
      var playerIds = this.data.lineup.map(function(slot) {
        return slot.player.player_id;
      });

      var postData = {
        players: playerIds,
        draft_group: 3
      };

      log.debug('DraftNewLineupStore.save()', postData);

      request.post('/lineup/create/')
        .set('Content-Type', 'application/json')
        .send(postData)
        .end(function(err, res) {
          if(err) {
            log.error(res.body);
          } else {
            log.info(res);
          }
      });
    }
  },


  // TODO: Validate lineup before attempting to save.
  isValid: function() {
    return true;
  },


  /**
   * Each roster_spot has an 'amount' property that indicates that there are multiple spots in the
   * lineup for that type of roster spot. This runs through and creates slots in our lineup taking
   * that into account.
   *
   * @param  {[type]} draftGroupData [description]
   */
  DraftGroupUpdated: function(draftGroupData) {
    if (this.data.lineup.length === 0) {
      this.data.lineup = this.rosterTemplates[draftGroupData.sport];
      this.trigger(this.data);
    }

    this.refreshLineupStats();
  },


  addPlayer: function(playerId) {
    log.debug('DraftNewLineupStore.addPlayer()', playerId);

    var player = this.getPlayerByPlayerId(playerId);

    if(this.canAddPlayer(player)) {
      log.debug('Adding Player:', this.getPlayerByPlayerId(playerId));
      this.insertPlayerIntoLineup(player);
      this.trigger(this.data);
    } else {
      log.error('Cannot add player to lineup!');
    }

    this.refreshLineupStats();
  },


  getAvailableLineupSlots: function() {
    return this.data.lineup.filter(function(slot) {
      if(!slot.player) {
        return slot;
      }
    });
  },


  /**
   * Determine which position types are still available.
   * @return {array} The avaolaible positions ex: ['WR', 'QB', 'DST']
   */
  findAvailablePositions: function() {
    var openSlots = this.getAvailableLineupSlots();
    var availablePositions = [];

    for (var i=0; i < openSlots.length; i++) {
      availablePositions = availablePositions.concat(openSlots[i].positions);
    }

    this.data.availablePositions = availablePositions;
  },


  /**
   * With a provided playerId, get a player object from the DraftGroupStore.
   * @param  {Integer} playerId The player_id of the player to fetch.
   * @return {Object}           A row from the DraftGrupStore.players array.
   */
  getPlayerByPlayerId: function(playerId) {
    log.debug('DraftNewLineupStore.getPlayerByPlayerId()', playerId);
    return _find(DraftGroupStore.data.players, 'player_id', playerId);
  },


  /**
   * Determine if we are able to add the supplied player to the lineup.
   * @param  {Object} player A player from the DraftGroupStore.
   * @return {bool}          Can the playe be added?
   */
  canAddPlayer: function(player) {
    log.debug('DraftNewLineupStore.canAddPlayer()', player);

    // First check if there is room in the salary cap.
    if (this.getTotalSalary() + player.salary > this.data.contestSalaryLimit) {
      log.error('Player exceeds maximum salary.');
      return false;
    }

    // Now run through each unoccupied slot and determine if any are able to accept this player's
    // position type. At this point, We don't care which slot specifically is open for the player,
    // just that there is one.
    var openSlots = this.getAvailableLineupSlots();

    // Once we find an open slot, return true;
    for (var i=0; i < openSlots.length; i++) {
      if (openSlots[i].positions.indexOf(player.position) !== -1) {
        return true;
      }
    }

    // No open slots were found. :(
    return false;
  },


  /**
   * Check if the player is already in the lineup.
   * @param  {Object} player A player.
   * @return {Boolean}
   */
  isPlayerInLineup: function(player) {
    log.debug(player);
  },


  /**
   * Insert the provided player into the lineup. This will place the player in the next avialable
   * slot that is valid for the player's position.
   * @param  {Object} player A row from the DraftGroupStore.
   */
  insertPlayerIntoLineup: function(player) {
    var openSlots = this.getAvailableLineupSlots();

    for (var i=0; i < openSlots.length; i++) {
      if (openSlots[i].positions.indexOf(player.position) !== -1) {
        openSlots[i].player = player;
        return;
      }
    }
  },


  /**
   * Remove a player from the lineup.
   */
  removePlayer: function() {
    log.debug('removePlayer()');
  },


  /**
   * Get the sum of lineup players' salary.
   * @return {Integer} The total lineup salary.
   */
  getTotalSalary: function() {
    log.debug('DraftNewLineupStore.getTotalSalary()');

    return this.data.lineup.reduce(function(previousValue, currentValue, index, lineup) {
      if (lineup[index].player) {
        return previousValue + lineup[index].player.salary;
      }
      // If there aren't any players in the lineup, return the default (0).
      return previousValue;
    }, 0);
  },


  /**
   * Find how much money is left to spend on players.
   * @return {Integer} Salary cap minus current lineup salary.
   */
  getRemainingSalary: function() {
    log.debug('DraftNewLineupStore.getRemainingSalary()');
    return this.data.contestSalaryLimit - this.getTotalSalary();
  },


  /**
   * How many players have been added to the lineup.
   * @return {Integer} The number of players in the lineup.
   */
  getPlayerCount: function() {
    log.debug('DraftNewLineupStore.getPlayerCount()');
    return this.data.lineup.reduce(function(prev, curr, i, lineup) {
        if (lineup[i].player) {
          return prev + 1;
        }
        return prev;
    }, 0);
  },


  /**
   * Find the average player salary.
   * @return {Inteter} The average player salary, rounded down to the nearest Int.
   */
  getAvgPlayerSalary: function() {
    log.debug('DraftNewLineupStore.findAvgPlayerSalary()');
    var playerCount = this.getPlayerCount();

    if (playerCount > 0) {
      return Math.floor(this.getTotalSalary() / playerCount);
    }

    return 0;
  },


  refreshLineupStats: function() {
    this.data.avgPlayerSalary =  this.getAvgPlayerSalary();
    this.data.remainingSalary = this.getRemainingSalary();
    this.findAvailablePositions();
    this.trigger(this.data);
  }


});


module.exports = DraftNewLineupStore;
