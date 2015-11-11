'use strict';

var _size = require('lodash/collection/size');
var expect = require('chai').expect;
var Lockr = require('lockr');
var log = require("../../lib/logging");
var React = require('react');
var ReactDOM = require('react-dom');
var request = require("superagent");
var sinon = require('sinon');

var LiveContestsActions = require('../../actions/live-contests-actions');
var LiveDraftGroupsActions = require('../../actions/live-draft-groups-actions');


describe('LiveContestsStore', function() {
  before(function() {
    var config = require('../../fixtures/live-contests-config.js');

    this.superagentMock = require('superagent-mock')(request, config);
    this.LiveContestsStore = require('../../stores/live-contests-store');
    this.LiveContestsStore.resetData();
  });

  after(function() {
    // unset mock urls
    this.superagentMock.unset();

    // reset data
    Lockr.flush();
    this.LiveContestsStore.resetData();
  });


  it('should loadContestLineups data', function(done) {
    var self = this;
    this.timeout(5000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadContestLineupsCompleted()') {
        expect(self.LiveContestsStore.data.apiData[2].bytes.length).to.equal(92);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    LiveContestsActions.loadContestLineups(2);
  });


  it('should loadContestInfo data', function(done) {
    var self = this;
    this.timeout(5000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadContestInfoCompleted()') {
        expect(self.LiveContestsStore.data.apiData[2].info.id).to.equal(2);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    LiveContestsActions.loadContestInfo(2);
  });


  it('should skip loadContest since it is already in self.data', function(done) {
    var self = this;
    this.timeout(5000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadContest() - Already in self.data') {
        // make sure that the size of the contest is still the same as last test
        expect(self.LiveContestsStore.data.apiData[2].bytes.length).to.equal(92);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    LiveContestsActions.loadContest(2);
  });


  it('should use localStorage for loadContest when data is reset', function() {
    var self = this;

    self.LiveContestsStore.resetData();
    expect(self.LiveContestsStore.data.apiData[2].bytes.length).to.equal(92);
  });


  it('should fail loadContestLineups when a non existant contest is passed in', function(done) {
    var self = this;
    this.timeout(5000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadContestLineupsFailed()') {
        expect(1).to.equal(1);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    LiveContestsActions.loadContestLineups(12381281);
  });


  it('should fail loadContestInfo when a non existant contest is passed in', function(done) {
    var self = this;
    this.timeout(5000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadContestInfoFailed()') {
        expect(1).to.equal(1);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    LiveContestsActions.loadContestInfo(12381281);
  });


  it('should run loadContestCompleted when data is done loading in', function(done) {
    var self = this;

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadContestCompleted()') {
        expect(1).to.equal(1);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    delete(self.LiveContestsStore.data.apiData[2]);
    LiveContestsActions.loadContest(2);
  });


  it('should not run _generateContestStats if draft group does not exist', function(done) {
    var self = this;

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadContestCompleted() - Draft group does not exist yet, 1') {
        expect(1).to.equal(1);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    // skip to being done as older tests have the data in there
    LiveContestsActions.loadContest.completed(2);
  });


  it('should run _generateContestStats when draft group exists', function(done) {
    var self = this;

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      // once the draft group is loaded, then we can rank the contest
      if (arg === 'onLoadDraftGroupFantasyPointsCompleted()') {
        // skip to being done as older tests have the data in there
        LiveContestsActions.loadContest.completed(2);
      };

      if (arg === 'onLoadContestCompleted() - contest 2 stats generated') {
        // console.log(self.LiveContestsStore.data.stats);
        expect(1).to.equal(1);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    LiveDraftGroupsActions.loadDraftGroup(1);
  });


  it('should return int having passed in byteArray', function() {
    var self = this;
    var lineups = new Uint8Array([0x00, 0x00, 0x00, 0x02, 0x00, 0x09, 0x00, 0x00, 0x00, 0x01, 0x00, 0x02, 0x00, 0x0F, 0x00, 0x03, 0x00, 0x04, 0x0F, 0x00, 0x00, 0x10, 0x00, 0x05, 0x00, 0x06, 0x00, 0x07, 0x00, 0x00, 0x00, 0x10, 0x02, 0x00, 0x00, 0x0F, 0x00, 0x03, 0x00, 0x04, 0x0F, 0x00, 0x00, 0x10, 0x00, 0x05, 0x00, 0x06, 0x00, 0x09]);

    try {
      self.LiveContestsStore._convertToInt(8, new Uint8Array([0x00, 0x02]), 0, 2);
    } catch(e) {
      expect(e.message).to.equal('You must pass in a byteSize of 16 or 32');
    }

    expect(self.LiveContestsStore._convertToInt(16, new Uint8Array([0x00, 0x02]), 0, 2)).to.equal(2);
    expect(self.LiveContestsStore._convertToInt(32, new Uint8Array([0x00, 0x00, 0x0F, 0x00]), 0, 4)).to.equal(3840);
  });


  it('should return object of lineups if passed in byteArray', function() {
    var self = this;
    var lineups = new Uint8Array([0x00, 0x00, 0x00, 0x02, 0x00, 0x09, 0x00, 0x00, 0x00, 0x01, 0x00, 0x02, 0x00, 0x0F, 0x00, 0x03, 0x00, 0x04, 0x0F, 0x00, 0x00, 0x10, 0x00, 0x05, 0x00, 0x06, 0x00, 0x07, 0x00, 0x00, 0x00, 0x10, 0x02, 0x00, 0x00, 0x0F, 0x00, 0x03, 0x00, 0x04, 0x0F, 0x00, 0x00, 0x10, 0x00, 0x05, 0x00, 0x06, 0x00, 0x09]);

    var myLineup = self.LiveContestsStore._convertLineup(9, lineups, 6);

    expect(myLineup.id).to.equal(1);
  });

});
