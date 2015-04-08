"use strict";

var Reflux = require("reflux");
var ContestActions = require("../actions/contest-actions");


var ContestStore = Reflux.createStore({
  data: [],

  init: function() {
    this.listenTo(ContestActions.contestsUpdated, this.getContests);
    this.listenTo(ContestActions.contestFocused, this.setFocusedContest);

    this.data = {
      // Some dummy data.
      contests: [
        {id: 0, "title": "NBA - Anonymouse Head-to-Head", "entries_total": "14,231", "entries_filled": "12,014",
          "prize": "$350,000"},
        {id: 1, "title": "NBA - $150,000 Championship", "entries_total": "10,001", "entries_filled": "2,993",
          "prize": "$150,000"},
        {id: 2, "title": "NBA - $50,000 Championship", "entries_total": "10,001", "entries_filled": "2,993",
          "prize": "2150,000"},
        {id: 3, "title": "NBA - $666 Championship", "entries_total": "2,001", "entries_filled": "2,993",
          "prize": "$666"},
        {id: 4, "title": "NBA - $9 Sunday game", "entries_total": "54,001", "entries_filled": "2,993",
          "prize": "$150,000"},
        {id: 5, "title": "NBA - Throwback 1999 thing", "entries_total": "10,001", "entries_filled": "2,993",
          "prize": "$150,000"},
      ],

      focusedContestId: null
    };
  },

  getInitialState: function() {
    return this.data;
  },

  getContests: function() {
    return this.data.contests;
  },

  getFocusedContest: function() {
    return this.data.contests[this.data.focusedContestId];
  },

  setFocusedContest: function(contestId) {
    this.data.focusedContestId = contestId;
    this.trigger(this.data);
  }

});


module.exports = ContestStore;
