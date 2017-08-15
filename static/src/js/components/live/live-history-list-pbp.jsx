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
    id: React.PropTypes.number.isRequired,
    sport: React.PropTypes.string.isRequired,
    description: React.PropTypes.string.isRequired,
    lineup: React.PropTypes.string.isRequired,
    game: React.PropTypes.shape({
      homeTeamAlias: React.PropTypes.string.isRequired,
      awayTeamAlias: React.PropTypes.string.isRequired,
      period: React.PropTypes.number.isRequired,
      clock: React.PropTypes.string.isRequired,
    }).isRequired,
    players: React.PropTypes.arrayOf(React.PropTypes.shape({
      lineup: React.PropTypes.string.isRequired,
      fp: React.PropTypes.number.isRequired,
      srid: React.PropTypes.string.isRequired,
    })),
  },

  shouldComponentUpdate(newProps) {
    return this.props.id !== newProps.id;
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
  renderPlayerHeadShotImg(player) {
    const playerImagesBaseUrl = `${window.dfs.playerImagesBaseUrl}/${this.props.sport}`;

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
        src={`${playerImagesBaseUrl}/120/${player.srid}.png`}
        alt="Player Headshot"
      />
    );
  },

  /**
   * Renders the avatar and points for each featured player.
   */
  renderPlayersDOM(players) {
    return players.map(player => (
      <li key={player.srid} className={`${block}__player ${block}__player--${player.lineup}`}>
        <div className={`${block}__player-points`}>
          {humanizeFP(player.fp, true)}
        </div>
        { this.renderPlayerHeadShotImg(player) }
      </li>
    ));
  },

  render() {
    const { sport, description, players, game, lineup } = this.props;

    return (
      <article className={`${block} ${block}--${sport} ${block}--${lineup}`}>
        <div className={`${block}__body`}>
          <p className={`${block}__description`}>{cleanDescription(description)}</p>
          <ul className={`${block}__players`}>
            {this.renderPlayersDOM(players)}
          </ul>
        </div>
        <footer className={`${block}__footer`}>
          <div className={`${block}__score`}>{`${game.awayTeamAlias} @ ${game.homeTeamAlias}`}</div>
          <div className={`${block}__when`}>{this.formatGameTime(game.period, game.clock)}</div>
        </footer>
      </article>
    );
  },
});
