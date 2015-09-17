'use strict';

var React = require('react');


var LineupCardPlayer = React.createClass({

  propTypes: {
    player: React.PropTypes.object.isRequired
  },

  render: function() {
    return (
      <li className="cmp-lineup-card__player">
        <span className="cmp-lineup-card__position">{this.props.player.roster_spot}</span>
        <span className="cmp-lineup-card__photo">😀</span>
        <span className="cmp-lineup-card__name">
          {this.props.player.player_meta.first_name[0]}.
          {this.props.player.player_meta.last_name}
          <span className="cmp-lineup-card__team">
            - {this.props.player.player_meta.team.alias}
          </span>
        </span>
        <span className="cmp-lineup-card__average">XX</span>
      </li>
    );
  }

});


module.exports = LineupCardPlayer;
