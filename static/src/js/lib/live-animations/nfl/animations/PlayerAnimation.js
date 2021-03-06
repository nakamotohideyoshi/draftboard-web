import { Timeline } from '../../utils/animate';
import NFLPlayRecapVO from '../NFLPlayRecapVO';
import {
  getIncompleteReceptionClip,
  getInterceptionClip,
  getKickReturnClip,
  getQBClip,
  getQBSackClip,
  getReceptionClip,
} from '../getClip';

export default class PlayerAnimation {

  getPlayerClip(type, recap) {
    switch (type) {
      case 'quarterback' :
        return getQBClip(recap.playFormation(), recap.qbAction(), recap.side());
      case 'quarterback_sacked':
        return getQBSackClip(recap.playFormation());
      case 'reception':
        return this.getReceptionClip(recap);
      case 'kick_return':
        return getKickReturnClip('reception_kick');
      default:
        return null;
    }
  }

  getReceptionClip(recap) {
    if (recap.isTurnover()) {
      return getInterceptionClip();
    }

    if (recap.isIncompletePass()) {
      return getIncompleteReceptionClip(recap.passType(), recap.side());
    }

    return getReceptionClip(recap.passType(), recap.side());
  }

  getYardline(type, recap) {
    if (type === 'quarterback' || type === 'quarterback_sacked') {
      return recap.startingYardLine();
    }

    if (type === 'reception') {
      if (recap.isTouchdown() && recap.rushingYards() === 0) {
        return recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT ? 1.04 : -0.04;
      }

      return recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT
        ? recap.startingYardLine() + recap.passingYards()
        : recap.startingYardLine() - recap.passingYards();
    }

    if (type === 'kick_return') {
      if (recap.isTouchback()) {
        return recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT ? 0 : 1;
      }
      return recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT
        ? recap.endingYardLine() - recap.rushingYards()
        : recap.endingYardLine() + recap.rushingYards();
    }

    return 0;
  }

  getSide(type, recap) {
    return type === 'quarterback' || type === 'quarterback_sacked'
    ? NFLPlayRecapVO.MIDDLE
    : recap.side();
  }

  getSequence(from, clip, timeline) {
    return {
      from,
      length: clip._data.length,
      onUpdate: frame => {
        for (let i = 0; i < clip._avatars.length; i++) {
          const avatar = clip._avatars[i];
          if (frame === avatar.in) {
            if (avatar.data.pause) {
              timeline.pause();
            }
            clip.playAvatar(avatar.name).then(() => {
              timeline.resume();
              return clip;
            });
            break;
          }
        }
        clip.goto(frame);
      },
    };
  }

  load(recap, field, type) {
    this._clip = this.getPlayerClip(type, recap);

    if (recap.driveDirection() === NFLPlayRecapVO.RIGHT_TO_LEFT) {
      this._clip.flipH();
    }

    if (window.DEBUG_LIVE_ANIMATIONS_CLIPS) {
      this._clip.debug();
    }

    return this._clip.load(recap.players(), 'nfl').then(() => {
      // Set the X position to where the player snaps the ball
      // by setting the initial position to the starting yard line.
      const yardline = this.getYardline(type, recap);
      const side = this.getSide(type, recap);
      field.setYardLine(yardline);
      field.addChildAtYardLine(this._clip.getElement(), yardline, side, this._clip.offsetX, this._clip.offsetY);
      return this;
    });
  }

  /**
   * Plays the quarterback animation.
   * @param {NFLPlayRecapVO}   The recap data.
   * @param {NFLField}         The field of play.
   * @return {Promise}
   */
  play(recap, field, type) {
    return this.load(recap, field, type).then(() => {
      const timeline = new Timeline();
      timeline.add(this.getSequence(1, this._clip, timeline));
      return new Promise(resolve => timeline.play(resolve));
    });
  }
}
