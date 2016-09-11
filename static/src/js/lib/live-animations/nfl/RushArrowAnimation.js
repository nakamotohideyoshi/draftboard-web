import LiveAnimation from '../LiveAnimation';
import NFLPlayRecapVO from './NFLPlayRecapVO';
import RushArrow from './graphics/RushArrow';

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
      return recap.startingYardLine() + recap.passDistance() + offsetX;
    }

    return recap.startingYardLine() - recap.passDistance() - offsetX;
  }

  /**
   * Returns the starting line of the rush.
   * @return {number}
   */
  getRushEndingYardLine(recap) {
    return recap.endingYardLine();
  }

  play(recap, field) {
    // Only show the rush arrow when there is visually enough room for
    // the mimimum length of the arrow (3 yards).
    if (recap.isTurnover() || recap.rushDistance() <= 0.03) {
      return Promise.resolve();
    }

    const arrowStart = this.getRushStartingYardLine(recap);
    const arrowEnd = this.getRushEndingYardLine(recap);
    const arrowY = field.getSideOffsetY(recap.side());
    const arrow = new RushArrow(field, arrowStart, arrowEnd, arrowY);

    field.addChild(arrow.el, 0, 0, 20);

    return new Promise(resolve => {
      arrow.progress = 0;
      const tick = () => {
        arrow.progress = arrow.progress + 0.020;

        if (arrow.progress !== 1) {
          window.requestAnimationFrame(tick);
        } else {
          resolve();
        }
      };

      tick();
    });
  }
}
