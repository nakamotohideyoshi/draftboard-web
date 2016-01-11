import React from 'react'

import { vsprintf } from 'sprintf-js'


/**
 * Reusable PMR progress bar using SVG
 */
var LivePMRProgressBar = React.createClass({
  propTypes: {
    decimalRemaining: React.PropTypes.number.isRequired,
    strokeWidth: React.PropTypes.string.isRequired,
    backgroundHex: React.PropTypes.string.isRequired,
    hexStart: React.PropTypes.string.isRequired,
    hexEnd: React.PropTypes.string.isRequired,
    svgWidth: React.PropTypes.string.isRequired
  },


  // helper method to find a halfway hex, since we have two semi circles to make an angular gradient on the circle stroke
  _percentageHexColor: function(start, end, percentage) {
    var hex = function(x) {
        x = x.toString(16);
        return (x.length == 1) ? '0' + x : x;
    };

    var r = Math.ceil(parseInt(start.substring(0,2), 16) * percentage + parseInt(end.substring(0,2), 16) * (1-percentage));
    var g = Math.ceil(parseInt(start.substring(2,4), 16) * percentage + parseInt(end.substring(2,4), 16) * (1-percentage));
    var b = Math.ceil(parseInt(start.substring(4,6), 16) * percentage + parseInt(end.substring(4,6), 16) * (1-percentage));

    return hex(r) + hex(g) + hex(b);
  },


  // http://goo.gl/yJFZMs
  _polarToCartesian: function(centerX, centerY, radius, angleInDegrees) {
    var angleInRadians = (angleInDegrees-90) * Math.PI / 180.0;

    return {
      x: centerX + (radius * Math.cos(angleInRadians)),
      y: centerY + (radius * Math.sin(angleInRadians))
    };
  },


  // http://goo.gl/yJFZMs
  _describeArc: function(x, y, radius, startAngle, endAngle) {
      var start = this._polarToCartesian(x, y, radius, endAngle);
      var end = this._polarToCartesian(x, y, radius, startAngle);

      var arcSweep = endAngle - startAngle <= 180 ? "0" : "1";

      var d = [
          "M", start.x, start.y,
          "A", radius, radius, 0, arcSweep, 0, end.x, end.y
      ].join(" ");

      return d;
  },


  render: function() {
    // not sure how to pass in these properly as propTypes number and decimal
    var decimalRemaining = parseFloat(this.props.decimalRemaining);
    var strokeWidth = parseInt(this.props.strokeWidth);
    var svgWidth = parseInt(this.props.svgWidth);

    var totalWidth = svgWidth + (2 * strokeWidth);
    var svgMidpoint = totalWidth / 2;
    var radius = svgWidth / 2;

    var svgProps = {
      viewBox: vsprintf('0 0 %d %d', [totalWidth, totalWidth]),
      translate: vsprintf('translate(%d, %d)', [svgMidpoint, svgMidpoint])
    };

    var backgroundCircle = {
      r: radius,
      stroke: '#' + this.props.backgroundHex,
      strokeWidth: strokeWidth
    };

    var progressArc = {
      hexStart: '#' + this.props.hexStart,
      hexHalfway: '#' + this._percentageHexColor(this.props.hexStart, this.props.hexEnd, 0.5),
      hexEnd: '#' + this.props.hexEnd,
      d: this._describeArc(0, 0, radius, decimalRemaining * 360, 360),
      strokeWidth: strokeWidth
    };

    // sadly react lacks support for svg tags like mask, have to use dangerouslySetInnerHTML to work
    // https://github.com/facebook/react/issues/1657#issuecomment-146905709
    var svgMaskMarkup = {
      __html: vsprintf('<g mask="url(#gradientMask)"><rect x="-%d" y="-%d" width="%d" height="%d" fill="url(#cl2)" /><rect x="0" y="-%d" height="%d" width="%d" fill="url(#cl1)" /></g>',[
        svgMidpoint,
        svgMidpoint,
        svgMidpoint,
        totalWidth,
        svgMidpoint,
        totalWidth,
        svgMidpoint
      ])
    };

    return (
      <div className="live-pmr">

        <svg className="pmr" viewBox={svgProps.viewBox}>
          <defs>
            <linearGradient id="cl1" gradientUnits="objectBoundingBox" x1="0" y1="0" x2="0" y2="1">
             <stop stopColor={progressArc.hexEnd} />
             <stop offset="100%" stopColor={progressArc.hexHalfway} />
            </linearGradient>
            <linearGradient id="cl2" gradientUnits="objectBoundingBox" x1="0" y1="1" x2="0" y2="0">
             <stop stopColor={progressArc.hexHalfway} />
             <stop offset="100%" stopColor={progressArc.hexStart} />
            </linearGradient>
          </defs>

          <g transform={svgProps.translate}>
            <circle r={backgroundCircle.r} stroke={backgroundCircle.stroke} strokeWidth={backgroundCircle.strokeWidth} fill="none"></circle>

            <mask id="gradientMask">
              <path fill="none" stroke="#fff" strokeWidth={progressArc.strokeWidth} d={progressArc.d}></path>
            </mask>
            <g dangerouslySetInnerHTML={svgMaskMarkup} />
          </g>
        </svg>
      </div>
    );
  }
});

module.exports = LivePMRProgressBar;
