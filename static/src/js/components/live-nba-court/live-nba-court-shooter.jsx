"use strict";

var React = require('react');
var renderComponent = require('../../lib/render-component');

/**
 * The score ticker on the top of the page.
 */
var LiveNBAShooter = React.createClass({
  getInitialState: function() {
    // example coordinates from the API
    var xCoord = 350;
    var yCoord = 350;

    // width and height of image
    var imgWidth = 2003;
    var imgHeight = 495;

    // left backcourt x coordinates
    var xTopLeft = 358;

    // right backcourt x coordinates
    var xTopRight = 1645;

    // sidecourts y coordinates
    var yTop = 45;
    var yBottom = 350;

    // distance between the two sidecourts
    var yHeight = yBottom - yTop;

    // API max distances, goes from 0 to max
    var xAPIMax = 1128;
    var yAPIMax = 600;

    // first we convert these into percentages (as decimals)
    var xPercent = (xCoord * (100 / xAPIMax)) / 100;
    var yPercent = (yCoord * (100 / yAPIMax)) / 100;

    // then we figure out where it is height wise on the trapezoid
    // since the top and bottom are parallel we can always figure out the height

    var transposedY = yPercent * yHeight;
    // and from this we can derive the final position from the top
    var finalTop = (transposedY + yTop) / imgHeight;

    // since this is a 45 deg trapezoid, we can deduce that the distance to the left will be the same as top

    // now that we know the transposedY, we can figure out what the x left and x right are and find the transposedXLength
    var transposedXLeft = xTopLeft - transposedY;
    var transposedXRight = xTopRight + transposedY;
    var transposedXLength = transposedXRight - transposedXLeft;

    // and now that we have the length we can find the final left position of the shooter
    var finalLeft = (transposedXLeft + (xPercent * transposedXLength)) / imgWidth;

    // convert from decimal to CSS percentage, and round to nearest hundredth
    finalTop = Math.ceil(finalTop * 10000) / 100;
    finalLeft = Math.ceil(finalLeft * 10000) / 100;

    return {
      finalLeft: finalLeft,
      finalTop: finalTop
    };
  },

  render: function() {
    var shooterPositionStyle = {
      left: this.state.finalLeft + '%',
      top: this.state.finalTop + '%'
    };

    return (
      <div className='shooter-position' style={shooterPositionStyle}>
        <div className='shooter-centered'></div>
      </div>
    );
  }

});


// Render the component.
renderComponent(<LiveNBAShooter />, '.live-nba-court');


module.exports = LiveNBAShooter;
