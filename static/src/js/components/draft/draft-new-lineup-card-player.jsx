import React from 'react';
import { roundUpToDecimalPlace } from '../../lib/utils.js';


/**
 * An individual player row in the new lineup card in the draft section sidebar
 */
const DraftNewLineupCardPlayer = React.createClass({

  propTypes: {
    // A player row object.
    player: React.PropTypes.object.isRequired,
    // What happens when the delete button is clicked.
    removePlayer: React.PropTypes.func.isRequired,
    onPlayerClick: React.PropTypes.func,
  },


  render() {
    if (this.props.player.player) {
      const names = this.props.player.player.name.split(' ');

      return (
        <li className="cmp-lineup-card__player occupied" key={this.props.player.idx}>
          <span className="cmp-lineup-card__position">{this.props.player.name}</span>
          <span className="cmp-lineup-card__photo">
            <img src="/static/src/img/temp/PAM_90212.png" width="auto" height="35px" />
          </span>

          <span
            className="cmp-lineup-card__name-salary"
            onClick={this.props.onPlayerClick.bind(null, this.props.player.player.player_id)}
          >
            <span className="name">
              {names[0][0]}. {names[names.length - 1]}
              <span className="cmp-lineup-card__team">- {this.props.player.player.team_alias}</span>
            </span>
            <span className="salary">${this.props.player.player.salary.toLocaleString('en')}</span>
          </span>

          <span className="cmp-lineup-card__average">
            {roundUpToDecimalPlace(this.props.player.player.fppg, 1)}
          </span>

          <span
            className="cmp-lineup-card__delete"
            onClick={this.props.removePlayer.bind(null, this.props.player.player.player_id)}
          >
            <div className="icon"></div>
          </span>
        </li>
      );
    }

    return (
      <li className="cmp-lineup-card__player vacant" key={this.props.player.idx}>
        <span className="cmp-lineup-card__position">{this.props.player.name}</span>
        <span className="cmp-lineup-card__photo-empty"><span className="photo"></span></span>
        <span className="cmp-lineup-card__name">&nbsp;</span>
        <span className="cmp-lineup-card__average">&nbsp;</span>
      </li>
    );
  },

});


module.exports = DraftNewLineupCardPlayer;
