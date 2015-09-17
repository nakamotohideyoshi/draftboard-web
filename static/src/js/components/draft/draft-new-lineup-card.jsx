'use strict';

var React = require('react');
var Tooltip = require('../site/tooltip.jsx');
var DraftActions = require('../../actions/draft-actions.js');


/**
 * Lineup creation card on the sidebar of the draft page.
 */
var DraftNewLineupCard = React.createClass({

  propTypes: {
    isActive: React.PropTypes.bool,
    lineup: React.PropTypes.array.isRequired,
    remainingSalary: React.PropTypes.number,
    avgPlayerSalary: React.PropTypes.number
  },


  getDefaultProps: function() {
    return {
        lineup: [],
        rosterSpots: 8,
        remainingSalary: 0,
        avgPlayerSalary: 0
    };
  },


  getInitialState: function() {
    return {
      lineupTitle: 'New Lineup'
    };
  },


  saveLineup: function() {
    DraftActions.saveLineup();
  },


  // Toggle the visibility of the tooltip.
  showControls: function() {
    this.refs.lineupCardTip.toggle();
  },


  render: function() {

    var players = this.props.lineup.map(function(player) {
      if (player.player) {
        return (
          <li className="cmp-lineup-card__player" key={player.player_id}>
            <span className="cmp-lineup-card__position">{player.player.position}</span>
            <span className="cmp-lineup-card__photo">😀</span>
            <span className="cmp-lineup-card__name">
              {player.player.first_name[0]}. {player.player.last_name}
              <span className="cmp-lineup-card__team">- {player.player.team_alias}</span>
            </span>
            <span className="cmp-lineup-card__average">???</span>
          </li>
        );
      } else {
        return (
          <li className="cmp-lineup-card__player" key={player.idx}>
            <span className="cmp-lineup-card__position">{player.name}</span>
            <span className="cmp-lineup-card__photo">👤</span>
            <span className="cmp-lineup-card__name"></span>
            <span className="cmp-lineup-card__average"></span>
          </li>
        );
      }
    });

    return (
      <div className="cmp-lineup-card">
        <header className="cmp-lineup-card__header" onClick={this.showControls}>
          <h3 className="cmp-lineup-card__title">{this.state.lineupTitle}</h3>

          <span className="button--small--outline" onClick={this.saveLineup}>
            Save
            <Tooltip
              position="bottom"
              isVisible={false}
              ref="lineupCardTip"
            >
              <span>You may only continue with a complete lineup.</span>
            </Tooltip>
          </span>
        </header>

        <ul>
          {players}
        </ul>

        <footer className="cmp-lineup-card__footer">
          <div className="cmp-lineup-card__fees cmp-lineup-card__footer-section">
            <span className="cmp-lineup-card__footer-title">Rem. Salary</span>
            ${this.props.remainingSalary.toLocaleString('en')}
          </div>
          <div className="cmp-lineup-card__countdown cmp-lineup-card__footer-section">
            <span className="cmp-lineup-card__footer-title">Avg / Player</span>
            ${this.props.avgPlayerSalary.toLocaleString('en')}
          </div>
        </footer>
      </div>
    );
  }

});


module.exports = DraftNewLineupCard;
