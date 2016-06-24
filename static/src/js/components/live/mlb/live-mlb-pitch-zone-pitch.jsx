import React from 'react';
import { generateBlockNameWithModifiers } from '../../../lib/utils/bem';

// assets
require('../../../../sass/blocks/live/mlb/live-mlb-pitch-zone-pitch.scss');


/**
 * Stateless component that houses MLB pitch within pitch zone
 * - we may want to remove zone at some point, in there right now in case we want to differentiate by them
 *
 * @param  {object} props React props
 * @return {jsx}          JSX of component
 */
const LiveMLBPitchZonePitch = (props) => {
  const { count, left, outcome, speed, top, type, zone } = props;

  const block = 'live-mlb-pitch-zone-pitch';
  const modifiers = [outcome, `zone-${zone}`];
  const classNames = generateBlockNameWithModifiers(block, modifiers);

  return (
    <li
      key={count}
      className={classNames}
      style={{ zIndex: `${count}`, left: `${left}%`, top: `${top}%` }}
    >
      <div className={`${block}__count`}>{count}</div>
      <div className={`${block}__info`}>
        <div className={`${block}__speed`}>{speed} MPH</div>
        <div className={`${block}__type`}>{type}</div>
      </div>
    </li>
  );
};

LiveMLBPitchZonePitch.propTypes = {
  count: React.PropTypes.number.isRequired,
  left: React.PropTypes.number.isRequired,
  outcome: React.PropTypes.string.isRequired,
  speed: React.PropTypes.number,
  top: React.PropTypes.number.isRequired,
  type: React.PropTypes.string,
  zone: React.PropTypes.number.isRequired,
};

export default LiveMLBPitchZonePitch;
