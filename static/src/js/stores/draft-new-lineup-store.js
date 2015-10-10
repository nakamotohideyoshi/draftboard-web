'use strict';

var Reflux = require('reflux');
var DraftActions = require('../actions/draft-actions');
var log = require('../lib/logging');
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

  salaryCaps: {
    'nba': 50000
  },

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
    ],
    'nba': [
      {idx: 0, name: 'PG', positions: ['PG'], player: null},
      {idx: 1, name: 'SG', positions: ['SG'], player: null},
      {idx: 2, name: 'SF', positions: ['SF'], player: null},
      {idx: 3, name: 'PF', positions: ['PF'], player: null},
      {idx: 4, name: 'C', positions: ['C'], player: null},
      {idx: 5, name: 'FX', positions: ['PG','SG','SF','PF','C'], player: null},
      {idx: 6, name: 'FX', positions: ['PG','SG','SF','PF','C'], player: null},
      {idx: 7, name: 'FX', positions: ['PG','SG','SF','PF','C'], player: null}
    ]
  },


  init: function() {
    log.debug('DraftNewLineupStore.init()');

    this.data = {
      lineupTitle: null,
      lineup: [],
      remainingSalary: 150000,
      avgPlayerSalary: 0,
      contestSalaryLimit: 0,
      availablePositions: [],
      errorMessage: ''
    };

    this.listenTo(DraftActions.addPlayerToLineup, this.addPlayer);
    this.listenTo(DraftActions.removePlayerToLineup, this.removePlayer);
    this.listenTo(DraftActions.saveLineup, this.save);
    this.listenTo(DraftActions.setLineupTitle, this.setLineupTitle);
    this.listenTo(DraftGroupStore, this.draftGroupUpdated);

    this.findAvailablePositions();
    this.trigger(this.data);
  },


  /**
   * Remove all players from the lineup.
   */
  resetLineup: function() {
    log.debug('DraftNewLineupStore.resetLineup()');

    this.data.lineup.forEach(function(slot) {
      slot.player = null;
    });

    this.refreshLineupStats();
  },


  /**
   * Save the lineup.
   */
  save: function() {
    log.debug('DraftNewLineupStore.save()');

    if(this.isValid()) {
      // Build an array of player_ids.
      var playerIds = this.data.lineup.map(function(slot) {
        return slot.player.player_id;
      });

      var postData = {
        name: this.data.lineupTitle || '',
        players: playerIds,
        // Grab the current draftGroupId from the DraftGroupStore.
        draft_group: DraftGroupStore.data.draftGroupId
      };

      request.post('/lineup/create/')
        .set('Content-Type', 'application/json')
        .send(postData)
        .end(function(err, res) {
          if(err) {
            DraftActions.saveLineup.failed(err);
            log.error(res.body);
            this.data.errorMessage = res.body;
            this.trigger(this.data);
          } else {
            DraftActions.saveLineup.completed();
            log.info(res);
            // Upon save success, send user to the lobby.
            document.location.href = '/frontend/lobby/';
          }
      }.bind(this));
    }
  },


  // TODO: Validate lineup before attempting to save.
  isValid: function() {
    log.debug('DraftNewLineupCard.isValid()');
    if (this.getPlayerCount() !== this.data.lineup.length) {
      this.data.errorMessage = 'You need to add more players';
      this.trigger(this.data);
      return false;
    }
    return true;
  },


  /**
   * Each roster_spot has an 'amount' property that indicates that there are multiple spots in the
   * lineup for that type of roster spot. This runs through and creates slots in our lineup taking
   * that into account.
   *
   * @param  {[type]} draftGroupData [description]
   */
  draftGroupUpdated: function(draftGroupData) {
    log.debug('DraftNewLineupCard.draftGroupUpdated()');
    if (this.data.lineup.length === 0 && draftGroupData.sport) {
      this.data.lineup = this.rosterTemplates[draftGroupData.sport];
      this.data.contestSalaryLimit = this.salaryCaps[draftGroupData.sport];
      this.refreshLineupStats();
    }
  },


  addPlayer: function(playerId) {
    log.debug('DraftNewLineupStore.addPlayer()', playerId);

    var player = this.getPlayerByPlayerId(playerId);

    if(this.canAddPlayer(player)) {
      this._insertPlayerIntoLineup(player);
      this.refreshLineupStats();
    } else {
      log.error('Cannot add player to lineup!');
      this.trigger(this.data);
    }
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

    openSlots.forEach(function(slot) {
      availablePositions = availablePositions.concat(slot.positions);
    });

    this.data.availablePositions = availablePositions;
  },


  /**
   * With a provided playerId, get a player object from the DraftGroupStore.
   * @param  {Integer} playerId The player_id of the player to fetch.
   * @return {Object}           A row from the DraftGrupStore.players array.
   */
  getPlayerByPlayerId: function(playerId) {
    log.debug('DraftNewLineupStore.getPlayerByPlayerId()', playerId);
    return _find(DraftGroupStore.allPlayers, 'player_id', playerId);
  },


  /**
   * Determine if we are able to add the supplied player to the lineup.
   * @param  {Object} player A player from the DraftGroupStore.
   * @return {bool}          Can the playe be added?
   */
  canAddPlayer: function(player) {
    log.debug('DraftNewLineupStore.canAddPlayer()', player);

    // Check if the player is already in the lineup.
    if (this.isPlayerInLineup(player)) {
      this.data.errorMessage = 'Selected player is already in the lineup';
      log.error("Selected player is already in the lineup.");
      return false;
    }

    // Check if there is room in the salary cap.
    if (this.getTotalSalary() + player.salary > this.data.contestSalaryLimit) {
      this.data.errorMessage = 'Player exceeds maximum salary';
      log.error('Player exceeds maximum salary.');
      return false;
    }

    // Check if there is a valid slot for the player.
    if (!this.isSlotAvailableForPlayer(player)) {
      this.data.errorMessage = 'There is no slot available for this player';
      log.error("There is no slot available for this player.");
      return false;
    }

    // If all checks pass, the player can be added.
    return true;
  },


  isSlotAvailableForPlayer: function(player) {
    log.debug('DraftNewLineupStore.isSlotAvailableForPlayer()', player);
    // Run through each unoccupied slot and determine if any are able to accept this player's
    // position type. At this point, We don't care which slot specifically is open for the player,
    // just that there is one.
    var openSlots = this.getAvailableLineupSlots();

    // Once we find an open slot, return true;
    for (var i=0; i < openSlots.length; i++) {
      if (openSlots[i].positions.indexOf(player.position) !== -1) {
        return true;
      }
    }

    return false;
  },


  /**
   * Check if the player is already in the lineup.
   * @param  {Object} player A player.
   * @return {Boolean}
   */
  isPlayerInLineup: function(player) {
    log.debug('DraftNewLineupStore.isPlayerInLineup()', player);
    return typeof _find(this.data.lineup, 'player', player) !== 'undefined';
  },


  /**
   * Insert the provided player into the lineup. This will place the player in the next avialable
   * slot that is valid for the player's position. NOTE: You should use addPlayer(), not this.
   * @param  {Object} player A row from the DraftGroupStore.
   */
  _insertPlayerIntoLineup: function(player) {
    log.debug('DraftNewLineupStore.insertPlayerIntoLineup()', player);
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
   * TODO: Remove a player from the lineup.
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


  setLineupTitle: function(title) {
    this.data.lineupTitle = title;
  },


  refreshLineupStats: function() {
    log.debug('DraftNewLineupStore.refreshLineupStats()');
    this.data.avgPlayerSalary =  this.getAvgPlayerSalary();
    this.data.remainingSalary = this.getRemainingSalary();
    this.findAvailablePositions();
    this.trigger(this.data);
  }


});


module.exports = DraftNewLineupStore;
