import PlayAnimation from '../../../lib/live-animations/nba/PlayAnimation';
import NBACourt from '../../../lib/live-animations/nba/NBACourt';
import NBAPlayRecapVO from '../../../lib/live-animations/nba/NBAPlayRecapVO';
import { generateBlockNameWithModifiers } from '../../../lib/utils/bem';
import log from '../../../lib/logging';
import React from 'react';
import Raven from 'raven-js';
import {
  removeCurrentEvent,
  shiftOldestEvent,
  showAnimationEventResults,
} from '../../../actions/events';
import store from '../../../store';

// assets
require('../../../../sass/blocks/live/nba/live-nba-court.scss');

// get custom logger for actions
const logComponent = log.getLogger('component');


/**
 * The court in the middle of the page
 */
export default React.createClass({
  propTypes: {
    event: React.PropTypes.object.isRequired,
  },

  getInitialState() {
    return {
      modifiers: [],
    };
  },

  componentDidMount() {
    this.court = new NBACourt(this.refs.liveNbaCourt);
    this.simulate();
  },

  simulate() {
    const { event } = this.props;

    logComponent.debug('liveNBACourt.simulate', event);

    // TEMP REMOVE ALL EXISTING ELEMENTS
    this.court.removeAll();

    let curAnimation = new PlayAnimation();
    curAnimation.play(new NBAPlayRecapVO(event), this.court).then(() => {
      curAnimation = null;
      this.court.removeAll();

      logComponent.debug('liveNBACourt.simulate complete');

      return this.afterEvent(event);
    }).catch(error => {
      // Log the request error to Sentry with some info.
      Raven.captureMessage(
        'Live animation failed',
        { extra: {
          event,
          curAnimation,
        },
      });

      curAnimation = null;
      this.court.removeAll();
      logComponent.error('LiveNBACourt.curAnimation error', error);

      this.afterEvent(event);
    });
  },

  afterEvent(event) {
    // show the results, remove the animation
    store.dispatch(showAnimationEventResults(event));

    // remove the event
    setTimeout(() => {
      store.dispatch(removeCurrentEvent());
    }, 4000);

    // // enter the next item in the queue once everything is done
    setTimeout(() => {
      store.dispatch(shiftOldestEvent());
    }, 6000);
  },

  render() {
    const classNames = generateBlockNameWithModifiers('live-nba-court', this.state.modifiers);
    return (
      <section className={classNames} ref="liveNbaCourt" />
    );
  },
});

