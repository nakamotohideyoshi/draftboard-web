import CountdownClock from '../site/countdown-clock';
import { humanizeCurrency } from '../../lib/utils/currency';
import { isTimeInFuture } from '../../lib/utils';
import PlayerPmrHeadshotComponent from '../site/PlayerPmrHeadshotComponent';
import PureRenderMixin from 'react-addons-pure-render-mixin';
import React from 'react';
import ResultsPane from './results-pane';

const ResultsLineup = React.createClass({

  propTypes: {
    dateIsToday: React.PropTypes.bool,
    id: React.PropTypes.number.isRequired,
    name: React.PropTypes.string,
    sport: React.PropTypes.string.isRequired,
    players: React.PropTypes.arrayOf(
      React.PropTypes.shape({
        player_id: React.PropTypes.number.isRequired,
        full_name: React.PropTypes.string.isRequired,
        fantasy_points: React.PropTypes.number.isRequired,
        roster_spot: React.PropTypes.string.isRequired,
        // only needed for live
        timeRemaining: React.PropTypes.object,
      })
    ).isRequired,
    entries: React.PropTypes.array.isRequired,
    stats: React.PropTypes.shape({
      buyin: React.PropTypes.number,
      won: React.PropTypes.number,
      entries: React.PropTypes.number,
    }),
    start: React.PropTypes.string,
    liveStats: React.PropTypes.shape({
      entries: React.PropTypes.number,
      fees: React.PropTypes.number,
      points: React.PropTypes.number,
      potentialWinnings: React.PropTypes.object,
    }),
  },

  mixins: [PureRenderMixin],

  getInitialState() {
    return {
      renderLineup: true,
      renderContestPane: false,
      contestPaneId: null,
      currentEntry: {},
    };
  },

  handleSwitchToLineup() {
    this.setState({ renderLineup: true });
  },

  handleSwitchToContests() {
    this.setState({ renderLineup: false });
  },

  handleShowContestPane(contestId, entry) {
    this.setState({
      contestPaneId: contestId,
      renderContestPane: true,
      currentEntry: entry,
    });
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
    const { sport } = this.props;
    const isUpcoming = isTimeInFuture(this.props.start);

    const players = this.props.players.map((player) => {
      let decimalRemaining = 0;

      // if live, then show progress bar
      if (this.props.dateIsToday === true && isUpcoming === false) {
        decimalRemaining = player.timeRemaining.decimal;
      }

      return (
        <div key={player.player_id} className="player">
          <span className="position">{player.roster_spot}</span>

          <div className="circle">
            <PlayerPmrHeadshotComponent
              colors={['46495e', '36b5cc', '214e9d']}
              decimalRemaining={decimalRemaining}
              modifiers={['results']}
              playerSrid={player.player_meta.srid}
              sport={sport}
              uniquePmrId={`pmr-live-lineup-player-${player.id}`}
              width={32}
            />
          </div>

          <span className="name">{player.full_name}</span>
          <span className="score">{player.fantasy_points}</span>
        </div>
      );
    });

    let rightStatTitle = 'PTS';
    if (isUpcoming === true) {
      rightStatTitle = 'AVG';
    }

    let lineupStats = (<div />);

    if (this.props.hasOwnProperty('stats')) {
      lineupStats = (
        <div className="footer">
          <div className="item">
            <span className="title">Fees</span>
            <span className="value">
              {humanizeCurrency(this.props.stats.buyin)}
            </span>
          </div>
          <div className="item">
            <span className="title">Won</span>
            <span className="value">
              {humanizeCurrency(this.props.stats.won)}
            </span>
          </div>
          <div className="item">
            <span className="title">Entries</span>
            <span className="value">
              {this.props.stats.entries}
            </span>
          </div>
        </div>
      );
    } else if (this.props.hasOwnProperty('liveStats')) {
      // if upcoming
      if (isUpcoming === true) {
        lineupStats = (
          <div className="footer-upcoming">
            <div className="item">
              <span className="title">Live In</span>
              <span className="value">
                <CountdownClock
                  time={ new Date(this.props.start).getTime() }
                />
              </span>
            </div>
            <div className="item">
              <span className="title">Fees&nbsp;/&nbsp;Entries</span>
              <span className="value">
                <span className="fees">{humanizeCurrency(this.props.liveStats.fees)}</span>
                &nbsp;/&nbsp;
                {this.props.liveStats.entries}
              </span>
            </div>
          </div>
        );

      // otherwise it's live
      } else {
        lineupStats = (
          <div className="footer-live">
            <a className="watch-live" target="_blank" href={`/live/${this.props.sport}/lineups/${this.props.id}/`}>
              Watch Live
            </a>
            <div className="item">
              <span className="title">Winning</span>
              <span className="value">
                {humanizeCurrency(this.props.liveStats.potentialWinnings.amount)}
              </span>
            </div>
            <div className="item">
              <span className="title">Pts</span>
              <span className="value">
                {this.props.liveStats.points}
              </span>
            </div>
          </div>
        );
      }
    }

    return (
      <div key={`${this.props.id}-lineup`} className="lineup">
        <div className="header">
          {this.props.name || 'Your Lineup'}

          <div className="to-contests" onClick={this.handleSwitchToContests}>
            <span>
              Contests <div className="arrow-right">&gt;</div>
            </span>
          </div>

          <div className="right-stat-title">
            {rightStatTitle}
          </div>
        </div>
        <div className="list">
          {players}
        </div>
        {lineupStats}
      </div>
    );
  },

  renderContests() {
    const isUpcoming = this.props.dateIsToday && isTimeInFuture(this.props.start);

    const entries = this.props.entries.map((entry) => {
      const contest = entry.contest || entry;

      if (isUpcoming === true) {
        return (
          <div key={contest.id}
            className="contest"
          >
            <div className="title">{contest.name}</div>
            <div className="prize">{humanizeCurrency(entry.buyin)}</div>
          </div>
        );
      }

      return (
        <div key={contest.id}
          className="contest"
          onClick={this.handleShowContestPane.bind(this, contest.id, entry)}
        >
          <div className="title">{contest.name}</div>
          <div className="prize">{humanizeCurrency(entry.payout.amount)}</div>
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
    if (this.state.renderContestPane) {
      className += ' shown-contest-pane';
    }

    return (
      <div className={className}>
        <div className="flipper">
          {this.renderLineup()}
          {this.renderContests()}
        </div>
        <ResultsPane
          contestId={this.state.contestPaneId}
          entry={this.state.currentEntry}
          onHide={this.handleHideContestPane}
          numToPlace={this.numToPlace}
          sport={this.props.sport}
        />
      </div>
    );
  },
});


export default ResultsLineup;
