import React from 'react';
import LiveMLBPitchZonePitch from './live-mlb-pitch-zone-pitch';
import { generateBlockNameWithModifiers } from '../../../lib/utils/bem';

// assets
require('../../../../sass/blocks/live/live-mlb-pitch-zone.scss');
import stadiumBgSrc from '../../../../img/blocks/live/bg-mlb.jpg';
// import zoneBg from '../../../../img/blocks/live-mlb-pitch-zone/bg.png';


/**
 * Stateless component that houses MLB pitch zone
 * - houses the stadium background within it, so we can center the catcher behind the pitch zone every time
 *
 * @param  {object} props React props
 * @return {jsx}          JSX of component
 */
const LiveMLBPitchZone = (props) => {
  const block = 'live-mlb-pitch-zone';
  const classNames = generateBlockNameWithModifiers(block, props.modifiers);

  const zonePitches = props.event.zonePitches || [];
  const pitches = zonePitches.map((pitch) => (
    <LiveMLBPitchZonePitch {...pitch} />
  ));

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
          src="/static/src/img/blocks/live-mlb-pitch-zone/bg.png"
        />
        <ul className={`${block}__pitches`}>
          {pitches}
        </ul>
      </div>
    </div>
  );
};

LiveMLBPitchZone.propTypes = {
  event: React.PropTypes.object.isRequired,
  modifiers: React.PropTypes.array,
};

export default LiveMLBPitchZone;
