import { humanizeCurrency } from '../../lib/utils/currency';
import { humanizeFP } from '../../lib/utils/numbers';
import { isTimeInFuture } from '../../lib/utils';
import PlayerPmrHeadshotComponent from '../site/PlayerPmrHeadshotComponent';
import PureRenderMixin from 'react-addons-pure-render-mixin';
import React from 'react';
import ResultsPane from './results-pane';
import LiveContestDetailPane from './live-contest-detail-pane';
import CardFooter from '../card/CardFooter';
import PlayerStats from '../card/PlayerStats';
import CountdownClock from '../site/countdown-clock';
import log from '../../lib/logging';


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
    fetchContestResults: React.PropTypes.func.isRequired,
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
    log.info('is clicking?');
    if (!isLive) {
      this.props.fetchContestResults(contestId);
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
  playerStatsBlackList(stat) {
    // this api is ridiculous
    // so much repeated values that already
    // exist in the parent
    // we need to seriously think about using graphQL
    const blacklist = [
      'created',
      'updated',
      'srid_game',
      'srid_player',
      'player_id',
      'player_type',
      'game_type',
      'game_id',
      'position',
      'fantasy_points',
    ];
    return blacklist.indexOf(stat) !== -1;
  },
  buildPlayerStat(player) {
    const stats = [];
    if (player.player_stats.length) {
      for (let i = 0; i < player.player_stats.length; i++) {
        for (const stat in player.player_stats[i]) {
          if (player.player_stats[i].hasOwnProperty(stat)) {
            // if not in blacklist push
            if (!this.playerStatsBlackList(stat)) {
              const statobj = {};
              statobj[stat] = player.player_stats[i][stat];
              stats.push(statobj);
            }
          }
        }
      }
    }
    return (<PlayerStats player_stats={stats} />);
  },
  renderLineup() {
    const { sport } = this.props;
    // const isLive = this.props.hasOwnProperty('liveStats');
    const isUpcoming = isTimeInFuture(this.props.start);
    const isFinished = this.props.hasOwnProperty('stats');
    log.info(isFinished);
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
        team = (<span className="team">{`${player.player_meta.team.alias}`}</span>);
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


          <PlayerPmrHeadshotComponent
            colors={['46495e', '36b5cc', '214e9d']}
            decimalRemaining={decimalRemaining}
            modifiers={['results']}
            playerSrid={player.player_meta.srid}
            sport={sport}
            uniquePmrId={`pmr-live-lineup-player-${player.id}`}
            width={28}
          />

          <span className="cmp-lineup-card__name-game">
            <span className="name">{player.full_name}</span>
          </span>
          <span className="team">{team}</span>
          <span className={`cmp-lineup-card__emvalue ${scoreClassName}`}>
            <span className="text">
              {score}
            </span>
          </span>
          {this.buildPlayerStat(player)}
        </li>
      );
    });

    let rightStatTitle = 'PTS';
    if (!isFinished && isUpcoming === true) {
      rightStatTitle = 'Salary';
    }
    const isLive = this.props.hasOwnProperty('liveStats');
    let lineupStats = (<div />);
    let popup = (<div />);

    // Figure out what the lineup footer should be (live vs finished)
    //
    // Is this lineup finished? If not it is a live lineup.
    if (isFinished) {
      lineupStats = (
        <CardFooter
          entries={this.props.stats.entries}
          won={humanizeCurrency(this.props.stats.won)}
          points={humanizeFP(totalFP)}
        />
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
        const humanizecur = humanizeCurrency(this.props.liveStats.totalBuyin);
        lineupStats = (
          <CardFooter
            start={
              <CountdownClock
                time={ new Date(this.props.start).getTime() }
              />
            }
            feesentries={`${humanizecur}</span>&nbsp;/&nbsp;
${this.props.liveStats.entries}`}
          />

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
          <CardFooter
            winning={humanizeCurrency(this.props.liveStats.potentialWinnings.amount)}
            points={humanizeFP(this.props.liveStats.points)}
          >
            <a className="watch-live" href={`/live/${this.props.sport}/lineups/${this.props.id}/`}>
              Watch Live
            </a>
          </CardFooter>
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

    // Return the lineup card with the proper footer.
    return (
      <div key={`${this.props.id}-lineup`} className="front">
        <header className="cmp-lineup-card__header">
          <h3 className="cmp-lineup-card__title">
            <div className={`cmp-sport-icon icon-${this.props.sport}`}></div>
            {this.props.name || 'Your Lineup'}
          </h3>

          {popup}

          <div className="cmp-lineup-card__list-header">
            <span className="cmp-lineup-card__list-header-salary">{rightStatTitle}</span>
          </div>
        </header>

        <ul className="players">
          {players}
        </ul>
        {lineupStats}
      </div>
    );
  },

  renderContests() {
    // const isLive = true;
    const isLive = this.props.hasOwnProperty('liveStats');

    // const isUpcoming = true
    // const isUpcoming = isTimeInFuture(this.props.start);

    const entries = this.props.entries.map((entry) => {
      const payout = entry.payout || {};
      const contest = entry.contest || entry;
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
    let totalFP = 0;

    for (let i = 0; i < this.props.players.length; i++) {
      totalFP += this.props.players[i].fantasy_points;
    }
    if (isLive) {
      footer = (
        <CardFooter
          winning={humanizeCurrency(this.props.liveStats.potentialWinnings.amount)}
          pts={humanizeFP(this.props.liveStats.points)}
        >
          <a className="watch-live" href={`/live/${this.props.sport}/lineups/${this.props.id}/`}>
            Watch Live
          </a>
        </CardFooter>
      );
    } else {
      footer = (
        <CardFooter
          entries={this.props.stats.entries}
          won={humanizeCurrency(this.props.stats.won)}
          points={humanizeFP(totalFP)}
        />
      );
    }

    return (
      <div key={this.props.id} className="back">
        <header className="cmp-lineup-card__header">
          <h3 className="cmp-lineup-card__title">
            <div className={`cmp-sport-icon icon-${this.props.sport}`}></div>
            {this.props.entries.length} Contests</h3>
          <div className="actions-menu-container">
            <ul className="actions">
              <li><div className="icon-flop action" onClick={this.handleSwitchToLineup}></div></li>
            </ul>
          </div>
          <div className="cmp-lineup-card__list-header">
            <span className="cmp-lineup-card__list-header-remove">Pos</span>
            <span className="cmp-lineup-card__list-header-contest">Contest</span>
            <span className="cmp-lineup-card__list-header-fee">Winning</span>
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

  renderResultsPane() {
    const isLive = this.props.hasOwnProperty('liveStats');
    // It's a live contest.
    if (isLive) {
      return (
        <LiveContestDetailPane
          contestId={this.state.contestPaneId}
          entry={this.state.currentEntry}
          onHide={this.handleHideContestPane}
          sport={this.props.sport}
        />
      );
    }

    // It's a finished contest.
    return (
        <ResultsPane
          contestId={this.state.contestPaneId}
          entry={this.state.currentEntry}
          onHide={this.handleHideContestPane}
          sport={this.props.sport}
        />
    );
  },

  render() {
    let className = 'cmp-lineup-card flip-container';
    className += ` ${this.props.sport}`;
    if (!this.state.renderLineup) className += ' hover';
    if (this.state.renderContestPane) {
      className += ' shown-contest-pane';
      log.info(this.state.renderContestPane);
    }

    return (
      <div className={className}>
        <div className="flipper-wrap">
          <div className="flipper">
            {this.renderLineup()}
            {this.renderContests()}
          </div>
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
