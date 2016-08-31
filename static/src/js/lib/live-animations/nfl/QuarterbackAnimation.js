import LiveAnimation from './LiveAnimation';
import NFLPlayRecapVO from './NFLPlayRecapVO';
import { getQBClip } from './getClip';
import Sprite from './Sprite';

/**
* ...
*/
export default class QuarterbackAnimation extends LiveAnimation {

  play(recap, field) {
    const clip = getQBClip(recap.playFormation(), recap.qbAction(), recap.side());
    const file = clip.colors[recap.whichSide()];
    const sprite = new Sprite();
    const flipAnimation = recap.driveDirection() === NFLPlayRecapVO.RIGHT_TO_LEFT;

    return sprite.load(`/nfl/animations/${file}`, clip.frame_width, clip.frame_height)
    .then(() => {
      // Set the X position to where the player snaps the ball
      // by setting the initial position to the starting yard line.
      const yardLine = recap.startingYardLine();

      // Get the sprite's offset position based on the clips's
      // pre-defined offset.
      const offsetY = clip.offset_y * 0.5;
      let offsetX = clip.offset_x * 0.5;

      if (flipAnimation) {
        offsetX = (clip.frame_width - clip.offset_x) * 0.5;
      }

      field.addChildAtYardLine(sprite.getElement(), yardLine, 'middle', offsetX, offsetY);

      return sprite.playOnce(flipAnimation);
    });
  }
}
