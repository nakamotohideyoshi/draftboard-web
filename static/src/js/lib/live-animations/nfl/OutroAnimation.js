import LiveAnimation from '../LiveAnimation';
import TweenLite from 'gsap';

export default class OutroAnimation extends LiveAnimation {

  play(recap, field) {
    return new Promise((resolve) => {
      TweenLite.to(field.children(), 0.5, {
        delay: 0.5,
        opacity: 0,
        ease: 'Sine.easeOut',
        onComplete: () => {
          field.removeAll();
          resolve();
        },
      });
    });
  }
}
