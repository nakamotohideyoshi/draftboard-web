import PlayerAnimation from './PlayerAnimation';
import NFLLiveAnimation from './NFLLiveAnimation';
import YardlineAnimation from './YardlineAnimation';

/**
 * Plays a pass play sequence by connecting a QB animation with a
 * pass arrow, catch, and rush arrow animation, based on the provided
 * play recap.
 */
export default class QuarterbackSackedAnimation extends NFLLiveAnimation {
  play(recap, field) {
    const snapPos = this.getSnapPos(recap, field);
    const sequence = [];

    // Mark the play
    sequence.push(() => {
      const animation = new YardlineAnimation();
      return animation.play(recap, field, snapPos.x, YardlineAnimation.COLOR_LINE_OF_SCRIMAGE);
    });

    // Sack the QB
    sequence.push(() => {
      const animation = new PlayerAnimation();
      return animation.play(recap, field, 'quarterback_sacked');
    });

    return sequence.reduce((p, fn) => p.then(fn), Promise.resolve());
  }
}
