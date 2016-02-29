import React from 'react';
import { timeRemaining } from '../../lib/utils.js';


/**
 * A countdown timer that updates itself.
 */
const CountdownClock = React.createClass({


  propTypes: {
    time: React.PropTypes.any,
    onCountdownOver: React.PropTypes.func,
    timePassedDisplay: React.PropTypes.string,
  },


  getDefaultProps() {
    return {
      timePassedDisplay: 'Loading...',
    };
  },

  getInitialState() {
    return {
      timeRemaining: {},
      countdownOver: false,
    };
  },

  componentDidMount() {
    this.updateTimeRemainingLoop = window.setInterval(this.setTimeRemaining, 1000);
  },

  componentWillUnmount() {
    window.clearInterval(this.updateTimeRemainingLoop);
    window.clearInterval(this.props.onCountdownOver);
  },

  setTimeRemaining() {
    if (!this.props.time) {
      return;
    }

    const timeObj = timeRemaining(this.props.time);

    if (timeObj.expired === true && this.updateTimeRemainingLoop !== null && this.updateTimeRemainingTimeout === null) {
      window.clearInterval(this.updateTimeRemainingLoop);
      this.updateTimeRemainingLoop = null;

      if (typeof this.props.onCountdownOver === 'function') {
        window.setInterval(this.props.onCountdownOver, 5000);
        this.props.onCountdownOver();
      }

      this.setState({
        timeRemaining: timeObj,
      });

      return;
    }

    // difference between when the contest starts and now.
    this.setState({ timeRemaining: timeObj });
  },

  updateTimeRemainingTimeout: null,

  render() {
    if (this.state.timeRemaining.hours === undefined) {
      return (
        <span className="cmp-countdown-clock">
          <span className="hours">&nbsp;</span>
        </span>
      );
    }

    return (
      <span className="cmp-countdown-clock">
        <span className="hours">{this.state.timeRemaining.hours}:</span>
        <span className="minutes">{this.state.timeRemaining.minutes}:</span>
        <span className="seconds">{this.state.timeRemaining.seconds}</span>
      </span>
    );
  },
});


export default CountdownClock;
