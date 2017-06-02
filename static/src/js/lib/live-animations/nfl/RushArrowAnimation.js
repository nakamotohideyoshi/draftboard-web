import LiveAnimation from '../LiveAnimation';
import NFLPlayRecapVO from './NFLPlayRecapVO';
import RushArrow from './graphics/RushArrow';
import TweenLite from 'gsap';

export default class RushArrowAnimation extends LiveAnimation {

  /**
   * Returns the starting line of the rush.
   * @return {number}
   */
  getRushStartingYardLine(recap) {
    // Define a slight offset to help move the arrow just forward
    // of the previous animation.
    const offsetX = 0.02;

    if (recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT) {
      return recap.startingYardLine() + recap.passingYards() + offsetX;
    }

    return recap.startingYardLine() - recap.passingYards() - offsetX;
  }

  /**
   * Returns the starting line of the rush.
   * @return {number}
   */
  getRushEndingYardLine(recap) {
    return recap.endingYardLine();
  }

  /**
   * Returns the duration of the pass animation in seconds
   * based on the distance of the pass.
   * @return {number}
   */
  getRushDuration(recap) {
    if (recap.rushingYards() <= 0.2) {
      return 0.5;
    } else if (recap.rushingYards() <= 0.4) {
      return 1;
    }

    return 1.5;
  }

  play(recap, field) {
    // Only show the rush arrow when there is visually enough room for
    // the mimimum length of the arrow (3 yards).
    if (recap.isTurnover() || recap.rushingYards() <= 0.03) {
      return Promise.resolve();
    }

    const arrowStart = this.getRushStartingYardLine(recap);
    const arrowEnd = this.getRushEndingYardLine(recap);
    const arrowY = field.getSideOffsetY(recap.side());
    const arrow = new RushArrow(field, arrowStart, arrowEnd, arrowY);

    field.addChild(arrow.el, 0, 0, 20);

    return new Promise(resolve => {
      arrow.progress = 0;
      TweenLite.to(arrow, this.getRushDuration(recap), {
        progress: 1,
        ease: 'Linear',
        onComplete: () => resolve(),
      });
    });
  }
}
