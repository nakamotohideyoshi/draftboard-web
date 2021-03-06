import { Timeline } from '../../utils/animate';
import NFLPlayRecapVO from '../NFLPlayRecapVO';
import FlightArrow from '../graphics/FlightArrow';
import NFLLiveAnimation from './NFLLiveAnimation';
import PlayerAnimation from './PlayerAnimation';
import RushArrowAnimation from './RushArrowAnimation';
import YardlineAnimation from './YardlineAnimation';

export default class PassingPlayAnimation extends NFLLiveAnimation {

  /**
   * Returns the field position of the throw.
   */
  getThrowPos(recap, field) {
    return {
      x: recap.startingYardLine(),
      y: field.getSideOffsetY(NFLPlayRecapVO.MIDDLE),
    };
  }

  /**
   * Returns the amount of "arc" the passing arrow should depict based on the
   * pass type. The bigger the pass the bigger the arc.
   */
  getPassArc(recap) {
    // Set a min and max arc. The arc's height is also going to be limited by
    // the width/height of the containing SVG (defined inside of the PassArrow
    // class.)
    const maxArc = 240;
    const minArc = 5;
    return Math.max(minArc, Math.min(maxArc, maxArc * recap.passingYards()));
  }

  /**
   * Returns the duration of the pass in seconds based on it's distance.
   */
  getPassDuration(recap) {
    if (recap.passingYards() >= 0.4) {
      return 1.4;
    } else if (recap.passingYards() >= 0.3) {
      return 1.2;
    } else if (recap.passingYards() >= 0.2) {
      return 1;
    }

    return 0.6;
  }

  /**
   * Returns the field position of the reception.
   */
  getCatchPos(recap, field) {
    const y = field.getSideOffsetY(recap.side());
    let x = recap.driveDirection() === NFLPlayRecapVO.RIGHT_TO_LEFT
    ? recap.startingYardLine() - recap.passingYards()
    : recap.startingYardLine() + recap.passingYards();

    // Force TDs into the endzone.
    if (recap.isTouchdown() && recap.rushingYards() === 0) {
      x = recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT ? 1.04 : -0.05;
    }

    return { x, y };
  }

  /**
   * Returns a promise containing the QB, ball, and receiver animations.
   */
  animatePassToReceiver(recap, field) {
    const quarterback = new PlayerAnimation();
    const receiver = new PlayerAnimation();

    const loadClips = () => Promise.all([
      quarterback.load(recap, field, 'quarterback'),
      receiver.load(recap, field, 'reception'),
    ]);

    return loadClips().then(() => {
      const timeline = new Timeline();
      const ballDuration = this.getPassDuration(recap) * 30;
      const throwCP = quarterback._clip.clip.getCuepoint('pass');
      const catchCP = receiver._clip.clip.getCuepoint('catch');

      // Quarterback snaps the ball
      timeline.add(quarterback.getSequence(1, quarterback._clip, timeline));

      // Fly the ball
      const qbClip = quarterback._clip.clip;
      const qbEl = qbClip.getElement().parentNode;
      const qbX = parseInt(qbEl.style.left, 10);
      const qbY = parseInt(qbEl.style.top, 10);
      const receiverClip = receiver._clip.clip;
      const receiverEl = receiverClip.getElement().parentNode;
      const receiverX = parseFloat(receiverEl.style.left, 10);
      const receiverY = parseFloat(receiverEl.style.top, 10);

      const ballStart = {
        x: qbX,
        y: qbY + throwCP.data.y * 0.5,
      };

      const ballEnd = {
        x: receiverX,
        y: receiverY + catchCP.data.y * 0.5,
      };

      if (recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT) {
        ballStart.x += throwCP.data.x * 0.5;
        ballEnd.x += catchCP.data.x * 0.5;
      } else {
        ballStart.x += qbClip.frameWidth * 0.5 - throwCP.data.x * 0.5;
        ballEnd.x += receiverClip.frameWidth * 0.5 - catchCP.data.x * 0.5;
      }

      const ball = new FlightArrow(field, ballStart, ballEnd, this.getPassArc(recap), 0, 0);
      ball.progress = 0;
      field.addChild(ball.el, 0, 0, 30);

      timeline.add({
        from: throwCP.in,
        length: ballDuration,
        onUpdate: (frame, len) => (ball.progress = frame / len),
      });

      // Receiver catches ball.
      const catchIn = throwCP.in + ballDuration - catchCP.in + 1;
      timeline.add(receiver.getSequence(catchIn, receiver._clip, timeline));

      return new Promise(resolve => {
        timeline.play(resolve);
      });
    });
  }

  /**
   * Plays a pass play sequence by connecting a QB animation with a
   * pass arrow, catch, and rush arrow animation, based on the provided
   * play recap.
   */
  play(recap, field) {
    const snapPos = this.getSnapPos(recap, field);
    const downPos = this.getDownPos(recap, field);
    const sequence = [];

    // Mark the play
    sequence.push(() => {
      const animation = new YardlineAnimation();
      const color = YardlineAnimation.COLOR_LINE_OF_SCRIMAGE;
      return animation.play(recap, field, snapPos.x, color);
    });

    // Pass and catch the ball
    sequence.push(() =>
      this.animatePassToReceiver(recap, field)
    );

    if (!recap.isIncompletePass()) {
      // Rush after catch (but only if it's more than a few yards)
      sequence.push(() => {
        const animation = new RushArrowAnimation();
        const catchPos = this.getCatchPos(recap, field);
        const rushEnd = recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT
        ? catchPos.x + recap.rushingYards()
        : catchPos.x - recap.rushingYards();
        return animation.play(recap, field, catchPos.x, rushEnd, catchPos.y);
      });

      // Complete the play
      if (!recap.isTouchdown()) {
        sequence.push(() => {
          // Down the ball
          const animation = new YardlineAnimation();
          const color = YardlineAnimation.COLOR_DOWN_LINE;
          return animation.play(recap, field, downPos.x, color);
        });
      }
    }

    return sequence.reduce((p, fn) => p.then(fn), Promise.resolve());
  }
}
