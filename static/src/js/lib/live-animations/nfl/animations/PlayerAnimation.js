import LiveAnimation from '../../LiveAnimation';
import NFLPlayRecapVO from '../NFLPlayRecapVO';
import { getKickReturnClip, getQBClip, getReceptionClip, getQBSackedClip } from '../getClip';

export default class PlayerAnimation extends LiveAnimation {

  getPlayerClip(type, recap) {
    switch (type) {
      case 'quarterback' :
        return getQBClip(recap.playFormation(), recap.qbAction(), recap.side());
      case 'quarterback_sacked':
        return getQBSackedClip(recap.playFormation());
      case 'reception':
        return getReceptionClip(recap.passType(), recap.side(), recap.isTurnover());
      case 'kick_return':
        return getKickReturnClip('reception_kick');
      default:
        return null;
    }
  }

  getYardline(type, recap) {
    if (type === 'quarterback' || type === 'quarterback_sacked') {
      return recap.startingYardLine();
    }

    if (type === 'reception') {
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

  /**
   * Plays the quarterback animation.
   * @param {NFLPlayRecapVO}   The recap data.
   * @param {NFLField}         The field of play.
   * @return {Promise}
   */
  play(recap, field, type) {
    const clip = this.getPlayerClip(type, recap);

    if (recap.driveDirection() === NFLPlayRecapVO.RIGHT_TO_LEFT) {
      clip.flipH();
    }

    clip.setPlayers(recap.players(), 'nfl');

    return clip.load(recap.whichSide()).then(() => {
      // Set the X position to where the player snaps the ball
      // by setting the initial position to the starting yard line.
      const yardline = this.getYardline(type, recap);

      const side = this.getSide(type, recap);

      field.setYardLine(yardline);

      field.addChildAtYardLine(clip.getElement(), yardline, side, clip.offsetX, clip.offsetY);

      return clip.play();
    });
  }
}
