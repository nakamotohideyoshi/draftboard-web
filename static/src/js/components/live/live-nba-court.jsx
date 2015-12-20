import React from 'react'

import LiveNBACourtShooter from'./live-nba-court-shooter'


/**
 * The court in the middle of the page
 */
var LiveNBACourt = React.createClass({
  propTypes: {
    courtEvents: React.PropTypes.object.isRequired
  },

  render() {
    const self = this
    const currentEvents = Object.keys(self.props.courtEvents).map(function(key) {
      const event = self.props.courtEvents[key];

      return (
        <LiveNBACourtShooter key={ event.id } x={ event.location.coord_x } y={ event.location.coord_y } />
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
