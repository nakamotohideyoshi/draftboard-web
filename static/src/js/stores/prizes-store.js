'use strict';

var _forEach = require('lodash/collection/forEach');
var _sortBy = require('lodash/collection/sortBy');
var Buffer = require('buffer/').Buffer;
var PrizesActions = require('../actions/prizes-actions');
var Lockr = require('lockr');
var log = require("../lib/logging");
var Reflux = require('reflux');
var request = require("superagent");
var vsprintf = require("sprintf-js").vsprintf;


/*
 * Store prize pool rules, caches in localStorage
 *
 * Used by lineup and contest stores to determine potential current earnings
*/
var PrizesStore = Reflux.createStore({
  data: {},

  init: function() {
    var self = this;
    log.debug('PrizesStore.init()');

    // Reflux auto call of actions, see http://git.io/vCAmc for more info
    self.listenToMany(PrizesActions);

    // set data structure on init
    self.resetData();
  },


  /**
   * method to reset the data to the initialization point. used in tests classes, in after() method reset before exiting
   */
  resetData: function() {
    var self = this;
    log.debug('PrizesStore.resetData()');

    self.data = {
      apiData: {}
    };

    // if the prizes are in localStorage, use them
    var localStorageKey = vsprintf('prizes');
    var localStorageValue = Lockr.get(localStorageKey, null);

    // make sure that the data exists and is less than a day old
    if (localStorageValue !== null) {
      log.debug('resetData() - localStorage for prizes exists');

      // associate data to store
      self.data.apiData = localStorageValue.apiData;

      self.savePrizesToLocalStorage();
    }
  },


  /**
   * Saves self.data.prizes to localStorage to speed up page load
   */
  savePrizesToLocalStorage: function() {
    log.debug('savePrizesToLocalStorage()');

    Lockr.set('prizes', {
      'date': Date.now(),
      'apiData': this.data.apiData
    });
  },




  // ACTIONS ----------------------------------------------

  /**
   * GET all lineups for a prize
   *
   * Use localStorage version if exists, otherwise GET and store in localStorage.
   */
  onLoadPrize: function(prizeId) {
    var self = this;
    log.debug('onLoadPrize()');

    // if we already have the prize, great, we're done
    if (prizeId in self.data.apiData) {
      log.debug('onLoadPrize() - Already in self.data', prizeId);
      return;
    }

    // otherwise request the prize and store in localStorage
    request
      .get('/prize/' + prizeId)
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .end(function(err, res) {
        if (err) {
          PrizesActions.loadPrize.failed(err);
        } else {
          self.data.apiData[prizeId] = res.body;

          // save, trigger, and complete
          self.savePrizesToLocalStorage();
          self.trigger(self.data);
          PrizesActions.loadPrize.completed(prizeId);
        }
    });
  },


  /**
   * Dynamically called via listenToMany for the PrizesActions.loadPrize action
   */
  onLoadPrizeCompleted: function(prizeId) {
    var self = this;
    log.debug('onLoadPrizeCompleted()');
  }


});


module.exports = PrizesStore;
