import LiveOverallStatsBg from './live-overall-stats-bg';
import Odometer from '../site/odometer';
import ordinal from '../../lib/ordinal.js';
import React from 'react';
import { describeArc, polarToCartesian } from '../../lib/utils/shapes';
import { generateBlockNameWithModifiers } from '../../lib/utils/bem';
import { humanizeCurrency } from '../../lib/utils/currency';
import { percentageHexColor } from '../../lib/utils/colors';

// assets
require('../../../sass/blocks/live/live-overall-stats.scss');

// constants
const BLOCK = 'live-overall-stats';


/**
 * Reusable PMR progress bar using SVG
 */
const LiveOverallStats = React.createClass({

  propTypes: {
    fp: React.PropTypes.number.isRequired,
    id: React.PropTypes.number.isRequired,
    modifiers: React.PropTypes.array.isRequired,
    name: React.PropTypes.string.isRequired,
    potentialWinnings: React.PropTypes.number.isRequired,
    rank: React.PropTypes.number,
    timeRemaining: React.PropTypes.object.isRequired,
    whichSide: React.PropTypes.string.isRequired,
  },

  renderOverallPMR() {
    const { id, timeRemaining, whichSide } = this.props;

    let hexStart = '34B4CC';
    let hexEnd = '2871AC';

    if (whichSide === 'opponent') {
      hexStart = 'e33c3c';
      hexEnd = '871c5a';
    }

    const strokeWidth = 2;
    const decimalDone = 1 - timeRemaining.decimal;
    const backgroundHex = '#0c0e16';
    const svgWidth = 280;

    const svgMidpoint = svgWidth / 2;
    const radius = (svgWidth - 40) / 2;

    const progressArc = {
      hexStart: `#${hexStart}`,
      hexHalfway: `#${percentageHexColor(hexStart, hexEnd, 0.5)}`,
      hexEnd: `#${hexEnd}`,
      d: describeArc(0, 0, radius, decimalDone * 360, 360),
      strokeWidth,
    };

    let renderPMRCircle;

    // as long as the lineup is still active
    if (decimalDone !== 1) {
      const dottedRemainingArc = {
        strokeWidth: strokeWidth + 3,
        d: describeArc(0, 0, radius, 0, decimalDone * 360),
      };

      const endpointCoord = polarToCartesian(0, 0, radius, decimalDone * 360);
      const endOuter = {
        r: strokeWidth + 6,
        stroke: `#${percentageHexColor(hexEnd, hexStart, decimalDone)}`,
        strokeWidth,
        fill: backgroundHex,
        cx: endpointCoord.x,
        cy: endpointCoord.y,
      };

      const endInner = {
        r: strokeWidth,
        cx: endpointCoord.x,
        cy: endpointCoord.y,
      };

      renderPMRCircle = (
        <g>
          <mask id={`gradientMaskOverall-lineup-${id}`}>
            <path
              fill="none"
              stroke="#fff"
              strokeWidth={progressArc.strokeWidth}
              d={progressArc.d}
            />
          </mask>
          <g mask={`url(#gradientMaskOverall-lineup-${id})`}>
            <rect
              x={-svgMidpoint}
              y={-svgMidpoint}
              width={svgMidpoint}
              height={svgWidth}
              fill={`url(#cl2-lineup-${id})`}
            />
            <rect
              x="0"
              y={-svgMidpoint}
              height={svgWidth}
              width={svgMidpoint}
              fill={`url(#cl1-lineup-${id})`}
            />
          </g>

          <path
            fill="none"
            stroke="#3f4255"
            strokeWidth={dottedRemainingArc.strokeWidth}
            strokeLinecap="round"
            strokeDasharray="0.01, 16"
            d={dottedRemainingArc.d}
          />

          <g className="progress-endpoint">
            <circle
              stroke={endOuter.stroke}
              strokeWidth={endOuter.strokeWidth}
              fill={endOuter.fill}
              r={endOuter.r}
              cx={endOuter.cx}
              cy={endOuter.cy}
            />
            <circle
              stroke="none"
              fill="#fff"
              r={endInner.r}
              cx={endInner.cx}
              cy={endInner.cy}
            />
          </g>
        </g>
      );
    }

    return (
      <div className={`${BLOCK}__pmr-circle`}>
        <LiveOverallStatsBg
          decimalRemaining={timeRemaining.decimal}
          diameter={220}
        />
        <svg className={`${BLOCK}__svg-arcs`} viewBox="0 0 280 280" width="220">
          <defs>
            <linearGradient
              id={`cl1-lineup-${id}`}
              gradientUnits="objectBoundingBox"
              x1="0" y1="0" x2="0" y2="1"
            >
             <stop stopColor={progressArc.hexEnd} />
             <stop offset="100%" stopColor={progressArc.hexHalfway} />
            </linearGradient>
            <linearGradient
              id={`cl2-lineup-${id}`}
              gradientUnits="objectBoundingBox"
              x1="0" y1="1" x2="0" y2="0"
            >
             <stop stopColor={progressArc.hexHalfway} />
             <stop offset="100%" stopColor={progressArc.hexStart} />
            </linearGradient>
          </defs>

          <g transform="translate(140, 140)">
            { renderPMRCircle }
          </g>
        </svg>
      </div>
    );
  },

  renderPotentialWinnings() {
    const { id, potentialWinnings, rank } = this.props;

    // default to villian
    let rankStr = '';
    let amountStr = 'N/A';

    // if not villian
    if (id !== 1) {
      amountStr = humanizeCurrency(potentialWinnings || 0);

      // if in contest mode
      if (rank) rankStr = `${ordinal(rank || '')} /`;
    }

    return (
      <div className={`${BLOCK}__potential-winnings`}>
        <span className={`${BLOCK}__rank`}>{rankStr}</span>
        <span className={`${BLOCK}__amount`}>{amountStr}</span>
      </div>
    );
  },

  render() {
    const { fp, modifiers, name, timeRemaining } = this.props;

    return (
      <section className={generateBlockNameWithModifiers(BLOCK, modifiers)}>
        <h1 className={`${BLOCK}__name`}>
          {name}
        </h1>

        {this.renderPotentialWinnings()}

        <div className={`${BLOCK}__circle-stats-container`}>
          {this.renderOverallPMR()}

          <div className={`${BLOCK}__overview`}>
            <div className={`${BLOCK}__fp-container`}>
              <div className={`${BLOCK}__fp-title`}>
                Points
              </div>
              <h4 className={`${BLOCK}__fp`}>
                <Odometer
                  modifiers={['live-overall-stats']}
                  value={fp}
                />
              </h4>
            </div>
            <div className={`${BLOCK}__time-remaining`}>
              <div className={`${BLOCK}__duration`}>{timeRemaining.duration}</div>
              <div className={`${BLOCK}__pmr-title`}>PMR</div>
            </div>
          </div>
        </div>
      </section>
    );
  },
});

export default LiveOverallStats;
