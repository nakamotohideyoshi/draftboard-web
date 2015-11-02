'use strict';

var _forEach = require('lodash/collection/forEach');
var _sortBy = require('lodash/collection/sortBy');
var Buffer = require('buffer/').Buffer;
var LiveLineupsActions = require('../actions/live-lineups-actions');
var LiveContestsActions = require('../actions/live-contests-actions')
var Lockr = require('lockr');
var log = require("../lib/logging");
var Reflux = require('reflux');
var request = require("superagent");
var vsprintf = require("sprintf-js").vsprintf;


/*
 * Store currently used live lineups, stores them in localStorage
 *
 * - EntriesStore feeds in lineup ID, then
 *     - uses lineup ID to get related contest data from LiveContestStore
 *     - loops through players in contest data, feeds each player to LivePlayersStore
 *     - uses LivePlayersStore data + related entry from EntriesStore to generate
 *         - current potential earnings
 *         - current standing
 *         - PMR
 *         - total minutes (to show PMR as percentage)
*/
var LiveLineupsStore = Reflux.createStore({
  data: {},

  init: function() {
    var self = this;
    log.debug('LiveLineupsStore.init()');

    // Reflux auto call of actions, see http://git.io/vCAmc for more info
    self.listenToMany(LiveLineupsActions);

    // set data structure on init
    self.resetData();

    // when a contest is done loading, then pull in the data and aggregate for a lineup
    self.listenTo(LiveContestsActions.loadContest.completed, LiveLineupsActions.loadLineup);
  },


  /**
   * method to reset the data to the initialization point. used in tests classes, in after() method reset before exiting
   */
  resetData: function() {
    var self = this;
    log.debug('LiveLineupsStore.resetData()');

    self.data = {
      stats: {}
    };

    // if the contests are in localStorage, use them
    var localStorageKey = vsprintf('live_lineups');
    var localStorageValue = Lockr.get(localStorageKey, null);

    // make sure to set expiration low enough for tests to work, otherwise make them 12 hours
    self.localStorageTTL = (process.env.NODE_ENV !== 'production') ? 10000 : 43200000;

    // make sure that the data exists and is less than a day old
    if (localStorageValue !== null) {
      log.debug('resetData() - localStorage for lineups exists');

      // associate data to store
      self.data.stats = localStorageValue.stats;

      // remove old contests
      _forEach(self.data.stats, function(lineup, id) {
        if (lineup.expires < Date.now()) {
          log.debug(vsprintf('resetData() - removing lineup %d', [id]));
          delete(self.data.apiData[id]);
        }
      });

      self.saveContestsToLocalStorage();
    }
  },


  /**
   * Saves self.data.contests to localStorage to speed up page load
   */
  saveLineupsToLocalStorage: function() {
    log.debug('saveLineupsToLocalStorage()');

    Lockr.set('live_lineups', {
      'date': Date.now(),
      'stats': this.data.stats
    });
  },




  // ACTIONS ----------------------------------------------

  /**
   * Shortcut method to async both loadContestLinups and loadContestInfo data
   */
  onLoadLineup: function(lineupId) {
    var self = this;
    log.debug('onLoadLineup()');

    // if we already have the contest, great, we're done
    if (lineupId in self.data.stats) {
      log.debug('onLoadLineup() - Already in self.data', lineupId);
      return;
    }

    self.saveLineupsToLocalStorage();
    self.trigger(self.data);
    LiveLineupsActions.loadLineup.completed(lineupId);
  },


  /**
   * Shortcut method to async both loadContestLinups and loadContestInfo data
   */
  onLoadLineupCompleted: function(lineupId) {
    var self = this;
    log.debug('onLoadLineupCompleted()');

    // add up potential earnings
    // _forEach(LiveContestStore.data.stats, function(contest, id) {
    //   if (id in self.data.stats) {

    //   }
    // });
  }


});


module.exports = LiveLineupsStore;
