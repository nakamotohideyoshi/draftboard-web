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
    this.setTimeRemaining();
    this.updateTimeRemainingLoop = window.setInterval(this.setTimeRemaining, 1000);
  },

  componentWillUnmount() {
    window.clearInterval(this.updateTimeRemainingLoop);
  },

  setTimeRemaining() {
    if (!this.props.time) {
      return;
    }

    const timeObj = timeRemaining(this.props.time);

    if (timeObj.expired === true && this.updateTimeRemainingLoop !== null && this.updateTimeRemainingTimeout === null) {
      window.clearInterval(this.updateTimeRemainingLoop);
      this.updateTimeRemainingLoop = null;

      if (typeof this.props.onCountdownOver === 'function') this.props.onCountdownOver();

      return;
    }

    // difference between when the contest starts and now.
    this.setState({ timeRemaining: timeObj });
  },

  updateTimeRemainingTimeout: null,

  render() {
    if (this.state.timeRemaining.hours === undefined) {
      return (
        <div className="cmp-countdown-clock">
          <span className="hours">&nbsp;</span>
        </div>
      );
    }

    return (
      <div className="cmp-countdown-clock">
        <div className="hours">
          <span>{this.state.timeRemaining.hours}</span>
          <span>:</span>
        </div>
        <div className="minutes">
          <span>{this.state.timeRemaining.minutes}</span>
          <span>:</span>
        </div>
        <div className="seconds">
          <span>{this.state.timeRemaining.seconds}</span>
        </div>
      </div>
    );
  },
});


export default CountdownClock;
