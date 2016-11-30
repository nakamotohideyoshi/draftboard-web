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


/**
 * Stateless component that houses a single big play
 *
 * @param  {object} props React props
 * @return {jsx}          JSX of component
 */
export const LiveBigPlay = React.createClass({
  propTypes: {
    event: React.PropTypes.object.isRequired,
  },

  // shouldn't ever need to change
  shouldComponentUpdate(newProps) {
    return this.props.event.id !== newProps.event.id;
  },

  render() {
    const block = 'live-big-play';
    const {
      awayScoreStr,
      description,
      eventPlayers,
      homeScoreStr,
      id,
      playerFPChanges,
      sport,
      when,
      winning,
    } = this.props.event;

    const playerImagesBaseUrl = `${window.dfs.playerImagesBaseUrl}/${sport}`;
    const cleanedDescription = cleanDescription(description);

    if (eventPlayers.length === 1) {
      const playerId = eventPlayers[0];
      const classNames = `${block} ${block}--1-players`;

      return (
        <div
          key={`${id}-${new Date().getTime()}`}
          className={classNames}
        >
          <div className={`${block}__inner`}>
            <img
              alt="Player Headshot"
              className={`${block}__player-photo`}
              onError={
                /* eslint-disable no-param-reassign */
                (e) => {
                  e.target.className = `${block}__player-photo ${block}__player-photo--default`;
                  e.target.src = defaultPlayerSrc;
                }
                /* eslint-enable no-param-reassign */
              }
              src={`${playerImagesBaseUrl}/120/${playerId}.png`}
            />
            <div className={`${block}__description`}>
              <div className={`${block}__description-content`}>
                {cleanedDescription}
              </div>
            </div>
            <div className={`${block}__player-points`}>
              {humanizeFP(playerFPChanges[playerId] || 0, true)}
            </div>
            <div className={`${block}__game`}>
              <div className={`${block}__score ${block}__${winning}-winning`}>
                <div className={`${block}__home-team`}>
                  {homeScoreStr}
                </div>
                &nbsp;-&nbsp;
                <div className={`${block}__away-team`}>
                  {awayScoreStr}
                </div>
              </div>
              <div className={`${block}__when`}>
                Q{when.quarter} {when.clock}
              </div>
            </div>
          </div>
        </div>
      );
    }

    // different template, maybe combine these in the future?
    if (eventPlayers.length > 1) {
      const classNames = `${block} ${block}--2-players`;

      const players = eventPlayers.map(playerId => (
        <li
          key={playerId}
          className={`${block}__player`}
        >
          <div className={`${block}__player-points`}>
            {humanizeFP(playerFPChanges[playerId] || 0, true)}
          </div>
          <div className={`${block}__fixed-player-photo`}>
            <img
              className={`${block}__player-photo`}
              onError={
                /* eslint-disable no-param-reassign */
                (e) => {
                  e.target.className = `${block}__player-photo ${block}__player-photo--default`;
                  e.target.src = defaultPlayerSrc;
                }
                /* eslint-enable no-param-reassign */
              }
              src={`${playerImagesBaseUrl}/120/${playerId}.png`}
              alt="Player Headshot"
            />
          </div>
        </li>
      ));

      return (
        <div
          key={id}
          className={classNames}
        >
          <div className={`${block}__inner`}>
            <div className={`${block}__description`}>
              <div className={`${block}__description-content`}>
                {cleanedDescription}
              </div>
            </div>
            <ul className={`${block}__players`}>
              {players}
            </ul>
            <div className={`${block}__game`}>
              <div className={`${block}__score ${block}__${winning}-winning`}>
                <div className={`${block}__home-team`}>
                  {homeScoreStr}
                </div>
                &nbsp;-&nbsp;
                <div className={`${block}__away-team`}>
                  {awayScoreStr}
                </div>
              </div>
              <div className={`${block}__when`}>
                Q{when.quarter} {when.clock}
              </div>
            </div>
          </div>
        </div>
      );
    }

    return null;
  },
});
