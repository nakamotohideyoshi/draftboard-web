var React = require('react');
var LineupCardPlayer = require('./lineup-card-player.jsx');
var Tooltip = require('../site/tooltip.jsx');
import CountdownClock from '../site/countdown-clock.jsx'


var LineupCard = React.createClass({

  propTypes: {
    isActive: React.PropTypes.bool,
    onCardClick: React.PropTypes.func.isRequired,
    lineup: React.PropTypes.object.isRequired,
    hoverText: React.PropTypes.string,
    draftGroupInfo: React.PropTypes.object.isRequired,
    fees: React.PropTypes.number,
    entries: React.PropTypes.number
  },


  getDefaultProps: function() {
    return ({
      hoverText: "Select This Lineup",
      draftGroupInfo: {}
    });
  },


  // Toggle the visibility of the tooltip.
  showControls: function() {
    this.refs.lineupCardTip.toggle()
  },


  render: function() {
    var lineup = '';

    if(this.props.isActive) {

      var players = this.props.lineup.players.map(function(player) {
        return (
          <LineupCardPlayer player={player} key={player.player_id} />
        );
      });

      lineup = (
        <div className="cmp-lineup-card">
          <header className="cmp-lineup-card__header" onClick={this.showControls}>
            <h3 className="cmp-lineup-card__title">
              {this.props.lineup.name || 'Untitled Lineup #' + this.props.lineup.id}
            </h3>

            <Tooltip
              additionalClassName="testClass"
              position="top"
              isVisible={false}
              ref="lineupCardTip"
            >
              <span>Edit and stuff in here</span>
            </Tooltip>
          </header>

          <ul>
            {players}
          </ul>

          <footer className="cmp-lineup-card__footer">
            <div className="cmp-lineup-card__fees cmp-lineup-card__footer-section">
              <span className="cmp-lineup-card__footer-title">Fees</span>
              ${this.props.fees}
            </div>

            <div className="cmp-lineup-card__countdown cmp-lineup-card__footer-section">
              <span className="cmp-lineup-card__footer-title">Live In</span>
              <CountdownClock time={this.props.draftGroupInfo.start}/>
            </div>

            <div className="cmp-lineup-card__entries cmp-lineup-card__footer-section">
              <span className="cmp-lineup-card__footer-title">Entries</span>
              {this.props.entries}
            </div>
          </footer>
        </div>
      );
    } else {
      lineup = (
        <div
          className="cmp-lineup-card cmp-lineup-card--collapsed"
          onClick={this.props.onCardClick.bind(null, this.props.lineup)}
        >
          <header className="cmp-lineup-card__header">
            <h3 className="cmp-lineup-card__title">{this.props.lineup.name || 'Untitled Lineup #' + this.props.lineup.id}</h3>
          </header>
          <div className="cmp-lineup-card__select">
            <h4>{this.props.hoverText}</h4>
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
