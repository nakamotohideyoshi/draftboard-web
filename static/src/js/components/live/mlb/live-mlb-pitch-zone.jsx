import React from 'react';


/**
 * Pitch zone when watching pitcher from your lineup
 */
const LiveMLBPitchZone = () => (
  <div className="live-mlb-stadium__pitch-zone live-mlb-pitch-zone" />
);

LiveMLBPitchZone.props = {
  event: React.PropTypes.object.isRequired,
};

export default LiveMLBPitchZone;
