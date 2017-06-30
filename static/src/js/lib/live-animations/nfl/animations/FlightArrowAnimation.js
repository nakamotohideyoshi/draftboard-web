import TweenLite from 'gsap';
import LiveAnimation from '../../LiveAnimation';
import FlightArrow from '../graphics/FlightArrow';

export default class FlightArrowAnimation extends LiveAnimation {

  play(recap, field, startPt, endPt, flightArc = 150, duration = 1.2) {
    const arrow = new FlightArrow(field, startPt.x, endPt.x, startPt.y, endPt.y, flightArc);

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
