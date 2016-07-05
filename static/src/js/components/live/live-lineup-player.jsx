import LiveMLBDiamond from './mlb/live-mlb-diamond';
import LiveMlbLineupPlayerWatch from './mlb/live-mlb-lineup-player-watch';
import React from 'react';
import merge from 'lodash/merge';
import extend from 'lodash/extend';
import size from 'lodash/size';
import { humanizeFP } from '../../actions/sports';
import PlayerPmrHeadshotComponent from '../site/PlayerPmrHeadshotComponent';


// map to convert socket call to needed css classname
export const mlbDiamondMap = {
  1: 'first',
  2: 'second',
  3: 'third',
  4: 'home',
};


const LiveLineupPlayer = React.createClass({

  propTypes: {
    draftGroupStarted: React.PropTypes.bool.isRequired,
    eventDescription: React.PropTypes.object.isRequired,
    gameStats: React.PropTypes.object.isRequired,
    isPlaying: React.PropTypes.bool.isRequired,
    playerType: React.PropTypes.string.isRequired,
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
        <div className="hover-stats__title">
          <h4 className="hover-stats__name">
            BRYCE HARPER
          </h4>
          <div className="hover-stats__place">
            <div className="hover-stats__triangle"></div>
            5th
          </div>
        </div>
        <ul>
          {renderedStats}
        </ul>
      </div>
    );
  },

  renderPhotoAndHover() {
    const { player, openPlayerPane, sport, whichSide } = this.props;

    // use different colors for which side client is viewing
    let colors = ['46495e', '34B4CC', '2871AC'];
    if (whichSide === 'opponent') {
      colors = ['3e4155', 'db3c3d', '611a59'];
    }

    return (
      <div key="1" className="live-lineup-player__headshot-gamestats" onClick={openPlayerPane}>
        <PlayerPmrHeadshotComponent
          colors={colors}
          decimalRemaining={player.timeRemaining.decimal}
          playerSrid={player.srid}
          sport={sport}
          uniquePmrId={`pmr-live-lineup-player-${player.id}-${whichSide}`}
          width={52}
        />

        {this.renderGameStats()}
      </div>
    );
  },

  renderMLBWatching() {
    const { player, multipartEvent, playerType, isWatching } = this.props;

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

    // override isWatchable and add in watching indicator
    if (isWatching) {
      status = 'active';
      elements.push((<div key="8" className="live-lineup-player__watching-indicator" />));
    }

    if (playerType === 'runner') {
      const runnerDiamond = merge({}, defaultDiamond);

      // add runner to diamond
      const { runners = [] } = multipartEvent;
      const runnerProps = runners.filter(runner => runner.playerSrid === player.srid)[0];
      const baseName = mlbDiamondMap[runnerProps.endingBase];
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
    elements.push(
      <LiveMlbLineupPlayerWatch
        key="9"
        modifiers={[status]}
        multipartEvent={multipartEvent}
        onClick={() => this.props.setWatchingPlayer(this.props.player.srid)}
        player={{
          id: player.id,
          name: player.name,
          type: playerType,
        }}
      />
    );

    return elements;
  },

  render() {
    const player = this.props.player;

    // if we have not started, show dumbed down version for countdown
    if (this.props.draftGroupStarted === false) {
      return (
        <li className={`live-lineup-player live-lineup-player--upcoming live-lineup-player--sport-${this.props.sport}`}>
          <div className="live-lineup-player__position">
            {player.position}
          </div>
          <div key="1" className="live-lineup-player__headshot-gamestats" onClick={this.props.openPlayerPane}>
            <PlayerPmrHeadshotComponent
              modifiers={['upcoming', `sport-${this.props.sport}`]}
              pmrColors={['46495e', '34B4CC', '2871AC']}
              playerSrid={this.props.player.srid}
              sport={this.props.sport}
              uniquePmrId={`pmr-live-lineup-player-${this.props.player.id}`}
              width={50}
            />
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
      (<div className="live-lineup-player__hover-area" key="0">
        <div className="live-lineup-player__position">
          {player.position}
        </div>
        {this.renderPhotoAndHover()}
      </div>),
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
