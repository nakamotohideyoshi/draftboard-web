import TweenLite from 'gsap';
import LiveAnimation from '../../LiveAnimation';

export default class FlashChildrenAnimation extends LiveAnimation {

  play(recap, field) {
    return new Promise(resolve => {
      const target = field.getElement();
      const duration = 0.4;
      const repeat = 3;

      // Flash the elements on the stage
      TweenLite.to(target, duration, { opacity: 0, repeat, yoyo: true });

      // Bring the elements on the stage back to full opacity
      TweenLite.to(target, duration, { delay: duration * repeat, opacity: 1, onComplete: resolve });
    });
  }
}
