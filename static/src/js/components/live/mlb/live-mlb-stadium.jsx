import { extend as _extend } from 'lodash';
import React from 'react';

import LiveMLBPitchZone from './live-mlb-pitch-zone';


/**
 * The court in the middle of the page
 */
const LiveMLBStadium = (props) => (
  <section className="cmp-live__mlb-stadium live-mlb-stadium">
    {React.createElement(
      LiveMLBPitchZone, _extend({}, props)
    )}
  </section>
);

LiveMLBStadium.propTypes = {
  animationEvents: React.PropTypes.object.isRequired,
  multipartEvents: React.PropTypes.object.isRequired,
};

export default LiveMLBStadium;
