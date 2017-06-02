import LiveAnimation from '../LiveAnimation';
import { getQBClip, getReceptionClip } from './getClip';
import NFLPlayRecapVO from './NFLPlayRecapVO';

export default class PlayerAnimation extends LiveAnimation {

  getPlayerClip(type, recap) {
    switch (type) {
      case 'quarterback' :
        return getQBClip(recap.playFormation(), recap.qbAction(), recap.side());
      case 'reception':
        return getReceptionClip(recap.passType(), recap.side(), recap.isTurnover());
      default:
        return null;
    }
  }

  getYardline(type, recap) {
    if (type === 'quarterback') {
      return recap.startingYardLine();
    }

    if (type === 'reception') {
      return recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT
        ? recap.startingYardLine() + recap.passingYards()
        : recap.startingYardLine() - recap.passingYards();
    }

    return 0;
  }

  getSide(type, recap) {
    return type === 'quarterback'
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
