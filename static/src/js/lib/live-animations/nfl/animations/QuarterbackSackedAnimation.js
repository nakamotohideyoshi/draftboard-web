import PlayerAnimation from './PlayerAnimation';
import NFLLiveAnimation from './NFLLiveAnimation';
import YardlineAnimation from './YardlineAnimation';

export default class QuarterbackSackedAnimation extends NFLLiveAnimation {

  /**
   * Plays an animation depicting the QB being sacked.
   */
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
