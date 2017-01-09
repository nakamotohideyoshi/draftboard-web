import DebugPlayAnimation from './DebugPlayAnimation';
import PlayerAnimation from './PlayerAnimation';
import LiveAnimation from '../LiveAnimation';
import OutroAnimation from './OutroAnimation';
import log from '../../../lib/logging';

// get custom logger for actions
const logComponent = log.getLogger('component');

export default class PlayAnimation extends LiveAnimation {

  play(recap, court) {
    logComponent.debug('liveNBAPlay.PlayAnimation.play', recap, court);
    const clips = [];

    if (recap._obj.debug) {
      clips.push(() => new DebugPlayAnimation().play(recap, court));
    }

    clips.push(() => new PlayerAnimation().play(recap, court));
    clips.push(() => new OutroAnimation().play(recap, court));

    return clips.reduce((p, fn) => p.then(fn), Promise.resolve());
  }
}
