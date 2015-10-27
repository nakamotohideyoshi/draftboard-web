'use strict';

var _forEach = require('lodash/collection/forEach');
var EntriesActions = require('../actions/entries-actions');
var log = require("../lib/logging");
var Reflux = require('reflux');
var request = require("superagent");


/*
 * Store a user's current entries, and generates relevant data and ties to it.
 *
 * GET user's upcoming/live entries every page load
 * loops through each entry, checks if that contest is live. if live
 *   - it feeds contest ID to LiveContestsStore to generate standings
 *   - it feeds draft group ID to LiveDraftGroupsStore to get players and their fantasy points
 *   - it feeds lineup ID to LiveLineupsStore to aggregate standings, earnings
 * once draft group and contest data is returned, it stores for each entry
 *   - current potential earnings
 *   - current standing
 *   - PMR (uses box scores information from LiveDraftGroupsStore, which has minutes remaining)
 *   - total minutes (to show PMR as percentage)
*/
var EntriesStore = Reflux.createStore({
  data: {},

  init: function() {
    // Reflux auto call of actions, see http://git.io/vCAmc for more info
    this.listenToMany(EntriesActions);

    // set data structure on init
    this.resetData();
  },


  /**
   * method to reset the data to the initialization point. used in tests classes, in after() method reset before exiting
   */
  resetData: function() {
    this.data = {
      apiEntries: {}
    };
  },


  /**
   * GET current entries for the logged in user
   */
  onLoadEntries: function() {
    log.debug('onLoadEntries()');
    var self = this;

    request
      .get('/contest/current-entries/')
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .end(function(err, res) {
        if(err) {
          EntriesActions.loadEntries.failed(err);
        } else {
          // TODO store the data
          self.data.apiEntries = res.body;

          // trigger and complete
          self.trigger(self.data);
          EntriesActions.loadEntries.completed();
        }
    });
  },


  /**
   * Dynamically called via listenToMany for the EntriesActions.loadEntries action
   */
  onLoadEntriesCompleted: function() {
    log.debug('onLoadEntriesCompleted()');
    var self = this;

    // loop through each entry and load lineup. if live, then also loads contest and draft group information
    _forEach(self.data.apiEntries.results, function(entry) {
      // TODO send to LiveLineupsStore

      if (entry.is_live === true) {
        // TODO send to LiveDraftGroupsStore
        // TODO send to LiveContestsStore
      }
    });
  }

});


module.exports = EntriesStore;
