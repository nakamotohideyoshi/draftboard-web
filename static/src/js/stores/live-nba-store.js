'use strict';

var Reflux = require('reflux');
var Lockr = require('lockr');


/*
* A store to keep track of our live section's state.
*/
var LiveNBAStore = Reflux.createStore({
  data: {},

  init: function() {
    // okay to mock a socket connection we are going to pull in some fixtures and then 'receive' them, aka emit them
    // in a timeout method

    this.data = {
      myHistoryEvents: [],
      opponentHistoryEvents: [],
      myLineupPlayers: [],
      opponentLineupPlayers: [],
      courtEvents: {}
    };

    this.fetchPlayerData();

    // // TODO replace this with socket statement
    // // socket.on(liveEvents.server.eventUpdate, this.onEventReceived);
    // setTimeout(function() {
    //   LiveNBAStore.onEventReceived('mine', {
    //     isSuccessful: true,
    //     id: 'a1a913a4-5156-11e5-885d-feff819cdc9b',
    //     'player': 'df187a36-4d7d-11e5-885d-feff819cdc9f',
    //     'action': 'Dunk',
    //     'points': 4,
    //     'x': 300,
    //     'y': 400
    //   });
    // }, 1000);

    // // TODO replace this with socket statement
    // // socket.on(liveEvents.server.eventUpdate, this.onEventReceived);
    // setTimeout(function() {
    //   LiveNBAStore.onEventReceived('mine', {
    //     isSuccessful: true,
    //     id: 'a1a91106-5156-11e5-885d-feff819cdc9f',
    //     'player': 'df187cd4-4d7d-11e5-885d-feff819cdc9g',
    //     'action': 'Layup',
    //     'points': 2,
    //     'x': 600,
    //     'y': 200
    //   });
    // }, 1800);


    // // TODO replace this with socket statement
    // // socket.on(liveEvents.server.eventUpdate, this.onEventReceived);
    // setTimeout(function() {
    //   LiveNBAStore.onEventReceived('opponent', {
    //     isSuccessful: true,
    //     id: 'a1a914c6-5156-11e5-885d-feff819cdc9h',
    //     'player': 'cbb8be42-4d7d-11e5-885d-feff819cdc9b',
    //     'action': 'Rebound',
    //     'points': 4,
    //     'x': 1000,
    //     'y': 400
    //   });
    // }, 6000);
  },


  /**
   * Push new events into the store
   * Note the order in which events occur:
   * - new history event shows up (without results)
   * - shooter has an animation
   * - show the result in the history and update the player in the lineup
   *
   * TODO connect this to socket connection that updates in the init() method
   * TODO what happens on a result error here? Should trigger an error to be stored that we are alerted to, and not show
   * the user perhaps?
   *
   * @param {String} (required) Which side is the event for, 'mine' or 'opponent'
   * @param {Object} (required) The event that needs to be added (eventually a socket update)
   *
   * @return undefined
   */
  onEventReceived: function(whichSide, event) {
    var historyEvents;
    var lineupPlayersLookup;
    var rowKey;

    if (whichSide === 'mine') {
      historyEvents = this.data.myHistoryEvents;
      lineupPlayersLookup = this.data.myLineupPlayersLookup;
    } else {
      historyEvents = this.data.opponentHistoryEvents;
      lineupPlayersLookup = this.data.opponentLineupPlayersLookup;
    }

    if (event.isSuccessful) {
      var player = lineupPlayersLookup[event.player];

      var initialEventData = {
        id: event.id,
        playerName: player.player,
        waitForAnimation: 'foo'
      };

      // set player name from data
      event.playerName = player.player;

      // TODO more efficient way of adding to opposite side
      if (whichSide === 'mine') {
        rowKey = historyEvents.push(initialEventData);
      } else {
        rowKey = historyEvents.unshift(initialEventData);
      }

      // show that the player is doing something
      lineupPlayersLookup[event.player].playStatus = 'eventInProgress';

      // make the user aware that a player is doing something
      this.trigger(historyEvents);

      // trigger the animation on the court first
      setTimeout(function() {
        this.data.courtEvents[event.id] = event;
        this.trigger(this.data.courtEvents);

        // show the results
        setTimeout(function() {
          // add the rest of the data to show the result
          historyEvents[rowKey - 1] = event;
          this.trigger(historyEvents);

          // update the player to have the appropriate score
          lineupPlayersLookup[event.player].points += event.points;
          lineupPlayersLookup[event.player].playStatus = undefined;
          this.trigger(lineupPlayersLookup);
        }.bind(this), 2000);

        // remove the player from the court
        setTimeout(function() {
          delete this.data.courtEvents[event.id];
          this.trigger(this.data.courtEvents);
        }.bind(this), 4000);

      }.bind(this), 1000);
    }
  },


  /**
   * Get the lineups for this matchup.
   * Note: this will become async to fetch the data via API, so will need to adjusts tests at that point
   */
  fetchPlayerData: function() {
    var self = this;

    var locallyStoredPlayerData = Lockr.get('player_data', null);

    if (locallyStoredPlayerData !== null) {
      self.data = locallyStoredPlayerData;
    } else {
      // self.data.myHistoryEvents = require('../fixtures/live-nba-history')[0].fixtures();
      // self.data.opponentHistoryEvents = require('../fixtures/live-nba-history')[0].fixtures().reverse();
      self.data.myLineupPlayers = require('../fixtures/live-nba-lineup')[0].fixtures();
      self.data.opponentLineupPlayers = require('../fixtures/live-nba-lineup-opponent')[0].fixtures();

      // create lookup table for players
      // TODO when a player changes (aka villian watch), then will need to update lookup table
      var i;
      var len;

      var myLineupPlayersLookup = {};
      var myLineupPlayers = self.data.myLineupPlayers;
      for (i = 0, len = myLineupPlayers.length; i < len; i++) {
          myLineupPlayersLookup[myLineupPlayers[i].id] = myLineupPlayers[i];
      }
      self.data.myLineupPlayersLookup = myLineupPlayersLookup;

      var opponentLineupPlayersLookup = {};
      var opponentLineupPlayers = self.data.opponentLineupPlayers;
      for (i = 0, len = opponentLineupPlayers.length; i < len; i++) {
          opponentLineupPlayersLookup[opponentLineupPlayers[i].id] = opponentLineupPlayers[i];
      }
      self.data.opponentLineupPlayersLookup = opponentLineupPlayersLookup;

      // TODO make this actual player data rather than example of lineups
      Lockr.set('player_data', self.data);
    }

    self.trigger(self.data);
  },


  /**
   * Converts big endian byte string of byteLength into an int
   *
   * @param {Integer} (required) Size of each byte, options are 16 or 32
   * @param {ByteArray} (required) Uint8Array of lineups
   * @param {Integer} (required) How many bytes in you should start parsing
   * @param {Integer} (required) The number of bytes to parse starting from byteOffset
   *
   * @return undefined
   */
  convertToInt: function(byteSize, byteArray, byteOffset, byteLength) {
    if (byteSize === 32) {
      return new DataView(byteArray.buffer, byteOffset, byteLength).getInt32(0, false);
    } else if (byteSize === 16) {
      return new DataView(byteArray.buffer, byteOffset, byteLength).getInt16(0, false);
    } else {
      throw new Error('You must pass in a byteSize of 16 or 32');
    }
  },


  /**
   * Converts big endian byte string of byteLength into an int
   *
   * @param {Integer} (required) Number of each players to parse out
   * @param {ByteArray} (required) Uint8Array of data
   * @param {Integer} (required) Where in the byte array should you start parsing data
   *
   * @return undefined
   */
  convertLineup: function(numberOfPlayers, byteArray, firstBytePosition) {
    var lineup = {
      'id': this.convertToInt(32, byteArray, firstBytePosition, 4),
      'roster': []
    };

    // move from the ID to the start of the players
    firstBytePosition += 4;

    // loop through the players
    for (var i = firstBytePosition; i < firstBytePosition + numberOfPlayers * 2; i += 2) {
      // parse out 2 bytes for each player's value
      lineup.roster.push(this.convertToInt(16, byteArray, i, 2));
    }

    return lineup;
  }


});


module.exports = LiveNBAStore;
