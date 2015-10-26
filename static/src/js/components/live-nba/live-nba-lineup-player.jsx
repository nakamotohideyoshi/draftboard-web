"use strict";

var React = require('react');
var LiveNBAPMRProgressBar = require('./live-nba-pmr-progress-bar');

/**
 * One entry within the live history ticker
 */
var LiveNBALineupPlayer = React.createClass({
  propTypes: {
    player: React.PropTypes.object.isRequired
  },

  render: function() {
    var playStatusClass = 'live-lineup-player__play-status play-status--' + this.props.player.playStatus;

    return (
      <li className="live-lineup-player state--is-playing">
        <div className="live-lineup-player__position">{this.props.player.position}</div>
        <div className="live-lineup-player__photo">
          <LiveNBAPMRProgressBar decimalRemaining="0.3" strokeWidth="2" backgroundHex="46495e" hexStart="34B4CC" hexEnd="2871AC" svgWidth="50" />
        </div>
        <div className="live-lineup-player__status"></div>
        <div className="live-lineup-player__points">{this.props.player.points}</div>
        <div className={ playStatusClass }></div>
      </li>
    );
  }
});


module.exports = LiveNBALineupPlayer;
