'use strict';

var React = require('react');
var ReactDOM = require('react-dom');
var Lockr = require('lockr');
var expect = require('chai').expect;
var sinon = require('sinon');
var log = require("../../lib/logging");
var request = require("superagent");
var _size = require('lodash/collection/size');
var LiveNBAActions = require('../../actions/live-nba-actions');


describe('LiveNBAStore', function() {
  before(function() {
    var config = require('../../fixtures/live-nba-store-config.js');

    this.superagentMock = require('superagent-mock')(request, config);
    this.LiveNBAStore = require('../../stores/live-nba-store');
  });

  after(function() {
    // unset mock urls
    this.superagentMock.unset();

    // reset data
    Lockr.flush();
    this.LiveNBAStore.resetData();
  });

  // TODO get working with binary, possibly use js nock?
  it('should loadContestLineups data and parse properly', function(done) {
    var self = this;
    this.timeout(10000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadContestLineupsCompleted()') {
        // make sure that the rquest has been converted into data properly
        expect(self.LiveNBAStore.data.apiContestLineupsBytes.length).to.equal(92);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    LiveNBAActions.loadContestLineups(1);
  });


  it('should loadDraftGroup data and parse properly', function(done) {
    var self = this;
    this.timeout(10000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadDraftGroupCompleted()') {
        // make sure that the rquest has been converted into data properly
        expect(self.LiveNBAStore.data.apiDraftGroup.length).to.equal(325);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    LiveNBAActions.loadDraftGroup(1);
  });


  it('should loadDraftGroupFantasyPoints data and parse properly', function(done) {
    var self = this;
    this.timeout(10000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadDraftGroupFantasyPointsCompleted()') {
        // make sure that the rquest has been converted into data properly
        expect(_size(self.LiveNBAStore.data.apiAllFantasyPoints.players)).to.equal(311);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    LiveNBAActions.loadDraftGroupFantasyPoints(1);
  });


  it('should loadLineup mine data and parse properly', function(done) {
    var self = this;
    this.timeout(10000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadLineupCompleted()') {
        // make sure that the rquest has been converted into data properly
        expect(self.LiveNBAStore.data.myLineupPlayers.order.length).to.equal(8);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    LiveNBAActions.loadLineup(2, 'mine');
  });


  it('should loadLineup opponent data and parse properly', function(done) {
    var self = this;
    this.timeout(10000);

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (arg === 'onLoadLineupCompleted()') {
        // make sure that the rquest has been converted into data properly
        expect(self.LiveNBAStore.data.opponentLineupPlayers.order.length).to.equal(8);

        // restore logging
        log.debug = prev;

        done();
      }
    };

    LiveNBAActions.loadLineup(3, 'opponent');
  });


  it('should update data.courtEvents after timeout within _onEventReceived', function(done) {
    var self = this;
    this.timeout(3000);

    var currentSize = Object.keys(self.LiveNBAStore.data.courtEvents).length;

    self.LiveNBAStore._onEventReceived({
      "id": "825e52a1-a6b1-49e2-8aad-269522a63bcf",
      "game__id": "a0f4ab88-e622-4041-8f9d-f3c6b954ed43",
      "location__list": {
        "coord_x": 119,
        "coord_y": 26
      },
      "statistics__list": {
        "fieldgoal__list": {
          "made": "true",
          "player": "ea162a49-c774-4ace-b629-8eaf2e889ddb",
          "points": 3,
          "shot_type": "jump shot",
          "team": "583ec825-fb46-11e1-82cb-f4ce4684ea4c",
          "three_point_shot": "true"
        }
      }
    });

    setTimeout(function () {
      expect(Object.keys(self.LiveNBAStore.data.courtEvents).length).to.be.above(currentSize);
      done();
    }, 2500);

  });


  it('should update player.history after timeout within _onEventReceived', function(done) {
    var self = this;
    this.timeout(4000);

    self.LiveNBAStore._onEventReceived({
      "id": "825e52a1-a6b1-49e2-8aad-269522a63bcf",
      "game__id": "1391bd60-8a63-4a62-aaab-158d612d507c",
      "location__list": {
        "coord_x": 119,
        "coord_y": 26
      },
      "statistics__list": {
        "fieldgoal__list": {
          "made": "true",
          "player": "ff76cdb2-9e72-4ba9-956f-9d99033cbe13",
          "points": 3,
          "shot_type": "jump shot",
          "team": "583ec825-fb46-11e1-82cb-f4ce4684ea4c",
          "three_point_shot": "true"
        },
        "assist__list": {
          "player": "not_a_player_in_matchup"
        }
      }
    });

    setTimeout(function () {
      var player = self.LiveNBAStore.data.matchupPlayers['443'];

      expect(player.history[player.history.length - 1].id).to.equal('825e52a1-a6b1-49e2-8aad-269522a63bcf');
      done();
    }, 3500);

  });


  it('should return false if the eventCall does not have any event statistics', function() {
    var self = this;

    var response = self.LiveNBAStore._onEventReceived({
      "id": "825e52a1-a6b1-49e2-8aad-269522a63bcf",
      "game__id": "1391bd60-8a63-4a62-aaab-158d612d507c",
      "location__list": {
        "coord_x": 119,
        "coord_y": 26
      }
    });

    expect(response).to.equal(false);
  });


  it('should return int having passed in byteArray', function() {
    var self = this;
    var lineups = new Uint8Array([0x00, 0x00, 0x00, 0x02, 0x00, 0x09, 0x00, 0x00, 0x00, 0x01, 0x00, 0x02, 0x00, 0x0F, 0x00, 0x03, 0x00, 0x04, 0x0F, 0x00, 0x00, 0x10, 0x00, 0x05, 0x00, 0x06, 0x00, 0x07, 0x00, 0x00, 0x00, 0x10, 0x02, 0x00, 0x00, 0x0F, 0x00, 0x03, 0x00, 0x04, 0x0F, 0x00, 0x00, 0x10, 0x00, 0x05, 0x00, 0x06, 0x00, 0x09]);

    try {
      self.LiveNBAStore._convertToInt(8, new Uint8Array([0x00, 0x02]), 0, 2);
    } catch(e) {
      expect(e.message).to.equal('You must pass in a byteSize of 16 or 32');
    }

    expect(self.LiveNBAStore._convertToInt(16, new Uint8Array([0x00, 0x02]), 0, 2)).to.equal(2);
    expect(self.LiveNBAStore._convertToInt(32, new Uint8Array([0x00, 0x00, 0x0F, 0x00]), 0, 4)).to.equal(3840);
  });


  it('should return object of lineups if passed in byteArray', function() {
    var self = this;
    var lineups = new Uint8Array([0x00, 0x00, 0x00, 0x02, 0x00, 0x09, 0x00, 0x00, 0x00, 0x01, 0x00, 0x02, 0x00, 0x0F, 0x00, 0x03, 0x00, 0x04, 0x0F, 0x00, 0x00, 0x10, 0x00, 0x05, 0x00, 0x06, 0x00, 0x07, 0x00, 0x00, 0x00, 0x10, 0x02, 0x00, 0x00, 0x0F, 0x00, 0x03, 0x00, 0x04, 0x0F, 0x00, 0x00, 0x10, 0x00, 0x05, 0x00, 0x06, 0x00, 0x09]);

    var myLineup = self.LiveNBAStore._convertLineup(9, lineups, 6);

    expect(myLineup.id).to.equal(1);
  });


  // it('should connect to socket properly', function(done) {
  //   this.timeout(10000);

  //   var io = require('socket.io')(5838);

  //   // replace log method to listen and check messages
  //   var prev = log.debug;
  //   var called;

  //   log.debug = function (arg) {
  //     console.log(arg);

  //     if (arg === 'value') {
  //       expect(true).to.equal(true);

  //       // restore and exit
  //       log.debug = prev;
  //       io = null;
  //       done();
  //     }
  //   };


  //   io.on('connection', function (socket) {
  //     socket.emit('key', 'value');
  //   });


    // var livestore = LiveNBAStore.init();
  // });


  // should parse 8 bit of all lineups in a contest on load, single call
  // should have method to take all lineups and determine scores for order on dropdown

  // event stream:
  // should ignore events that do not involve the players on the lineup

  // player update stream:
  // should wait 10 seconds to see if a corresponding event shows, then show
  // should show update if event has already passed
  // should reset event stream and player data through api calls when socket reconnects
  //   should it say something if not connected to socket stream?

});
