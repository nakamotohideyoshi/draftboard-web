'use strict';

var _size = require('lodash/collection/size');
var expect = require('chai').expect;
var Lockr = require('lockr');
var log = require("../../lib/logging");
var React = require('react');
var ReactDOM = require('react-dom');
var request = require("superagent");
var sinon = require('sinon');

var LiveDraftGroupsActions = require('../../actions/live-draft-groups-actions');


describe('LiveDraftGroupsStore', function() {
  before(function() {
    var config = require('../../fixtures/live-draft-groups-config.js');

    this.superagentMock = require('superagent-mock')(request, config);
    this.LiveDraftGroupsStore = require('../../stores/live-draft-groups-store');
    this.LiveDraftGroupsStore.resetData();
  });

  after(function() {
    // unset mock urls
    this.superagentMock.unset();

    // reset data
    Lockr.flush();
    this.LiveDraftGroupsStore.resetData();
  });


  it('should loadDraftGroup data and fantasy points', function(done) {
    var self = this;
    this.timeout(5000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadDraftGroupFantasyPointsCompleted()') {
        expect(_size(self.LiveDraftGroupsStore.data.draftGroups[1])).to.equal(79);
        expect(1 in self.LiveDraftGroupsStore.data.fantasyPointsLastUpdated);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    LiveDraftGroupsActions.loadDraftGroup(1);
  });


  it('should skip loadDraftGroup since it is already in self.data', function(done) {
    var self = this;
    this.timeout(5000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadDraftGroup() - Already in self.data') {
        // make sure that the size of draft groups is still the same as last test
        expect(_size(self.LiveDraftGroupsStore.data.draftGroups[1])).to.equal(79);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    LiveDraftGroupsActions.loadDraftGroup(1);
  });


  it('should use localStorage for loadDraftGroup when data is reset', function(done) {
    var self = this;
    this.timeout(5000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadDraftGroup() - Using localStorage') {
        // make sure that the size of draft groups is still the same as last test
        expect(_size(self.LiveDraftGroupsStore.data.draftGroups[1])).to.equal(79);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    self.LiveDraftGroupsStore.resetData();
    LiveDraftGroupsActions.loadDraftGroup(1);
  });


  it('should fail loadDraftGroup when a non existant draft group is passed in', function(done) {
    var self = this;
    this.timeout(5000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadDraftGroupFailed()') {
        expect(1).to.equal(1);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    LiveDraftGroupsActions.loadDraftGroup(12381281);
  });


  it('should fail loadDraftGroupFantasyPoints when a non existant draft group is passed in', function(done) {
    var self = this;
    this.timeout(5000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadDraftGroupFantasyPoints() - Draft group not in self.data, exiting') {
        expect(1).to.equal(1);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    LiveDraftGroupsActions.loadDraftGroupFantasyPoints(12381281);
  });


  it('should stop loadDraftGroupFantasyPoints() if draft group does not exist', function(done) {
    var self = this;
    this.timeout(5000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadDraftGroupCompleted()') {
        LiveDraftGroupsActions.loadDraftGroupFantasyPoints(114128);

      } else if (arg === 'onLoadDraftGroupFantasyPointsFailed()') {
        expect(1).to.equal(1);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    LiveDraftGroupsActions.loadDraftGroup(114128);
  });

});
