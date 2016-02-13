import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';
import ResultsPane from './results-pane.jsx';

const ResultsLineup = React.createClass({

  propTypes: {
    id: React.PropTypes.number.isRequired,
    name: React.PropTypes.string,
    players: React.PropTypes.arrayOf(
      React.PropTypes.shape({
        player_id: React.PropTypes.number.isRequired,
        full_name: React.PropTypes.string.isRequired,
        fppg: React.PropTypes.number.isRequired,
        roster_spot: React.PropTypes.string.isRequired,
      })
    ).isRequired,
    entries: React.PropTypes.array.isRequired,
    stats: React.PropTypes.shape({
      buyin: React.PropTypes.number.isRequired,
      won: React.PropTypes.number.isRequired,
      entries: React.PropTypes.number.isRequired,
    }),
  },

  mixins: [PureRenderMixin],

  getInitialState() {
    return {
      renderLineup: true,
      renderContestPane: false,
    };
  },

  handleSwitchToLineup() {
    this.setState({ renderLineup: true });
  },

  handleSwitchToContests() {
    this.setState({ renderLineup: false });
  },

  handleShowContestPane() {
    this.setState({ renderContestPane: true });
  },

  handleHideContestPane() {
    this.setState({ renderContestPane: false });
  },

  numToPlace(number) {
    let place = number;

    switch (number) {
      case 1: place += 'st'; break;
      case 2: place += 'nd'; break;
      case 3: place += 'rd'; break;
      default: place += 'th';
    }

    return place;
  },

  renderLineup() {
    const players = this.props.players.map((player) => (
      <div key={player.id} className="player">
        <span className="position">{player.roster_spot}</span>
        <span className="image"
          style={{
            // TODO:
            // backgroundImage: "url('" + player.image + "')"
          }}
        >
        </span>
        <span className="name">{player.full_name}</span>
        <span className="score">{player.fppg.toFixed(2)}</span>
      </div>
    ));

    return (
      <div key={`${this.props.id}-lineup`} className="lineup">
        <div className="header">
          {this.props.name || 'Your Lineup'}

          <div className="to-contests" onClick={this.handleSwitchToContests}>
            <span>
              Contests <div className="arrow-right">&gt;</div>
            </span>
          </div>
        </div>
        <div className="list">
          {players}
        </div>
        <div className="footer">
          <div className="item">
            <span className="title">Fees</span>
            <span className="value">
              {this.props.stats.buyin.toFixed(2)}
            </span>
          </div>
          <div className="item">
            <span className="title">Won</span>
            <span className="value">
              {this.props.stats.won.toFixed(2)}
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
  },

  renderContests() {
    const entries = this.props.entries.map((entry) => {
      const contest = entry.contest;

      return (
        <div key={contest.id}
          className="contest"
          onClick={this.handleShowContestPane}
        >
          <div className="title">{contest.name}</div>
          <div className="prize">${entry.payout.amount.toFixed(2)}</div>
          <div className="place">{this.numToPlace(entry.final_rank)}</div>
        </div>
      );
    });

    return (
      <div key={this.props.id} className="contests">
        <div className="header">
          {this.props.entries.length} Contests

          <div className="to-lineup" onClick={this.handleSwitchToLineup}>
            Lineup <div className="arrow-right">&gt;</div>
          </div>
        </div>
        <div className="list">
          {entries}
        </div>
      </div>
    );
  },

  render() {
    let className = 'flip-container';
    if (!this.state.renderLineup) className += ' hover';
    if (this.state.renderContestPane) className += ' shown-contest-pane';

    return (
      <div className={className}>
        <div className="flipper">
          {this.renderLineup()}
          {this.renderContests()}
        </div>
        <ResultsPane onHide={this.handleHideContestPane} />
      </div>
    );
  },
});


export default ResultsLineup;
