import React from 'react';
import round from 'lodash/round';

import { percentageHexColor } from '../../lib/utils/colors';
import { describeArc } from '../../lib/utils/shapes';


/**
 * Reusable PMR progress bar using SVG
 */
const LivePMRProgressBar = (props) => {
  const { colors, decimalRemaining, id, strokeDecimal, svgWidth } = props;

  if (decimalRemaining === 0) return null;
  if (strokeDecimal === 0) return null;

  const decimalDone = 1 - decimalRemaining;
  const [backgroundHex, hexStart, hexEnd] = colors;
  const strokeWidth = round(svgWidth * strokeDecimal, 1);
  const svgMidpoint = svgWidth / 2;
  const radius = (svgWidth - strokeWidth) / 2;

  const svgProps = {
    viewBox: `0 0 ${svgWidth} ${svgWidth}`,
    translate: `translate(${svgMidpoint}, ${svgMidpoint})`,
  };

  const backgroundCircleProps = {
    r: svgWidth / 2,
    stroke: `#${backgroundHex}`,
    strokeWidth,
  };

  const progressArc = {
    hexStart: `#${hexStart}`,
    hexHalfway: `#${percentageHexColor(hexStart, hexEnd, 0.5)}`,
    hexEnd: `#${hexEnd}`,
    d: describeArc(0, 0, radius, decimalDone * 360, 360),
    strokeWidth,
  };

  return (
    <svg className="pmr" viewBox={svgProps.viewBox}>
      <defs>
        <linearGradient id={`cl1-${id}`} gradientUnits="objectBoundingBox" x1="0" y1="0" x2="0" y2="1">
          <stop stopColor={progressArc.hexEnd} />
          <stop offset="100%" stopColor={progressArc.hexHalfway} />
        </linearGradient>
        <linearGradient id={`cl2-${id}`} gradientUnits="objectBoundingBox" x1="0" y1="1" x2="0" y2="0">
          <stop stopColor={progressArc.hexHalfway} />
          <stop offset="100%" stopColor={progressArc.hexStart} />
        </linearGradient>
      </defs>

      <g transform={svgProps.translate}>
        <circle
          r={backgroundCircleProps.r}
          fill="none"
        />

        <mask id={`gradientMask-${id}`}>
          <path fill="none" stroke="#fff" strokeWidth={progressArc.strokeWidth} d={progressArc.d}></path>
        </mask>
        <g mask={`url(#gradientMask-${id})`}>
          <rect
            x={-svgMidpoint}
            y={-svgMidpoint}
            width={svgMidpoint}
            height={svgWidth}
            fill={`url(#cl2-${id})`}
          />
          <rect
            x="0"
            y={-svgMidpoint}
            height={svgWidth}
            width={svgMidpoint}
            fill={`url(#cl1-${id})`}
          />
        </g>
      </g>
    </svg>
  );
};

LivePMRProgressBar.propTypes = {
  colors: React.PropTypes.array,
  decimalRemaining: React.PropTypes.number.isRequired,
  id: React.PropTypes.string.isRequired,
  strokeDecimal: React.PropTypes.number,
  svgWidth: React.PropTypes.number.isRequired,
};

LivePMRProgressBar.defaultProps = {
  decimalRemaining: 0,
  strokeDecimal: 0.05,
};

export default LivePMRProgressBar;
