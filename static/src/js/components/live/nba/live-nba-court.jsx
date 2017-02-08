import Raven from 'raven-js';
import React from 'react';
import PlayAnimation from '../../../lib/live-animations/nba/PlayAnimation';
import NBACourt from '../../../lib/live-animations/nba/NBACourt';
import NBAPlayRecapVO from '../../../lib/live-animations/nba/NBAPlayRecapVO';

// assets
require('../../../../sass/blocks/live/nba/live-nba-court.scss');

/**
 * The court in the middle of the page
 */
export default React.createClass({

  propTypes: {
    animationEvent: React.PropTypes.object,
    onAnimationComplete: React.PropTypes.func,
    onAnimationStart: React.PropTypes.func,
  },

  componentDidUpdate() {
    if (!this.props.animationEvent) {
      return;
    }

    // Simulate the current animationEvent.
    const court = new NBACourt(this.refs.court);
    const recap = new NBAPlayRecapVO(this.props.animationEvent);
    const animation = new PlayAnimation();

    this.animationStarted();

    animation.play(recap, court).catch(error =>
      Raven.captureMessage('Live animation failed', {
        extra: {
          message: error.message,
          animationEvent: this.props.animationEvent,
        },
      })
    ).then(
      () => this.animationCompleted()
    ).catch(
      // ESLint forced catch (catch-or-return).
    );
  },

  animationStarted() {
    if (this.props.onAnimationStart) {
      this.props.onAnimationStart();
    }
  },

  animationCompleted() {
    if (this.props.onAnimationComplete) {
      this.props.onAnimationComplete();
    }
  },

  render() {
    return (
      <section key="court" ref="court" className="live-nba-court" ></section>
    );
  },
});
