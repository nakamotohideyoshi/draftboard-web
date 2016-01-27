var React = require('react');
var Tooltip = require('../site/tooltip.jsx');
var DraftNewLineupCardTitle = require('./draft-new-lineup-card-title.jsx');
var DraftNewLineupCardPlayer = require('./draft-new-lineup-card-player.jsx');
var defaultLineupTitle = 'New Lineup'


/**
 * Lineup creation card on the sidebar of the draft page.
 */
var DraftNewLineupCard = React.createClass({

  propTypes: {
    isActive: React.PropTypes.bool,
    lineup: React.PropTypes.array.isRequired,
    lineupTitle: React.PropTypes.string,
    removePlayer: React.PropTypes.func.isRequired,
    remainingSalary: React.PropTypes.number,
    avgRemainingPlayerSalary: React.PropTypes.number,
    errorMessage: React.PropTypes.string,
    saveLineup: React.PropTypes.func,
    handlePlayerClick: React.PropTypes.func
  },


  getDefaultProps: function() {
    return {
        lineup: [],
        remainingSalary: 0,
        avgRemainingPlayerSalary: 0,
        errorMessage: ''
    };
  },


  getInitialState: function() {
    return {
      lineupTitle: defaultLineupTitle
    };
  },


  componentWillReceiveProps: function(nextProps) {
    if (nextProps.lineupTitle) {
      this.setState({lineupTitle: nextProps.lineupTitle})
    }
  },

  saveLineup: function() {
    var title = this.state.lineupTitle
    if (title === defaultLineupTitle) {
      title = ''
    }

    this.props.saveLineup(title)
  },


  setTitle: function(title) {
    this.state.lineupTitle = title
  },


  // Toggle the visibility of the tooltip.
  showControls: function() {
    // this.refs.lineupCardTip.toggle();
  },


  render: function() {
    var showError = (!this.props.errorMessage)? false : true;

    var players = this.props.lineup.map(function(player) {
      return (
        <DraftNewLineupCardPlayer
          player={player}
          key={player.idx}
          removePlayer={this.props.removePlayer}
          onPlayerClick={this.props.handlePlayerClick}
        />
      );
    }.bind(this));

    return (
      <div className="cmp-lineup-card cmp-lineup-card--new">
        <header className="cmp-lineup-card__header clearfix" onClick={this.showControls}>
          <DraftNewLineupCardTitle
            title={this.state.lineupTitle}
            setTitle={this.setTitle}
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
          <span className="cmp-lineup-card__list-header-average">Avg</span>
        </div>

        <ul className="players">
          {players}
        </ul>

        <footer className="cmp-lineup-card__footer">
          <div className="cmp-lineup-card__fees cmp-lineup-card__footer-section">
            <span className="cmp-lineup-card__footer-title">Rem. Salary</span>
            ${this.props.remainingSalary.toLocaleString('en')}
          </div>
          <div className="cmp-lineup-card__countdown cmp-lineup-card__footer-section">
            <span className="cmp-lineup-card__footer-title">Avg. Salary Rem.</span>
            ${this.props.avgRemainingPlayerSalary.toLocaleString('en')}
          </div>
        </footer>
      </div>
    );
  }

});


module.exports = DraftNewLineupCard;
