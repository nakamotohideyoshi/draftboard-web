import LiveAnimation from './LiveAnimation';
import NFLPlayRecapVO from './NFLPlayRecapVO';
import {getQBClip} from './getClip';
import Sprite from './Sprite';

/**
 * ...
 */
export default class QuarterbackAnimation extends LiveAnimation {

    play (recap, field) {

        let clip = getQBClip(recap.playFormation(), recap.qbAction(), recap.side());

        let file = clip.colors[recap.whichSide()];

        let sprite = new Sprite();

        let flipAnimation = recap.driveDirection() == NFLPlayRecapVO.RIGHT_TO_LEFT;

        return sprite.load(`/nfl/animations/${file}`, clip.frame_width, clip.frame_height)
        .then(() => {

            // Set the X position to where the player snaps the ball
            // by setting the initial position to the starting yard line.
            let yardLine = recap.startingYardLine();

            // Get the sprite's offset position based on the clips's
            // pre-defined offset.
            let offsetY = clip.offset_y * .5;
            let offsetX = clip.offset_x * .5;

            if (flipAnimation) {
                offsetX = (clip.frame_width - clip.offset_x) * .5;
            }

            let child = field.addChildAtYardLine(sprite.getElement(), yardLine, 'middle', offsetX, offsetY);

            return sprite.playOnce(flipAnimation);
        });
    }
}
