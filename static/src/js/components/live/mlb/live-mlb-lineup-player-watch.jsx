import LiveMLBDiamond from './live-mlb-diamond';
import React from 'react';
import { generateBlockNameWithModifiers } from '../../../lib/utils/bem';
import { mlbDiamondMap } from '../live-lineup-player';

// assets
require('../../../../sass/blocks/live/mlb/live-mlb-lineup-player-watch.scss');


/**
 * Stateless component that houses MLB pitch zone
 * - houses the stadium background within it, so we can center the catcher behind the pitch zone every time
 *
 * @param  {object} props React props
 * @return {jsx}          JSX of component
 */
const LiveMlbLineupPlayerWatch = (props) => {
  const { modifiers, multipartEvent, player } = props;
  const { id, name, type } = player;

  // only show for watchable player types
  if (['pitcher', 'hitter'].indexOf(type) === -1) return null;

  const block = 'live-mlb-lineup-player-watch';
  // sadly putting in non BEM modifier, should be parent but weird absolute stuff happening, want to fix up
  const classNames = `${generateBlockNameWithModifiers(block, modifiers)} live-lineup-player__watching-info`;

  // default to no one on base
  const watchingDiamondProps = {
    key: id,
    first: 'none',
    second: 'none',
    third: 'none',
  };

  // put runners on base
  multipartEvent.runners.map((runner) => {
    const baseName = mlbDiamondMap[runner.endingBase];
    watchingDiamondProps[baseName] = runner.whichSide;
  });

  // event const
  const { when, pitchCount } = multipartEvent;
  const halfInningString = (when.half === 't') ? 'top' : 'bottom';
  const { outcomeFp } = multipartEvent[type];

  return (
    <div key={`live-mlb-lineup-player-watch--${id}`} className={classNames} onClick={props.onClick}>
      <div className={`${block}__fp`}>{outcomeFp}</div>
      <div className={`${block}__name-stats`}>
        <div className={`${block}__name`}>{name}</div>
        <div className={`${block}__stats`}>
          <span className={`${block}__pitch-count`}>{pitchCount}</span>
          <span className={`${block}__inning ${block}__inning--${halfInningString}`}>
            <svg className="down-arrow" viewBox="0 0 40 22.12">
              <path d="M20,31.06L0,8.94H40Z" transform="translate(0 -8.94)" />
            </svg>
            <span className={`${block}__inning-str`}>{when.inning}</span>
          </span>
        </div>
        <div className={`${block}__choose`}>Click Here to Watch</div>
      </div>
      <div className={`${block}__bases`}>
        <LiveMLBDiamond {...watchingDiamondProps} />
      </div>
    </div>
  );
};

LiveMlbLineupPlayerWatch.propTypes = {
  modifiers: React.PropTypes.array,
  multipartEvent: React.PropTypes.object.isRequired,
  onClick: React.PropTypes.func.isRequired,
  player: React.PropTypes.object.isRequired,
};

LiveMlbLineupPlayerWatch.defaultProps = {
  modifiers: [],
};

export default LiveMlbLineupPlayerWatch;
