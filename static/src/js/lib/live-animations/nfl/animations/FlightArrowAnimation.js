import TweenLite from 'gsap';
import FlightArrow from '../graphics/FlightArrow';

export default class FlightArrowAnimation {

  play(recap, field, startPt, endPt, options) {
    const {
      arc = 150,
      duration = 1.5,
      startOffsetY = 0,
      endOffsetY = 0,
    } = options;

    const arrow = new FlightArrow(field, startPt, endPt, arc, startOffsetY, endOffsetY);

    field.addChild(arrow.el, 0, 0, 30);

    return new Promise(resolve => {
      TweenLite.from(arrow, duration, {
        progress: 0,
        ease: 'none',
        onComplete: () => resolve(),
      });
    });
  }
}
