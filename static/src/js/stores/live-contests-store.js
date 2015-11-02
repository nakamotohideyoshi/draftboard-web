'use strict';

var _forEach = require('lodash/collection/forEach');
var _sortBy = require('lodash/collection/sortBy');
var Buffer = require('buffer/').Buffer;
var LiveContestsActions = require('../actions/live-contests-actions');
var LiveDraftGroupsStore = require('./live-draft-groups-store');
var Lockr = require('lockr');
var log = require("../lib/logging");
var Reflux = require('reflux');
var request = require("superagent");
var vsprintf = require("sprintf-js").vsprintf;


/*
 * Store currently used live contests, stores them in localStorage
 *
 * - EntriesStore feeds in contest ID, then GET
 *     - all lineups for a contest once per night, stores as hex bytes in localStorage
 *     - contest details for the payout structure once per night, stores in localStorage
 * - with each contest's data it
 *     - converts from hex bytes into list of lineups
 *     - takes the LiveContestStore fantasy points and generates standings order
 *     - when asked, shows top players owned by position, top players owned
*/
var LiveContestsStore = Reflux.createStore({
  data: {},

  init: function() {
    var self = this;
    log.debug('LiveContestsStore.init()');

    // Reflux auto call of actions, see http://git.io/vCAmc for more info
    self.listenToMany(LiveContestsActions);

    // set data structure on init
    self.resetData();
  },


  /**
   * method to reset the data to the initialization point. used in tests classes, in after() method reset before exiting
   */
  resetData: function() {
    var self = this;
    log.debug('LiveContestsStore.resetData()');

    self.data = {
      apiData: {},
      stats: {}
    };

    // if the contests are in localStorage, use them
    var localStorageKey = vsprintf('live_contests');
    var localStorageValue = Lockr.get(localStorageKey, null);

    // make sure to set expiration low enough for tests to work, otherwise make them 12 hours
    self.localStorageTTL = (process.env.NODE_ENV !== 'production') ? 10000 : 43200000;

    // make sure that the data exists and is less than a day old
    if (localStorageValue !== null) {
      log.debug('resetData() - localStorage for contests exists');

      // associate data to store
      self.data.apiData = localStorageValue.apiData;

      // remove old contests
      _forEach(self.data.apiData, function(contest, id) {
        if (contest.expires < Date.now()) {
          log.debug(vsprintf('resetData() - removing contest %d', [id]));
          delete(self.data.apiData[id]);
        }
      });

      self.saveContestsToLocalStorage();
    }
  },


  /**
   * Saves self.data.contests to localStorage to speed up page load
   */
  saveContestsToLocalStorage: function() {
    log.debug('saveContestsToLocalStorage()');

    Lockr.set('live_contests', {
      'date': Date.now(),
      'apiData': this.data.apiData
    });
  },




  // ACTIONS ----------------------------------------------

  /**
   * Shortcut method to async both loadContestLinups and loadContestInfo data
   */
  onLoadContest: function(contestId) {
    var self = this;
    log.debug('onLoadContest()');

    // if we already have the contest, great, we're done
    if (contestId in self.data.apiData) {
      log.debug('onLoadContest() - Already in self.data', contestId);
      return;
    }

    LiveContestsActions.loadContestLineups(contestId);
    LiveContestsActions.loadContestInfo(contestId);
  },


  /**
   * GET all lineups for a contest
   *
   * Use localStorage version if exists, otherwise GET and store in localStorage.
   *
   * NOTE: we force a refresh by running this method. loadContest checks whether it's already in localStorage, NOT here.
   */
  onLoadContestLineups: function(contestId) {
    log.debug('onLoadContestLineups()');
    var self = this;

    // otherwise request the contest and store in localStorage
    request
      .get('/contest/all-lineups/' + contestId)
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .end(function(err, res) {
        if (err) {
          LiveContestsActions.loadContestLineups.failed(err);
        } else {
          var expiration = Date.now() + self.localStorageTTL;

          if (contestId in self.data.apiData) {
            self.data.apiData[contestId]['bytes'] = res.text;
            self.data.apiData[contestId]['expires'] = expiration;
          } else {
            // 12 hour expiration for now, eventually would be smart to expire when contest is complete
            self.data.apiData[contestId] = {
              'expires': expiration,
              'bytes': res.text
            };
          }

          // save, trigger, and complete
          self.saveContestsToLocalStorage();
          self.trigger(self.data);
          LiveContestsActions.loadContestLineups.completed(contestId);

          log.debug(vsprintf('onLoadContestLineups() - GET, %d', [contestId]));
        }
    });
  },


  /**
   * GET contest information
   *
   * Use localStorage version if exists, otherwise GET and store in localStorage
   *
   * NOTE: we force a refresh by running this method. loadContest checks whether it's already in localStorage, NOT here.
   */
  onLoadContestInfo: function(contestId) {
    log.debug('onLoadContestInfo()');
    var self = this;

    // otherwise request the contest and store in localStorage
    request
      .get('/contest/info/' + contestId)
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .end(function(err, res) {
        if (err) {
          LiveContestsActions.loadContestInfo.failed(err);
        } else {
          var expiration = Date.now() + self.localStorageTTL;

          if (contestId in self.data.apiData) {
            self.data.apiData[contestId]['info'] = res.body;
            self.data.apiData[contestId]['expires'] = expiration;
          } else {
            // 12 hour expiration for now, eventually would be smart to expire when contest is complete
            self.data.apiData[contestId] = {
              'expires': expiration,
              'info': res.body
            };
          }

          // save, trigger, and complete
          self.saveContestsToLocalStorage();
          self.trigger(self.data);
          LiveContestsActions.loadContestInfo.completed(contestId);
        }
    });
  },




  // COMPLETED ACTIONS ----------------------------------------------


  /**
   * Dynamically called via listenToMany for the LiveContestsActions.loadContestLineups action
   */
  onLoadContestCompleted: function(contestId) {
    var self = this;
    log.debug('onLoadContestCompleted()');

    // TODO LiveContestsStore - generate contest standings
    var storedContest = self.data.apiData[contestId];

    // TODO fix this when we have real data
    var draftGroupId = storedContest.info.draft_group;

    if (draftGroupId in LiveDraftGroupsStore.data.draftGroups === false) {
      log.debug(vsprintf('onLoadContestCompleted() - Draft group does not exist yet, %d', [draftGroupId]));
      return;
    }

    self._generateContestStats(contestId, LiveDraftGroupsStore.data.draftGroups[draftGroupId]);

    log.debug(vsprintf('onLoadContestCompleted() - contest %d stats generated', [contestId]));
  },


  /**
   * Dynamically called via listenToMany for the LiveContestsActions.loadContestLineups action
   */
  onLoadContestLineupsCompleted: function(contestId) {
    log.debug('onLoadContestLineupsCompleted()');

    // check if contest is done loading
    LiveContestsActions.loadContest.status(contestId);
  },


  /**
   * Dynamically called via listenToMany for the LiveContestsActions.loadContestLineups action
   */
  onLoadContestInfoCompleted: function(contestId) {
    log.debug('onLoadContestInfoCompleted()');

    // check if contest is done loading
    LiveContestsActions.loadContest.status(contestId);
  },




  // FAILED ACTIONS ----------------------------------------------


  onLoadContestLineupsFailed: function(err) {
    log.debug('onLoadContestLineupsFailed()');

    // TODO LiveContestsStore - send failed loadContest to Sentry
  },

  onLoadContestInfoFailed: function(err) {
    log.debug('onLoadContestInfoFailed()');

    // TODO LiveContestsStore - send failed loadContest to Sentry
  },



  /**
   * Check if async calls for loading lineups and info are done
   */
  onLoadContestStatus: function(contestId) {
    var self = this;
    log.debug('onLoadContestStatus()');

    if (contestId in self.data.apiData) {
      var contest = self.data.apiData[contestId];

      if ('info' in contest && 'bytes' in contest) {
        LiveContestsActions.loadContest.completed(contestId);
      }
    }
  },




  // INTERNAL HELPER METHODS ----------------------------------------------


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
   * Generates sorted lineups for a contest
   *
   * @param {integer} (required) Contest PK
   * @param {Object} (required) Draft group, used for fantasy points of players
   */
  _generateContestStats: function(contestId, draftGroup) {
    log.debug('_generateContestStats()');
    var self = this;
    var storedContest = self.data.apiData[contestId];

    self.data.stats[contestId] = {
      'sortedLineups': self._rankContestLineups(storedContest.bytes, draftGroup),
      'lastUpdated': Date.now()
    };
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
  _rankContestLineups: function(apiContestLineupsBytes, draftGroup) {
    var self = this;
    log.debug('_updateFantasyPoints()');

    // add up who's in what place
    var responseByteArray = new Buffer(apiContestLineupsBytes, 'hex');

    var lineups = [];

    // each lineup is 20 bytes long
    for (var i=6; i < responseByteArray.length; i += 20) {
      var lineup = self._convertLineup(8, responseByteArray, i);

      // potentially combine this with converting bytes to remove one loop, but then
      // each time we get updated fantasy points we'd have to make a different method to just do this part
      lineup.points = self._updateFantasyPointsForLineup(lineup, draftGroup);
    }

    var sortedLineups = _sortBy(lineups, 'points').reverse();

    return sortedLineups;
  },


  /**
   * Takes the lineup object, loops through the roster, and totals the fantasy points using the latest fantasy stats
   *
   * @param {Object} (required) The lineup object, containing id, roster and points
   * @param {Object} (required) Fantasy points object from API, has player array
   *
   * @return {Integer} Return the total points
   */
  _updateFantasyPointsForLineup: function(lineup, draftGroup) {
    // log.debug('_updateFantasyPointsForLineup');
    var total = 0;

    _forEach(lineup.roster, function(playerId) {
      if (playerId in draftGroup === false) {
        log.error(vsprintf('_updateFantasyPointsForLineup() - player does not exist: %d', [playerId]));
        return 0;
      }

      var fantasyPlayer = draftGroup[playerId];

      total += fantasyPlayer.fp;
    });

    return total;
  }

});


module.exports = LiveContestsStore;
