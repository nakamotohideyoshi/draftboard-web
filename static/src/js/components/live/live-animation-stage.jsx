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
    onAnimationComplete: React.PropTypes.func,
    onAnimationStart: React.PropTypes.func,
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
    if (this.props.currentEvent === null || this.props.currentEvent.id === this.eventId) {
      return;
    }

    this.eventId = this.props.currentEvent.id;

    if (this.props.onAnimationStart) {
      this.props.onAnimationStart();
    }

    const animation = new LiveAnimationFactory();
    animation.play(this.props.currentEvent, this.refs.stage)
    .catch(error => {
      console.log('-------------');
      console.log(error);
      console.log('-------------');
    })
    // .catch(error => Raven.captureMessage('Live animation failed', {
    //   extra: { message: error.message, currentEvent: this.props.currentEvent },
    // }))
    .then(() => this.props.onAnimationComplete());
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
