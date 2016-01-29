import React from 'react'
import { timeRemaining } from '../../lib/utils.js'


/**
 * A countdown timer that updates itself.
 */
const CountdownClock = React.createClass({


  propTypes: {
    time: React.PropTypes.any,
    onCountdownOver: React.PropTypes.func,
  },


  getInitialState() {
    return {
      timeRemaining: {},
    }
  },


  componentWillMount() {
    this.updateTimeRemainingLoop = window.setInterval(this.setTimeRemaining, this.updateInterval);
  },


  componentWillUnmount() {
    window.clearInterval(this.updateTimeRemainingLoop)
  },


  setTimeRemaining() {
    if (!this.props.time) {
      return
    }

    const timeObj = timeRemaining(this.props.time)

    if (timeObj.expired === true && typeof this.props.onCountdownOver === 'function') {
      this.props.onCountdownOver()
    }

    // difference between when the contest starts and now.
    this.setState({ timeRemaining: timeObj })
  },

  updateInterval: 500,

  render() {
    if (this.state.timeRemaining.expired === true) {
      return (
        <span className="cmp-countdown-clock">
          <span className="hours">Loading...</span>
        </span>
      )
    }

    return (
      <span className="cmp-countdown-clock">
        <span className="hours">{this.state.timeRemaining.hours}:</span>
        <span className="minutes">{this.state.timeRemaining.minutes}:</span>
        <span className="seconds">{this.state.timeRemaining.seconds}</span>
      </span>
    )
  },
})


export default CountdownClock
