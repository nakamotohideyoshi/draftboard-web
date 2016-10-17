import LiveAnimation from '../LiveAnimation';
import YardLineMarker from './graphics/YardLineMarker';
import TweenLite from 'gsap';

export default class DownLineAnimation extends LiveAnimation {

  play(recap, field) {
    const marker = new YardLineMarker(field, recap.endingYardLine());
    const markerEl = field.addChild(marker.el, 0, 0, 1);

    return new Promise(resolve => {
      TweenLite.from(markerEl, 0.25, {
        opacity: 0,
        ease: 'none',
        onComplete: () => resolve(),
      });
    });
  }
}
