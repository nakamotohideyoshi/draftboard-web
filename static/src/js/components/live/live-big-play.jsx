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
   * Formats the specified `quarter` and `clock` into a human readable gametime.
   */
  formatGameTime(quarter, clock) {
    if (quarter > 5) {
      return `${quarter - 4}OT ${clock}`;
    }

    return quarter === 5
      ? `OT ${clock}`
      : `Q${quarter} ${clock}`;
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
  renderPlayersDOM(playerStats) {
    const players = playerStats.map(player => {
      const {
        fp_change: fpChange,
        srid_player: srPlayerID,
      } = player;

      return (
        <li key={srPlayerID} className={`${block}__player`}>
          <div className={`${block}__player-points`}>
            {!fpChange ? '' : humanizeFP(fpChange, true)}
          </div>
          { this.renderPlayerHeadShotImg(srPlayerID) }
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
    const { pbp, game, stats, sport, quarter } = this.props.event;
    const score = `${game.away.alias} @ ${game.home.alias}`;
    const time = this.formatGameTime(quarter, pbp.clock);

    return (
      <article className={`${block} ${block}--${sport}`}>
        <div className={`${block}__body`}>
          <p className={`${block}__description`}>{cleanDescription(pbp.description)}</p>
          {this.renderPlayersDOM(stats)}
        </div>
        <footer className={`${block}__footer`}>
          <div className={`${block}__score`}>{score}</div>
          <div className={`${block}__when`}>{time}</div>
        </footer>
      </article>
    );
  },
});
