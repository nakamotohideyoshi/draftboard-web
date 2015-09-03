'use strict';

var React = require('react');


var LineupCardPlayer = React.createClass({

  propTypes: {
    player: React.PropTypes.object.isRequired
  },


  // getInitialState: function() {
  //   return {};
  // },


  render: function() {
    return (
      <li className="cmp-lineup-card__player">
        <span className="cmp-lineup-card__position">NEEDED</span>
        <span className="cmp-lineup-card__photo">😀</span>
        <span className="cmp-lineup-card__name">{this.props.player.full_name}</span>
        <span className="cmp-lineup-card__average">NEEDED</span>
      </li>
    );
  }
});


module.exports = LineupCardPlayer;
