import NFLPlayRecapVO from '../NFLPlayRecapVO';
import LiveAnimation from '../../LiveAnimation';

export default class NFLLiveAnimation extends LiveAnimation {

  /**
   * Returns the field position where the ball was snapped.
   */
  getSnapPos(recap, field) {
    return {
      x: recap.startingYardLine(),
      y: field.getSideOffsetY(NFLPlayRecapVO.MIDDLE),
    };
  }

  /**
   * Returns the down position of the ball. The down position represents where
   * the play ended before any penalties are assessed.
   */
  getDownPos(recap, field) {
    const carry = recap.passingYards() + recap.rushingYards();
    const yardline = recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT
    ? recap.startingYardLine() + carry
    : recap.startingYardLine() - carry;

    return {
      x: yardline,
      y: field.getSideOffsetY(recap.side()),
    };
  }
}
