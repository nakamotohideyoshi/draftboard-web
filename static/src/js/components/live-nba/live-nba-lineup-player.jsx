"use strict";

var React = require('react');

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
        <div className="live-lineup-player__photo"></div>
        <div className="live-lineup-player__status"></div>
        <div className="live-lineup-player__points">{this.props.player.points}</div>
        <div className={ playStatusClass }></div>
      </li>
    );
  }
});


module.exports = LiveNBALineupPlayer;
