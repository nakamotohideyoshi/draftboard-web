// NOTE this is not functioning.
// Needed a place to store what had been done in Reflux + socket, needs to be converted to Pusher + Redux


import { forEach as _forEach, map as _map, sortBy as _sortBy } from 'lodash'

var io = require('socket.io-client');
var Lockr = require('lockr');
var log = require("../lib/logging");
var Reflux = require('reflux');
var request = require("superagent");
var Buffer = require('buffer/').Buffer;


/**
 * Push an event into a game queue. If that queue is not currently showing any events, show the oldest one.
 *
 * @param {Object} (required) The event call information
 */
const _addEventToGameQueue = function(eventCall) {
  log.debug('_addEventToGameQueue()')
  var self = this

  // set the game ID to know which queue to push to
  var gameId = eventCall.game__id
  if (gameId in self.data.gameQueues === false) {
    self.data.gameQueues[gameId] = {
      queue: [],
      isRunning: false
    }
  }
  var gameQueue = self.data.gameQueues[gameId]

  gameQueue.queue.push(eventCall)

  if (gameQueue.isRunning === false) {
    self._pushOldestGameEvent(gameId)
  }
}


const _startDataInflux = function() {
  this._initEventsSocket()

  this.data.intervalApiFantasyPoints = setInterval(LiveNBAActions.loadDraftGroupFantasyPoints, this.data.apiFantasyPointsCheckInterval, 1)
}


/**
 * Start up a connection to the socket server that pulls in events
 *
 * If you want to test this, you can run js/simulations/live-events.js, and add event data to test/data/live-events.json.
 * Craig will eventually make tailored data to show all possible events, see the animations, but until then am just
 * using random data that's too large to add to the git repo.
 */
const _initEventsSocket = function() {
  log.debug('_initEventsSocket()')

  var self = this
  var socket = io('http://localhost:5838')

  // implement reconnect when available to avoid tons of errors in chrome
  // https://github.com/socketio/socket.io-client/issues/326

  socket.on('connect', function () {
    log.debug('Socket connected')

    socket.on('event', function(eventData) {
      log.debug('event')

      self._onEventReceived(eventData)
    })
  })

  // directly pull in events rather than running separate cmd
  // var history = require('../fixtures/live-nba-history')[0].fixtures()
  // _forEach(history, this._onEventReceived)
}


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
const _onEventReceived = function(eventCall) {
  // log.debug('_onEventReceived', eventCall.id)
  var self = this

  // if this is a statistical based call
  if ('statistics__list' in eventCall === false) {
    return false
  }

  var events = eventCall.statistics__list

  // loop through players to see if they match one of the players in the lineup match
  _forEach(events, function(event) {
    if (event.player in self.data.matchupPlayersBySportsRadarId) {
      self._addEventToGameQueue(eventCall)
    }
  })
}


/**
 * This pops out the oldest event from the game queue and then sends it to _showEvent() to show the user.
 * If the queue isn't running, when it gets called again the cycle starts up again.
 *
 * @param {uuid} (required) The id of the game queue
 * @return {mixed} Returns false if there are no more events in the queue
 */
const _pushOldestGameEvent = function(gameId) {
  log.debug('_pushOldestGameEvent')

  var self = this
  var gameQueue = self.data.gameQueues[gameId]
  log.debug('gameQueue length', gameQueue.queue.length)

  if (gameQueue.queue.length === 0) {
    gameQueue.isRunning = false

    return false
  }

  var oldestEvent = gameQueue.queue.shift()

  gameQueue.isRunning = true
  self._showEvent(oldestEvent)
}


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
const _showEvent = function(eventCall) {
  log.debug('_showEvent()')

  var self = this

  var players = []

  // relevant information for court animation
  var courtInformation = {
    'id': eventCall.id,
    'location': eventCall.location__list,
    'events': {}
  }

  // for now limit to one event per statistical event
  _forEach(eventCall.statistics__list, function(event, key) {
    event.whichSide = null

    // if the player applies to our lineups
    _forEach(self.data.matchupPlayers, function(player) {
      if (player.stats.srid_player === event.player) {
        players.push(player)
        player.playStatus = 'eventInProgress'

        event.whichSide = player.whichSide
      }
    })

    courtInformation.events[key.slice(0, -6)] = event
  })

  // make the user aware that a player is doing something
  this.trigger(self.data.matchupPlayers)

  // trigger the animation on the court first
  setTimeout(function() {
    this.data.courtEvents[courtInformation.id] = courtInformation
    this.trigger(this.data.courtEvents)

    // show the results
    setTimeout(function() {
      _forEach(players, function(player) {
        // update the player to have the appropriate history
        player.history.push(eventCall)
        player.playStatus = undefined
      })

      this.trigger(self.data.matchupPlayers)
    }.bind(this), 2000)

    // remove the player from the court
    setTimeout(function() {
      self._pushOldestGameEvent(eventCall.game__id)

      delete this.data.courtEvents[courtInformation.id]
      this.trigger(this.data.courtEvents)
    }.bind(this), 4000)

  }.bind(this), 1000)
}