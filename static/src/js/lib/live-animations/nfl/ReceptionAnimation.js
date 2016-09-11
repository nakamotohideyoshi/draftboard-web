import LiveAnimation from '../LiveAnimation';
import NFLPlayRecapVO from './NFLPlayRecapVO';
import { getReceptionClip } from './getClip';
import Sprite from '../Sprite';

export default class ReceptionAnimation extends LiveAnimation {

  /**
   * Returns the yard line the reception occurred at.
   * @return {number}
   */
  getReceptionYardLine(recap) {
    if (recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT) {
      return recap.startingYardLine() + recap.passDistance();
    }

    return recap.startingYardLine() - recap.passDistance();
  }

  /**
   * Plays the reception animation.
   * @param {NFLPlayRecapVO}   The recap data.
   * @param {NFLField}         The field of play.
   * @return {Promise}
   */
  play(recap, field) {
    const clip = getReceptionClip(recap.passType(), recap.side(), recap.isTurnover());
    const file = `/nfl/live-animations/${clip.file}`;
    return (new Sprite()).load(file, clip.width, clip.height)
    .then(sprite => {
      // Set the X position to where the player catches the ball
      // by setting the initial position to the point of the
      // catch then nudging the position based on the clips's
      // X offset.
      const yardLine = this.getReceptionYardLine(recap);

      // Flip the sequence based on the drive direction. The natural
      // orientation of sequences is "left to right".
      const flipAnimation = recap.driveDirection() === NFLPlayRecapVO.RIGHT_TO_LEFT;

      // Select a color for the sequence based on which side is
      // earning points.
      const color = clip.colors[recap.whichSide()];

      if (!color) {
        throw new Error(`Color variant for "${recap.whichSide()}" not defined for "${clip.file}"`);
      }

      // Get the sprite's offset position based on the clips's
      // pre-defined offset.
      const offsetY = clip.offset_y * 0.5;
      let offsetX = clip.offset_x * 0.5;

      if (flipAnimation) {
        offsetX = (clip.width - clip.offset_x) * 0.5;
      }

      field.addChildAtYardLine(sprite.getElement(), yardLine, recap.side(), offsetX, offsetY);

      return sprite.playOnce(flipAnimation, color.start, clip.length);
    });
  }
}
