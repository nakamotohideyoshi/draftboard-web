"use strict";

var React = require('react');

/**
 * One entry within the live history ticker
 */
var LiveHistoryEvent = React.createClass({
  propTypes: {
    event: React.PropTypes.object.isRequired
  },

  render: function() {
    var points = this.props.event.points;

    if (points > 0) {
      points = '+' + points;
    }

    return (
      <div className="live-history__event live-history-event">
        <div className="live-history-event__inner">
          <h3 className="live-history-event__player-name">
            {this.props.event.playerName}
            <span className="live-history-event__points">{points}</span>
          </h3>
          <div className="live-history-event__event-name">{this.props.event.action}</div>
        </div>
      </div>
    );
  }
});


module.exports = LiveHistoryEvent;
