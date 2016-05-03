import React from 'react';


/**
 * Reusable MLB diamond to show who is on what base for hitting team
 */
const LiveMLBDiamond = (props) => (
  <div className="live-mlb-diamond mlb-diamond">
    <svg viewBox="0 0 42 42">
      <defs>
        <linearGradient
          id="live-mlb-diamond--mine"
          x1="0%" y1="0%" x2="0%" y2="100%" gradientTransform="rotate(45)"
        >
          <stop offset="0%" stopColor="#33b0ca" />
          <stop offset="100%" stopColor="#214e9d" />
        </linearGradient>
        <linearGradient
          id="live-mlb-diamond--opponent"
          x1="0%" y1="0%" x2="0%" y2="100%" gradientTransform="rotate(45)"
        >
          <stop offset="0%" stopColor="#e23b3c" />
          <stop offset="100%" stopColor="#600765" />
        </linearGradient>
        <linearGradient id="live-mlb-diamond--both" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#fff" />
          <stop offset="100%" stopColor="#fff" />
        </linearGradient>
        <linearGradient id="live-mlb-diamond--none" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#484b5c" />
          <stop offset="100%" stopColor="#484b5c" />
        </linearGradient>
      </defs>
      <g>
        <rect
          className="mlb-diamond__base"
          style={{ fill: `url(#live-mlb-diamond--${props.first})` }}
          x="30.2" y="15.9" transform="matrix(0.7071 -0.7071 0.7071 0.7071 -4.5024 30.8994)" width="9.6" height="10.1"
        />
        <rect
          className="mlb-diamond__base"
          style={{ fill: `url(#live-mlb-diamond--${props.second})` }}
          x="16.2" y="1.9" transform="matrix(0.7071 -0.7071 0.7071 0.7071 1.2212 16.853)" width="9.6" height="10.1"
        />
        <rect
          className="mlb-diamond__base"
          style={{ fill: `url(#live-mlb-diamond--${props.third})` }}
          x="2.3" y="15.9" transform="matrix(0.7071 -0.7071 0.7071 0.7071 -12.7174 11.1741)" width="9.6" height="10.1"
        />
        <polygon
          className="mlb-diamond__base"
          style={{ fill: `url(#live-mlb-diamond--${props.home})` }}
          points="14.4,28 27.7,28 27.7,35.6 21.3,42 14.4,35"
        />
      </g>
    </svg>
  </div>
);

// possible choices for each of these are: ['none', 'mine', 'opponent', 'both',]
LiveMLBDiamond.propTypes = {
  first: React.PropTypes.string,
  second: React.PropTypes.string,
  third: React.PropTypes.string,
  home: React.PropTypes.string,
};

// default to no one being on base
LiveMLBDiamond.defaultProps = {
  first: 'none',
  second: 'none',
  third: 'none',
  home: 'none',
};

export default LiveMLBDiamond;
