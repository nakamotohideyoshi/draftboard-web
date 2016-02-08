import React from 'react'


/**
 * Responsible for rendering the moneylines scattered throughout the live section
 */
const LiveMoneyline = React.createClass({

  propTypes: {
    percentageCanWin: React.PropTypes.number.isRequired,
    myWinPercent: React.PropTypes.number.isRequired,
    opponentWinPercent: React.PropTypes.number,
  },

  render() {
    // flip so that everything is right aligned
    const myWinPercent = 100 - this.props.myWinPercent

    let opponentWinPercent
    let opponentWinPosition
    if (this.props.opponentWinPercent) {
      opponentWinPercent = 100 - this.props.opponentWinPercent

      opponentWinPosition = (
        <div
          className="live-moneyline__current-position live-moneyline__opponent"
          style={{ left: `${opponentWinPercent}%` }}
        >
        </div>
      )
    }

    return (
      <div className="live-moneyline__pmr-line">
        <div className="live-moneyline__winners" style={{ width: `${this.props.percentageCanWin}%` }}></div>
        <div className="live-moneyline__current-position" style={{ left: `${myWinPercent}%` }}></div>
        { opponentWinPosition }
      </div>
    )
  },
})


export default LiveMoneyline
