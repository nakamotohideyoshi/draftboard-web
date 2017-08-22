import { Timeline } from '../../utils/animate';
import NFLPlayRecapVO from '../NFLPlayRecapVO';
import FlightArrow from '../graphics/FlightArrow';
import NFLLiveAnimation from './NFLLiveAnimation';
import PlayerAnimation from './PlayerAnimation';
import RushArrowAnimation from './RushArrowAnimation';
import YardlineAnimation from './YardlineAnimation';

/**
 * Plays a rushing play sequence by connecting a QB animation
 * with a rush arrow animation.
 */
export default class KickReturnAnimation extends NFLLiveAnimation {

  /**
   * The yardline the ball is kicked from.
   */
  getSnapPos(recap, field) {
    // Flip flop the recap's starting yardline to reflect our desired returning
    // teams drive direction. This is neccessary because the recaps `startingYardLine()`
    // is based based on the `start_situation` and not the `end_situation`.
    return {
      x: 1 - recap.startingYardLine(),
      y: field.getSideOffsetY(NFLPlayRecapVO.MIDDLE),
    };
  }

  /**
   * The field position the ball is caught at.
   */
  getCatchPos(recap, field) {
    let x = recap.endingYardLine();

    if (recap.isTouchback()) {
      x = recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT ? 0 : 1;
    } else if (recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT) {
      x -= recap.rushingYards();
    } else {
      x += recap.rushingYards();
    }

    return { x, y: field.getSideOffsetY(NFLPlayRecapVO.MIDDLE) };
  }

  /**
   * Returns the ending position of return by calculating the distance the
   * receiver runs the ball after the catch.
   */
  getDownPos(recap, field) {
    const catchPos = this.getCatchPos(recap, field);
    const yardline = recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT
    ? catchPos.x + recap.rushingYards()
    : catchPos.x - recap.rushingYards();

    return {
      x: yardline,
      y: field.getSideOffsetY(NFLPlayRecapVO.MIDDLE),
    };
  }

  play(recap, field) {
    const snapPos = this.getSnapPos(recap, field);
    const catchPos = this.getCatchPos(recap, field);
    const downPos = this.getDownPos(recap, field);

    const sequence = [];
    const receiver = new PlayerAnimation();

    sequence.push(() => receiver.load(recap, field, 'kick_return'));

    // Mark the play (only Punts)
    if (recap.playType() === NFLPlayRecapVO.PUNT) {
      sequence.push(() => {
        const animation = new YardlineAnimation();
        return animation.play(recap, field, snapPos.x, YardlineAnimation.COLOR_LINE_OF_SCRIMAGE);
      });
    }

    // Catch the ball
    sequence.push(() => {
      const timeline = new Timeline();

      const catchCP = receiver._clip.clip.getCuepoint('catch');
      const receiverClip = receiver._clip.clip;
      const receiverEl = receiverClip.getElement().parentNode;
      const receiverX = parseFloat(receiverEl.style.left, 10);
      const receiverY = parseFloat(receiverEl.style.top, 10);

      const ballDuration = 1.5 * 30;
      const ballStart = field.getFieldPos(snapPos.x, snapPos.y);
      const ballEnd = {
        x: receiverX,
        y: receiverY + catchCP.data.y * 0.5,
      };

      if (recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT) {
        ballEnd.x += catchCP.data.x * 0.5;
      } else {
        ballEnd.x += receiverClip.frameWidth * 0.5 - catchCP.data.x * 0.5;
      }

      const ball = new FlightArrow(field, ballStart, ballEnd, 220, 0, 0);
      ball.progress = 0;
      field.addChild(ball.el, 0, 0, 30);

      timeline.add({
        from: 1,
        length: ballDuration,
        onUpdate: (frame, len) => (ball.progress = frame / len),
      });

      // Receiver catches ball.
      const catchIn = ballDuration - catchCP.in + 1;
      timeline.add(receiver.getSequence(catchIn, receiver._clip, timeline));

      return new Promise(resolve => timeline.play(resolve));
    });

    // Rush the ball (if they ran with it)
    if (recap.rushingYards() > 0) {
      sequence.push(() => {
        const animation = new RushArrowAnimation();
        return animation.play(recap, field, catchPos.x, downPos.x, catchPos.y);
      });
    }

    // Down the ball
    sequence.push(() => {
      const animation = new YardlineAnimation();
      return animation.play(recap, field, downPos.x, YardlineAnimation.COLOR_DOWN_LINE);
    });

    return sequence.reduce((p, fn) => p.then(fn), Promise.resolve());
  }
}
