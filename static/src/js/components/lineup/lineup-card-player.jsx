import React from 'react';
import { roundUpToDecimalPlace } from '../../lib/utils.js';


const LineupCardPlayer = React.createClass({

  propTypes: {
    player: React.PropTypes.object.isRequired,
  },

  render() {
    return (
      <li className="cmp-lineup-card__player">
        <span className="cmp-lineup-card__position">{this.props.player.roster_spot}</span>
        <span className="cmp-lineup-card__photo">
          <img src="/static/src/img/temp/PAM_90212.png" width="auto" height="35px" />
        </span>
        <span className="cmp-lineup-card__name">
          {this.props.player.player_meta.first_name[0]}.
          {this.props.player.player_meta.last_name}
          <span className="cmp-lineup-card__team">
            - {this.props.player.player_meta.team.alias}
          </span>
        </span>
        <span className="cmp-lineup-card__average">{roundUpToDecimalPlace(this.props.player.fppg, 1)}</span>
      </li>
    );
  },

});


module.exports = LineupCardPlayer;
