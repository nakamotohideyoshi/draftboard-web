import LivePMRProgressBar from '../live/live-pmr-progress-bar';
import React from 'react';
import { generateBlockNameWithModifiers } from '../../lib/utils/bem';

// assets
let defaultPlayerSrc;
if (process.env.NODE_ENV !== 'test') {
  require('../../../sass/site/player-pmr-headshot.scss');
  defaultPlayerSrc = require('../../../img/blocks/draft-list/lineup-no-player.png');
}


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
          strokeDecimal={0.05}
          svgWidth={width}
        />
      </div>
    );
  };

  return (
    <div>
      <div className="circle">
        <span
          className={`cmp-lineup-card__photo ${block}__headshot ${block}__headshot--${sport}`}
          style={{ backgroundImage: `url(https:${headshotSrc})` }}
          onError={
            /* eslint-disable no-param-reassign */
            (e) => {
              e.target.className = `${block}__headshot ${block}__headshot--default`;
              e.target.style.backgroundImage = defaultPlayerSrc;
            }
            /* eslint-enable no-param-reassign */
          }
        >
        </span>
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
