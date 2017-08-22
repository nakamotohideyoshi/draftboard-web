import NFLLiveAnimation from './NFLLiveAnimation';
import NFLPlayRecapVO from '../NFLPlayRecapVO';
import PlayerAnimation from './PlayerAnimation';
import RushArrowAnimation from './RushArrowAnimation';
import TouchdownAnimation from './TouchdownAnimation';
import YardlineAnimation from './YardlineAnimation';

/**
 * Plays a rushing play sequence by connecting a QB animation
 * with a rush arrow animation.
 */
export default class RushingPlayAnimation extends NFLLiveAnimation {

  play(recap, field) {
    const snapPos = this.getSnapPos(recap, field);
    const downPos = this.getCarryEndPos(recap, field);
    const sequence = [];

    // Mark the play
    sequence.push(() => {
      const animation = new YardlineAnimation();
      return animation.play(recap, field, snapPos.x, YardlineAnimation.COLOR_LINE_OF_SCRIMAGE);
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
        return animation.play(recap, field, snapPos.x, downPos.x, snapPos.y);
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
      return animation.play(recap, field, downPos.x, YardlineAnimation.COLOR_DOWN_LINE);
    });

    return sequence.reduce((p, fn) => p.then(fn), Promise.resolve());
  }
}
