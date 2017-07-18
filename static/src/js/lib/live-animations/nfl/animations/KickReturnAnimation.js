import LiveAnimation from '../../LiveAnimation';
import NFLPlayRecapVO from '../NFLPlayRecapVO';
import FlightArrowAnimation from './FlightArrowAnimation';
import PlayerAnimation from './PlayerAnimation';
import RushArrowAnimation from './RushArrowAnimation';
import YardlineAnimation from './YardlineAnimation';

/**
 * Plays a rushing play sequence by connecting a QB animation
 * with a rush arrow animation.
 */
export default class KickReturnAnimation extends LiveAnimation {

  /**
   * The yardline the ball is kicked from.
   */
  getKickoffPos(recap, field) {
    // Flip flop the recap's starting yardline to reflect our desired returning
    // teams drive direction. This is neccessary because the recaps `startingYardLine()`
    // is based based on the `start_situation` and not the `end_situation`.
    return {
      x: 1 - recap.startingYardLine(),
      y: field.getSideOffsetY(NFLPlayRecapVO.MIDDLE),
    };
  }

  /**
   * The field position the ball is caught at.
   */
  getCatchPos(recap, field) {
    let x = recap.endingYardLine();

    if (recap.isTouchback()) {
      x = recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT ? 0 : 1;
    } else if (recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT) {
      x -= recap.rushingYards();
    } else {
      x += recap.rushingYards();
    }

    return { x, y: field.getSideOffsetY(NFLPlayRecapVO.MIDDLE) };
  }

  /**
   * The field position the ball is downed at.
   */
  getDownPos(recap, field) {
    return {
      x: recap.endingYardLine(),
      y: field.getSideOffsetY(NFLPlayRecapVO.MIDDLE),
    };
  }

  play(recap, field) {
    const kickPos = this.getKickoffPos(recap, field);
    const catchPos = this.getCatchPos(recap, field);
    const downPos = this.getDownPos(recap, field);
    const sequence = [];

    // Mark the play (only Punts)
    if (recap.playType() === NFLPlayRecapVO.PUNT) {
      sequence.push(() => {
        const animation = new YardlineAnimation();
        return animation.play(recap, field, kickPos.x, YardlineAnimation.COLOR_LINE_OF_SCRIMAGE);
      });
    }

    // Kick the ball
    sequence.push(() => {
      const animation = new FlightArrowAnimation();
      const arc = recap.playType() === NFLPlayRecapVO.KICKOFF ? 220 : 150;
      const duration = recap.playType() === NFLPlayRecapVO.KICKOFF ? 2 : 1.5;
      return animation.play(recap, field, kickPos, catchPos, {
        arc,
        duration,
      });
    });

    // Catch the ball
    sequence.push(() => {
      const animation = new PlayerAnimation();
      return animation.play(recap, field, 'kick_return');
    });

    // Rush the ball (if they ran with it)
    if (recap.rushingYards() > 0) {
      sequence.push(() => {
        const animation = new RushArrowAnimation();
        return animation.play(recap, field, catchPos.x, downPos.x, catchPos.y);
      });
    }

    // Down the ball
    sequence.push(() => {
      const animation = new YardlineAnimation();
      return animation.play(recap, field, downPos.x, YardlineAnimation.COLOR_DOWN_LINE);
    });

    return sequence.reduce((p, fn) => p.then(fn), Promise.resolve());
  }
}
