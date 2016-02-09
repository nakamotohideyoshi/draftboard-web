import React from 'react';

import LiveNBACourtShooter from'./live-nba-court-shooter';


/**
 * The court in the middle of the page
 */
const LiveNBACourt = React.createClass({
  propTypes: {
    courtEvents: React.PropTypes.object.isRequired,
    liveSelector: React.PropTypes.object.isRequired,
  },

  render() {
    const self = this;
    const currentEvents = Object.keys(self.props.courtEvents).map((key) => {
      const event = self.props.courtEvents[key];

      return (
        <LiveNBACourtShooter
          whichSide={ event.whichSide }
          key={ event.id }
          x={ event.location.coord_x }
          y={ event.location.coord_y }
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
