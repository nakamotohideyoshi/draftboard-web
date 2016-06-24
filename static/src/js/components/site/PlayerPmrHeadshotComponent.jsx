import LivePMRProgressBar from '../live/live-pmr-progress-bar';
import React from 'react';
import { generateBlockNameWithModifiers } from '../../lib/utils/bem';

// assets
require('../../../sass/site/player-pmr-headshot.scss');
import defaultPlayerSrc from '../../../img/blocks/draft-list/lineup-no-player.png';


/**
 * Stateless component that houses PMR circle and headshot
 * - if headshot doesn't exist, it uses defaultPlayerSrc instead
 * - consider having a single param of PMR props that gets passed through
 *
 * @param  {object} props React props
 * @return {jsx}          JSX of component
 */
const PlayerPmrHeadshotComponent = (props) => {
  const { colors, decimalRemaining, modifiers, playerSrid, sport, uniquePmrId, width } = props;

  const block = 'player-pmr-headshot';
  const classNames = generateBlockNameWithModifiers(block, modifiers);
  const headshotSrc = `${window.dfs.playerImagesBaseUrl}/${sport}/120/${playerSrid}.png`;

  // if there's no pmr to render, don't bother
  const renderPmr = () => {
    if (decimalRemaining === 0) return null;

    return (
      <div className="player-pmr-headshot__pmr">
        <LivePMRProgressBar
          colors={colors}
          decimalRemaining={decimalRemaining}
          id={uniquePmrId}
          svgWidth={width}
        />
      </div>
    );
  };

  return (
    <div className={classNames} style={{ height: `${width}px`, width: `${width}px` }}>
      <div className="player-pmr-headshot__bg">
        <img
          alt="Player Headshot"
          className={`${block}__headshot ${block}__headshot--${sport}`}
          onError={
            /* eslint-disable no-param-reassign */
            (e) => {
              e.target.className = `${block}__headshot ${block}__headshot--default`;
              e.target.src = defaultPlayerSrc;
            }
            /* eslint-enable no-param-reassign */
          }
          src={headshotSrc}
        />
      </div>

      {renderPmr()}
    </div>
  );
};

PlayerPmrHeadshotComponent.propTypes = {
  // passed to PMR bar
  colors: React.PropTypes.array,

  // passed to PMR bar
  decimalRemaining: React.PropTypes.number,

  // BEM modifiers depending on where the component is put
  modifiers: React.PropTypes.array,

  // for headshot src
  playerSrid: React.PropTypes.string.isRequired,

  // for headshot positioning
  sport: React.PropTypes.string.isRequired,

  // id used to differentiate IDs for the PMR bar
  uniquePmrId: React.PropTypes.string.isRequired,

  // outer width of the component, percentage based within
  width: React.PropTypes.number.isRequired,
};

PlayerPmrHeadshotComponent.defaultProps = {
  decimalRemaining: 0,
  modifiers: [],
};

export default PlayerPmrHeadshotComponent;
