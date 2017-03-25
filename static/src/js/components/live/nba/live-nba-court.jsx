import Raven from 'raven-js';
import React from 'react';
import PlayAnimation from '../../../lib/live-animations/nba/PlayAnimation';
import NBACourt from '../../../lib/live-animations/nba/NBACourt';
import NBAPlayRecapVO from '../../../lib/live-animations/nba/NBAPlayRecapVO';

// assets
require('../../../../sass/blocks/live/nba/live-nba-court.scss');

const DEFAULT_WIDTH = 1280;
const DEFAULT_HEIGHT = 337;

/**
 * The court in the middle of the page
 */
export default React.createClass({

  propTypes: {
    currentEvent: React.PropTypes.object,
    onAnimationComplete: React.PropTypes.func,
    onAnimationStart: React.PropTypes.func,
  },

  getInitialState() {
    return { scale: 1, height: DEFAULT_HEIGHT };
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

    const court = new NBACourt(this.refs.stage);
    const recap = new NBAPlayRecapVO(this.props.currentEvent);
    const animation = new PlayAnimation();

    if (this.props.onAnimationStart) {
      this.props.onAnimationStart();
    }

    animation.play(recap, court)
    .catch(error => Raven.capture('Live animation failed', {
      extra: { message: error.message, currentEvent: this.props.currentEvent },
    }))
    .then(() => this.props.onAnimationComplete());
  },

  componentWillUnmount() {
    window.removeEventListener('resize', this.handleWindowResize);
    window.removeEventListener('orientationchange', this.handleWindowResize);
  },

  getScale() {
    const containerWidth = this.refs.container.offsetWidth;
    const originalWidth = DEFAULT_WIDTH;
    const originalHeight = DEFAULT_HEIGHT;
    const scale = containerWidth / originalWidth;

    return {
      scale,
      height: originalHeight * scale,
    };
  },

  handleWindowResize() {
    this.setState(this.getScale);
  },

  render() {
    const courtStyles = {
      width: '1280px',
      height: '337px',
      transformOrigin: '0 top',
      transform: `scale(${this.state.scale})`,
    };

    const containerStyles = {
      width: '100%',
      height: `${this.state.height}px`,
    };

    return (
      <div ref="container" style={containerStyles}>
        <section ref="stage" className="live-nba-court" style={courtStyles}></section>
      </div>
    );
  },
});
