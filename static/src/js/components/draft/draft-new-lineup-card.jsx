var React = require('react');
var Tooltip = require('../site/tooltip.jsx');
// var DraftActions = require('../../actions/draft-actions.js');
var DraftNewLineupCardTitle = require('./draft-new-lineup-card-title.jsx');
var DraftNewLineupCardPlayer = require('./draft-new-lineup-card-player.jsx');


/**
 * Lineup creation card on the sidebar of the draft page.
 */
var DraftNewLineupCard = React.createClass({

  propTypes: {
    isActive: React.PropTypes.bool,
    lineup: React.PropTypes.array.isRequired,
    removePlayer: React.PropTypes.func.isRequired,
    remainingSalary: React.PropTypes.number,
    avgPlayerSalary: React.PropTypes.number,
    errorMessage: React.PropTypes.string,
    saveLineup: React.PropTypes.func
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
    this.props.saveLineup()
  },


  setLineupTitle: function(title) {
    // DraftActions.setLineupTitle(title);
  },


  // Toggle the visibility of the tooltip.
  showControls: function() {
    // this.refs.lineupCardTip.toggle();
  },


  render: function() {
    var showError = (this.props.errorMessage === '')? false : true;

    var players = this.props.lineup.map(function(player) {
      return (
        <DraftNewLineupCardPlayer
          player={player}
          key={player.idx}
          removePlayer={this.props.removePlayer}
        />
      );
    }.bind(this));

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

        <div className="cmp-lineup-card__list-header">
          <span className="cmp-lineup-card__list-header-average">avg</span>
        </div>

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
