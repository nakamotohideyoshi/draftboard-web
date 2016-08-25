import LiveAnimation from './LiveAnimation';
import NFLPlayRecapVO from './NFLPlayRecapVO';
import { getReceptionClip } from './getClip';
import Sprite from './Sprite';

/**
* ...
*/
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

  play(recap, field) {
    const clip = getReceptionClip(recap.passType(), recap.side(), recap.isTurnover(), recap.whichSide());
    const file = clip.colors[recap.whichSide()];
    const sprite = new Sprite();
    const flipAnimation = recap.driveDirection() === NFLPlayRecapVO.RIGHT_TO_LEFT;

    return sprite.load(`/nfl/animations/${file}`, clip.frame_width, clip.frame_height)
    .then(() => {
      // Set the X position to where the player catches the ball
      // by setting the initial position to the point of the
      // catch then nudging the position based on the clips's
      // X offset.
      const yardLine = this.getReceptionYardLine(recap);

      // Get the sprite's offset position based on the clips's
      // pre-defined offset.
      const offsetY = clip.offset_y * 0.5;
      let offsetX = clip.offset_x * 0.5;

      if (flipAnimation) {
        offsetX = (clip.frame_width - clip.offset_x) * 0.5;
      }

      field.addChildAtYardLine(sprite.getElement(), yardLine, recap.side(), offsetX, offsetY);

      return sprite.playOnce(flipAnimation);
    });
  }
}
