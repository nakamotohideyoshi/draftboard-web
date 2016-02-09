import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';
import ResultsPane from './results-pane.jsx';

const ResultsLineup = React.createClass({

  propTypes: {
    id: React.PropTypes.number.isRequired,
    name: React.PropTypes.string.isRequired,
    players: React.PropTypes.arrayOf(
      React.PropTypes.shape({
        id: React.PropTypes.number.isRequired,
        name: React.PropTypes.string.isRequired,
        score: React.PropTypes.number.isRequired,
        image: React.PropTypes.string.isRequired,
        position: React.PropTypes.string.isRequired,
      })
    ).isRequired,
    contests: React.PropTypes.arrayOf(
      React.PropTypes.shape({
        id: React.PropTypes.number.isRequired,
        factor: React.PropTypes.number.isRequired,
        title: React.PropTypes.string.isRequired,
        place: React.PropTypes.number.isRequired,
        prize: React.PropTypes.string.isRequired,
      })
    ).isRequired,
    stats: React.PropTypes.shape({
      fees: React.PropTypes.string.isRequired,
      won: React.PropTypes.string.isRequired,
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
        <span className="position">{player.position}</span>
        <span className="image"
          style={{
            // TODO:
            // backgroundImage: "url('" + player.image + "')"
          }}
        >
        </span>
        <span className="name">{player.name}</span>
        <span className="score">{player.score}</span>
      </div>
    ));

    return (
      <div key={`${this.props.id}-lineup`} className="lineup">
        <div className="header">
          {this.props.name}

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
  },

  renderContests() {
    const contests = this.props.contests.map((c) => (
      <div key={c.id}
        className="contest"
        onClick={this.handleShowContestPane}
      >
        <div className="factor">{`${c.factor}X`}</div>
        <div className="title">{c.title}</div>
        <div className="place">{this.numToPlace(c.place)}</div>
        <div className="prize">{c.prize}</div>
      </div>
    ));

    return (
      <div key={this.props.id} className="contests">
        <div className="header">
          {this.props.contests.length} Contests

          <div className="to-lineup" onClick={this.handleSwitchToLineup}>
            Lineup <div className="arrow-right">&gt;</div>
          </div>
        </div>
        <div className="list">
          {contests}
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
