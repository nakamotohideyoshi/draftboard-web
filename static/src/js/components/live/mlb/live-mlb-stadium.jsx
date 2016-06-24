import React from 'react';
import LiveMLBPitchZone from './live-mlb-pitch-zone';
import { generateBlockNameWithModifiers } from '../../../lib/utils/bem';

// assets
require('../../../../sass/blocks/live/mlb/live-mlb-stadium.scss');


/**
 * Stateless component that houses MLB stadium
 * - if no opponent, then show the stadium full width
 * - with opponent, have split screen between the two
 *
 * @param  {object} props React props
 * @return {jsx}          JSX of component
 */
const LiveMLBStadium = (props) => {
  const { event, modifiers, whichSide } = props;

  const block = 'live-mlb-stadium';
  const classNames = generateBlockNameWithModifiers(block, modifiers);
  let hitterInfo = null;

  if (event.message) {
    const atBatStats = event.message.at_bat_stats;

    hitterInfo = (
      <div className={`${block}__hitter`}>
        <div className={`${block}__hitter-at-bat`}>At bat</div>
        <div className={`${block}__hitter-name`}>
          {`4. ${atBatStats.preferred_name} ${atBatStats.last_name}`}
        </div>
        <div className={`${block}__hitter-record`}>1 for 3 (2B, B)</div>
      </div>
    );
  }

  return (
    <section className={classNames}>
      <div className={`${block}__pitch-zone`}>
        <LiveMLBPitchZone event={event} modifiers={[whichSide]} />
        {hitterInfo}
      </div>
    </section>
  );
};

LiveMLBStadium.propTypes = {
  event: React.PropTypes.object.isRequired,
  modifiers: React.PropTypes.array,
  whichSide: React.PropTypes.string.isRequired,
};

export default LiveMLBStadium;
