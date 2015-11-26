'use strict';

import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';

const ResultsLineup = React.createClass({

  mixins: [PureRenderMixin],

  propTypes: {
    id: React.PropTypes.number.isRequired,
    name: React.PropTypes.string.isRequired,
    players: React.PropTypes.arrayOf(
      React.PropTypes.shape({
        id: React.PropTypes.number.isRequired,
        name: React.PropTypes.string.isRequired,
        score: React.PropTypes.number.isRequired,
        image: React.PropTypes.string.isRequired,
        position: React.PropTypes.string.isRequired
      })
    ).isRequired,
    stats: React.PropTypes.shape({
      fees: React.PropTypes.string.isRequired,
      won: React.PropTypes.string.isRequired,
      entries: React.PropTypes.number.isRequired
    })
  },

  render() {
    const players = this.props.players.map((player) => {
      return (
        <div key={player.id} className="player">
          <span className="position">{player.position}</span>
          <span className="image">{player.image}</span>
          <span className="name">{player.name}</span>
          <span className="score">{player.score}</span>
        </div>
      );
    });

    return (
      <div key={this.props.id} className="lineup">
        <div className="header">
          {this.props.name}
        </div>
        <div className="list">
          {players}
        </div>
        <div className="footer">
          <div className="item">
            <span className="title">Fees</span>
            <span className="value">
              {this.props.stats.fees}
            </span>
          </div>
          <div className="item">
            <span className="title">Won</span>
            <span className="value">
              {this.props.stats.won}
            </span>
          </div>
          <div className="item">
            <span className="title">Entries</span>
            <span className="value">
              {this.props.stats.entries}
            </span>
          </div>
        </div>
        </div>
    );
  }

});


export default ResultsLineup;
