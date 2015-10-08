'use strict';

var Reflux = require('reflux');
// var ContestActions = require('../actions/contest-actions');
var ContestStore = require('./contest-store.js');
// var request = require('superagent');
var log = require('../lib/logging');


/**
 * Stores information about all draft groups.
 */
var DraftGroupsStore = Reflux.createStore({

  data: {},

  init: function() {
    // this.listenTo(DraftActions.loadDraftGroup, this.fetchDraftGroup);
    ContestStore.listen(function(status) {
        log.info('status: ', status);
    });

    this.data = {
    };
  }


});


module.exports = DraftGroupsStore;
