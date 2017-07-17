import Raven from 'raven-js';
import React from 'react';
import LiveAnimationFactory from '../../lib/live-animations/LiveAnimationFactory';

// assets
require('../../../sass/blocks/live/live-animation-stage.scss');

const STAGE_SIZES = {
  nba: { width: 1280, height: 337 },
  nfl: { width: 1326, height: 337 },
  nhl: { width: 1300, height: 374 },
};

/**
 * The court in the middle of the page
 */
export default React.createClass({

  propTypes: {
    sport: React.PropTypes.oneOf(['nba', 'nfl', 'nhl']),
    currentEvent: React.PropTypes.object,
    onAnimationStarted: React.PropTypes.func,
  },

  getInitialState() {
    const { width, height } = STAGE_SIZES[this.props.sport];

    return {
      scale: 1,
      stageOriginalWidth: width,
      stageOriginalHeight: height,
      containerScaledHeight: height,
    };
  },

  componentDidMount() {
    window.addEventListener('resize', this.handleWindowResize);
    window.addEventListener('orientationchange', this.handleWindowResize);
    this.handleWindowResize();
  },

  componentDidUpdate() {
    const { currentEvent, onAnimationStarted } = this.props;

    if (currentEvent === null || currentEvent.id === this.eventId) {
      return;
    }

    this.eventId = currentEvent.id;

    const playCurrentAnimation = (resolve) => {
      const animation = new LiveAnimationFactory();
      animation.play(currentEvent, this.refs.stage)
      .catch(error => (
        Raven.captureMessage('Live animation failed', {
          extra: {
            message: error.message,
            currentEvent: this.props.currentEvent,
          },
        })
      ))
      .then(() => Promise.resolve())
      .then(() => resolve());
    };

    if (onAnimationStarted) {
      onAnimationStarted(new Promise(playCurrentAnimation), currentEvent);
    }
  },

  componentWillUnmount() {
    window.removeEventListener('resize', this.handleWindowResize);
    window.removeEventListener('orientationchange', this.handleWindowResize);
  },

  handleWindowResize() {
    const containerWidth = this.refs.container.offsetWidth;
    const scale = containerWidth / this.state.stageOriginalWidth;

    this.setState({ scale });
  },

  render() {
    const courtStyles = {
      width: this.state.stageOriginalWidth,
      height: this.state.stageOriginalHeight,
      transformOrigin: '0 top',
      transform: `scale(${this.state.scale})`,
    };

    const containerStyles = {
      width: '100%',
      height: `${this.state.scale * this.state.stageOriginalHeight}px`,
    };

    const block = 'live-animation-stage';

    return (
      <div ref="container" style={containerStyles}>
        <section ref="stage"
          className={`${block} ${block}--${this.props.sport}`}
          style={courtStyles}
        />
      </div>
    );
  },
});
