'use strict';

var React = require('react');


/**
 * An individual player row in the new lineup card in the draft section sidebar
 */
var DraftNewLineupCardPlayer = React.createClass({

  propTypes: {
    // A player row object.
    player: React.PropTypes.object.isRequired,
    // What happens when the delete button is clicked.
    removePlayer: React.PropTypes.func.isRequired
  },


  render: function() {
    if (this.props.player.player) {
      var names = this.props.player.player.name.split(' ');

      return (
        <li className="cmp-lineup-card__player occupied" key={this.props.player.idx}>
          <span className="cmp-lineup-card__position">{this.props.player.name}</span>
          <span className="cmp-lineup-card__photo">😀</span>
          <span className="cmp-lineup-card__name">
            {names[0][0]}. {names[names.length - 1]}
            <span className="cmp-lineup-card__team">- {this.props.player.player.team_alias}</span>
          </span>
          <span className="cmp-lineup-card__average">${this.props.player.player.salary.toLocaleString('en')}</span>
          <span
            className="cmp-lineup-card__delete"
            onClick={this.props.removePlayer.bind(null, this.props.player.player.player_id)}
          >
            <div className="icon"></div>
          </span>
        </li>
      );
    } else {
      return (
        <li className="cmp-lineup-card__player vacant" key={this.props.player.idx}>
          <span className="cmp-lineup-card__position">{this.props.player.name}</span>
          <span className="cmp-lineup-card__photo-empty"><span className="photo"></span></span>
          <span className="cmp-lineup-card__name">&nbsp;</span>
          <span className="cmp-lineup-card__average">&nbsp;</span>
        </li>
      );
    }

  }

});


module.exports = DraftNewLineupCardPlayer;
