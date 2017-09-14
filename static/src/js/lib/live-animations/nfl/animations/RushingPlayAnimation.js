import NFLLiveAnimation from './NFLLiveAnimation';
import NFLPlayRecapVO from '../NFLPlayRecapVO';
import PlayerAnimation from './PlayerAnimation';
import RushArrowAnimation from './RushArrowAnimation';
import YardlineAnimation from './YardlineAnimation';

export default class RushingPlayAnimation extends NFLLiveAnimation {

  /**
   * Plays a rushing play sequence by connecting a QB animation
   * with a rush arrow animation.
   */
  play(recap, field) {
    const snapPos = this.getSnapPos(recap, field);
    const downPos = this.getDownPos(recap, field);
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

    // Rush for yards
    sequence.push(() => {
      const animation = new RushArrowAnimation();
      return animation.play(recap, field, snapPos.x, downPos.x, snapPos.y);
    });

    // Finish the play
    if (!recap.isTouchdown()) {
      sequence.push(() => {
        // Skip the downline for turnovers/fumbles
        if (recap.isFumble() || recap.isTurnover()) {
          return Promise.resolve();
        }

        // Down the ball
        const animation = new YardlineAnimation();
        return animation.play(recap, field, downPos.x, YardlineAnimation.COLOR_DOWN_LINE);
      });
    }

    return sequence.reduce((p, fn) => p.then(fn), Promise.resolve());
  }
}
