import LiveAnimation from '../LiveAnimation';
import OutroAnimation from './OutroAnimation';
import PlayerAnimation from './PlayerAnimation';
import RushArrowAnimation from './RushArrowAnimation';
import YardlineAnimation from './YardlineAnimation';
import TouchdownAnimation from './TouchdownAnimation';

const COLOR_LINE_OF_SCRIMAGE = '#072ea1';
const COLOR_DOWN_LINE = '#bdcc1a';

/**
* Plays a rushing play sequence by connecting a QB animation
* with a rush arrow animation.
*/
export default class RushingPlayAnimation extends LiveAnimation {

  play(recap, field) {
    const clips = [];
    clips.push(() => new YardlineAnimation().play(recap, field, recap.startingYardLine(), COLOR_LINE_OF_SCRIMAGE));
    clips.push(() => new PlayerAnimation().play(recap, field, 'quarterback'));
    clips.push(() => new RushArrowAnimation().play(recap, field));

    if (recap.isTouchdown()) {
      clips.push(() => new TouchdownAnimation().play(recap, field));
    } else {
      clips.push(() => new YardlineAnimation().play(recap, field, recap.endingYardLine(), COLOR_DOWN_LINE));
    }

    clips.push(() => new OutroAnimation().play(recap, field));

    return clips.reduce((p, fn) => p.then(fn), Promise.resolve());
  }
}
