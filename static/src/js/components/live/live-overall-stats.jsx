import React from 'react'
import { vsprintf } from 'sprintf-js'
import _ from 'lodash'

import log from '../../lib/logging'


/**
 * Reusable PMR progress bar using SVG
 */
var LiveOverallStats = React.createClass({
  propTypes: {
    whichSide: React.PropTypes.string.isRequired,
    hasContest: React.PropTypes.bool.isRequired,
    lineup: React.PropTypes.object.isRequired
  },


  // helper method to find a halfway hex, since we have two semi circles to make an angular gradient on the circle stroke
  _percentageHexColor: function(start, end, percentage) {
    var hex = function(x) {
        x = x.toString(16)
        return (x.length == 1) ? '0' + x : x
    }

    var r = Math.ceil(parseInt(start.substring(0,2), 16) * percentage + parseInt(end.substring(0,2), 16) * (1-percentage))
    var g = Math.ceil(parseInt(start.substring(2,4), 16) * percentage + parseInt(end.substring(2,4), 16) * (1-percentage))
    var b = Math.ceil(parseInt(start.substring(4,6), 16) * percentage + parseInt(end.substring(4,6), 16) * (1-percentage))

    return hex(r) + hex(g) + hex(b)
  },


  // http://goo.gl/yJFZMs
  _polarToCartesian: function(centerX, centerY, radius, angleInDegrees) {
    var angleInRadians = (angleInDegrees-90) * Math.PI / 180.0

    return {
      x: centerX + (radius * Math.cos(angleInRadians)),
      y: centerY + (radius * Math.sin(angleInRadians))
    }
  },


  // http://goo.gl/yJFZMs
  _describeArc: function(x, y, radius, startAngle, endAngle) {
      var start = this._polarToCartesian(x, y, radius, endAngle)
      var end = this._polarToCartesian(x, y, radius, startAngle)

      var arcSweep = endAngle - startAngle <= 180 ? "0" : "1"

      var d = [
          "M", start.x, start.y,
          "A", radius, radius, 0, arcSweep, 0, end.x, end.y
      ].join(" ")

      return d
  },


  render: function() {
    let hexStart, hexEnd
    const lineup = this.props.lineup

    switch (this.props.whichSide) {
      case 'mine':
        hexStart = '34B4CC'
        hexEnd = '2871AC'
        break
      case 'opponent':
        hexStart = 'e33c3c'
        hexEnd = '871c5a'
        break
    }

    // TODO props
    var strokeWidth = 2
    var decimalRemaining = lineup.decimalRemaining
    var backgroundHex = '#0c0e16'
    var svgWidth = 280

    var svgMidpoint = svgWidth / 2
    var radius = (svgWidth - 40) / 2

    var backgroundCircle = {
      r: radius - (strokeWidth / 2),
      stroke: backgroundHex,
      strokeWidth: strokeWidth + 26
    }

    var progressArc = {
      hexStart: '#' + hexStart,
      hexHalfway: '#' + this._percentageHexColor(hexStart, hexEnd, 0.5),
      hexEnd: '#' + hexEnd,
      d: this._describeArc(0, 0, radius, decimalRemaining * 360, 360),
      strokeWidth: strokeWidth
    }

    var dottedRemainingArc = {
      strokeWidth: strokeWidth + 3,
      d: this._describeArc(0, 0, radius, 0, decimalRemaining * 360)
    }

    // sadly react lacks support for svg tags like mask, have to use dangerouslySetInnerHTML to work
    // https://github.com/facebook/react/issues/1657#issuecomment-146905709
    var svgMaskMarkup = {
      __html: vsprintf('<g mask="url(#gradientMask)"><rect x="-%d" y="-%d" width="%d" height="%d" fill="url(#cl2)" /><rect x="0" y="-%d" height="%d" width="%d" fill="url(#cl1)" /></g>',[
        svgMidpoint,
        svgMidpoint,
        svgMidpoint,
        svgWidth,
        svgMidpoint,
        svgWidth,
        svgMidpoint
      ])
    }

    var endpointCoord = this._polarToCartesian(0, 0, radius, decimalRemaining * 360)
    var endOuter = {
      r: strokeWidth + 6,
      stroke: '#' + this._percentageHexColor(hexEnd, hexStart, decimalRemaining),
      strokeWidth: strokeWidth,
      fill: backgroundHex,
      cx: endpointCoord.x,
      cy: endpointCoord.y
    }

    var endInner = {
      r: strokeWidth,
      cx: endpointCoord.x,
      cy: endpointCoord.y
    }

    // log.debug('LiveOverallStats', progressArc, dottedRemainingArc, endOuter, endInner)

    let potentialEarnings = 0
    if (this.props.hasContest === false) {
      potentialEarnings = lineup.totalPotentialEarnings
    } else {
      potentialEarnings = lineup.potentialEarnings
    }

    if (potentialEarnings !== 0) {
      potentialEarnings = potentialEarnings.toFixed(2)
    }


    return (
      <div className="live-overall-stats live-overall-stats--me">

        <svg className="pmr-circle" viewBox="0 0 280 280" width="220">
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

          <g transform="translate(140, 140)">
            <circle r={backgroundCircle.r} stroke={backgroundCircle.stroke} strokeWidth={backgroundCircle.strokeWidth} fill="none"></circle>

            <mask id="gradientMask">
              <path fill="none" stroke="#fff" strokeWidth={progressArc.strokeWidth} d={progressArc.d}></path>
            </mask>
            <g dangerouslySetInnerHTML={svgMaskMarkup} />

            <path fill="none" stroke="#3f4255" strokeWidth={dottedRemainingArc.strokeWidth} strokeLinecap="round" strokeDasharray="0.01, 16" d={dottedRemainingArc.d}></path>

            <g className="progress-endpoint">
              <circle
                stroke={endOuter.stroke}
                strokeWidth={endOuter.strokeWidth}
                fill={endOuter.fill}
                r={endOuter.r}
                cx={endOuter.cx}
                cy={endOuter.cy} />
              <circle
                stroke="none"
                fill="#fff"
                r={endInner.r}
                cx={endInner.cx}
                cy={endInner.cy} />
            </g>
          </g>
        </svg>

        <section className="live-overview live-overview--lineup">
          <div className="live-overview__points">
            <div className="live-overview__help">
              Points
            </div>
            <h4 className="live-overview__quantity">{ _.round(lineup.points, 0) }</h4>
          </div>
          <div className="live-overview__potential-earnings">${ potentialEarnings }</div>
          <div className="live-overview__pmr">
            <div className="live-overview__pmr__quantity">{ lineup.minutesRemaining }</div>
            <div className="live-overview__pmr__title">PMR</div>
          </div>
        </section>
      </div>
    )
  }
})

module.exports = LiveOverallStats
