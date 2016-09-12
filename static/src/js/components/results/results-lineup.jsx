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
    dateIsToday: React.PropTypes.bool,
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
    const isLive = this.props.hasOwnProperty('liveStats');
    const isUpcoming = isTimeInFuture(this.props.start);
    const isFinished = this.props.hasOwnProperty('stats');

    const players = this.props.players.map((player) => {
      let decimalRemaining = 0;

      // if live, then show progress bar
      if (this.props.dateIsToday === true && isUpcoming === false) {
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
          {team}
          <span className={scoreClassName}>
            {score}
          </span>
        </div>
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
        <div className="footer">
          <div className="item">
            <span className="title">Won</span>
            <span className="value">
              {humanizeCurrency(this.props.stats.won)}
            </span>
          </div>
          <div className="item">
            <span className="title">PTS</span>
            <span className="value">
              {this.props.stats.entries}
            </span>
          </div>
        </div>
      );

      popup = (
        <div className="to-contests--popup">
          <div className="triangle-border"></div>
          <div className="triangle"></div>
          <div className="item switch-to-contests" onClick={this.handleSwitchToContests}>
            View Entered Contests
          </div>
        </div>
      );
    } else if (isLive) {
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
                <span className="fees">{humanizeCurrency(this.props.liveStats.totalBuyin)}</span>
                &nbsp;/&nbsp;
                {this.props.liveStats.entries}
              </span>
            </div>
          </div>
        );

        let editLineupURL = `/draft/${this.props.draftGroupId}/lineup/${this.props.id}/edit`;
        let copyLineupURL = `/draft/${this.props.draftGroupId}/lineup/${this.props.id}/copy`;
        popup = (
          <div className="to-contests--popup">
            <div className="triangle-border"></div>
            <div className="triangle"></div>
            <div className="item">
              <a href={editLineupURL}>Edit Lineup</a>
            </div>
            <div className="item">
              <a href={copyLineupURL}>New Lineup via Copy</a>
            </div>
            <div className="item switch-to-contests" onClick={this.handleSwitchToContests}>
              View Entered Contests
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
                {humanizeFP(this.props.liveStats.points)}
              </span>
            </div>
          </div>
        );

        popup = (
          <div className="to-contests--popup">
            <div className="triangle-border"></div>
            <div className="triangle"></div>
            <div className="item switch-to-contests" onClick={this.handleSwitchToContests}>
              View Entered Contests
            </div>
          </div>
        );
      }
    }

    return (
      <div key={`${this.props.id}-lineup`} className="lineup">
        <div className="header">
          {this.props.name || 'Your Lineup'}

          <div className="to-contests">
            <span>
              …
            </span>
            {popup}
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
    const isLive = this.props.hasOwnProperty('liveStats');
    const isUpcoming = this.props.dateIsToday && isTimeInFuture(this.props.start);

    const entries = this.props.entries.map((entry) => {
      const payout = entry.payout || {};
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

      let prizeClassName = 'prize';
      if (!payout.amount || payout.amount === 0) {
        prizeClassName += ' prize-zero';
      }

      return (
        <div key={contest.id}
          className="contest"
          onClick={this.handleShowContestPane.bind(this, contest.id, entry)}
        >
          <div className="place">{entry.final_rank}</div>
          <div className="title">{contest.name}</div>
          <div className={prizeClassName}>{humanizeCurrency(payout.amount || 0)}</div>
        </div>
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
      <div key={this.props.id} className="contests">
        <div className="header">
          {this.props.entries.length} Contests

          <div className="to-lineup" onClick={this.handleSwitchToLineup}>
          </div>
          <div className="titles">
            <div className="titles--pos">Pos</div>
            <div className="titles--contest">Contest</div>
            <div className="titles--winning">Winning</div>
          </div>
        </div>
        <div className="list">
          {entries}
        </div>
        {footer}
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
