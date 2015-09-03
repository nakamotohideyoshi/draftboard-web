'use strict';

var React = require('react/addons');
var LiveNBAStore = require('../../stores/live-nba-store.js');
var Lockr = require('lockr');
var expect = require('chai').expect;


describe('LiveNBAStore', function() {
  it('should update data.courtEvents after timeout within onEventReceived', function(done) {
    var self = this;
    this.timeout(3000);

    var currentSize = Object.keys(LiveNBAStore.data.courtEvents).length;

    LiveNBAStore.onEventReceived('mine', {
      isSuccessful: true,
      id: 'fae52402-5157-11e5-885d-feff819cdc9f',
      'player': 'df187cd4-4d7d-11e5-885d-feff819cdc9g',
      'action': 'Layup',
      'points': 2,
      'x': 600,
      'y': 200
    });

    setTimeout(function () {
      expect(Object.keys(LiveNBAStore.data.courtEvents).length).to.be.above(currentSize);
      done();
    }, 2500);

  });


  it('should update data.historyEvents after timeout within onEventReceived', function(done) {
    var self = this;
    this.timeout(4000);

    LiveNBAStore.onEventReceived('mine', {
      isSuccessful: true,
      id: 'fae52402-5157-11e5-885d-feff819cdc9e',
      'player': 'df187cd4-4d7d-11e5-885d-feff819cdc9g',
      'action': 'Layup',
      'points': 2,
      'x': 600,
      'y': 200
    });

    setTimeout(function () {
      var historyEvents = LiveNBAStore.data.myHistoryEvents;

      expect(historyEvents[historyEvents.length - 1].points).to.equal(2);
      done();
    }, 3500);

  });


  it('should fail when event is not successful', function() {
    var self = this;

    var historySize = LiveNBAStore.data.myHistoryEvents.length;

    LiveNBAStore.onEventReceived('mine', {
      isSuccessful: false
    });

    expect(LiveNBAStore.data.myHistoryEvents.length).to.equal(historySize);
  });


  it('should use opponentHistoryEvents when `opponent` is passed in', function() {
    var self = this;

    var historySize = LiveNBAStore.data.opponentHistoryEvents.length;

    LiveNBAStore.onEventReceived('opponent', {
      isSuccessful: true,
      id: 'fae52402-5157-11e5-885d-feff819cdc9d',
      'player': 'cbb8bb72-4d7d-11e5-885d-feff819cdc9a',
      'action': 'Layup',
      'points': 2,
      'x': 600,
      'y': 200
    });

    expect(LiveNBAStore.data.opponentHistoryEvents.length).to.be.above(historySize);
  });


  it('should update player data when fetchPlayerData is called', function() {
    var self = this;

    LiveNBAStore.data.myLineupPlayers.push({'foo': 'bar'});

    var playerSize = Object.keys(LiveNBAStore.data.myLineupPlayers).length;

    LiveNBAStore.fetchPlayerData();

    expect(Object.keys(LiveNBAStore.data.myLineupPlayers).length).to.be.below(playerSize);

    // TODO figure out way to check if there is localStorage set...
    // Lockr.set('player_data', {'foo': 'bar'});
    // LiveNBAStore.fetchPlayerData();

    // expect(LiveNBAStore.data.foo).to.equal('bar');
  });


  it('should return int having passed in byteArray', function() {
    var self = this;
    var lineups = new Uint8Array([0x00, 0x00, 0x00, 0x02, 0x00, 0x09, 0x00, 0x00, 0x00, 0x01, 0x00, 0x02, 0x00, 0x0F, 0x00, 0x03, 0x00, 0x04, 0x0F, 0x00, 0x00, 0x10, 0x00, 0x05, 0x00, 0x06, 0x00, 0x07, 0x00, 0x00, 0x00, 0x10, 0x02, 0x00, 0x00, 0x0F, 0x00, 0x03, 0x00, 0x04, 0x0F, 0x00, 0x00, 0x10, 0x00, 0x05, 0x00, 0x06, 0x00, 0x09]);

    try {
      LiveNBAStore.convertToInt(8, new Uint8Array([0x00, 0x02]), 0, 2);
    } catch(e) {
      expect(e.message).to.equal('You must pass in a byteSize of 16 or 32');
    }

    expect(LiveNBAStore.convertToInt(16, new Uint8Array([0x00, 0x02]), 0, 2)).to.equal(2);
    expect(LiveNBAStore.convertToInt(32, new Uint8Array([0x00, 0x00, 0x0F, 0x00]), 0, 4)).to.equal(3840);
  });


  it('should return object of lineups if passed in byteArray', function() {
    var self = this;
    var lineups = new Uint8Array([0x00, 0x00, 0x00, 0x02, 0x00, 0x09, 0x00, 0x00, 0x00, 0x01, 0x00, 0x02, 0x00, 0x0F, 0x00, 0x03, 0x00, 0x04, 0x0F, 0x00, 0x00, 0x10, 0x00, 0x05, 0x00, 0x06, 0x00, 0x07, 0x00, 0x00, 0x00, 0x10, 0x02, 0x00, 0x00, 0x0F, 0x00, 0x03, 0x00, 0x04, 0x0F, 0x00, 0x00, 0x10, 0x00, 0x05, 0x00, 0x06, 0x00, 0x09]);

    var myLineup = LiveNBAStore.convertLineup(9, lineups, 6);

    expect(myLineup.id).to.equal(1);
  });

});
