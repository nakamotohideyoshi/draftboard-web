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
  const { zonePitches } = event;

  const block = 'live-mlb-stadium';
  const classNames = generateBlockNameWithModifiers(block, modifiers);

  let hitterInfo = null;
  if (event.hitter) {
    const { atBatStats, name } = event.hitter;
    hitterInfo = (
      <div className={`${block}__hitter`}>
        <div className={`${block}__hitter-at-bat`}>At bat</div>
        <div className={`${block}__hitter-name`}>{name}</div>
        <div className={`${block}__hitter-record`}>{atBatStats}</div>
      </div>
    );
  }

  return (
    <section className={classNames}>
      <div className={`${block}__pitch-zone`}>
        <LiveMLBPitchZone zonePitches={zonePitches} modifiers={[whichSide]} />
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
