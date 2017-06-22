import LiveAnimation from '../../LiveAnimation';
import NFLPlayRecapVO from '../NFLPlayRecapVO';
import Rectangle from '../graphics/Rectangle';
import TweenLite from 'gsap';

export default class TouchdownAnimation extends LiveAnimation {

  play(recap, field) {
    const { x, y, w, h } = this.getEndzone(recap);
    const marker = new Rectangle(field, x, y, w, h, '#bdcc1a');
    const markerEl = field.addChild(marker.el, 0, 0, 1);

    return new Promise(resolve => {
      TweenLite.from(markerEl, 0.25, {
        opacity: 0,
        ease: 'none',
        onComplete: () => resolve(),
      });
    });
  }

  getEndzone(recap) {
    const w = 0.073;
    const x = recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT ? 1 : -w;
    const y = 0;
    const h = 1;

    return { x, y, w, h };
  }
}
