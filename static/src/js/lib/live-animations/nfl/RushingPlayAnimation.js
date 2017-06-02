import LiveAnimation from '../LiveAnimation';
import OutroAnimation from './OutroAnimation';
import PlayerAnimation from './PlayerAnimation';
import RushArrowAnimation from './RushArrowAnimation';
import YardlineAnimation from './YardlineAnimation';

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
    clips.push(() => new YardlineAnimation().play(recap, field, recap.endingYardLine(), COLOR_DOWN_LINE));
    clips.push(() => new OutroAnimation().play(recap, field));

    // TODO: Ensure the clip can be fully played before playing, or
    // provide a way of clearing the current animation.
    // TODO: Load all clips fully before playback.
    return clips.reduce((p, fn) => p.then(fn), Promise.resolve());
  }
}
