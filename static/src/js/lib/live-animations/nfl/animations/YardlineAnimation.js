import LiveAnimation from '../../LiveAnimation';
import YardLineMarker from '../graphics/YardLineMarker';
import TweenLite from 'gsap';

export default class YardlineAnimation extends LiveAnimation {

  static get COLOR_DOWN_LINE() {
    return '#bdcc1a';
  }

  static get COLOR_LINE_OF_SCRIMAGE() {
    return '#072ea1';
  }

  play(recap, field, yardline, color = '#00FF00') {
    const marker = new YardLineMarker(field, yardline, color);
    const markerEl = field.addChild(marker.el, 0, 0, 1);
    markerEl.style.opacity = 0;

    return new Promise(resolve => {
      TweenLite.to(markerEl, 0.5, {
        opacity: 1,
        ease: 'none',
        onComplete: () => resolve(),
      });
    });
  }
}
