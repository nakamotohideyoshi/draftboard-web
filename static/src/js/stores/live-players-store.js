'use strict';

var _forEach = require('lodash/collection/forEach');
var _sortBy = require('lodash/collection/sortBy');
var Buffer = require('buffer/').Buffer;
var LivePlayersActions = require('../actions/live-players-actions');
var Lockr = require('lockr');
var log = require("../lib/logging");
var Reflux = require('reflux');
var request = require("superagent");
var vsprintf = require("sprintf-js").vsprintf;


/*
 * Store player statistics, correlate with draft group information
 * Note that this is based on a draft group, to separate the players
 *
 * Used by lineup and contest stores to determine PMR
*/
var LivePlayersStore = Reflux.createStore({
  data: {},

  init: function() {
    var self = this;
    log.debug('LivePlayersStore.init()');

    // Reflux auto call of actions, see http://git.io/vCAmc for more info
    self.listenToMany(LivePlayersActions);

    // set data structure on init
    self.resetData();
  },


  /**
   * method to reset the data to the initialization point. used in tests classes, in after() method reset before exiting
   */
  resetData: function() {
    var self = this;
    log.debug('LivePlayersStore.resetData()');

    self.data = {
      playersByDraftGroup: {}
    };

    // if the players are in localStorage, use them
    var localStorageKey = vsprintf('live-players');
    var localStorageValue = Lockr.get(localStorageKey, null);

    // make sure that the data exists and is less than a day old
    if (localStorageValue !== null) {
      log.debug('resetData() - localStorage for live players exists');

      // associate data to store
      self.data.playersByDraftGroup = localStorageValue.playersByDraftGroup;

      self.saveLivePlayersToLocalStorage();
    }
  },


  /**
   * Saves self.data.players to localStorage to speed up page load
   */
  saveToLocalStorage: function() {
    log.debug('saveToLocalStorage()');

    Lockr.set('live-players', {
      'date': Date.now(),
      'playersByDraftGroup': this.data.playersByDraftGroup
    });
  },




  // ACTIONS ----------------------------------------------

  /**
   * Correlate to draft group and game
   *
   * Use localStorage version if exists, otherwise GET and store in localStorage.
   */
  onLoadPlayer: function(playerId, draftGroupId) {
    var self = this;
    log.debug('onLoadPrize()');

    // TODO attach to promise
    if (draftGroupId in self.data.playersByDraftGroup === false) {

    }

    // if we already have the player, great, we're done
    if (playerId in self.data.players[draftGroupId]) {
      log.debug('onLoadPlayer() - Already in self.data', playerId);
      return;
    }

    // otherwise request the player and store in localStorage

  },


  /**
   * Dynamically called via listenToMany for the LivePlayersActions.loadPrize action
   */
  onLoadPlayerCompleted: function(playerId) {
    var self = this;
    log.debug('onLoadPlayerCompleted()');
  }


});


module.exports = LivePlayersStore;
