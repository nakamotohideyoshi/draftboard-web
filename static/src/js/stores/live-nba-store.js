'use strict';

var _forEach = require('lodash/collection/forEach');
var _map = require('lodash/collection/map');
var _sortBy = require('lodash/collection/sortBy');
var io = require('socket.io-client');
var LiveNBAActions = require("../actions/live-nba-actions");
var Lockr = require('lockr');
var log = require("../lib/logging");
var Reflux = require('reflux');
var request = require("superagent");
var Buffer = require('buffer/').Buffer;


/*
* A store to keep track of our live section's state.
*
* Overall function: init() sets up the data structure and calls fetchPlayerData() to pull in the players and the lineups.
* It also starts up a socket server connection and listens for event and player messages. Upon receiving an event, we
* check to see if the call has a player relevant to the matchup (_onEventReceived), then send to the appropriate game
* queue (_addEventToGameQueue). The game queue is a syncronous list of events to force viewing of events in the order in
* which they came in, rather than all at once. _addEventToGameQueue calls _pushOldestGameEvent, which pops off the oldest
* event from the queue and sends to _showEvent. When the animation sequenece in _showEvent is complete it calls
* _pushOldestGameEvent to pop off the next event.
*/
var LiveNBAStore = Reflux.createStore({
  data: {},

  init: function() {
    log.debug('LiveNBAStore.init()');

    // trickiness used by Reflex to auto call methods, see docs for more info
    // TODO consider explicitly showing
    this.listenToMany(LiveNBAActions);

    this.resetData();
  },


  resetData: function() {
    this.data = {
      // Stored API calls
      apiAllFantasyPoints: {},
      apiContestLineupsBytes: '',
      apiDraftGroup: [],

      // constants
      apiFantasyPointsCheckInterval: 15000,
      initLoaded: false,

      // initial ajax checks, this way we can concurrently pull in everything!
      initAjaxCompleted: {
        'contestLineups': 0,
        'draftGroup': 0,
        'draftGroupFantasyPoints': 0,
        'lineup': 0
      },

      // Information uesd by React components
      courtEvents: {},
      gameQueues: {},
      matchupPlayers: {},
      matchupPlayersBySportsRadarId: {},
      myLineupPlayers: {
        'originalData': {},
        'order': [],
        'players': {}
      },
      opponentLineupPlayers: {
        'originalData': {},
        'order': [],
        'players': {}
      },
      rankedContestLineups: []
    };
  },


  /**
   * Get fantasy points for all draftable players.
   * Used in conjunction with the draftGroup players and allLineups to determine standings.
   *
   * @param {integer} (required) The ID of the contest.
   */
  onLoadContestLineups: function(contestId) {
    if (!contestId) {
      log.error('onLoadContestLineups() - No contest specified.');
      return;
    }

    var self = this;
    var localLineupsData = Lockr.get('contest_lineups_data_' + contestId, null);

    // one min for dev, 12 hours for production
    var timeLocalStorage = (process.env.NODE_ENV !== 'production') ? 60000 : 43200000;

    // make sure that the data exists and is less than 12 hours old
    if (localLineupsData !== null && localLineupsData.date + timeLocalStorage > Date.now()) {
      log.debug('onLoadContestLineups() - Using localStorage of apiContestLineupsBytes');

      self.data.apiContestLineupsBytes = localLineupsData.apiContestLineupsBytes;

      // trigger and complete
      self.trigger(self.data);
      LiveNBAActions.loadContestLineups.completed();
    } else {
      log.debug('onLoadContestLineups() - Pulling latest apiContestLineupsBytes');

      request
        .get("/contest/all-lineups/" + contestId)
        .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
        .end(function(err, res) {
          if(err) {
            LiveNBAActions.loadContestLineups.failed(err);
          } else {
            // save the bytes to parse once all the calls come through
            self.data.apiContestLineupsBytes = res.text;

            // set the localStorage
            Lockr.set('contest_lineups_data_' + contestId, {
              'date': Date.now(),
              'apiContestLineupsBytes': self.data.apiContestLineupsBytes
            });

            // trigger and complete
            self.trigger(self.data);
            LiveNBAActions.loadContestLineups.completed();
          }
      });
    }
  },


  /**
   * Get a list of the draftable players.
   * Used to show player names, teams for the GUI
   *
   * @param {integer} (required) The ID of the draft group.
   */
  onLoadDraftGroup: function(draftGroupId) {
    log.debug('onLoadDraftGroup()');

    if (!draftGroupId) {
      log.error('onLoadDraftGroup() - No draftGroupId specified.');
      return;
    }

    var self = this;
    var localPlayerData = Lockr.get('player_data', null);

    // one min for dev, 12 hours for production
    var timeLocalStorage = (process.env.NODE_ENV !== 'production') ? 60000 : 86400000;

    // make sure that the data exists and is less than a day old
    if (localPlayerData !== null && localPlayerData.date + timeLocalStorage > Date.now()) {
      log.debug('onLoadDraftGroup() - Using localStorage of draftGroup');

      self.data.apiDraftGroup = localPlayerData.players;

      // trigger and complete
      self.trigger(self.data.apiDraftGroup);
      LiveNBAActions.loadDraftGroup.completed();
    } else {
      log.debug('onLoadDraftGroup() - Pulling latest draftGroup');

      request
        .get("/draft-group/" + draftGroupId + '/')
        .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
        .end(function(err, res) {
          if(err) {
            LiveNBAActions.loadDraftGroup.failed(err);
          } else {
            self.data.apiDraftGroup = res.body.players;

            // set the localStorage
            Lockr.set('player_data', {
              'date': Date.now(),
              'players': self.data.apiDraftGroup
            });

            // trigger and complete
            self.trigger(self.data.apiDraftGroup);
            LiveNBAActions.loadDraftGroup.completed();
          }
      });
    }
  },


  /**
   * Get fantasy points for all draftable players.
   * Used in conjunction with the draftGroup players and allLineups to determine standings.
   *
   * @param {integer} (required) The ID of the draft group.
   */
  onLoadDraftGroupFantasyPoints: function(draftGroupId) {
    if (!draftGroupId) {
      log.error('onLoadDraftGroupFantasyPoints() - No draft group specified.');
      return;
    }

    var self = this;

    log.debug('onLoadDraftGroupFantasyPoints() - Pulling latest draftGroup');

    request
      .get("/draft-group/fantasy-points/" + draftGroupId)
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .end(function(err, res) {
        if(err) {
          LiveNBAActions.loadDraftGroupFantasyPoints.failed(err);
        } else {
          self.data.apiAllFantasyPoints = res.body;
          self.data.apiAllFantasyPoints.created = Date.now();

          // trigger and complete
          self.trigger(self.data.apiAllFantasyPoints);
          LiveNBAActions.loadDraftGroupFantasyPoints.completed();
        }
    });
  },


  /**
   * Get a list of the draftable players.
   * Used to show player names, teams for the GUI
   *
   * @param {integer} (required) The ID of the lineup.
   * @param {string} (required) Which side this lineup is for, options are ['mine', 'opponent']
   */
  onLoadLineup: function(lineupId, whichSide) {
    if (!lineupId) {
      log.error('onLoadLineup() - No lineupId specified.');
      return;
    }

    var self = this;

    log.debug('onLoadLineup() - Pulling latest draftGroup');

    request
      .get("/contest/single-lineup/1/" + lineupId)
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .end(function(err, res) {
        if(err) {
          LiveNBAActions.loadLineup.failed(err);
        } else {
          var lineupPlayers, matchupPlayers = {};

          matchupPlayers, lineupPlayers = self._organizePlayerData(res.body, matchupPlayers, whichSide);

          switch (whichSide) {
            case 'opponent':
              self.data.opponentLineupPlayers = lineupPlayers;
              break;
            case 'mine':
              self.data.myLineupPlayers = lineupPlayers;
              break;
            default:
              LiveNBAActions.loadLineup.failed('whichSide was not a valid value');
          }

          self.data.matchupPlayers = matchupPlayers;

          // trigger and complete
          self.trigger(self.data);
          LiveNBAActions.loadLineup.completed();
        }
    });
  },


  /**
   * Dynamically called via listenToMany in this.init()
   */
  onLoadContestLineupsCompleted: function() {
    log.debug('onLoadContestLineupsCompleted()');

    this.data.initAjaxCompleted['contestLineups'] += 1;

    this._checkInitAjaxCompleted();
  },


  /**
   * Dynamically called via listenToMany in this.init()
   */
  onLoadDraftGroupCompleted: function() {
    log.debug('onLoadDraftGroupCompleted()');

    this.data.initAjaxCompleted['draftGroup'] += 1;

    this._checkInitAjaxCompleted();
  },


  /**
   * Dynamically called via listenToMany in this.init()
   */
  onLoadDraftGroupFantasyPointsCompleted: function() {
    log.debug('onLoadDraftGroupFantasyPointsCompleted()');

    // if already loaded, then just update the matchupPlayer totals
    if (this.data.initLoaded === true) {
      this._updateMatchupPlayerFantasyPoints();

      return;
    }

    this.data.initAjaxCompleted['draftGroupFantasyPoints'] += 1;
    this._checkInitAjaxCompleted();
  },


  /**
   * Dynamically called via listenToMany in this.init()
   */
  onLoadLineupCompleted: function() {
    log.debug('onLoadLineupCompleted()');

    this.data.initAjaxCompleted['lineup'] += 1;

    this._checkInitAjaxCompleted();
  },



  // "PRIVATE" METHODS


  /**
   * Push an event into a game queue. If that queue is not currently showing any events, show the oldest one.
   *
   * @param {Object} (required) The event call information
   */
  _addEventToGameQueue: function(eventCall) {
    log.debug('_addEventToGameQueue()');
    var self = this;

    // set the game ID to know which queue to push to
    var gameId = eventCall.game__id;
    if (gameId in self.data.gameQueues === false) {
      self.data.gameQueues[gameId] = {
        queue: [],
        isRunning: false
      };
    }
    var gameQueue = self.data.gameQueues[gameId];

    gameQueue.queue.push(eventCall);

    if (gameQueue.isRunning === false) {
      self._pushOldestGameEvent(gameId);
    }
  },


  /**
   * Checks whether all the initial ajax calls are completed, this way we can concurrently async in all the calls
   * If they are complete, then we organize the data and start up the socket server
   */
  _checkInitAjaxCompleted: function() {
    // if already loaded then don't bother
    if (this.data.initLoaded === true) {
      return;
    }

    var checks = this.data.initAjaxCompleted;


    if (checks.draftGroup === 1 && checks.lineup === 2 && checks.draftGroupFantasyPoints === 1) {
      this.data.initLoaded = true;

      log.debug('_checkInitAjaxCompleted() - Initial ajax calls completed');

      this._setupPlayerDataRelationships();
      this._startDataInflux();
    }
  },


  /**
   * Relate fantasy points, draft group to lineups
   * Run this each time a new lineup is added in.
   */
  _setupPlayerDataRelationships: function() {
    log.debug('_setupPlayerDataRelationships()');
    var self = this;


    // associate latest fantasy points to matchupPlayers and update
    self._updateMatchupPlayerFantasyPoints();

    var matchupPlayers = self.data.matchupPlayers;
    _forEach(self.data.apiDraftGroup, function(player) {
      if (player.player_id in matchupPlayers) {
        matchupPlayers[player.player_id].info = player;
      }
    });

    var contestLineups = self._rankContestLineups(self.data.apiContestLineupsBytes, self.data.apiAllFantasyPoints);
    self.data.rankedContestLineups = contestLineups;

    self.trigger(self.data);
    // log.debug('_setupPlayerDataRelationships data', self.data);
  },


  _startDataInflux: function() {
    // this._initEventsSocket();

    // this.data.intervalApiFantasyPoints = setInterval(LiveNBAActions.loadDraftGroupFantasyPoints, this.data.apiFantasyPointsCheckInterval, 1);
    // LiveNBAActions.loadDraftGroupFantasyPoints(1);

  },


  /**
   * Converts byte array into lineup object with id and roster
   *
   * @param {Integer} (required) Number of each players to parse out
   * @param {ByteArray} (required) Uint8Array of data
   * @param {Integer} (required) Where in the byte array should you start parsing data
   *
   * @return {Object} The parsed lineup object
   */
  _convertLineup: function(numberOfPlayers, byteArray, firstBytePosition) {
    var lineup = {
      'id': this._convertToInt(32, byteArray, firstBytePosition, 4),
      'roster': [],
      'total_points': ''
    };

    // move from the ID to the start of the players
    firstBytePosition += 4;

    // loop through the players
    for (var i = firstBytePosition; i < firstBytePosition + numberOfPlayers * 2; i += 2) {
      // parse out 2 bytes for each player's value
      lineup.roster.push(this._convertToInt(16, byteArray, i, 2));
    }

    return lineup;
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
  _convertToInt: function(byteSize, byteArray, byteOffset, byteLength) {
    if (byteSize === 32) {
      return new DataView(byteArray.buffer, byteOffset, byteLength).getInt32(0, false);
    } else if (byteSize === 16) {
      return new DataView(byteArray.buffer, byteOffset, byteLength).getInt16(0, false);
    } else {
      throw new Error('You must pass in a byteSize of 16 or 32');
    }
  },


  /**
   * Start up a connection to the socket server that pulls in events
   *
   * If you want to test this, you can run js/simulations/live-events.js, and add event data to test/data/live-events.json.
   * Craig will eventually make tailored data to show all possible events, see the animations, but until then am just
   * using random data that's too large to add to the git repo.
   */
  _initEventsSocket: function() {
    log.debug('_initEventsSocket()');

    var self = this;
    var socket = io('http://localhost:5838');

    // implement reconnect when available to avoid tons of errors in chrome
    // https://github.com/socketio/socket.io-client/issues/326

    socket.on('connect', function () {
      log.debug('Socket connected');

      socket.on('event', function(eventData) {
        log.debug('event');

        self._onEventReceived(eventData);
      });
    });

    // directly pull in events rather than running separate cmd
    // var history = require('../fixtures/live-nba-history')[0].fixtures();
    // _forEach(history, this._onEventReceived);
  },


  /**
   * Parse an event call from socket, and check to make sure it's a valid call that has a player relevant to the matchup
   * If it does, then pass along the information to the appropriate game queue
   *
   * TODO connect this to socket connection that updates in the init() method
   * TODO what happens on a result error here? Should trigger an error to be stored that we are alerted to, and not show
   * the user perhaps?
   *
   * @param {Object} (required) The event call information
   */
  _onEventReceived: function(eventCall) {
    // log.debug('_onEventReceived', eventCall.id);
    var self = this;

    // if this is a statistical based call
    if ('statistics__list' in eventCall === false) {
      return false;
    }

    var events = eventCall.statistics__list;

    // loop through players to see if they match one of the players in the lineup match
    _forEach(events, function(event) {
      if (event.player in self.data.matchupPlayersBySportsRadarId) {
        self._addEventToGameQueue(eventCall);
      }
    });
  },


  /**
   * Uses the original data set and converts into lineup object and adds players to the matchup pool
   *
   * @param {Object} (required) Original set of players from API
   * @param {Object} (required) Final, centralized associative array of players
   * @param {String} (required) Which lineup, mine or opponent?
   *
   * @return {Object, Object} Return the matchupPlayers and lineupPlayer objects
   */
  _organizePlayerData: function(originalSet, matchupPlayers, whichSide) {
    log.debug('_organizePlayerData()');
    var self = this;

    // store the order that the lineup should be shown in
    var orderedIds = _map(originalSet, function (item) {
      if (item.data.length === 1) {
        return item.data[0].fields.player_id;
      }
    });

    var matchupPlayersBySportsRadarId = self.data.matchupPlayersBySportsRadarId;

    // store the lineup to use with LiveNBALineup
    var lineupPlayers = {
      'originalData': originalSet,
      'order': orderedIds,
      'players': {}
    };

    _forEach(originalSet, function(item) {
      // TODO add sentry error for this, should never happen
      if (item.data.length === 0) {
        log.debug('Player has no stats associated');
        return;
      }

      var player = item.data[0].fields;
      var id = player.player_id;

      // generate player objects that are stored in matchupPlayers
      if (id in matchupPlayers) {
        matchupPlayers[id].whichSide = 'both';
      } else {
        matchupPlayersBySportsRadarId[player.srid_player] = id;

        matchupPlayers[id] = {
          'history': [],
          'stats': player,
          'whichSide': whichSide
        };
      }

      // reference matchupPlayers player in lineupPlayers.players
      lineupPlayers.players[id] = matchupPlayers[id];
    });

    return matchupPlayers, lineupPlayers;
  },


  /**
   * This pops out the oldest event from the game queue and then sends it to _showEvent() to show the user.
   * If the queue isn't running, when it gets called again the cycle starts up again.
   *
   * @param {uuid} (required) The id of the game queue
   * @return {mixed} Returns false if there are no more events in the queue
   */
  _pushOldestGameEvent: function(gameId) {
    log.debug('_pushOldestGameEvent');

    var self = this;
    var gameQueue = self.data.gameQueues[gameId];
    log.debug('gameQueue length', gameQueue.queue.length);

    if (gameQueue.queue.length === 0) {
      gameQueue.isRunning = false;

      return false;
    }

    var oldestEvent = gameQueue.queue.shift();

    gameQueue.isRunning = true;
    self._showEvent(oldestEvent);
  },


  /**
   * Takes the contest lineups, converts each out of bytes, then adds up fantasy total
   *
   * @param {Object} (required) Original set of players from API
   * @param {Object} (required) Final, centralized associative array of players
   * @param {String} (required) Which lineup, mine or opponent?
   *
   * @return {Object, Object} Return the lineups, sorted highest to lowest points
   */
  _rankContestLineups: function(apiContestLineupsBytes, fantasyPoints) {
    log.debug('_updateFantasyPoints()');

    // add up who's in what place
    var responseByteArray = new Buffer(apiContestLineupsBytes, 'hex');

    var lineups = [];

    // each lineup is 20 bytes long
    for (var i=6; i < responseByteArray.length; i += 20) {
      var lineup = this._convertLineup(8, responseByteArray, i);

      // potentially combine this with converting bytes to remove one loop, but then
      // each time we get updated fantasy points we'd have to make a different method to just do this part
      lineup.points = this._updateFantasyPointsForLineup(lineup, fantasyPoints);

      lineups.push(lineup);
    }

    var sortedLineups = _sortBy(lineups, 'points').reverse();

    return sortedLineups;
  },


  /**
   * Show the event on the court and beside the player
   * This is called from a game queue when its turn comes up
   * Note the order in which events occur:
   * - new history event shows up (without results)
   * - shooter has an animation
   * - show the result in the history and update the player in the lineup
   *
   * @param {Object} (required) The event that needs to be added (eventually a socket update)
   */
  _showEvent: function(eventCall) {
    log.debug('_showEvent()');

    var self = this;

    var players = [];

    // relevant information for court animation
    var courtInformation = {
      'id': eventCall.id,
      'location': eventCall.location__list,
      'events': {}
    };

    // for now limit to one event per statistical event
    _forEach(eventCall.statistics__list, function(event, key) {
      event.whichSide = null;

      // if the player applies to our lineups
      _forEach(self.data.matchupPlayers, function(player) {
        if (player.stats.srid_player === event.player) {
          players.push(player);
          player.playStatus = 'eventInProgress';

          event.whichSide = player.whichSide;
        }
      });

      courtInformation.events[key.slice(0, -6)] = event;
    });

    // make the user aware that a player is doing something
    this.trigger(self.data.matchupPlayers);

    // trigger the animation on the court first
    setTimeout(function() {
      this.data.courtEvents[courtInformation.id] = courtInformation;
      this.trigger(this.data.courtEvents);

      // show the results
      setTimeout(function() {
        _forEach(players, function(player) {
          // update the player to have the appropriate history
          player.history.push(eventCall);
          player.playStatus = undefined;
        });

        this.trigger(self.data.matchupPlayers);
      }.bind(this), 2000);

      // remove the player from the court
      setTimeout(function() {
        self._pushOldestGameEvent(eventCall.game__id);

        delete this.data.courtEvents[courtInformation.id];
        this.trigger(this.data.courtEvents);
      }.bind(this), 4000);

    }.bind(this), 1000);
  },


  /**
   * Takes the lineup object, loops through the roster, and totals the fantasy points using the latest fantasy stats
   *
   * @param {Object} (required) The lineup object, containing id, roster and points
   * @param {Object} (required) Fantasy points object from API, has player array
   *
   * @return {Integer} Return the total points
   */
  _updateFantasyPointsForLineup: function(lineup, fantasyPoints) {
    var total = 0;

    _forEach(lineup.roster, function(playerId) {
      var fantasyPlayer = fantasyPoints.players[playerId];

      // TODO may not need this, could be a dev problem
      if (fantasyPlayer === undefined) {
        return;
      }

      total += fantasyPlayer.fp;
    });

    return total;
  },


  /**
   * Takes the latest pull from API for fantasy points by draft group, and updates matchupPlayer fantasy totals.
   */
  _updateMatchupPlayerFantasyPoints: function() {
    log.debug('_updateMatchupPlayerFantasyPoints()');

    var fantasyPoints = this.data.apiAllFantasyPoints;

    _forEach(this.data.matchupPlayers, function(player, id) {
      player.stats.points = fantasyPoints.players[id];
      player.stats.last_updated = fantasyPoints.created;
    });

    this.trigger(this.data.matchupPlayers);
  }

});


module.exports = LiveNBAStore;
