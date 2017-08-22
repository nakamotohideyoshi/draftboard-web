import LiveAnimation from '../LiveAnimation';
import NFLPlayRecapVO from './NFLPlayRecapVO';
import KickReturnAnimation from './animations/KickReturnAnimation';
import PassingPlayAnimation from './animations/PassingPlayAnimation';
import QuarterbackSackedAnimation from './animations/QuarterbackSackedAnimation';
import RushingPlayAnimation from './animations/RushingPlayAnimation';

export default class NFLLivePlayAnimation extends LiveAnimation {

  /**
   * Returns a Live Animation based on the provided recap.
   * @param {NFLPlayRecapVO}  The recap.
   */
  getAnimation(recap) {
    if (recap.isQBSack()) {
      return new QuarterbackSackedAnimation();
    }

    switch (recap.playType()) {
      case NFLPlayRecapVO.KICKOFF:
      case NFLPlayRecapVO.PUNT:
        return new KickReturnAnimation();
      case NFLPlayRecapVO.PASS:
        return new PassingPlayAnimation();
      case NFLPlayRecapVO.RUSH:
        return new RushingPlayAnimation();
      default:
        return null;
    }
  }

  /**
   * Plays the provided recap.
   * @param {NFLPlayRecapVO}  The recap.
   * @param {NFLField}    Field of play.
   */
  play(recap, field) {
    const animation = this.getAnimation(recap);

    if (!animation) {
      return Promise.reject(`Unsupported animation for type "${recap.playType()}."`);
    }

    return animation.play(recap, field);
  }
}
