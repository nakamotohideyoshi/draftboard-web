'use strict';

var expect = require('chai').expect;
var Lockr = require('lockr');
var log = require("../../lib/logging");
var React = require('react');
var ReactDOM = require('react-dom');
var request = require("superagent");
var sinon = require('sinon');

var EntriesActions = require('../../actions/entries-actions');


describe('EntriesStore', function() {
  before(function() {
    var config = require('../../fixtures/entries-store-config.js');

    this.superagentMock = require('superagent-mock')(request, config);
    this.EntriesStore = require('../../stores/entries-store');
  });

  after(function() {
    // unset mock urls
    this.superagentMock.unset();

    // reset data
    this.EntriesStore.resetData();
  });


  it('should loadEntries data and parse properly', function(done) {
    var self = this;
    this.timeout(2000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadEntriesCompleted()') {
        // make sure that the request has been converted into data properly
        expect(self.EntriesStore.data.apiEntries.results.length).to.equal(10);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    EntriesActions.loadEntries();
  });

});
