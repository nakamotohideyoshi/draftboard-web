import DebugPlayAnimation from './DebugPlayAnimation';
import PlayerAnimation from './PlayerAnimation';
import LiveAnimation from '../LiveAnimation';
import OutroAnimation from './OutroAnimation';
import NBAPlayRecapVO from './NBAPlayRecapVO';
import BasketAnimation from './BasketAnimation';

export default class PlayAnimation extends LiveAnimation {

  play(recap, court) {
    const clips = [];

    if (window.DEBUG_LIVE_ANIMATIONS) {
      clips.push(() => new DebugPlayAnimation().play(recap, court));
    }

    clips.push(() => new PlayerAnimation().play(recap, court));

    if (recap.playType() === NBAPlayRecapVO.JUMPSHOT ||
        recap.playType() === NBAPlayRecapVO.FREETHROW) {
      clips.push(() => new BasketAnimation().play(recap, court));
    }

    clips.push(() => new OutroAnimation().play(recap, court));

    return clips.reduce((p, fn) => p.then(fn), Promise.resolve())
      .catch(error => {
        court.removeAll();
        throw new Error(error);
      });
  }
}
