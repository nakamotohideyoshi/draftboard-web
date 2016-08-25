import React from 'react';
import ImageLoader from 'react-imageloader';
import * as AppActions from '../../stores/app-state-store';
import LivePMRProgressBar from './live-pmr-progress-bar';
import { stringifyMLBWhen } from '../../actions/events/pbp';
import { SPORT_CONST } from '../../actions/sports';
import { humanizeFP } from '../../lib/utils/numbers';

function preloader() {
  return (
    <div className="loading-player-image">
      <div className="spinner">
        <div className="double-bounce1" />
        <div className="double-bounce2" />
      </div>
    </div>
  );
}

/**
 * When a lineup player is clicked, this pane will show seasonal data, player information, team information and
 * game history.
 */
const LivePlayerPane = React.createClass({

  propTypes: {
    eventHistory: React.PropTypes.array.isRequired,
    game: React.PropTypes.object,
    player: React.PropTypes.object.isRequired,
    playerImagesBaseUrl: React.PropTypes.string.isRequired,
    seasonStats: React.PropTypes.object.isRequired,
    sport: React.PropTypes.string.isRequired,
    whichSide: React.PropTypes.string.isRequired,
  },

  /**
   * Close the player pane using AppActions
   */
  closePane() {
    if (this.props.whichSide === 'opponent') {
      AppActions.togglePlayerPane('right');
    } else {
      AppActions.togglePlayerPane('left');
    }
  },

  /**
   * Render out the seasonal stats
   *
   * @return {JSXElement}
   */
  renderStatsAverage() {
    const seasonStats = this.props.seasonStats;
    const { sport } = this.props;
    let whichStats = {};

    switch (sport) {
      case 'nfl': {
        const { position } = this.props.player;
        const statsType = (position === 'QB') ? 'qb' : 'nonQb';
        whichStats = SPORT_CONST[this.props.sport].seasonStats[statsType];
        break;
      }
      default:
        whichStats = SPORT_CONST[this.props.sport].seasonStats;
    }

    const { types, names } = whichStats;

    let renderedStats;
    if (seasonStats.hasOwnProperty('fp') === true) {
      renderedStats = types.map((statType, index) => {
        const value = seasonStats[statType].toFixed(1);

        return (
          <li key={statType}>
            <div className="stat-name">{names[index]}</div>
            <div className="stat-score">{value}</div>
          </li>
        );
      });
    }

    return (
      <div className="player-stats">
        <ul>
          {renderedStats}
        </ul>
      </div>
    );
  },

  /**
   * Render out information about the player's current game
   *
   * @return {JSXElement}
   */
  renderCurrentGame() {
    const game = this.props.game;

    // if the game isn't loaded yet or something then return
    if (!game.hasOwnProperty('boxscore')) return (<div className="current-game" />);

    const boxScore = game.boxscore;
    let gameTimeInfo;
    let gameTimeElement;
    const doneStatuses = ['closed', 'complete'];
    if (doneStatuses.indexOf(boxScore.status) !== -1) {
      gameTimeInfo = ['', 'Final'];
    } else {
      switch (this.props.sport) {
        case 'mlb': {
          const className = `current-game__mlb-half-inning \
            mlb-half-inning--${(boxScore.inning_half === 'B') ? 'bottom' : 'top'}`;

          if (boxScore.inning > 0) {
            gameTimeElement = (
              <div className="current-game__time">
                <div className={className}>
                  <svg className="down-arrow" viewBox="0 0 40 22.12">
                    <path d="M20,31.06L0,8.94H40Z" transform="translate(0 -8.94)" />
                  </svg>
                </div>
                <div className="current-game__time__timer">{stringifyMLBWhen(boxScore.inning)}</div>
              </div>
            );
          }


          break;
        }
        case 'nba':
        case 'nhl':
        default:
          gameTimeInfo = [
            boxScore.clock,
            boxScore.periodDisplay,
          ];
      }
    }

    if (gameTimeInfo) {
      gameTimeElement = (
        <div className="current-game__time">
          <div className="current-game__time__timer">{gameTimeInfo[0]}</div>
          <div className="current-game__time__period">{gameTimeInfo[1]}</div>
        </div>
      );
    }

    return (
      <div className="current-game">
        <div>
          <div className="current-game__team">
            <div className="current-game__team__points">{boxScore.away_score}</div>
            <div className="current-game__team-name">
              <div className="city">{game.awayTeamInfo.city}</div>
              <div className="name">{game.awayTeamInfo.name}</div>
            </div>
          </div>
          {gameTimeElement}
          <div className="current-game__team">
            <div className="current-game__team__points">{boxScore.home_score}</div>
            <div className="current-game__team-name">
              <div className="city">{game.homeTeamInfo.city}</div>
              <div className="name">{game.homeTeamInfo.name}</div>
            </div>
          </div>
        </div>
      </div>
    );
  },

  /**
   * Render out the recent activities, aka props.eventHistory that's available
   * This history erases on refresh, is not cached and lives in the Live component state.
   *
   * @return {JSXElement}
   */
  renderActivities() {
    // reverse to show most recent event first
    const eventHistory = this.props.eventHistory;

    const activitiesHTML = eventHistory.map((activity, index) => {
      const { points, description, when } = activity;
      let whenStr = when;
      if (typeof when === 'object' && 'clock' in when) {
        whenStr = when.clock;
      }
      return (
        <li className="activity" key={index}>
          <div className="points-gained">{points}</div>
          <div className="activity-info">
            {description}
            <p className="time">{whenStr}</p>
          </div>
        </li>
      );
    });

    return (
      <div className="recent-activity">
        <div className="recent-activity__title">Recent activity</div>
        <ul>{activitiesHTML}</ul>
      </div>
    );
  },

  /**
   * Render out the header of the pane, which includes team information and pertinent player information
   *
   * @return {JSXElement}
   */
  renderHeader() {
    const { player, game } = this.props;
    let playerImage = `${this.props.playerImagesBaseUrl}/${player.srid}.png`;

    let teamInfo = {};
    if (player.teamSRID === game.srid_home) {
      teamInfo = game.homeTeamInfo;
    }
    if (player.teamSRID === game.srid_away) {
      teamInfo = game.awayTeamInfo;
    }

    let percentOwned = '';

    if (player.ownershipPercent !== undefined) {
      percentOwned = (
        <div className="header__pts-stats__info">
          <p>% owned</p>
          <p>{player.ownershipPercent}</p>
        </div>
      );
    }

    return (
      <section className="header-section">
        <div className="header__player-image">
          <ImageLoader
            src={playerImage}
            wrapper={React.DOM.div}
            preloader={preloader}
          />
        </div>

        <div className="header__team-role">
          {teamInfo.city} {teamInfo.name} - {player.position}
        </div>
        <div className="header__name">{player.name}</div>

        <div className="header__pts-stats">
          <div className="header__pts-stats__info">
            <LivePMRProgressBar
              colors={['46495e', '34B4CC', '2871AC']}
              decimalRemaining={player.timeRemaining.decimal}
              id={`${player.id}PlayerPane`}
              strokeDecimal={0.03}
              svgWidth={50}
            />

            <div className="header__pts-stats__info__insvg">
              <p>pts</p>
              <p>{humanizeFP(player.fp)}</p>
            </div>
          </div>

          {percentOwned}

        </div>
      </section>
    );
  },

  render() {
    const side = this.props.whichSide === 'opponent' ? 'right' : 'left';
    const className = `player-detail-pane live-player-pane live-pane live-pane--${side} live-pane-player--${side}`;

    return (
      <div className={className}>
        <div className="live-pane__close" onClick={this.closePane}></div>

        <div className="pane-upper">
          {this.renderHeader()}
          {this.renderStatsAverage()}
          {this.renderCurrentGame()}
        </div>

        <div className="pane-lower">
          {this.renderActivities()}
        </div>
      </div>
    );
  },
});


export default LivePlayerPane;
