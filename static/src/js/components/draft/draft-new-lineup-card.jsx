'use strict';

var React = require('react');
var Tooltip = require('../site/tooltip.jsx');
var DraftActions = require('../../actions/draft-actions.js');
var DraftNewLineupCardTitle = require('./draft-new-lineup-card-title.jsx');

/**
 * Lineup creation card on the sidebar of the draft page.
 */
var DraftNewLineupCard = React.createClass({

  propTypes: {
    isActive: React.PropTypes.bool,
    lineup: React.PropTypes.array.isRequired,
    remainingSalary: React.PropTypes.number,
    avgPlayerSalary: React.PropTypes.number,
    errorMessage: React.PropTypes.string
  },


  getDefaultProps: function() {
    return {
        lineup: [],
        remainingSalary: 0,
        avgPlayerSalary: 0,
        errorMessage: ''
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


  setLineupTitle: function(title) {
    DraftActions.setLineupTitle(title);
  },

  // Toggle the visibility of the tooltip.
  showControls: function() {
    // this.refs.lineupCardTip.toggle();
  },


  render: function() {
    var showError = (this.props.errorMessage === '')? false : true;

    var players = this.props.lineup.map(function(player) {
      if (player.player) {
        var names = player.player.name.split(' ');

        return (
          <li className="cmp-lineup-card__player" key={player.idx}>
            <span className="cmp-lineup-card__position">{player.name}</span>
            <span className="cmp-lineup-card__photo">😀</span>
            <span className="cmp-lineup-card__name">
              {names[0][0]}. {names[names.length - 1]}
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
      <div className="cmp-lineup-card cmp-lineup-card--new">
        <header className="cmp-lineup-card__header clearfix" onClick={this.showControls}>
          <DraftNewLineupCardTitle
            title={this.state.lineupTitle}
            setTitle={this.setLineupTitle}
          />

          <span
            className="cmp-lineup-card__save button--mini--outline button--gradient-outline"
            onClick={this.saveLineup}>
            Save
          </span>

          <Tooltip
            position="bottom"
            isVisible={showError}
            ref="lineupCardTip">
            <span>{this.props.errorMessage}</span>
          </Tooltip>

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
