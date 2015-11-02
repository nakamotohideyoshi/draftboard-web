'use strict';

var expect = require('chai').expect;
var Lockr = require('lockr');
var log = require("../../lib/logging");
var React = require('react');
var ReactDOM = require('react-dom');
var request = require("superagent");
var sinon = require('sinon');

var PrizesActions = require('../../actions/prizes-actions');


describe('PrizesStore', function() {
  before(function() {
    var config = require('../../fixtures/prizes-store-config.js');

    this.superagentMock = require('superagent-mock')(request, config);
    this.PrizesStore = require('../../stores/prizes-store');
  });

  after(function() {
    // unset mock urls
    this.superagentMock.unset();

    // reset data
    Lockr.flush();
    this.PrizesStore.resetData();
  });


  it('should loadPrizes data and parse properly', function(done) {
    var self = this;
    this.timeout(2000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadPrizeCompleted()') {
        // make sure that the request has been converted into data properly
        expect(self.PrizesStore.data.apiData[1].prize_pool).to.equal(9);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    PrizesActions.loadPrize(1);
  });


  // it('should fail loadContestLineups when a non existant contest is passed in', function(done) {
  //   var self = this;
  //   this.timeout(5000);

  //   // replace log method to listen and check messages
  //   var prev = log.debug;

  //   log.debug = function (arg) {
  //     if (arg === 'onLoadContestLineupsFailed()') {
  //       expect(1).to.equal(1);

  //       // restore logging
  //       log.debug = prev;

  //       done();
  //     }
  //   };

  //   LiveContestsActions.loadContestLineups(12381281);
  // });

});
