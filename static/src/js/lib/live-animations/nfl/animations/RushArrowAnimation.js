import TweenLite from 'gsap';
import LiveAnimation from '../../LiveAnimation';
import RushArrow from '../graphics/RushArrow';

export default class RushArrowAnimation extends LiveAnimation {

  /**
   * Returns the duration of the animation in seconds based on the length of the arrow.
   */
  getDuration(startingYardline, endingYardline) {
    const dist = startingYardline > endingYardline
    ? startingYardline - endingYardline
    : endingYardline - startingYardline;

    if (dist <= 0.2) {
      return 0.5;
    } else if (dist <= 0.4) {
      return 1;
    } else if (dist > 1) {
      return 2;
    }

    return 1.5;
  }

  play(recap, field, startingYardline, endingYardline, fieldY) {
    // You need at least 2 yards to successfully draw the arrow.
    if (recap.rushingYards() < 0.02) {
      return Promise.resolve();
    }

    // Do not show the arrow during a turn-over, it would be confusing.
    if (recap.isTurnover()) {
      return Promise.resolve();
    }

    const arrow = new RushArrow(field, startingYardline, endingYardline, fieldY);
    arrow.progress = 0;
    field.addChild(arrow.el, 0, 0, 20);

    return new Promise(resolve => {
      TweenLite.to(arrow, this.getDuration(startingYardline, endingYardline), {
        progress: 1,
        ease: 'Linear',
        onComplete: () => resolve(),
      });
    });
  }
}
