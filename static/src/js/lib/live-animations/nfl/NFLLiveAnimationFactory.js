import KickReturnAnimation from './animations/KickReturnAnimation';
import NFLField from './NFLField';
import NFLPlayRecapVO from './NFLPlayRecapVO';
import PassingPlayAnimation from './animations/PassingPlayAnimation';
import QuarterbackSackedAnimation from './animations/QuarterbackSackedAnimation';
import RushingPlayAnimation from './animations/RushingPlayAnimation';

export default class NFLLiveAnimationAnimation {

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
   * Plays an NFL animation based on the provided `pbpObj`.
   */
  play(pbpObj, element) {
    const recap = new NFLPlayRecapVO(pbpObj);
    const field = new NFLField(element);
    const animation = this.getAnimation(recap);

    if (!animation) {
      return Promise.reject(`Unsupported animation for type "${recap.playType()}."`);
    }

    return animation.play(recap, field);
  }
}
