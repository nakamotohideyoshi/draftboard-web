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
    var lineupPlayers;

    if (this.props.whichSide === 'me') {
      lineupPlayers = LiveNBAStore.data.myLineupPlayers;
    } else {
      lineupPlayers = LiveNBAStore.data.opponentLineupPlayers;
    }


    var currentPlayers = lineupPlayers.map(function(player) {
      return (
        <LiveNBALineupPlayer key={player.id} player={player} />
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
