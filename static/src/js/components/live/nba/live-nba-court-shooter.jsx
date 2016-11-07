import React from 'react';
import {
  removeCurrentEvent,
  shiftOldestEvent,
  showAnimationEventResults,
} from '../../../actions/events';
import store from '../../../store';

/**
 * The shooter that appears and disappears. This will be changing to an animation
 */
const LiveNBACourtShooter = React.createClass({

  propTypes: {
    event: React.PropTypes.object.isRequired,
  },

  getInitialState() {
    // needed event props
    const event = this.props.event;
    const xCoord = event.location.coord_x;
    const yCoord = event.location.coord_y;

    // width and height of image
    const imgWidth = 2003;
    const imgHeight = 495;

    // left backcourt x coordinates
    const xTopLeft = 378;

    // right backcourt x coordinates
    const xTopRight = 1633;

    // sidecourts y coordinates
    const yTop = 44;
    const yBottom = 340;

    // distance between the two sidecourts
    const yHeight = yBottom - yTop;

    // API max distances, goes from 0 to max
    const xAPIMax = 1128;
    const yAPIMax = 600;

    // first we convert these into percentages (as decimals)
    const xPercent = (xCoord * (100 / xAPIMax)) / 100;
    const yPercent = (yCoord * (100 / yAPIMax)) / 100;

    // then we figure out where it is height wise on the trapezoid
    // since the top and bottom are parallel we can always figure out the height

    const transposedY = yPercent * yHeight;
    // and from this we can derive the final position from the top
    let finalTop = (transposedY + yTop) / imgHeight;

    // since this is a 45 deg trapezoid, we can deduce that the distance to the left will be the same as top

    // now that we know the transposedY,
    // we can figure out what the x left and x right are and find the transposedXLength
    const transposedXLeft = xTopLeft - transposedY;
    const transposedXRight = xTopRight + transposedY;
    const transposedXLength = transposedXRight - transposedXLeft;

    // and now that we have the length we can find the final left position of the shooter
    let finalLeft = (transposedXLeft + (xPercent * transposedXLength)) / imgWidth;

    // convert from decimal to CSS percentage, and round to nearest hundredth
    finalTop = Math.ceil(finalTop * 10000) / 100;
    finalLeft = Math.ceil(finalLeft * 10000) / 100;

    // Triggered in court component once animation is complete!
    setTimeout(() => {
      // show the results, remove the animation
      store.dispatch(showAnimationEventResults(event));
      store.dispatch(removeCurrentEvent());

      // enter the next item in the queue once everything is done
      setTimeout(() => {
        shiftOldestEvent(event.gameId);
      }, 3000);
    }, 5000);

    return {
      finalLeft,
      finalTop,
    };
  },

  shouldComponentUpdate() {
    return false;
  },

  render() {
    const shooterPositionStyle = {
      left: `${this.state.finalLeft}%`,
      top: `${this.state.finalTop}%`,
    };
    const className = `shooter-position shooter-position--${this.props.event.whichSide}`;

    return (
      <div className={className} style={shooterPositionStyle}>
        <div className="shooter-centered"></div>
      </div>
    );
  },
});


export default LiveNBACourtShooter;
