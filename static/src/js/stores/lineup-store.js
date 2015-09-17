"use strict";

var Reflux = require("reflux");
var LineupActions = require("../actions/lineup-actions");
var request = require("superagent");
// var log = require("../lib/logging");
// var _sortByOrder = require("lodash/collection/sortByOrder");


var LineupStore = Reflux.createStore({

  data: {},
  filters: [],

  init: function() {
    this.listenTo(LineupActions.load, this.fetchLineups);
    this.listenTo(LineupActions.lineupFocused, this.setFocusedLineup);

    this.data = {
      lineups: {},
      focusedLineupId: null
    };

    this.fetchLineups();
  },


  /**
   * Get a list of the user's lineups from the data source.
   */
  fetchLineups: function() {
    var self = this;
    request
      .get("/lineup/upcoming/")
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          LineupActions.load.failed(err);
        } else {

          self.data.lineups = res.body.results;

          // If this is the first time fetching lineups, make the first one active.
          if (!self.focuesedLineupId && res.body.results.length > 0) {
            self.setFocusedLineup(res.body.results[0].id);
          }
          // Trigger a data flow.
          self.trigger(self.data);
          // Complete the promise.
          // LineupActions.load.completed();
        }
    });
  },


  /**
   * Set the focused lineup based on the provided lineup ID.
   * @param {number} lineupId the ID of the lineup to set as active.
   */
  setFocusedLineup: function(lineupId) {
    if(typeof lineupId === 'number') {
      this.data.focusedLineupId = lineupId;
      this.trigger(this.data);
    }
  }

});


module.exports = LineupStore;
