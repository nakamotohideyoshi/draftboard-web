import TweenLite from 'gsap';
import RushArrow from '../graphics/RushArrow';

export default class RushArrowAnimation {

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
    let arrowStop = endingYardline;

    if (recap.rushingYards() === 0) {
      return Promise.resolve();
    }

    // You need at least 2 yards to successfully draw the arrow.
    // Unless it's TD... if it's a TD we force the arrow.
    if (recap.rushingYards() < 0.02 && !recap.isTouchdown()) {
      return Promise.resolve();
    }

    // Do not show the arrow during a turn-over, it would be confusing.
    if (recap.isTurnover()) {
      return Promise.resolve();
    }

    // Force the arrow into the endzone during TDs.
    if (recap.isTouchdown()) {
      arrowStop = startingYardline < endingYardline ? 1.04 : -0.04;
    }

    const arrow = new RushArrow(field, startingYardline, arrowStop, fieldY);
    arrow.progress = 0;
    field.addChild(arrow.el, 0, 0, 20);

    return new Promise(resolve => {
      TweenLite.to(arrow, this.getDuration(startingYardline, arrowStop), {
        progress: 1,
        ease: 'Linear',
        onComplete: () => resolve(),
      });
    });
  }
}
