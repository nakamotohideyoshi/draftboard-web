'use strict';

var React = require('react');
var LineupCardPlayer = require('./lineup-card-player.jsx');

var LineupCard = React.createClass({

  propTypes: {
    isActive: React.PropTypes.bool,
    onCardClick: React.PropTypes.func,
    // TODO: Once we have real data coming in, this needs to be removed
    tempId: React.PropTypes.any
  },


  getInitialState: function() {
    return {};
  },


  render: function() {
    var lineup = '';

    if(this.props.isActive) {
      lineup = (
        <div className="cmp-lineup-card">
          <header className="cmp-lineup-card__header">
            <h3 className="cmp-lineup-card__title">Nuggs Stack {this.props.tempId}</h3>
          </header>

          <ul>
            <LineupCardPlayer />
            <LineupCardPlayer />
            <LineupCardPlayer />
            <LineupCardPlayer />
            <LineupCardPlayer />
            <LineupCardPlayer />
            <LineupCardPlayer />
            <LineupCardPlayer />
          </ul>

          <footer className="cmp-lineup-card__footer">
            <div className="cmp-lineup-card__fees cmp-lineup-card__footer-section">
              <span className="cmp-lineup-card__footer-title">Fees</span>
              120
            </div>
            <div className="cmp-lineup-card__countdown cmp-lineup-card__footer-section">
              <span className="cmp-lineup-card__footer-title">Live In</span>
              00:38:48
            </div>
            <div className="cmp-lineup-card__entries cmp-lineup-card__footer-section">
              <span className="cmp-lineup-card__footer-title">Entries</span>
              22
            </div>
          </footer>
        </div>
      );
    } else {
      lineup = (
        <div
          className="cmp-lineup-card cmp-lineup-card--collapsed"
          onClick={this.props.onCardClick.bind(null, this, this.props.tempId)}
        >
          <header className="cmp-lineup-card__header">
            <h3 className="cmp-lineup-card__title">Nuggs Stack {this.props.tempId}</h3>
          </header>
          <div className="cmp-lineup-card__select">
            <h4>Select This Lineup</h4>
          </div>
        </div>
      );
    }

    return (
      lineup
    );
  }

});


module.exports = LineupCard;
