import React from 'react';

import LiveNBACourtShooter from'./live-nba-court-shooter';


/**
 * The court in the middle of the page
 */
const LiveNBACourt = React.createClass({
  propTypes: {
    animationEvents: React.PropTypes.object.isRequired,
    liveSelector: React.PropTypes.object.isRequired,
  },

  render() {
    const self = this;
    const currentEvents = Object.keys(self.props.animationEvents).map((key) => {
      const event = self.props.animationEvents[key];

      return (
        <LiveNBACourtShooter
          event={ event }
          key={ event.id }
        />
      );
    });

    return (
      <section className="cmp-live__court live-nba-court">
        { currentEvents }
      </section>
    );
  },
});

export default LiveNBACourt;
