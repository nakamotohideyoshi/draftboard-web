import DownLineAnimation from './DownLineAnimation';
import LiveAnimation from '../LiveAnimation';
import OutroAnimation from './OutroAnimation';
import QuarterbackAnimation from './QuarterbackAnimation';
import RushArrowAnimation from './RushArrowAnimation';

/**
* Plays a rushing play sequence by connecting a QB animation
* with a rush arrow animation.
*/
export default class RushingPlayAnimation extends LiveAnimation {

  play(recap, field) {
    const clips = [];
    clips.push(() => new QuarterbackAnimation().play(recap, field));
    clips.push(() => new RushArrowAnimation().play(recap, field));
    clips.push(() => new DownLineAnimation().play(recap, field));
    clips.push(() => new OutroAnimation().play(recap, field));

    // TODO: Ensure the clip can be fully played before playing, or
    // provide a way of clearing the current animation.
    // TODO: Load all clips fully before playback.
    return clips.reduce((p, fn) => p.then(fn), Promise.resolve());
  }
}
