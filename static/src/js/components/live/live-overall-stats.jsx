import ordinal from '../../lib/ordinal.js';
import React from 'react';
import size from 'lodash/size';
import { humanizeFP } from '../../actions/sports';
import { percentageHexColor, polarToCartesian, describeArc } from './live-pmr-progress-bar';

/**
 * Reusable PMR progress bar using SVG
 */
const LiveOverallStats = React.createClass({

  propTypes: {
    contest: React.PropTypes.object.isRequired,
    hasContest: React.PropTypes.bool.isRequired,
    hasOpponent: React.PropTypes.bool.isRequired,
    lineup: React.PropTypes.object.isRequired,
    whichSide: React.PropTypes.string.isRequired,
  },

  componentDidMount() {
    this.updateCanvas();
  },

  componentWillReceiveProps(nextProps) {
    if (nextProps.lineup.timeRemaining.decimal !== this.props.lineup.timeRemaining.decimal) {
      this.updateCanvas();
    }
  },

  updateCanvas() {
    const diameter = 220;
    const decimalRemaining = this.props.lineup.timeRemaining.decimal;
    const radiansRemaining = decimalRemaining * 360 - 180;
    const ctx = this.refs.canvas.getContext('2d');

    // skip update if canvas is not supported (like in tests)
    if (!ctx) return;

    // move to the center
    ctx.translate(diameter / 2, diameter / 2);

    // start the gradient at the point remaining
    ctx.rotate(-radiansRemaining * Math.PI / 180);

    // make sure to cap it so that it's smooth around and the right diameter
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';

    // loop through all 360 degrees and draw a line from the center out
    for (let i = 0; i <= 360; i++) {
      ctx.save();

      // invert the gradient to move from
      ctx.rotate(-Math.PI * i / 180);
      ctx.translate(-ctx.lineWidth / 2, ctx.lineWidth / 2);

      // move to the center
      ctx.beginPath();
      ctx.moveTo(0, 0);

      // top out at 30%, as the comp does
      let percentage = i / 15;
      if (percentage > 40) percentage = 40;

      ctx.strokeStyle = `rgba(0,0,0,${percentage / 100})`;

      // write and close
      ctx.lineTo(0, diameter);
      ctx.stroke();
      ctx.closePath();

      ctx.restore();
    }
  },

  renderOverallPMR() {
    let hexStart;
    let hexEnd;
    const lineup = this.props.lineup;

    switch (this.props.whichSide) {
      case 'opponent':
        hexStart = 'e33c3c';
        hexEnd = '871c5a';
        break;
      default:
        hexStart = '34B4CC';
        hexEnd = '2871AC';
        break;
    }

    const strokeWidth = 2;
    const decimalDone = 1 - lineup.timeRemaining.decimal;
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
          <mask id="gradientMaskOverall">
            <path
              fill="none"
              stroke="#fff"
              strokeWidth={progressArc.strokeWidth}
              d={progressArc.d}
            />
          </mask>
          <g mask="url(#gradientMaskOverall)">
            <rect x={-svgMidpoint} y={-svgMidpoint} width={svgMidpoint} height={svgWidth} fill="url(#cl2)" />
            <rect x="0" y={-svgMidpoint} height={svgWidth} width={svgMidpoint} fill="url(#cl1)" />
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

    // log.trace('LiveOverallStats', progressArc, dottedRemainingArc, endOuter, endInner)

    return (
      <div className="pmr-circle">
        <canvas ref="canvas" width="220" height="220" />
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
            { renderPMRCircle }
          </g>
        </svg>
      </div>
    );
  },

  renderStats() {
    if (!this.props.hasOpponent) {
      return (<div className="live-overall-stats__stats" />);
    }

    let potentialWinnings = this.props.lineup.potentialWinnings.amount || 0;
    let rank = this.props.lineup.potentialWinnings.rank || '';
    if (this.props.whichSide === 'mine') {
      rank = this.props.contest.potentialWinnings.rank || '';
      potentialWinnings = this.props.contest.potentialWinnings.amount || 0;
    }
    rank = ordinal(rank);

    if (this.props.lineup.id === 1) {
      potentialWinnings = 'N/A';
    } else if (potentialWinnings === 0) {
      potentialWinnings = `$${potentialWinnings}`;
    } else {
      potentialWinnings = `$${potentialWinnings.toFixed(2)}`;
    }

    return (
      <div className="live-overall-stats__stats">
        <span className="live-overall-stats__rank">{rank} / </span>
        <span className="live-overall-stats__potential-winnings">{potentialWinnings}</span>
      </div>
    );
  },

  render() {
    const lineup = this.props.lineup;

    if (size(lineup) === 0) return (<div />);

    return (
      <div className="live-overall-stats live-overall-stats--me">
        <h1 className="live-overall-stats__name">
          {lineup.name}
        </h1>

        {this.renderStats()}

        <div className="live-overall-stats__live-overview">
          {this.renderOverallPMR()}

          <section className="live-overview live-overview--lineup">
            <div className="live-overview__points">
              <div className="live-overview__help">
                Points
              </div>
              <h4 className="live-overview__quantity">{humanizeFP(lineup.fp)}</h4>
            </div>
            <div className="live-overview__pmr">
              <div className="live-overview__pmr__quantity">{lineup.timeRemaining.duration}</div>
              <div className="live-overview__pmr__title">PMR</div>
            </div>
          </section>
        </div>
      </div>
    );
  },
});

export default LiveOverallStats;
