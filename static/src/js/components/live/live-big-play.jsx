import _ from 'lodash';
import React from 'react';
import { humanizeFP } from '../../lib/utils/numbers';
import cleanDescription from '../../lib/utils/nfl-clean-pbp-description';

// assets
require('../../../sass/blocks/live/live-big-play.scss');
let defaultPlayerSrc;
if (process.env.NODE_ENV !== 'test') {
  require('../../../sass/site/player-pmr-headshot.scss');
  defaultPlayerSrc = require('../../../img/blocks/draft-list/lineup-no-player.png');
}

const block = 'live-big-play';

export default React.createClass({
  propTypes: {
    event: React.PropTypes.object.isRequired,
  },

  shouldComponentUpdate(newProps) {
    return this.props.event.id !== newProps.event.id;
  },

  /**
   *  Renders the IMG element for a player's headshot.
   */
  renderPlayerHeadShotImg(playerId) {
    const playerImagesBaseUrl = `${window.dfs.playerImagesBaseUrl}/${this.props.event.sport}`;

    const onError = (e) => {
      /* eslint-disable no-param-reassign */
      e.target.className = `${block}__player-photo ${block}__player-photo--default`;
      e.target.src = defaultPlayerSrc;
      /* eslint-enable no-param-reassign */
    };

    return (
      <img
        className={`${block}__player-photo`}
        onError={ onError }
        src={`${playerImagesBaseUrl}/120/${playerId}.png`}
        alt="Player Headshot"
      />
    );
  },

  /**
   * Renders the avatar and points for each featured player.
   */
  renderPlayersDOM(event) {
    const players = _.uniq(event.eventPlayers)
      .map(playerId => {
        const playerPoints = event.playerFPChanges[playerId];

        return (
          <li key={playerId} className={`${block}__player`}>
            <div className={`${block}__player-points`}>
              {!playerPoints ? '' : humanizeFP(playerPoints, true)}
            </div>
            { this.renderPlayerHeadShotImg(playerId) }
          </li>
        );
      });

    return (
      <ul className={`${block}__players`}>
        {players}
      </ul>
    );
  },

  render() {
    const { event } = this.props;
    const id = `${event.id}-${new Date().getTime()}`;
    const score = `${event.homeScoreStr} - ${event.awayScoreStr}`;
    const time = `Q?! ${event.when}`;

    return (
      <article key={id} className={`${block} ${block}--${event.sport}`}>
        <div className={`${block}__inner`}>
          <p className={`${block}__description`}>{cleanDescription(event.description)}</p>
          {this.renderPlayersDOM(event)}
        </div>
        <footer className={`${block}__footer`}>
          <div className={`${block}__score`}>{score}</div>
          <div className={`${block}__when`}>{time}</div>
        </footer>
      </article>
    );
  },
});
