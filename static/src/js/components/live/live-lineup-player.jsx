import extend from 'lodash/extend';
import LiveLineupPlayerEventInfo from './lineup-player/live-lineup-player-event-info';
import LiveMLBDiamond from './mlb/live-mlb-diamond';
import LiveMlbLineupPlayerWatch from './mlb/live-mlb-lineup-player-watch';
import merge from 'lodash/merge';
import PlayerPmrHeadshotComponent from '../site/PlayerPmrHeadshotComponent';
import React from 'react';
import { generateBlockNameWithModifiers } from '../../lib/utils/bem';
import { humanizeFP } from '../../lib/utils/numbers';
import { SPORT_CONST } from '../../actions/sports';

// assets
require('../../../sass/blocks/live/live-lineup-player.scss');

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
    if (Object.keys(this.props.eventDescription).length === 0) return null;

    const { points, description, when } = this.props.eventDescription;
    const eventProps = { description, points, when };

    return (
      <div key="5" className="live-lineup-player__event-description">
        <LiveLineupPlayerEventInfo {...eventProps} />
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
    const { sport, player } = this.props;
    let whichStats = {};

    switch (sport) {
      case 'nfl': {
        const { position } = this.props.player;
        const statsType = (position === 'QB') ? 'qb' : 'nonQb';
        whichStats = SPORT_CONST[this.props.sport].liveStats[statsType];
        break;
      }
      default:
        whichStats = SPORT_CONST[this.props.sport].liveStats;
    }

    const { types, names } = whichStats;

    const renderedStats = types.map((statType, index) => (
      <li key={statType} className="live-lineup-player__hover-stat">
        <div className="hover-stats__amount">{values[statType] || 0}</div>
        <div className="hover-stats__name">{names[index]}</div>
      </li>
    ));

    return (
      <div key="6" className="live-lineup-player__hover-stats">
        <div className="hover-stats__title">
          <h4 className="hover-stats__name">
            {player.name}
          </h4>
        </div>
        <ul className="live-lineup-player__hover-stats-list">
          {renderedStats}
        </ul>
      </div>
    );
  },

  renderPhotoAndHover() {
    const { player, sport, whichSide } = this.props;

    // use different colors for which side client is viewing
    let colors = ['46495e', '34B4CC', '2871AC'];
    if (whichSide === 'opponent') {
      colors = ['3e4155', 'db3c3d', '611a59'];
    }

    return (
      <div key="1" className="live-lineup-player__headshot-gamestats">
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
    const { player, multipartEvent, playerType, isWatching, whichSide } = this.props;

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
        modifiers={[status, whichSide]}
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
    const { player, whichSide } = this.props;

    // if we have not started, show dumbed down version for countdown
    if (this.props.draftGroupStarted === false) {
      return (
        <li className={`live-lineup-player live-lineup-player--upcoming live-lineup-player--sport-${this.props.sport}`}>
          <div className="live-lineup-player__position">
            {player.position}
          </div>
          <div key="1" className="live-lineup-player__headshot-gamestats">
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
    const block = 'live-lineup-player';
    const modifiers = [whichSide, `state-${gameCompleted}-playing`, `sport-${this.props.sport}`];
    const classNames = generateBlockNameWithModifiers(block, modifiers);

    // classname to determine whether the player is live or not
    const isPlayingClass = this.props.isPlaying === true ? 'play-status--playing' : '';
    const playStatusClass = `live-lineup-player__play-status ${isPlayingClass}`;

    // in an effort to have DRY code, i render this list and reverse it for the opponent side
    // note that the key is required by React when rendering multiple children
    let playerElements = [
      (<div className="live-lineup-player__position" key="0">
        {player.position}
      </div>),
      (<div className="live-lineup-player__hover-area" key="1">
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
      <li className={classNames}>
        {playerElements}
      </li>
    );
  },
});

export default LiveLineupPlayer;
