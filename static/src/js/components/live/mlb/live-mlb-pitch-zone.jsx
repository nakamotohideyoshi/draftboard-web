import React from 'react';
import map from 'lodash/map';


/**
 * Pitch zone when watching pitcher from your lineup
 */
const LiveMLBPitchZone = (props) => {
  const pitches = map(props.event.zonePitches || [], (pitch) => (
    <li
      key={pitch.count}
      className={`pitch pitch--${pitch.outcome} pitch--zone-${pitch.zone}`}
      style={{ zIndex: `${pitch.count}` }}
    >
      <div className="pitch-count">{pitch.count}</div>
      <div className="pitch-info">
        <div className="speed">{pitch.speed} MPH</div>
        <div className="type">{pitch.type}</div>
      </div>
    </li>
  ));
  return (
    <div className={`live-mlb-stadium__pitch-zone live-mlb-pitch-zone live-mlb-pitch-zone__${props.whichSide}`}>
      <div className="live-mlb-pitch-zone__inner">
        <img src="/static/src/img/blocks/live-mlb-pitch-zone/bg.png" alt="Pitch Zone" />
        <ul>
          {pitches}
        </ul>
      </div>
    </div>
  );
};

LiveMLBPitchZone.propTypes = {
  event: React.PropTypes.object.isRequired,
  whichSide: React.PropTypes.string.isRequired,
};

export default LiveMLBPitchZone;
