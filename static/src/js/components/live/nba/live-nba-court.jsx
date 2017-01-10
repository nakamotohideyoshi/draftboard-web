import React from 'react';
import LiveNBAPlay from './live-nba-play';


// assets
require('../../../../sass/blocks/live/nba/live-nba-court.scss');

/**
 * The court in the middle of the page
 */
export default React.createClass({

  propTypes: {
    animationEvent: React.PropTypes.object,
  },

  render() {
    const { animationEvent } = this.props;
    const currentEvent = (animationEvent === null) ? null : (
      <LiveNBAPlay
        event={ animationEvent }
      />
    );

    return (
      <section className="live-nba-court" ref="liveNbaCourt">
        {currentEvent}
      </section>
    );
  },
});
