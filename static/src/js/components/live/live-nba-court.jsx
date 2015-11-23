import React from 'react'

import LiveNBACourtShooter from'./live-nba-court-shooter'


/**
 * The court in the middle of the page
 */
var LiveNBACourt = React.createClass({
  render: function() {
    // var currentEvents = Object.keys(LiveNBAStore.data.courtEvents).map(function(key) {
    // var event = LiveNBAStore.data.courtEvents[key];

    //   return (
    //     <LiveNBACourtShooter key={ event.id } x={ event.location.coord_x } y={ event.location.coord_y } />
    //   );
    // });

    // { currentEvents }
    return (
      <section className="cmp-live__court live-nba-court">
      </section>
    );
  }
});


module.exports = LiveNBACourt;
