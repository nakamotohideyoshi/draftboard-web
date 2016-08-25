import LiveAnimation from './LiveAnimation';
import PassingPlayAnimation from './PassingPlayAnimation';
import RushingPlayAnimation from './RushingPlayAnimation';
import log from '../../logging.js';


// get custom logger for actions
const logLib = log.getLogger('lib');


/**
 * ...
 */
export default class NFLLivePlayAnimation extends LiveAnimation {

  /**
   * Returns a Live Animation based on the provided recap.
   * @param {NFLPlayRecapVO}  The recap.
   */
  getAnimation(recap) {
    if (recap.isPassingPlay()) {
      return new PassingPlayAnimation();
    }

    if (recap.isRushingPlay()) {
      return new RushingPlayAnimation();
    }

    logLib.warn('NFLLivePlayAnimation.getAnimation - type not found', recap);
    return null;
  }

  /**
   * Plays the provided recap.
   * @param {NFLPlayRecapVO}  The recap.
   * @param {NFLField}    Field of play.
   */
  play(recap, field) {
    const animation = this.getAnimation(recap);

    if (!animation) {
      return Promise.reject('Unknown animation.');
    }

    return animation.play(recap, field);
  }
}
