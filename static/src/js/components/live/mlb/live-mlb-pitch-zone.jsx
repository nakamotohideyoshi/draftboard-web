import React from 'react';
import LiveMLBPitchZonePitch from './live-mlb-pitch-zone-pitch';
import { generateBlockNameWithModifiers } from '../../../lib/utils/bem';

// assets
require('../../../../sass/blocks/live/live-mlb-pitch-zone.scss');
import stadiumBgSrc from '../../../../img/blocks/live/bg-mlb.jpg';
const zoneBg = require('../../../../img/blocks/live-mlb-pitch-zone/bg-pitch-zone.png');


/**
 * Stateless component that houses MLB pitch zone
 * - houses the stadium background within it, so we can center the catcher behind the pitch zone every time
 *
 * @param  {object} props React props
 * @return {jsx}          JSX of component
 */
const LiveMLBPitchZone = (props) => {
  const { modifiers, zonePitches } = props;

  const block = 'live-mlb-pitch-zone';
  const classNames = generateBlockNameWithModifiers(block, modifiers);

  let pitches = null;
  if (zonePitches.length > 0) {
    pitches = (
      <ul className={`${block}__pitches`}>
        {zonePitches.map((pitch) => (
          <LiveMLBPitchZonePitch {...pitch} key={pitch.count} />
        ))}
      </ul>
    );
  }

  return (
    <div className={classNames}>
      <img
        alt="Stadium background"
        className={`${block}__stadium-bg`}
        src={stadiumBgSrc}
      />

      <div className={`${block}__inner`}>
        <img
          alt="Pitch zone background"
          className={`${block}__zone-bg`}
          src={zoneBg}
        />
        {pitches}
      </div>
    </div>
  );
};

LiveMLBPitchZone.propTypes = {
  zonePitches: React.PropTypes.array.isRequired,
  modifiers: React.PropTypes.array,
};

LiveMLBPitchZone.defaultProps = {
  zonePitches: [],
};

export default LiveMLBPitchZone;
