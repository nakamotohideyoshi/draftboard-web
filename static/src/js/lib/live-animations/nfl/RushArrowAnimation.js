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
    const yards = recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT
    ? recap.startingYardLine() + recap.passingYards()
    : recap.startingYardLine() - recap.passingYards();

    return yards;
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
    } else if (recap.rushingYards() > 1) {
      return 2;
    }

    return 1.5;
  }

  play(recap, field) {
    // Short handoffs do not get an arrow.
    if (recap.qbAction() === NFLPlayRecapVO.HANDOFF_SHORT) {
      return Promise.resolve();
    }

    // You need at least 2 yards to successfully draw the arrow.
    if (recap.rushingYards() < 0.02) {
      return Promise.resolve();
    }

    // Do not show the arrow during a turn-over, it would be confusing.
    if (recap.isTurnover()) {
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
