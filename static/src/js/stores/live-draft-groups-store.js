'use strict';

var _forEach = require('lodash/collection/forEach');
var LiveDraftGroupsActions = require('../actions/live-draft-groups-actions');
var Lockr = require('lockr');
var log = require("../lib/logging");
var Reflux = require('reflux');
var request = require("superagent");
var vsprintf = require("sprintf-js").vsprintf;


/*
 * Store currently used live draft groups, stores them in localStorage and listens to players socket stream for fantasy
 * point updates.
 *
 * - EntriesStore feeds in draft group ID, then GET
 *     - list of players once per night, stores in localStorage and references from there until expires
 *     - list of player's fantasy points per page load, then calls once every two minutes for parity check of scores
 *     - list of box scores
 *     - starts listening to player and event streams
 *         - on box score event, it updates box scores and in turn updates PMR
 *         - on player update, updates the tied LivePlayersStore player with new fantasy points
*/
var LiveDraftGroupsStore = Reflux.createStore({
  data: {},

  init: function() {
    // Reflux auto call of actions, see http://git.io/vCAmc for more info
    this.listenToMany(LiveDraftGroupsActions);

    // set data structure on init
    this.resetData();
  },


  /**
   * method to reset the data to the initialization point. used in tests classes, in after() method reset before exiting
   */
  resetData: function() {
    this.data = {
      draftGroups: {},
      fantasyPointsLastUpdated: {}
    };
  },



  // ACTIONS ----------------------------------------------


  /**
   * GET player information for a draft group
   *
   * First we check if it already exists in self.data, and if so, returns. Then we check if it's in localStorage,
   * and if so, we add to self.data. As a last resort we GET the players and save to localStorage and self.data.
   */
  onLoadDraftGroup: function(draftGroupId) {
    log.debug('onLoadDraftGroup()');
    var self = this;


    // if we already have the draft group, great, we're done
    if (draftGroupId in self.data.draftGroups) {
      log.debug('onLoadDraftGroup() - Already in self.data', draftGroupId);
      return;
    }


    // if the draft group is in localStorage, then set to completed and move on to getting fantasy points
    var localStorageKey = vsprintf('draft_group_%d', [draftGroupId]);
    var localStorageValue = Lockr.get(localStorageKey, null);
    var localStorageTTL = (process.env.NODE_ENV !== 'production') ? 60000 : 86400000;

    // make sure that the data exists and is less than a day old
    if (localStorageValue !== null && localStorageValue.date + localStorageTTL > Date.now()) {
      // associate data to store
      self.data.draftGroups[draftGroupId] = localStorageValue.players;

      // trigger and complete
      self.trigger(self.data);
      LiveDraftGroupsActions.loadDraftGroup.completed();

      log.debug('onLoadDraftGroup() - Using localStorage', draftGroupId);
      return;
    }


    // otherwise request the draft group and store in localStorage
    request
      .get('/draft-group/' + draftGroupId + '/')
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .end(function(err, res) {
        if(err) {
          LiveDraftGroupsActions.loadDraftGroup.failed(err);
        } else {
          // associate data to store
          var players = {};
          _forEach(res.body.players, function(player) {
            players[player.player_id] = player;
          });
          self.data.draftGroups[draftGroupId] = players;

          // store in localStorage
          Lockr.set(localStorageKey, {
            'date': Date.now(),
            'players': players
          });

          // trigger and complete
          self.trigger(self.data);
          LiveDraftGroupsActions.loadDraftGroup.completed(draftGroupId);

          log.debug('onLoadDraftGroup() - GET', draftGroupId);
        }
    });
  },


  /**
   * GET player fantasy points
   */
  onLoadDraftGroupFantasyPoints: function(draftGroupId) {
    log.debug('onLoadDraftGroupFantasyPoints()');
    var self = this;

    if (draftGroupId in self.data.draftGroups === false) {
      log.debug('onLoadDraftGroupFantasyPoints() - Draft group not in self.data, exiting', draftGroupId);
    }

    request
      .get("/draft-group/fantasy-points/" + draftGroupId)
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .end(function(err, res) {
        if(err) {
          LiveDraftGroupsActions.loadDraftGroupFantasyPoints.failed(err);
        } else {
          var draftGroup = self.data.draftGroups[draftGroupId];

          // add points to the draftGroup players object
          _forEach(res.body.players, function(player, id) {
            if (id in draftGroup === false) {
              // TODO LiveDraftGroupsStore - why would players not in a draft group be in the fantasy points call?
              log.debug('onLoadDraftGroupFantasyPoints() - Player not in draft group', id);
              return;
            }

            draftGroup[id].fp = player.fp;
          });

          self.data.fantasyPointsLastUpdated[draftGroupId] = Date.now();

          // trigger and complete
          self.trigger(self.data);
          LiveDraftGroupsActions.loadDraftGroupFantasyPoints.completed();
        }
    });
  },



  // COMPLETED ACTIONS ----------------------------------------------


  /**
   * Dynamically called via listenToMany for the LiveDraftGroupsActions.loadDraftGroup action
   *
   * Since on page load we load everything from localStorage and then start refreshing data, we wait until this call
   * to pull in fantasy points after we know the draft group exists
   */
  onLoadDraftGroupCompleted: function(draftGroupId) {
    log.debug('onLoadDraftGroupCompleted()');

    LiveDraftGroupsActions.loadDraftGroupFantasyPoints(draftGroupId);
  },


  /**
   * Dynamically called via listenToMany for the LiveDraftGroupsActions.loadDraftGroupFantasyPoints action
   */
  onLoadDraftGroupFantasyPointsCompleted: function() {
    log.debug('onLoadDraftGroupFantasyPointsCompleted()');

    // TODO LiveDraftGroupsStore - set up setTimeout to run loadDraftGroupFantasyPoints again periodically for parity
  },



  // FAILED ACTIONS ----------------------------------------------


  onLoadDraftGroupFailed: function(err) {
    log.debug('onLoadDraftGroupFailed()');

    // TODO LiveDraftGroupsStore - send failed loadDraftGroup to Sentry
  },

  onLoadDraftGroupFantasyPointsFailed: function(err) {
    log.debug('onLoadDraftGroupFantasyPointsFailed()');

    // TODO LiveDraftGroupsStore - send failed loadDraftGroupFantasyPoints to Sentry
  }

});


module.exports = LiveDraftGroupsStore;
