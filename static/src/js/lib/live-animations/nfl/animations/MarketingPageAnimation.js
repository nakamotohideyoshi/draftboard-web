import { Timeline } from '../../utils/animate';
import { merge } from 'lodash';
import Clip from '../../clips/Clip';
import NFLPlayRecapVO from '../NFLPlayRecapVO';
import FlightArrow from '../graphics/FlightArrow';
import YardlineAnimation from './YardlineAnimation';
import { clip as qbClip } from '../clips/qb-shotgun-pass-middle';
import { clip as receiverClip } from '../clips/reception-basket';

export default class MarketingPageAnimation {

  /**
   * The yardline the ball is kicked from.
   */
  getSnapPos(recap, field) {
    // Flip flop the recap's starting yardline to reflect our desired returning
    // teams drive direction. This is neccessary because the recaps `startingYardLine()`
    // is based based on the `start_situation` and not the `end_situation`.
    return {
      x: 0.5,
      y: field.getSideOffsetY(NFLPlayRecapVO.MIDDLE),
    };
  }

  /**
   * The field position the ball is caught at.
   */
  getCatchPos(recap, field) {
    return {
      x: 1,
      y: field.getSideOffsetY(NFLPlayRecapVO.LEFT) };
  }

  /**
   * Returns a promise containing the QB, ball, and receiver animations.
   */
  animatePassToReceiver(recap, field) {
    const quarterback = new Clip(merge(qbClip, {
      // files: { mine: 'something!' },
    }));

    const receiver = new Clip(merge(receiverClip, {
      // files: { mine: 'something!' },
    }));

    const catchPos = this.getCatchPos(recap, field);
    catchPos.x += 0.05;

    const snapPos = this.getSnapPos(recap, field);

    return Promise.all([
      quarterback.load('mine'),
      receiver.load('none'),
    ]).then(() => {
      // Add clips to field
      /* eslint-disable max-len */
      field.addChildAtYardLine(quarterback.getElement(), snapPos.x, snapPos.y, quarterback.registrationX, quarterback.registrationY);
      field.addChildAtYardLine(receiver.getElement(), catchPos.x, catchPos.y, receiver.registrationX, receiver.registrationY);
      /* eslint-enable max-len */

      const timeline = new Timeline();

      // Quarterback snaps the ball
      timeline.add({
        from: 1,
        length: quarterback.length,
        onUpdate: frame => quarterback.goto(frame),
      });

      // Fly the ball
      const throwCP = quarterback.getCuepoint('pass');
      const catchCP = receiver.getCuepoint('avatar');
      const ballDuration = 1.5 * 30;
      const ballPassArc = 120;
      const qbEl = quarterback.getElement().parentNode;
      const qbX = parseInt(qbEl.style.left, 10);
      const qbY = parseInt(qbEl.style.top, 10);
      const receiverEl = receiver.getElement().parentNode;
      const receiverX = parseFloat(receiverEl.style.left, 10);
      const receiverY = parseFloat(receiverEl.style.top, 10);

      const ballStart = {
        x: qbX + throwCP.data.x * 0.5,
        y: qbY + throwCP.data.y * 0.5,
      };

      const ballEnd = {
        x: receiverX + catchCP.data.x * 0.5,
        y: receiverY + catchCP.data.y * 0.5,
      };

      const ball = new FlightArrow(field, ballStart, ballEnd, ballPassArc, 0, 0);
      ball.progress = 0;
      field.addChild(ball.el, 0, 0, 30);

      // Ball flys across screen
      timeline.add({
        from: throwCP.in,
        length: ballDuration,
        onUpdate: (frame, len) => (ball.progress = frame / len),
      });

      // Receiver catches ball.
      const catchIn = throwCP.in + ballDuration - catchCP.in + 1;
      timeline.add({
        from: catchIn,
        length: receiver.length,
        onUpdate: frame => receiver.goto(frame),
      });

      return new Promise(resolve => {
        timeline.play(resolve);
      });
    });
  }

  /**
   * Plays a kick return sequencing showing the ball traveling down field to
   * the receiver, and the receiver running it back based on the recap provided.
   */
  play(recap, field) {
    const snapPos = this.getSnapPos(recap, field);
    const sequence = [];

    // Mark the play
    sequence.push(() => {
      const animation = new YardlineAnimation();
      return animation.play(recap, field, snapPos.x, YardlineAnimation.COLOR_LINE_OF_SCRIMAGE);
    });

    // Throw & Catch the ball
    sequence.push(() => this.animatePassToReceiver(recap, field));

    return sequence.reduce((p, fn) => p.then(fn), Promise.resolve());
  }
}
