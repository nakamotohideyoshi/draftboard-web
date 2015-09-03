"use strict";

var React = require('react');
var Reflux = require('reflux');
var LiveNBACourtShooter = require('./live-nba-court-shooter');
var LiveNBAStore = require("../../stores/live-nba-store");

/**
 * The court in the middle of the page
 */
var LiveNBACourt = React.createClass({
  getInitialState: function() {
  },

  mixins: [
    Reflux.connect(LiveNBAStore)
  ],

  render: function() {
    var currentEvents = Object.keys(LiveNBAStore.data.courtEvents).map(function(key) {
      var event = LiveNBAStore.data.courtEvents[key];

      return (
        <LiveNBACourtShooter key={ event.id } x={ event.x } y={ event.y } />
      );
    });

    return (
      <section className="live-nba__court live-nba-court">
        { currentEvents }
      </section>
    );
  }
});


module.exports = LiveNBACourt;
