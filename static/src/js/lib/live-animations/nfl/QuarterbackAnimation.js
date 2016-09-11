import LiveAnimation from '../LiveAnimation';
import NFLPlayRecapVO from './NFLPlayRecapVO';
import { getQBClip } from './getClip';
import Sprite from '../Sprite';

export default class QuarterbackAnimation extends LiveAnimation {

  /**
   * Plays the quarterback animation.
   * @param {NFLPlayRecapVO}   The recap data.
   * @param {NFLField}         The field of play.
   * @return {Promise}
   */
  play(recap, field) {
    const clip = getQBClip(recap.playFormation(), recap.qbAction(), recap.side());
    const file = `/nfl/live-animations/${clip.file}`;
    return (new Sprite()).load(file, clip.width, clip.height)
    .then(sprite => {
      // Set the X position to where the player snaps the ball
      // by setting the initial position to the starting yard line.
      const yardLine = recap.startingYardLine();

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

      field.setYardLine(yardLine);

      field.addChildAtYardLine(sprite.getElement(), yardLine, 'middle', offsetX, offsetY);

      return sprite.playOnce(flipAnimation, color.start, clip.length);
    });
  }
}
