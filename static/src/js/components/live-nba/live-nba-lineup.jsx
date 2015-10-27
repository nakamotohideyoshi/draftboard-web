"use strict";

var React = require('react');
var Reflux = require('reflux');
var renderComponent = require('../../lib/render-component');
var LiveNBALineupPlayer = require('./live-nba-lineup-player');
var LiveNBAStore = require("../../stores/live-nba-store");

/**
 * The history ticker at the bottom of the live page
 */
var LiveNBALineup = React.createClass({
  propTypes: {
    whichSide: React.PropTypes.string.isRequired
  },

  mixins: [
    Reflux.connect(LiveNBAStore)
  ],

  getDefaultProps: function() {
    return {
      whichSide: ''
    };
  },

  render: function() {
    var lineupData;

    if (this.props.whichSide === 'me') {
      lineupData = LiveNBAStore.data.myLineupPlayers;
    } else {
      lineupData = LiveNBAStore.data.opponentLineupPlayers;
    }

    var currentPlayers = lineupData.order.map(function(playerId) {
      // need a better check here
      if (lineupData.players[playerId] === undefined) {
        return null;
      }

      return (
        <LiveNBALineupPlayer key={playerId} player={lineupData.players[playerId]} />
      );
    });

    var className = 'live-nba__lineup live-lineup live-lineup--' + this.props.whichSide;

    return (
      <div className={ className }>
        <ul className="live-lineup__players">
          {currentPlayers}
        </ul>
      </div>
    );
  }
});


// Render the component.
renderComponent(<LiveNBALineup />, '.live-history');

module.exports = LiveNBALineup;
