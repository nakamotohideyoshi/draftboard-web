import LiveAnimation from '../../LiveAnimation';
import OutroAnimation from './OutroAnimation';
import PlayerAnimation from './PlayerAnimation';
import YardlineAnimation from './YardlineAnimation';

/**
 * Plays a pass play sequence by connecting a QB animation with a
 * pass arrow, catch, and rush arrow animation, based on the provided
 * play recap.
 */
export default class QuarterbackSackedAnimation extends LiveAnimation {
  play(recap, field) {
    const sequence = [];

    // Mark the play
    sequence.push(() => {
      const animation = new YardlineAnimation();
      return animation.play(recap, field, recap.startingYardLine(), YardlineAnimation.COLOR_LINE_OF_SCRIMAGE);
    });

    // Sack the QB
    sequence.push(() => {
      const animation = new PlayerAnimation();
      return animation.play(recap, field, 'quarterback_sacked');
    });

    // Down the ball
    sequence.push(() => {
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
