import LiveAnimation from '../../LiveAnimation';
import NFLPlayRecapVO from '../NFLPlayRecapVO';
import OutroAnimation from './OutroAnimation';
import PlayerAnimation from './PlayerAnimation';
import RushArrowAnimation from './RushArrowAnimation';
import TouchdownAnimation from './TouchdownAnimation';
import YardlineAnimation from './YardlineAnimation';

/**
* Plays a rushing play sequence by connecting a QB animation
* with a rush arrow animation.
*/
export default class RushingPlayAnimation extends LiveAnimation {

  play(recap, field) {
    const sequence = [];

    // Mark the play
    sequence.push(() => {
      const animation = new YardlineAnimation();
      return animation.play(recap, field, recap.startingYardLine(), YardlineAnimation.COLOR_LINE_OF_SCRIMAGE);
    });

    // Snap the ball
    sequence.push(() => {
      const animation = new PlayerAnimation();
      return animation.play(recap, field, 'quarterback');
    });

    // Rush for yards (except short handoffs)
    if (recap.qbAction() !== NFLPlayRecapVO.HANDOFF_SHORT) {
      sequence.push(() => {
        const animation = new RushArrowAnimation();
        const start = recap.startingYardLine();
        const end = recap.endingYardLine();
        const fieldY = field.getSideOffsetY('middle');
        return animation.play(recap, field, start, end, fieldY);
      });
    }

    // Finish the play
    sequence.push(() => {
      // Skip the downline for turnovers/fumbles
      if (recap.isFumble() || recap.isTurnover()) {
        return Promise.resolve();
      }

      // Touchdown!
      if (recap.isTouchdown()) {
        return new TouchdownAnimation().play(recap, field);
      }

      // Down the ball
      const animation = new YardlineAnimation();
      return animation.play(recap, field, recap.endingYardLine(), YardlineAnimation.COLOR_DOWN_LINE);
    });

    // Clear the field
    sequence.push(() => {
      const animation = new OutroAnimation();
      return animation.play(recap, field);
    });

    return sequence.reduce((p, fn) => p.then(fn), Promise.resolve());
  }
}
