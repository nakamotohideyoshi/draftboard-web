import { flipOperator } from '../utils/flipPos';
import LiveAnimation from '../LiveAnimation';
import NFLPlayRecapVO from './NFLPlayRecapVO';
import PassArrow from './graphics/PassArrow';
import TweenLite from 'gsap';

export default class PassArrowAnimation extends LiveAnimation {

  /**
   * Returns the amount of "arc" the passing arrow should depict based
   * on the pass type. The bigger the pass the bigger the arc.
   */
  getPassArc(recap) {
    // Set a min and max arc. The arc's height is also going to be
    // limited by the width/height of the containing SVG (defined
    // inside of the PassArrow class.)
    const maxArc = 240;
    const minArc = 5;
    return Math.max(minArc, Math.min(maxArc, maxArc * recap.passDistance()));
  }

  /**
   * Returns the yard line the reception occurred at.
   * @return {number}
   */
  getReceptionYardLine(recap) {
    if (recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT) {
      return recap.startingYardLine() + recap.passDistance();
    }

    return recap.startingYardLine() - recap.passDistance();
  }

  /**
   * Returns the duration of the pass animation in seconds
   * based on the distance of the pass.
   * @return {number}
   */
  getPassDuration(recap) {
    if (recap.passDistance() <= 0.2) {
      return 0.25;
    } else if (recap.passDistance() <= 0.4) {
      return 0.8;
    }

    return 1.2;
  }

  getStartPos(recap, field) {
    const isFlipped = recap.driveDirection() === NFLPlayRecapVO.RIGHT_TO_LEFT;
    return {
      x: flipOperator(recap.startingYardLine(), '-', 0.04, isFlipped),
      y: field.getSideOffsetY(NFLPlayRecapVO.MIDDLE),
    };
  }

  getEndPos(recap, field) {
    const isFlipped = recap.driveDirection() === NFLPlayRecapVO.RIGHT_TO_LEFT;
    return {
      x: flipOperator(this.getReceptionYardLine(recap), '-', 0.04, isFlipped),
      y: field.getSideOffsetY(recap.side()) - 0.05,
    };
  }

  play(recap, field) {
    const startPos = this.getStartPos(recap, field);
    const endPos = this.getEndPos(recap, field);
    const arc = this.getPassArc(recap);
    console.log(startPos);
    const arrow = new PassArrow(field, startPos.x, endPos.x, startPos.y, endPos.y, arc);

    field.addChild(arrow.el, 0, 0, 30);

    return new Promise(resolve => {
      arrow.progress = 0;
      TweenLite.to(arrow, this.getPassDuration(recap), {
        progress: 1,
        ease: 'none',
        onComplete: () => resolve(),
      });
    });
  }
}
