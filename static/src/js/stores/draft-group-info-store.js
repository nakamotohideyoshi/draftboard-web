'use strict';

var Reflux = require('reflux');
var ContestStore = require('./contest-store.js');
// var request = require('superagent');
var log = require('../lib/logging');
var _countBy = require('lodash/collection/countBy');

/**
 * Stores aggregate information about all active draft groups that is derived from what we know
 * about active contests.
 */
var DraftGroupInfoStore = Reflux.createStore({

  data: {
    sportCounts: []
  },


  init: function() {
    log.debug('DraftGroupsStore.init()');

    ContestStore.listen(function() {
        this.findDraftGroupSportCounts(ContestStore.allContests);
        this.data.sportCounts['nfl'] = 5;
        this.data.sportCounts['mlb'] = 534;
        this.trigger(this.data);
    }.bind(this));
  },


  findDraftGroupSportCounts: function(contestData) {
    this.data.sportCounts = _countBy(contestData, function(contest) {
      return contest.sport;
    });
  }

});


module.exports = DraftGroupInfoStore;
