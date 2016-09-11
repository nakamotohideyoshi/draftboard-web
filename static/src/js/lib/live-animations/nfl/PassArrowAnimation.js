import LiveAnimation from '../LiveAnimation';
import NFLPlayRecapVO from './NFLPlayRecapVO';
import PassArrow from './graphics/PassArrow';

/**
 * ...
 */
export default class PassArrowAnimation extends LiveAnimation {

  /**
   * Returns the amount of "arc" the passing arrow should depict based
   * on the pass type. The bigger the pass the bigger the arc.
   */
  getPassArc(recap) {
    // Set a min and max arc. The arc's height is also going to be
    // limited by the width/height of the containing SVG (defined
    // inside of the PassArrow class.)
    const maxArc = 250;
    const minArc = 10;
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

  play(recap, field) {
    const arrowStart = field.getYardLine();
    const arrowEnd = this.getReceptionYardLine(recap);
    const arrowArc = this.getPassArc(recap);
    const arrowEndY = field.getSideOffsetY(recap.side());
    const arrowStartY = field.getSideOffsetY(NFLPlayRecapVO.MIDDLE);
    const arrow = new PassArrow(field, arrowStart, arrowEnd, arrowStartY, arrowEndY, arrowArc);

    field.addChild(arrow.el, 0, 0, 30);

    return super.play(recap, field);
  }
}
