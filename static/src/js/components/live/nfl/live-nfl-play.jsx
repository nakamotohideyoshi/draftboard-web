import Field from '../../../lib/live-animations/nfl/NFLField';
import NFLLivePlayAnimation from '../../../lib/live-animations/nfl/NFLLivePlayAnimation';
import NFLPlayRecapVO from '../../../lib/live-animations/nfl/NFLPlayRecapVO';
import { generateBlockNameWithModifiers } from '../../../lib/utils/bem';
import React from 'react';
import log from '../../../lib/logging';
import {
  removeCurrentEvent,
  shiftOldestEvent,
  showAnimationEventResults,
} from '../../../actions/events';
import store from '../../../store';

// assets
require('../../../../sass/blocks/live/nfl/live-nfl-play.scss');

// get custom logger for actions
const logComponent = log.getLogger('component');


/**
 * LiveNFLPlay component
 * - loops through animationEvent and maps them to LiveNFLFieldAnimations
 * - when an animation is done, calls onAnimationComplete to show event results and remove from queue
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
    this.field = new Field(this.refs.liveNflPlay);
    // this.updateMenu(passEvent);
    this.simulate();
  },

  toggleDebugMode() {
    let { modifiers } = this.state;
    modifiers = ('debug' in modifiers) ? [] : ['debug'];
    this.setState({ modifiers });
  },

  simulate() {
    const { event } = this.props;

    const curAnimation = new NFLLivePlayAnimation();
    curAnimation.play(new NFLPlayRecapVO(event), this.field).then(() => {
      // show the results, remove the animation
      store.dispatch(showAnimationEventResults(event));
      store.dispatch(removeCurrentEvent());

      // enter the next item in the queue once everything is done
      setTimeout(() => {
        store.dispatch(shiftOldestEvent());
      }, 3000);
    }).catch(error => {
      logComponent.error('LiveNFLField.curAnimation error', error);
    });
  },

  render() {
    const classNames = generateBlockNameWithModifiers('live-nfl-play', this.state.modifiers);
    return (
      <section className={classNames} ref="liveNflPlay" />
    );
  },
});
