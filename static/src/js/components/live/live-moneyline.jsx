import React from 'react';


/**
 * Responsible for rendering the moneylines scattered throughout the live section
 */
const LiveMoneyline = (props) => {
  // flip so that everything is right aligned
  const myWinPercent = 100 - props.myWinPercent;

  let opponentWinPercent;
  let opponentWinPosition;
  if (props.opponentWinPercent) {
    opponentWinPercent = 100 - props.opponentWinPercent;

    opponentWinPosition = (
      <div
        className="live-moneyline__current-position live-moneyline__opponent"
        style={{ left: `${opponentWinPercent}%` }}
      >
      </div>
    );
  }

  return (
    <div className="live-moneyline__pmr-line">
      <div className="live-moneyline__winners" style={{ width: `${props.percentageCanWin}%` }}></div>
      <div className="live-moneyline__current-position" style={{ left: `${myWinPercent}%` }}></div>
      { opponentWinPosition }
    </div>
  );
};

LiveMoneyline.propTypes = {
  percentageCanWin: React.PropTypes.number.isRequired,
  myWinPercent: React.PropTypes.number.isRequired,
  opponentWinPercent: React.PropTypes.number,
};

export default LiveMoneyline;
