import DownLineAnimation from './DownLineAnimation';
import LiveAnimation from './LiveAnimation';
import OutroAnimation from './OutroAnimation';
import PassArrowAnimation from './PassArrowAnimation';
import ReceptionAnimation from './ReceptionAnimation';
import RushArrowAnimation from './RushArrowAnimation';
import QuarterbackAnimation from './QuarterbackAnimation';
import log from '../../logging.js';


// get custom logger for actions
const logLib = log.getLogger('lib');

/**
 * Plays a pass play sequence by connecting a QB animation with a
 * pass arrow, catch, and rush arrow animation, based on the provided
 * play recap.
 */
export default class PassingPlayAnimation extends LiveAnimation {

  play(recap, field) {
    logLib.debug('PassingPlayAnimation.play', recap);

    const clips = [];
    clips.push(() => new QuarterbackAnimation().play(recap, field));
    clips.push(() => new PassArrowAnimation().play(recap, field));
    clips.push(() => new ReceptionAnimation().play(recap, field));
    clips.push(() => new RushArrowAnimation().play(recap, field));
    clips.push(() => new DownLineAnimation().play(recap, field));
    clips.push(() => new OutroAnimation().play(recap, field));

    // TODO: Load all clips fully before playback.
    // TODO: Ensure the clip can be fully played before playing, or
    // provide a way of clearing the current animation.

    return clips.reduce((p, fn) => p.then(fn), Promise.resolve());
  }
}
