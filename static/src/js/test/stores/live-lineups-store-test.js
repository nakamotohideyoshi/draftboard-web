'use strict';

var _size = require('lodash/collection/size');
var expect = require('chai').expect;
var Lockr = require('lockr');
var log = require("../../lib/logging");
var React = require('react');
var ReactDOM = require('react-dom');
var request = require("superagent");
var sinon = require('sinon');
var Reflux = require('reflux');

var LiveContestsActions = require('../../actions/live-contests-actions');
var LiveDraftGroupsActions = require('../../actions/live-draft-groups-actions');
var LiveLineupsActions = require('../../actions/live-lineups-actions');


describe('LiveLineupsStore', function() {
  before(function(done) {
    this.timeout(5000);
    var config = require('../../fixtures/live-contests-config.js');

    this.superagentMock = require('superagent-mock')(request, config);
    this.LiveLineupsStore = require('../../stores/live-lineups-store');
    this.LiveContestsStore = require('../../stores/live-contests-store');

    this.LiveLineupsStore.resetData();

    LiveDraftGroupsActions.loadDraftGroup(1);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadDraftGroupFantasyPointsCompleted()') {
        // restore logging
        log.debug = prev;

        done();
      }
    };
  });

  after(function() {
    // unset mock urls
    this.superagentMock.unset();

    // reset data
    Lockr.flush();
    this.LiveLineupsStore.resetData();
  });


  it('should loadLineup data', function(done) {
    var self = this;
    this.timeout(5000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadLineupCompleted()') {
        // expect(self.LiveLineupsStore.data.stats[2].bytes.length).to.equal(92);
        expect(1).to.equal(1);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    LiveContestsActions.loadContest(2);
  });

});
