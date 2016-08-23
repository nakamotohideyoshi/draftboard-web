import React from 'react';
import LiveNFLPlay from './live-nfl-play';


// assets
require('../../../../sass/blocks/live/nfl/live-nfl-field.scss');

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
      <LiveNFLPlay
        event={ animationEvent }
      />
    );

    return (
      <section className="live-nfl-field" ref="liveNflField">
        {currentEvent}
      </section>
    );
  },
});
