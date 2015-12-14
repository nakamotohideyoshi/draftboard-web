import React from 'react'
import {forEach as _forEach} from 'lodash'



/**
 * A sparkline graph created from an array of numbers. Used on the draft page for player histories.
 */
var Sparkline = React.createClass({

  chartPixelHeight: 15,
  chartPixelWidth: 45,

  propTypes: {
    points: React.PropTypes.array.isRequired
  },


  getDefaultProps: function() {
    return {
      points: []
    };
  },


  getAverage: function(points) {
    if (!points.length) {
      return 0
    }

    let sum  = points.reduce(function(a, b) {
      return a + b
    })

    return sum / points.length
  },


  findHighest: function(points) {
    let highest
    for(let i of points) {
      if (highest === undefined || i > highest) {highest = i}
    }
    return highest
  },


  findLowest: function(points) {
    let lowest
    for(let i of points) {
      if (lowest === undefined || i < lowest) {lowest = i}
    }
    return lowest
  },


  pointToPixel: function(point, high, low) {
    // We need to offset the point value based on if the lowest point was actually 0.
    point = point - low
    // Default Y value to height of chart (point displayed at bottom of chart)
    let y = this.chartPixelHeight
    // The range is the absolute difference between the highest and lowest point.
    // If you think of the drawn graph, 15 (chartPixelHeight) is the highest, 0 is the lowest.
    // Since we need to make the lowest point 15, and the highest 0, we need to know the range
    // in order to stretch the points out.
    let range = high - low
    // Default this to 0.
    let percentageOfRange = 0

    // Don't try to divide a zero range.
    if (range != 0) {
      percentageOfRange = point / range
    }

    // now that we know what percenage of our range the point is, figure out how many pixels that
    // equates to.
    y = percentageOfRange * this.chartPixelHeight
    // Since we're draing to an svg, we need to flip the coordinates because 0,0 is top left.
    y = this.chartPixelHeight - y

    return y
  },


  drawLine: function(points) {
    // The distance between each plotted point.
    const interval = this.chartPixelWidth / (points.length - 1)
    // The lowest value point.
    const low = this.findLowest(points)
    // The highest value point.
    const high = this.findHighest(points)
    // Average of all points.
    const average = parseInt(this.pointToPixel(this.getAverage(this.props.points), high, low))
    let line = ''
    // Our x axis marker. Gets pushed forward by 1 interval every time a point is plotted.
    let x = 0

    // Loop through each point and determine where it should be plotted, then push it into the line.
    _forEach(points, function(point) {
      // Figure out what pixel the point should be plotted at.
      let y = this.pointToPixel(point, high, low)
      // The first point needs to use the 'move' command.
      if (line === '') {
        line += 'M' + x +',' + y
      }
      // All subsequent points use the draw line command.
      else {
        line +=  'L' + x +',' + y
      }
      // Push the next line over 1 interval point.
      x += interval
    }.bind(this))

    return (
      <g>
        <path
          ref="average"
          stroke="#dddfe3"
          strokeWidth="1" d={'M0,' + average + 'L' + this.chartPixelWidth +',' + average}>
        </path>
        <path
          ref="spark"
          stroke="#2cb776"
          strokeWidth="1"
          fill="none"
          d={line}>
        </path>
      </g>
    )
  },


  render: function() {
    if (this.props.points.length < 1) {
      return (<span className="cmp-sparkline"></span>)
    }
    let sparkine = this.drawLine(this.props.points)

    return (
      <span className="cmp-sparkline">
        <svg height={this.chartPixelHeight + 2} width={this.chartPixelWidth}>
          {sparkine}
        </svg>
      </span>
    )
  }
})


module.exports = Sparkline
