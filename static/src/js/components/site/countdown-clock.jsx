import React from 'react'
import {timeRemaining} from '../../lib/utils.js'


/**
 * A countdown timer that updates itself.
 */
let CountdownClock = React.createClass({

  updateInterval: 1000,


  propTypes: {
    time: React.PropTypes.any
  },


  getInitialState: function() {
    return {
      timeRemaining: {}
    }
  },


  componentWillMount: function() {
    this.updateTimeRemainingLoop = window.setInterval(this.setTimeRemaining, this.updateInterval);
  },


  componentWillUnmount: function() {
    window.clearInterval(this.updateTimeRemainingLoop)
  },


  setTimeRemaining: function() {
    if (!this.props.time) {
      return
    }

    // difference between when the contest starts and now.
    this.setState({
      timeRemaining: timeRemaining(this.props.time)
    })
  },


  render: function() {
    return (
      <span className="cmp-countdown-clock">
        <span className="hours">{this.state.timeRemaining.hours}:</span>
        <span className="minutes">{this.state.timeRemaining.minutes}:</span>
        <span className="seconds">{this.state.timeRemaining.seconds}</span>
      </span>
    )
  }
})


module.exports = CountdownClock
