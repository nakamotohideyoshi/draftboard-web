import React from 'react'


/**
 * Responsible for rendering the moneylines scattered throughout the live section
 */
const LiveMoneyline = React.createClass({

  propTypes: {
    percentageCanWin: React.PropTypes.number.isRequired,
    myWinPercent: React.PropTypes.number.isRequired,
    opponentWinPercent: React.PropTypes.number
  },

  shouldComponentUpdate() {
    return false;
  },

  render() {
    let opponentWinPosition
    if (this.props.opponentWinPercent) {
      opponentWinPosition = (
        <div className="live-winning-graph__current-position live-winning-graph__opponent" style={{ left: this.props.opponentWinPercent + '%' }}></div>
      )
    }

    return (
      <div className="live-winning-graph__pmr-line">
        <div className="live-winning-graph__winners" style={{ width: this.props.percentageCanWin + '%' }}></div>
        <div className="live-winning-graph__current-position" style={{ left: this.props.myWinPercent + '%' }}></div>
        { opponentWinPosition }
      </div>
    )
  }

});


export default LiveMoneyline
