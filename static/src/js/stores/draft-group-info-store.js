'use strict';

var Reflux = require('reflux');
var ContestStore = require('./contest-store.js');
var request = require('superagent');
var log = require('../lib/logging');
var _countBy = require('lodash/collection/countBy');
var _filter = require('lodash/collection/filter');


/**
 * Stores aggregate information about all active draft groups that is derived from what we know
 * about active contests.
 */
var DraftGroupInfoStore = Reflux.createStore({

  data: {
    sportContestCounts: [],
    draftGroups: []
  },


  init: function() {
    log.debug('DraftGroupsStore.init()');

    // When the ContestStore fetches data, we need to find our relevant info.
    ContestStore.listen(function() {
      this.getDraftGroupInfo(this.data.draftGroups, ContestStore.allContests);
    }.bind(this));

    // Hydrate this thing with data.
    this.fetchDraftGroups();
  },


  fetchDraftGroups: function() {
    request
      .get("/draft-group/upcoming/")
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          log.error(err);
        } else {
          this.data.draftGroups = res.body.results;
          this.getDraftGroupInfo(this.data.draftGroups, ContestStore.allContests);
        }
    }.bind(this));
  },


  // This gets run when either the ContestStore updates, or when we fetch drafGroups. It checks
  // to make sure we have both data sets, then finds relevant info about draft groups.
  getDraftGroupInfo: function(draftGroups, contests) {
    if (draftGroups && contests) {
      this.findSportContestCounts(contests);
      this.findContestCountForDraftGroups(draftGroups, contests);
      this.trigger(this.data);
    }
  },


  findContestCountForDraftGroups: function(draftGroups, contests) {
     for (let group of draftGroups) {
       group.contestCount = _filter(contests, 'draft_group', group.pk).length;
     }
  },


  findSportContestCounts: function(contestData) {
    this.data.sportContestCounts = _countBy(contestData, function(contest) {
      return contest.sport;
    });
  }

});


module.exports = DraftGroupInfoStore;
