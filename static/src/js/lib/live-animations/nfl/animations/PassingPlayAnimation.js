import LiveAnimation from '../../LiveAnimation';
import NFLPlayRecapVO from '../NFLPlayRecapVO';
import FlightArrowAnimation from './FlightArrowAnimation';
import PlayerAnimation from './PlayerAnimation';
import RushArrowAnimation from './RushArrowAnimation';
import TouchdownAnimation from './TouchdownAnimation';
import YardlineAnimation from './YardlineAnimation';
import FlashChildrenAnimation from './FlashChildrenAnimation';

/**
 * Plays a pass play sequence by connecting a QB animation with a
 * pass arrow, catch, and rush arrow animation, based on the provided
 * play recap.
 */
export default class PassingPlayAnimation extends LiveAnimation {

  /**
   * Returns the field position where the ball was snapped.
   */
  getSnapPos(recap, field) {
    return {
      x: recap.startingYardLine(),
      y: field.getSideOffsetY(NFLPlayRecapVO.MIDDLE),
    };
  }

  /**
   * Returns the field position of the throw.
   */
  getThrowPos(recap, field) {
    // Shotguns originate a little further back than default formations.
    const xOffset = recap.playFormation() === 'shotgun' ? 0.05 : 0.04;

    // Returns the position of the throw with a slight offset to account for
    // the QB's hand position.
    const x = recap.driveDirection() === NFLPlayRecapVO.RIGHT_TO_LEFT
    ? recap.startingYardLine() + xOffset
    : recap.startingYardLine() - xOffset;

    return { x, y: field.getSideOffsetY(NFLPlayRecapVO.MIDDLE) };
  }

  /**
   * Returns the amount of "arc" the passing arrow should depict based on the
   * pass type. The bigger the pass the bigger the arc.
   */
  getPassArc(recap) {
    // Set a min and max arc. The arc's height is also going to be limited by
    // the width/height of the containing SVG (defined inside of the PassArrow
    // class.)
    const maxArc = 240;
    const minArc = 5;
    return Math.max(minArc, Math.min(maxArc, maxArc * recap.passingYards()));
  }

  /**
   * Returns the duration of the pass in seconds based on it's distance.
   */
  getPassDuration(recap) {
    if (recap.passingYards() >= 0.4) {
      return 1.8;
    } else if (recap.passingYards() >= 0.3) {
      return 1.4;
    } else if (recap.passingYards() >= 0.2) {
      return 1;
    }

    return 0.6;
  }

  /**
   * Returns the field position of the reception.
   */
  getCatchPos(recap, field) {
    const y = field.getSideOffsetY(recap.side());
    const x = recap.driveDirection() === NFLPlayRecapVO.RIGHT_TO_LEFT
    ? recap.startingYardLine() - recap.passingYards()
    : recap.startingYardLine() + recap.passingYards();

    return { x, y };
  }

  /**
   * Returns the field position of the end of the play.
   */
  getDownPos(recap, field) {
    return {
      x: recap.endingYardLine(),
      y: field.getSideOffsetY(recap.side()),
    };
  }

  play(recap, field) {
    const snapPos = this.getSnapPos(recap, field);
    const throwPos = this.getThrowPos(recap, field);
    const catchPos = this.getCatchPos(recap, field);
    const downPos = this.getDownPos(recap, field);
    const sequence = [];

    // Mark the play
    sequence.push(() => {
      const animation = new YardlineAnimation();
      const color = YardlineAnimation.COLOR_LINE_OF_SCRIMAGE;
      return animation.play(recap, field, snapPos.x, color);
    });

    // Snap the ball
    sequence.push(() => {
      const animation = new PlayerAnimation();
      return animation.play(recap, field, 'quarterback');
    });

    // Throw the ball (but only if it's more than a few yards)
    if (recap.passingYards() > 0.03) {
      sequence.push(() => {
        const animation = new FlightArrowAnimation();
        return animation.play(recap, field, throwPos, catchPos, {
          arc: this.getPassArc(recap),
          duration: this.getPassDuration(recap),
        });
      });
    }

    // Catch the ball
    sequence.push(() => {
      const animation = new PlayerAnimation();
      return animation.play(recap, field, 'reception');
    });

    if (recap.isIncompletePass()) {
      sequence.push(() => {
        const animation = new FlashChildrenAnimation();
        return animation.play(recap, field);
      });
    } else {
      // Rush after catch (but only if it's more than a few yards)
      if (recap.rushingYards() > 0.03) {
        sequence.push(() => {
          const animation = new RushArrowAnimation();
          return animation.play(recap, field, catchPos.x, downPos.x, catchPos.y);
        });
      }

      // Complete the play
      sequence.push(() => {
        // Touchdown!
        if (recap.isTouchdown()) {
          return new TouchdownAnimation().play(recap, field);
        }

        // Down the ball
        const animation = new YardlineAnimation();
        const color = YardlineAnimation.COLOR_DOWN_LINE;
        return animation.play(recap, field, downPos.x, color);
      });
    }

    return sequence.reduce((p, fn) => p.then(fn), Promise.resolve());
  }
}
