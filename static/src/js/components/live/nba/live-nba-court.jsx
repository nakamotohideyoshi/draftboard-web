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
    currentEvent: React.PropTypes.object,
    onAnimationComplete: React.PropTypes.func,
    onAnimationStart: React.PropTypes.func,
  },

  shouldComponentUpdate(nextProps) {
    const curEventId = this.props.currentEvent ? this.props.currentEvent.id : null;
    const newEventId = nextProps.currentEvent ? nextProps.currentEvent.id : null;
    return curEventId !== newEventId;
  },

  componentDidUpdate() {
    if (!this.props.currentEvent) {
      return;
    }

    // Simulate the current currentEvent.
    const court = new NBACourt(this.refs.court);
    const recap = new NBAPlayRecapVO(this.props.currentEvent);
    const animation = new PlayAnimation();

    this.animationStarted();

    animation.play(recap, court).catch(error =>
      Raven.captureMessage('Live animation failed', {
        extra: {
          message: error.message,
          currentEvent: this.props.currentEvent,
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
