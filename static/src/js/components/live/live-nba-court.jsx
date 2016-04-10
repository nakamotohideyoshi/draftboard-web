import React from 'react';

import LiveNBACourtShooter from './live-nba-court-shooter';


/**
 * The court in the middle of the page
 */
const LiveNBACourt = (props) => {
  const currentEvents = Object.keys(props.animationEvents).map((key) => {
    const event = props.animationEvents[key];

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
};

LiveNBACourt.propTypes = {
  animationEvents: React.PropTypes.object.isRequired,
  liveSelector: React.PropTypes.object.isRequired,
};

export default LiveNBACourt;
