"use strict";

var Reflux = require("reflux");
var DraftActions = require("../actions/draft-actions");
var request = require("superagent");
var log = require("../lib/logging");
var _sortBy = require("lodash/collection/sortBy");


/**
 * Store a DraftGroup (players for a specific set of contests).
 */
var DraftGroupStore = Reflux.createStore({

  data: {},
  filters: [],

  init: function() {
    this.listenTo(DraftActions.loadDraftGroup, this.fetchDraftGroup);
    this.listenTo(DraftActions.playerFocused, this.setFocusedPlayer);

    this.data = {
      players: [],
      filteredPlayers: [],
      sport: null,
      focusedPlayerId: null
    };
  },


  /**
   * Get a list of the user's lineups from the data source.
   */
  fetchDraftGroup: function(draftGroupId) {
    if (!draftGroupId) {
      log.error('fetchDraftGroup() - No draftGroupId specified.');
      return;
    }

    var self = this;

    request
      .get("/draft-group/" + draftGroupId + '/')
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .end(function(err, res) {
        if(err) {
          DraftActions.loadDraftGroup.failed(err);
        } else {
          self.data.sport = res.body.sport;
          self.data.players = res.body.players;
          self.data.filteredPlayers = self.sortBySalary(self.data.players);
          // Trigger a data flow.
          self.trigger(self.data);
          // Complete the promise.
          DraftActions.loadDraftGroup.completed();
        }
    });
  },


  sortBySalary: function(players) {
    return _sortBy(players, 'salary').reverse();
  },


  /**
   * Set the focused player based on the provided player ID.
   * @param {number} lineupId the ID of the lineup to set as active.
   */
  setFocusedPlayer: function(playerId) {
    if(typeof playerId === 'number') {
      this.data.focusedPlayerId = playerId;
      this.trigger(this.data);
    }
  }

});


module.exports = DraftGroupStore;
