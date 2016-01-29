import React from 'react'


/**
 * Helper method to find a middle hex, since we have two semi circles to make an angular gradient on the circle stroke
 *
 * @param  {string} Starting hex string (without the leading #)
 * @param  {string} Ending hex string (without the leading #)
 * @param  {number} What percentage between the two hex strings do we need to return
 * @return {string} The generated hex string
 */
export const percentageHexColor = (start, end, percentage) => {
  const hex = (x) => {
    const strX = x.toString(16)
    return (strX.length == 1) ? '0' + strX : strX
  }

  const r = Math.ceil(parseInt(start.substring(0,2), 16) * percentage + parseInt(end.substring(0,2), 16) * (1-percentage))
  const g = Math.ceil(parseInt(start.substring(2,4), 16) * percentage + parseInt(end.substring(2,4), 16) * (1-percentage))
  const b = Math.ceil(parseInt(start.substring(4,6), 16) * percentage + parseInt(end.substring(4,6), 16) * (1-percentage))

  return hex(r) + hex(g) + hex(b)
}

/**
 * Convert polar coordinates into cartesian
 * - Polar coordinates are when you have an origin x,y coordinate, a radius, and an angle
 * - Cartesian coordinates are where you have an origin x,y coordinate, and then x and y distances to go to
 *
 * Method based on http://goo.gl/yJFZMs
 *
 * @param  {number} The origin x coordinate
 * @param  {number} The origin y coordinate
 * @param  {number} Radius from the origin point
 * @param  {number} Angle of the line created of distance radius from the origin x,y
 * @return {object} Object with x and y distances to go from origin x,y coordinate
 */
export const polarToCartesian = (originX, originY, radius, angleInDegrees) => {
  const angleInRadians = (angleInDegrees-90) * Math.PI / 180.0

  return {
    x: originX + (radius * Math.cos(angleInRadians)),
    y: originY + (radius * Math.sin(angleInRadians))
  }
}

/**
 * Generate svg arc path, based on method from http://goo.gl/yJFZMs
 * @param  {number} Origin x coordinate
 * @param  {number} Origin y coordinate
 * @param  {number} Radius to go from origin x,y
 * @param  {number} Starting angle
 * @param  {number} Ending angle
 * @return {string} Generated arc path used in an svg
 */
export const describeArc = (x, y, radius, startAngle, endAngle) => {
    // determine start and end cartesian paths
    const start = polarToCartesian(x, y, radius, endAngle)
    const end = polarToCartesian(x, y, radius, startAngle)

    // determine the semicircle on which the arc goes, 0 being left 1 being right
    const arcSweep = endAngle - startAngle <= 180 ? "0" : "1"

    return [
      "M", start.x, start.y,
      "A", radius, radius, 0, arcSweep, 0, end.x, end.y
    ].join(" ")
}

/**
 * Reusable PMR progress bar using SVG
 */
const LivePMRProgressBar = React.createClass({

  propTypes: {
    decimalRemaining: React.PropTypes.number.isRequired,
    strokeWidth: React.PropTypes.number.isRequired,
    backgroundHex: React.PropTypes.string.isRequired,
    hexStart: React.PropTypes.string.isRequired,
    hexEnd: React.PropTypes.string.isRequired,
    svgWidth: React.PropTypes.number.isRequired
  },

  render() {
    const { decimalRemaining, strokeWidth, svgWidth } = this.props
    const decimalDone = 1 - decimalRemaining

    if (decimalRemaining === 0) {
      return <div />
    }

    const totalWidth = svgWidth + (2 * strokeWidth)
    const svgMidpoint = totalWidth / 2
    const radius = svgWidth / 2

    const svgProps = {
      viewBox: `0 0 ${totalWidth} ${totalWidth}`,
      translate: `translate(${svgMidpoint}, ${svgMidpoint})`
    }

    const backgroundCircleProps = {
      r: radius,
      stroke: '#' + this.props.backgroundHex,
      strokeWidth: strokeWidth
    }

    const progressArc = {
      hexStart: '#' + this.props.hexStart,
      hexHalfway: '#' + percentageHexColor(this.props.hexStart, this.props.hexEnd, 0.5),
      hexEnd: '#' + this.props.hexEnd,
      d: describeArc(0, 0, radius, decimalDone * 360, 360),
      strokeWidth: strokeWidth
    }

    // sadly react lacks support for svg tags like mask, have to use dangerouslySetInnerHTML to work
    // https://github.com/facebook/react/issues/1657#issuecomment-146905709
    const svgMaskMarkup = {
      __html: `<g mask="url(#gradientMask)">\
        <rect x="-${svgMidpoint}" y="-${svgMidpoint}" width="${svgMidpoint}" height="${totalWidth}" fill="url(#cl2)" />\
        <rect x="0" y="-${svgMidpoint}" height="${totalWidth}" width="${svgMidpoint}" fill="url(#cl1)" /></g>`
    }

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
            <circle
              r={backgroundCircleProps.r}
              stroke={backgroundCircleProps.stroke}
              strokeWidth={backgroundCircleProps.strokeWidth}
              fill="none" />

            <mask id="gradientMask">
              <path fill="none" stroke="#fff" strokeWidth={progressArc.strokeWidth} d={progressArc.d}></path>
            </mask>
            <g dangerouslySetInnerHTML={svgMaskMarkup} />
          </g>
        </svg>
      </div>
    )
  }
})

export default LivePMRProgressBar
