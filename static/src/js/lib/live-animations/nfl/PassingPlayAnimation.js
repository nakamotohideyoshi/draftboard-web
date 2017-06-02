import YardlineAnimation from './YardlineAnimation';
import LiveAnimation from '../LiveAnimation';
import OutroAnimation from './OutroAnimation';
import PassArrowAnimation from './PassArrowAnimation';
import RushArrowAnimation from './RushArrowAnimation';
import PlayerAnimation from './PlayerAnimation';

const COLOR_LINE_OF_SCRIMAGE = '#072ea1';
const COLOR_DOWN_LINE = '#bdcc1a';

/**
 * Plays a pass play sequence by connecting a QB animation with a
 * pass arrow, catch, and rush arrow animation, based on the provided
 * play recap.
 */
export default class PassingPlayAnimation extends LiveAnimation {

  play(recap, field) {
    const clips = [];
    clips.push(() => new YardlineAnimation().play(recap, field, recap.startingYardLine(), COLOR_LINE_OF_SCRIMAGE));
    clips.push(() => new PlayerAnimation().play(recap, field, 'quarterback'));
    clips.push(() => new PassArrowAnimation().play(recap, field));
    clips.push(() => new PlayerAnimation().play(recap, field, 'reception'));
    clips.push(() => new RushArrowAnimation().play(recap, field));
    clips.push(() => new YardlineAnimation().play(recap, field, recap.endingYardLine(), COLOR_DOWN_LINE));
    clips.push(() => new OutroAnimation().play(recap, field));

    return clips.reduce((p, fn) => p.then(fn), Promise.resolve());
  }
}
