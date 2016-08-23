import React from 'react';

import LiveNBACourtShooter from './live-nba-court-shooter';


/**
 * The court in the middle of the page
 */
const LiveNBACourt = (props) => {
  const { animationEvent } = props;
  const currentEvent = (animationEvent === null) ? null : (
    <LiveNBACourtShooter
      event={ animationEvent }
      key={ animationEvent.id }
    />
  );

  return (
    <section className="live__court live-nba-court">
      { currentEvent }
    </section>
  );
};

LiveNBACourt.propTypes = {
  animationEvent: React.PropTypes.object,
};

export default LiveNBACourt;
