"use strict";

var React = require('react');
var ReactCSSTransitionGroup = require('react-addons-css-transition-group');
var renderComponent = require('../../lib/render-component');
var LiveNBAHistoryEvent = require('./live-nba-history-event');


/**
 * The history ticker at the bottom of the live page
 */
var LiveNBAHistory = React.createClass({
  propTypes: {
    whichSide: React.PropTypes.string.isRequired,
    data: React.PropTypes.array.isRequired
  },

  getDefaultProps: function() {
    return {
      whichSide: '',
      data: []
    };
  },

  render: function() {
    // must copy the dataset if you're going to mess with the order
    // eventually this will be a different dataset and we will just reverse in LiveNBAStore before triggering

    var currentEvents = this.props.data.map(function(event) {
      return (
        <LiveNBAHistoryEvent key={event.id} event={event} />
      );
    });

    var className = 'live-history live-history--' + this.props.whichSide + ' live-nba__history';

    return (
      <div className={ className }>
        <ReactCSSTransitionGroup
          transitionEnterTimeout={290}
          transitionLeaveTimeout={290}
          transitionName="event"
          className="live-history__slider">
          {currentEvents}
        </ReactCSSTransitionGroup>
      </div>
    );
  }
});


// Render the component.
renderComponent(<LiveNBAHistory />, '.live-history');

module.exports = LiveNBAHistory;
