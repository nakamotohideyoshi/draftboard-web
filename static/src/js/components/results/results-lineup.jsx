import CountdownClock from '../site/countdown-clock';
import { humanizeCurrency } from '../../lib/utils/currency';
import { humanizeFP } from '../../lib/utils/numbers';
import { isTimeInFuture } from '../../lib/utils';
import PlayerPmrHeadshotComponent from '../site/PlayerPmrHeadshotComponent';
import PureRenderMixin from 'react-addons-pure-render-mixin';
import React from 'react';
import ResultsPane from './results-pane';


const ResultsLineup = React.createClass({

  propTypes: {
    isWatchingLive: React.PropTypes.bool,
    id: React.PropTypes.number.isRequired,
    draftGroupId: React.PropTypes.number,
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
      totalBuyin: React.PropTypes.number,
      entries: React.PropTypes.number,
      fees: React.PropTypes.number,
      points: React.PropTypes.number,
      potentialWinnings: React.PropTypes.object,
    }),
    fetchEntryResults: React.PropTypes.func.isRequired,
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

  handleShowContestPane(contestId, entry, isLive) {
    // Don't show contest details for the live lineup view.
    // It's broken and we want to send people to the live section anyway.
    if (!isLive) {
      this.props.fetchEntryResults(entry.id);
      this.setState({
        contestPaneId: contestId,
        renderContestPane: true,
        currentEntry: entry,
      });
    }
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
    const isLive = this.props.hasOwnProperty('liveStats');
    const isUpcoming = isTimeInFuture(this.props.start);
    const isFinished = this.props.hasOwnProperty('stats');

    let totalFP = 0;

    const players = this.props.players.map((player) => {
      let decimalRemaining = 0;
      totalFP += player.fantasy_points;

      // if live, then show progress bar
      if (this.props.isWatchingLive === true && isUpcoming === false) {
        decimalRemaining = player.timeRemaining.decimal;
      }

      let team;
      if (player.player_meta.team) {
        team = (<span className="team">- {player.player_meta.team.alias}</span>);
      }

      let score = humanizeFP(player.fantasy_points);
      if (!isFinished && isUpcoming === true) {
        score = `$${player.salary.toLocaleString('en')}`;
      }

      let scoreClassName = 'score';
      if (score === 0) {
        scoreClassName += ' score-zero';
      }

      return (
        <li key={player.player_id} className="cmp-lineup-card__player">
          <span className="cmp-lineup-card__position">{player.roster_spot}</span>

          <div className="circle">
            <PlayerPmrHeadshotComponent
              colors={['46495e', '36b5cc', '214e9d']}
              decimalRemaining={decimalRemaining}
              modifiers={['results']}
              playerSrid={player.player_meta.srid}
              sport={sport}
              uniquePmrId={`pmr-live-lineup-player-${player.id}`}
              width={28}
            />
          </div>

          <span className="cmp-lineup-card__name-game">
            <span className="name">{player.full_name}</span>
          </span>
          <span className="team">{team}</span>
          <span className={`cmp-lineup-card__emvalue ${scoreClassName}`}>
            <span className="text">
              {score}
            </span>
          </span>
        </li>
      );
    });

    let rightStatTitle = 'PTS';
    if (!isFinished && isUpcoming === true) {
      rightStatTitle = 'Salary';
    }

    let lineupStats = (<div />);
    let popup = (<div />);

    if (isFinished) {
      lineupStats = (
        <footer className="cmp-lineup-card__footer">
          <div className="cmp-lineup-card__footer-section">
            <span className="cmp-lineup-card__footer-title">Won</span>
            <span className="value">
              {humanizeCurrency(this.props.stats.won)}
            </span>
          </div>
          <div className="cmp-lineup-card__footer-section">
            <span className="cmp-lineup-card__footer-title">Entries</span>
            <span className="value">
              {this.props.stats.entries}
            </span>
          </div>
          <div className="cmp-lineup-card__footer-section">
            <span className="cmp-lineup-card__footer-title">PTS</span>
            <span className="value">
              {humanizeFP(totalFP)}
            </span>
          </div>
        </footer>
      );

      popup = (
        <div className="actions-menu-container">
          <ul className="actions">
            <li>
              <div
                className="icon-flip action"
                onClick={this.handleSwitchToContests}
              ></div>
            </li>
          </ul>
        </div>
      );
    } else if (isLive) {
      // if upcoming
      if (isUpcoming === true) {
        lineupStats = (
          <div className="footer-upcoming">
            <div className="item">
              <span className="cmp-lineup-card__footer-title">Live In</span>
              <span className="value">
                <CountdownClock
                  time={ new Date(this.props.start).getTime() }
                />
              </span>
            </div>
            <div className="item">
              <span className="cmp-lineup-card__footer-title">Fees&nbsp;/&nbsp;Entries</span>
              <span className="value">
                <span className="fees">{humanizeCurrency(this.props.liveStats.totalBuyin)}</span>
                &nbsp;/&nbsp;
                {this.props.liveStats.entries}
              </span>
            </div>
          </div>
        );

        let editLineupURL = `/draft/${this.props.draftGroupId}/lineup/${this.props.id}/edit`;
        popup = (
          <div className="actions-menu-container">
            <ul className="actions">
              <li>
                <a className="icon-edit action" href={editLineupURL} />
              </li>

              <li>
                <div
                  className="icon-flip action"
                  onClick={this.handleSwitchToContests}
                ></div>
              </li>
            </ul>
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
                {humanizeFP(this.props.liveStats.points)}
              </span>
            </div>
          </div>
        );

        popup = (
          <div className="actions-menu-container">
            <ul className="actions">
              <li>
                <div
                  className="icon-flip action"
                  onClick={this.handleSwitchToContests}
                ></div>
              </li>
            </ul>
          </div>
        );
      }
    }

    return (
      <div key={`${this.props.id}-lineup`} className="front">
        <header className="cmp-lineup-card__header">
          <h3 className="cmp-lineup-card__title">{this.props.name || 'Your Lineup'}</h3>

          {popup}


        </header>
        <div className="cmp-lineup-card__list-header">
          <span className="cmp-lineup-card__list-header-salary">{rightStatTitle}</span>
        </div>
        <ul className="players">
          {players}
        </ul>
        {lineupStats}
      </div>
    );
  },

  renderContests() {
    const isLive = this.props.hasOwnProperty('liveStats');
    const isUpcoming = this.props.isWatchingLive && isTimeInFuture(this.props.start);

    const entries = this.props.entries.map((entry) => {
      const payout = entry.payout || {};
      const contest = entry.contest || entry;

      if (isUpcoming === true) {
        return (
          <li key={contest.id}
            className="entry"
          >
            <span className="title">{contest.name}</span>
            <span className="prize">{humanizeCurrency(entry.buyin)}</span>
          </li>
        );
      }

      let prizeClassName = 'prize';
      if (!payout.amount || payout.amount === 0) {
        prizeClassName += ' prize-zero';
      }

      return (
        <li key={contest.id}
          className="entry"
          onClick={this.handleShowContestPane.bind(this, contest.id, entry, isLive)}
        >
          <span className="place">{entry.final_rank}</span>
          <span className="title">{contest.name}</span>
          <span className={prizeClassName}>{humanizeCurrency(payout.amount || 0)}</span>
        </li>
      );
    });

    let footer = (<div />);

    if (isLive) {
      footer = (
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
              {humanizeFP(this.props.liveStats.points)}
            </span>
          </div>
        </div>
      );
    }

    return (
      <div key={this.props.id} className="back">
        <header className="cmp-lineup-card__header">
          <h3 className="cmp-lineup-card__title">{this.props.entries.length} Contests</h3>
          <div className="actions-menu-container">
            <ul className="actions">
              <li><div className="icon-flop action" onClick={this.handleSwitchToLineup}></div></li>
            </ul>

          </div>
          <div className="cmp-lineup-card__list-header">
            <span className="cmp-lineup-card__list-header-remove">Pos</span>
            <span className="cmp-lineup-card__list-header-remove">Contest</span>
            <span className="cmp-lineup-card__list-header-remove">Winning</span>
          </div>
        </header>

        <div className="cmp-lineup-card-entries">
          <ul className="entry-list">
            {entries}
          </ul>
        </div>
        {footer}
      </div>
    );
  },

  render() {
    let className = 'cmp-lineup-card flip-container';

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
