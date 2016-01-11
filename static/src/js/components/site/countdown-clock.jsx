import React from 'react'
import {timeRemaining} from '../../lib/utils.js'


/**
 * A countdown timer that updates itself.
 */
let CountdownClock = React.createClass({

  updateInterval: 500,


  propTypes: {
    time: React.PropTypes.any,
    onCountdownOver: React.PropTypes.func
  },


  getInitialState: function() {
    return {timeRemaining: {}}
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

    if (!this.state.timeRemaining.seconds) {
      return (
        <span className="cmp-countdown-clock">&nbsp;</span>
      )
    }

    if (
      typeof this.props.onCountdownOver !== 'undefined' &&
      !this.state.timeRemaining.seconds &&
      !this.state.timeRemaining.minutes &&
      !this.state.timeRemaining.hours
    ) {
      this.props.onCountdownOver()
      return null
    }

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
