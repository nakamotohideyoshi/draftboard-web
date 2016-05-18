import LiveMLBDiamond from './mlb/live-mlb-diamond';
import LivePMRProgressBar from './live-pmr-progress-bar';
import React from 'react';
import { extend } from 'lodash';
import { size as _size } from 'lodash';
import { humanizeFP } from '../../actions/sports';


const LiveLineupPlayer = React.createClass({

  propTypes: {
    draftGroupStarted: React.PropTypes.bool.isRequired,
    eventDescription: React.PropTypes.object.isRequired,
    gameStats: React.PropTypes.object.isRequired,
    isPlaying: React.PropTypes.bool.isRequired,
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
    if (_size(this.props.eventDescription) === 0) {
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

    // TODO remove once we have player images
    if (this.props.sport === 'mlb') {
      playerImage = '/static/src/img/temp/mlb-player.png';
    }

    return (
      <div key="1" className="live-lineup-player__circle" onClick={this.props.openPlayerPane}>
        <div className="live-lineup-player__photo">
          <img
            alt="Player Headshot"
            width="62"
            src={playerImage}
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

  renderWatching() {
    const { player } = this.props;

    // only applicable sport right now
    if (this.props.sport !== 'mlb') {
      return [];
    }

    const diamondProps = {
      key: player.id,
      first: 'mine',
      second: 'both',
      third: 'opponent',
    };

    let status = 'possible';
    const elements = [];

    // override isWatchable and add in watching indicator
    if (this.props.isWatching) {
      status = 'active';

      elements.push((<div key="8" className="live-lineup-player__watching-indicator" />));
    }

    // always put in the watchable information
    if (this.props.isWatchable) {
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
              <span>1B/2S - 2 Outs</span>
              <span className="live-player-watching__inning live-player-watching__inning--bottom">
                5th
              </span>
            </div>
            <div className="live-player-watching__choose">Click Here to Watch</div>
          </div>
          <div className="live-player-watching__bases">
            {React.createElement(
              LiveMLBDiamond, extend({}, diamondProps)
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

      // TODO remove once we have player images
      if (this.props.sport === 'mlb') {
        playerImage = '/static/src/img/temp/mlb-player.png';
      }

      return (
        <li className="live-lineup-player live-lineup-player--upcoming">
          <div className="live-lineup-player__position">
            {player.position}
          </div>
          <div className="live-lineup-player__circle">
            <div className="live-lineup-player__photo">
              <img
                alt="Player Headshot"
                width="62"
                src={playerImage}
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
    const className = `live-lineup-player state--${gameCompleted}-playing`;

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
    playerElements = [...playerElements, ...this.renderWatching()];

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
