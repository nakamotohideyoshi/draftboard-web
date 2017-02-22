import React from 'react';
import LiveNFLPlay from './live-nfl-play';


// assets
require('../../../../sass/blocks/live/nfl/live-nfl-field.scss');

/**
 * The court in the middle of the page
 */
export default React.createClass({

  propTypes: {
    currentEvent: React.PropTypes.object,
  },

  render() {
    const { currentEvent } = this.props;
    const nflPlay = (currentEvent === null) ? null : (
      <LiveNFLPlay
        event={ currentEvent }
      />
    );

    return (
      <section className="live-nfl-field" ref="liveNflField">
        {nflPlay}
      </section>
    );
  },
});
