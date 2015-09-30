"use strict";

var Reflux = require("reflux");
var DraftActions = require("../actions/draft-actions");
var log = require("../lib/logging");
var DraftGroupStore = require('./draft-group-store.js');
var _find = require("lodash/collection/find");


/**
 * Store the active player in a DraftGroup (players for a specific set of contests).
 */
var DraftGroupActivePlayerStore = Reflux.createStore({

  data: {},


  init: function() {
    this.listenTo(DraftActions.playerFocused, this.setActivePlayer);
    this.data.activePlayer = null;
  },


  /**
   * Set the focused player based on the provided player ID.
   * @param {number} lineupId the ID of the lineup to set as active.
   */
  setActivePlayer: function(playerId) {
    var player = _find(DraftGroupStore.allPlayers, 'player_id', playerId);
    log.debug('DraftGroupActivePlayerStore.setFocusedPlayer()', playerId);

    if(typeof playerId === 'number') {
      this.data.activePlayer = player;
      this.trigger(this.data);
    }
  }

});


module.exports = DraftGroupActivePlayerStore;
