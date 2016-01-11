import React from 'react'

import LiveNBACourtShooter from'./live-nba-court-shooter'
import log from '../../lib/logging'


/**
 * The court in the middle of the page
 */
var LiveNBACourt = React.createClass({
  propTypes: {
    courtEvents: React.PropTypes.object.isRequired,
    liveSelector: React.PropTypes.object.isRequired,
    mode: React.PropTypes.object.isRequired
  },

  render() {
    const self = this
    const currentEvents = Object.keys(self.props.courtEvents).map(function(key) {
      const event = self.props.courtEvents[key];

      log.debug('LiveNBACourt.whichSide', event)


      return (
        <LiveNBACourtShooter
          whichSide={ event.whichSide }
          key={ event.id }
          x={ event.location.coord_x }
          y={ event.location.coord_y } />
      );
    });

    { currentEvents }
    return (
      <section className="cmp-live__court live-nba-court">
        { currentEvents }
      </section>
    );
  }
});


module.exports = LiveNBACourt;
