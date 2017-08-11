import React from 'react';
import { humanizeFP } from '../../lib/utils/numbers';
import cleanDescription from '../../lib/utils/nfl-clean-pbp-description';

// assets
require('../../../sass/blocks/live/live-history-list-pbp.scss');
let defaultPlayerSrc;
if (process.env.NODE_ENV !== 'test') {
  require('../../../sass/site/player-pmr-headshot.scss');
  defaultPlayerSrc = require('../../../img/blocks/draft-list/lineup-no-player.png');
}

const block = 'live-history-list-pbp';

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
    const q = parseInt(quarter, 10);
    if (q > 5) {
      return `${q - 4}OT ${clock}`;
    }

    return q === 5
      ? `OT ${clock}`
      : `Q${q} ${clock}`;
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
  renderPlayersDOM(playerStats, fpValues) {
    const players = playerStats.map(player => {
      const { srid_player: srPlayerID } = player;
      const fp = fpValues[srPlayerID] || 0;

      return (
        <li key={srPlayerID} className={`${block}__player`}>
          <div className={`${block}__player-points`}>
            {!fp ? '' : humanizeFP(fp, true)}
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
    const { pbp, game, stats, sport, fp_values } = this.props.event;
    const score = `${game.away.alias} @ ${game.home.alias}`;
    const time = this.formatGameTime(game.period, pbp.clock);

    return (
      <article className={`${block} ${block}--${sport}`}>
        <div className={`${block}__body`}>
          <p className={`${block}__description`}>{cleanDescription(pbp.description)}</p>
          {this.renderPlayersDOM(stats, fp_values)}
        </div>
        <footer className={`${block}__footer`}>
          <div className={`${block}__score`}>{score}</div>
          <div className={`${block}__when`}>{time}</div>
        </footer>
      </article>
    );
  },
});
