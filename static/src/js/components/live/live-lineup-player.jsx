import LiveMLBDiamond from './mlb/live-mlb-diamond';
import LivePMRProgressBar from './live-pmr-progress-bar';
import React from 'react';
import forEach from 'lodash/forEach';
import merge from 'lodash/merge';
import extend from 'lodash/extend';
import size from 'lodash/size';
import { humanizeFP } from '../../actions/sports';


const LiveLineupPlayer = React.createClass({

  propTypes: {
    draftGroupStarted: React.PropTypes.bool.isRequired,
    eventDescription: React.PropTypes.object.isRequired,
    gameStats: React.PropTypes.object.isRequired,
    isPlaying: React.PropTypes.bool.isRequired,
    isRunner: React.PropTypes.bool.isRequired,
    isWatchable: React.PropTypes.bool.isRequired,
    isWatching: React.PropTypes.bool.isRequired,
    multipartEvent: React.PropTypes.object.isRequired,
    openPlayerPane: React.PropTypes.func.isRequired,
    player: React.PropTypes.object.isRequired,
    playerImagesBaseUrl: React.PropTypes.string.isRequired,
    setWatchingPlayer: React.PropTypes.func.isRequired,
    sport: React.PropTypes.string.isRequired,
    whichSide: React.PropTypes.string.isRequired,
  },

  /**
   * Propogating up a click handler to choose the player to watch
   */
  _onClick() {
    this.props.setWatchingPlayer(this.props.player.srid);
  },

  /**
   * Render the event description if a Pusher pbp event comes through
   *
   * @return {JSXElement}
   */
  renderEventDescription() {
    // only show when there's an event
    if (size(this.props.eventDescription) === 0) {
      return (<div key="5" />);
    }

    const { points, info, when } = this.props.eventDescription;

    const pointsDiv = (points !== null) ? (<div className="event-description__points">{points}</div>) : '';

    return (
      <div key="5" className="live-lineup-player__event-description event-description showing">
        {pointsDiv}
        <div className="event-description__info">{info}</div>
        <div className="event-description__when">{when}</div>
      </div>
    );
  },

  /**
   * Render game stats that show up when you hover over a player.
   *
   * @return {JSXElement}
   */
  renderGameStats() {
    const values = this.props.gameStats;

    // ordered stats
    const statTypes = ['points', 'rebounds', 'steals', 'assists', 'blocks', 'turnovers'];
    const statNames = ['PTS', 'RB', 'ST', 'ASST', 'BLK', 'TO'];

    const renderedStats = statTypes.map((statType, index) => (
      <li key={statType}>
        <div className="hover-stats__amount">{values[statType] || 0}</div>
        <div className="hover-stats__name">{statNames[index]}</div>
      </li>
    ));

    return (
      <div key="6" className="live-lineup-player__hover-stats" onClick={this.props.openPlayerPane}>
        <ul>
          {renderedStats}
        </ul>
      </div>
    );
  },

  renderPhotoAndHover() {
    const decimalRemaining = this.props.player.timeRemaining.decimal;
    let playerImage = `${this.props.playerImagesBaseUrl}/${this.props.player.srid}.png`;

    return (
      <div key="1" className="live-lineup-player__circle" onClick={this.props.openPlayerPane}>
        <div className="live-lineup-player__photo">
          <img
            alt="Player Headshot"
            src={playerImage}
            onError={
              /* eslint-disable no-param-reassign */
              (e) => {
                e.target.className = 'default-player';
                e.target.src = '/static/src/img/blocks/draft-list/lineup-no-player.png';
              }
              /* eslint-enable no-param-reassign */
            }
          />
        </div>

        <LivePMRProgressBar
          decimalRemaining={decimalRemaining}
          strokeWidth={2}
          backgroundHex="46495e"
          hexStart="34B4CC"
          hexEnd="2871AC"
          svgWidth={50}
          id={`${this.props.player.id}LineupPlayer`}
        />
        {this.renderGameStats()}
      </div>
    );
  },

  renderMLBWatching() {
    const { player, multipartEvent, isRunner, isWatchable, isWatching } = this.props;

    // only applicable sport right now
    if (this.props.sport !== 'mlb') return [];

    let status = 'possible';
    const elements = [];

    // default to no one on base
    const defaultDiamond = {
      key: player.id,
      first: 'none',
      second: 'none',
      third: 'none',
    };

    // map to convert socket call to needed css classname
    const diamondMap = {
      1: 'first',
      2: 'second',
      3: 'third',
      4: 'home',
    };

    // override isWatchable and add in watching indicator
    if (isWatching) {
      status = 'active';
      elements.push((<div key="8" className="live-lineup-player__watching-indicator" />));
    }

    if (isRunner) {
      const runnerDiamond = merge({}, defaultDiamond);

      // add runner to diamond
      const runnerProps = multipartEvent.runners.filter(runner => runner.playerSrid === player.srid)[0];
      const baseName = diamondMap[runnerProps.endingBase];
      runnerDiamond[baseName] = runnerProps.whichSide;

      elements.push((
        <div key="10" className="live-lineup-player__runner-bases">
          {React.createElement(
            LiveMLBDiamond, extend({}, runnerDiamond)
          )}
        </div>
      ));
    }

    // always put in the watchable information
    if (isWatchable) {
      const watchingDiamondProps = merge({}, defaultDiamond);

      // put runners on base
      forEach(multipartEvent.runners, (runner) => {
        const baseName = diamondMap[runner.endingBase];
        watchingDiamondProps[baseName] = runner.whichSide;
      });

      const { when, pitchCount } = multipartEvent;

      let halfInningString = 'bottom';
      if (when.half === 't') halfInningString = 'top';

      elements.push((
        <div
          key="9"
          className={`live-lineup-player__watching-info live-player-watching live-player-watching--${status}`}
          onClick={this._onClick}
        >
          <div className="live-player-watching__fp" />
          <div className="live-player-watching__name-stats">
            <div className="live-player-watching__name">{player.name}</div>
            <div className="live-player-watching__stats">
              <span>{pitchCount}</span>
              <span className={`live-player-watching__inning live-player-watching__inning--${halfInningString}`}>
                <svg className="down-arrow" viewBox="0 0 40 22.12">
                  <path d="M20,31.06L0,8.94H40Z" transform="translate(0 -8.94)" />
                </svg>
                {multipartEvent.when.inning}
              </span>
            </div>
            <div className="live-player-watching__choose">Click Here to Watch</div>
          </div>
          <div className="live-player-watching__bases">
            {React.createElement(
              LiveMLBDiamond, extend({}, watchingDiamondProps)
            )}
          </div>
        </div>
      ));
    }

    return elements;
  },

  render() {
    const player = this.props.player;

    // if we have not started, show dumbed down version for countdown
    if (this.props.draftGroupStarted === false) {
      let playerImage = `${this.props.playerImagesBaseUrl}/${player.srid}.png`;

      return (
        <li className={`live-lineup-player live-lineup-player--upcoming live-lineup-player--sport-${this.props.sport}`}>
          <div className="live-lineup-player__position">
            {player.position}
          </div>
          <div className="live-lineup-player__circle">
            <div className="live-lineup-player__photo">
              <img
                alt="Player Headshot"
                src={playerImage}
                onError={
                  /* eslint-disable no-param-reassign */
                  (e) => {
                    e.target.className = 'default-player';
                    e.target.src = '/static/src/img/blocks/draft-list/lineup-no-player.png';
                  }
                  /* eslint-enable no-param-reassign */
                }
              />
            </div>
          </div>
          <div className="live-lineup-player__only-name">
            {player.name}
          </div>
        </li>
      );
    }

    // classname for the whole player
    const gameCompleted = (player.timeRemaining.decimal === 0) ? 'not' : 'is';
    const className = `live-lineup-player \
      state--${gameCompleted}-playing \
      live-lineup-player--sport-${this.props.sport}`;

    // classname to determine whether the player is live or not
    const isPlayingClass = this.props.isPlaying === true ? 'play-status--playing' : '';
    const playStatusClass = `live-lineup-player__play-status ${isPlayingClass}`;

    // in an effort to have DRY code, i render this list and reverse it for the opponent side
    // note that the key is required by React when rendering multiple children
    let playerElements = [
      (<div key="0" className="live-lineup-player__position">
        {player.position}
      </div>),
      this.renderPhotoAndHover(),
      (<div key="2" className="live-lineup-player__status"></div>),
      (<div key="3" className="live-lineup-player__points">{humanizeFP(player.fp)}</div>),
      (<div key="4" className={ playStatusClass } />),
      this.renderEventDescription(),
    ];

    // add in watching, if applicable
    playerElements = [...playerElements, ...this.renderMLBWatching()];

    // flip the order of elements for opponent
    if (this.props.whichSide === 'opponent') {
      playerElements = playerElements.reverse();
    }

    return (
      <li className={className}>
        {playerElements}
      </li>
    );
  },
});

export default LiveLineupPlayer;
