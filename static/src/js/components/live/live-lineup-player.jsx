import React from 'react';

import LivePMRProgressBar from './live-pmr-progress-bar';


const LiveLineupPlayer = React.createClass({

  propTypes: {
    eventDescription: React.PropTypes.object,
    isPlaying: React.PropTypes.bool.isRequired,
    openPlayerPane: React.PropTypes.func.isRequired,
    player: React.PropTypes.object.isRequired,
    playerImagesBaseUrl: React.PropTypes.string.isRequired,
    whichSide: React.PropTypes.string.isRequired,
  },

  /**
   * Render the event description if a Pusher pbp event comes through
   *
   * @return {JSXElement}
   */
  renderEventDescription() {
    // only show when there's an event
    if (this.props.eventDescription === 'empty') {
      return (<div key="5" />);
    }

    const { points, info, when } = this.props.eventDescription;

    return (
      <div className="live-lineup-player__event-description event-description showing">
        <div className="event-description__points">{points}</div>
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
    const values = this.props.player.liveStats || {};

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
      <div key="6" className="live-lineup-player__hover-stats">
        <ul>
          {renderedStats}
        </ul>
      </div>
    );
  },

  renderPhotoAndHover() {
    const decimalRemaining = this.props.player.stats.decimalRemaining;
    const playerImage = `${this.props.playerImagesBaseUrl}/${this.props.player.info.player_srid}.png`;

    return (
      <div key="1" className="live-lineup-player__circle">
        <div className="live-lineup-player__photo">
          <img
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
        />
        {this.renderGameStats()}
      </div>
    );
  },

  render() {
    const stats = this.props.player.stats;

    // classname for the whole player
    const gameCompleted = (stats.decimalRemaining === 0) ? 'not' : 'is';
    const className = `live-lineup-player state--${gameCompleted}-playing`;

    // classname to determine whether the player is live or not
    const isPlayingClass = this.props.isPlaying === true ? 'play-status--playing' : '';
    const playStatusClass = `live-lineup-player__play-status ${isPlayingClass}`;

    // in an effort to have DRY code, i render this list and reverse it for the opponent side
    // note that the key is required by React when rendering multiple children
    let playerElements = [
      (<div key="0" className="live-lineup-player__position">
        {this.props.player.info.position}
      </div>),
      this.renderPhotoAndHover(),
      (<div key="2" className="live-lineup-player__status"></div>),
      (<div key="3" className="live-lineup-player__points">{stats.fp}</div>),
      (<div key="4" className={ playStatusClass } />),
      this.renderEventDescription(),
    ];

    // flip the order of elements for opponent
    if (this.props.whichSide === 'opponent') {
      playerElements = playerElements.reverse();
    }

    return (
      <li className={className} onClick={this.props.openPlayerPane}>
        {playerElements}
      </li>
    );
  },
});

export default LiveLineupPlayer;
