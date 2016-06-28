import React from 'react';
import { generateBlockNameWithModifiers } from '../../lib/utils/bem';
import { timeRemaining } from '../../lib/utils';

// assets
require('../../../sass/blocks/site/countdown-clock.scss');


/**
 * A countdown timer that updates itself.
 */
const CountdownClock = React.createClass({


  propTypes: {
    modifiers: React.PropTypes.array,
    onCountdownOver: React.PropTypes.func,
    time: React.PropTypes.any,
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
    const block = 'cmp-countdown-clock';
    const classNames = generateBlockNameWithModifiers(block, this.props.modifiers || []);

    if (this.state.timeRemaining.hours === undefined) {
      return (
        <div className={classNames}>
          <span className="hours">&nbsp;</span>
        </div>
      );
    }

    return (
      <div className={classNames}>
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
