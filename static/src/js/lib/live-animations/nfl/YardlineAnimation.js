import LiveAnimation from '../LiveAnimation';
import YardLineMarker from './graphics/YardLineMarker';
import TweenLite from 'gsap';

export default class YardlineAnimation extends LiveAnimation {

  play(recap, field, yardline, color = '#00FF00') {
    const marker = new YardLineMarker(field, yardline, color);
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
