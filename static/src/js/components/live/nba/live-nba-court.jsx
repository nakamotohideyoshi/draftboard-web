import React from 'react';
import LiveNBAPlay from './live-nba-play';
import {
  removeCurrentEvent,
  shiftOldestEvent,
  showAnimationEventResults,
} from '../../../actions/events';
import store from '../../../store';

// assets
require('../../../../sass/blocks/live/nba/live-nba-court.scss');

/**
 * The court in the middle of the page
 */
export default React.createClass({

  propTypes: {
    animationEvent: React.PropTypes.object,
  },

  getInitialState() {
    return {
      curAnimationEvent: this.props.animationEvent,
    };
  },

  shouldComponentUpdate() {
    return !this.isAnimationPlaying;
  },

  pbpAnimationStarted() {
    this.isAnimationPlaying = true;
  },

  pbpAnimationCompleted() {
    this.isAnimationPlaying = false;

    // show the results, remove the animation
    store.dispatch(showAnimationEventResults(this.props.animationEvent));

    // wait for the results to finish displaying before removing the
    // currentEvent from the queue.
    setTimeout(() => {
      store.dispatch(removeCurrentEvent());
    }, 4000);

    // enter the next item in the queue once everything is done.
    setTimeout(() => {
      store.dispatch(shiftOldestEvent());
    }, 6000);
  },

  render() {
    const liveNBAPlay = this.props.animationEvent === null
      ? null
      : <LiveNBAPlay
        key={ this.props.animationEvent.id }
        event={ this.props.animationEvent }
        animationStarted={ this.pbpAnimationStarted }
        animationCompleted={ this.pbpAnimationCompleted }
      />;

    return (
      <section className="live-nba-court">
        { liveNBAPlay }
      </section>
    );
  },
});
