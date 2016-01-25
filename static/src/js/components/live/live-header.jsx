import * as ReactRedux from 'react-redux'
import React from 'react'
import {updatePath} from 'redux-simple-router'
import {vsprintf} from 'sprintf-js'

import log from '../../lib/logging'
import * as AppActions from '../../stores/app-state-store'
import {updateLiveMode} from '../../actions/live'
import LiveOverallStats from './live-overall-stats'


// Redux integration
let {Provider, connect} = ReactRedux

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {}
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    updateLiveMode: (newMode) => dispatch(updateLiveMode(newMode)),
    updatePath: (path) => dispatch(updatePath(path))
 }
}


// Wrap the component to inject dispatch and selected state into it.
var LiveHeader = connect(
  mapStateToProps,
  mapDispatchToProps
)(React.createClass({
  propTypes: {
    liveSelector: React.PropTypes.object.isRequired,
    updateLiveMode: React.PropTypes.func,
    updatePath: React.PropTypes.func
 },

  returnToLineup() {
    const mode = this.props.liveSelector.mode

    this.props.updatePath(vsprintf('/live/lineups/%d/', [mode.myLineupId]))

    const newMode = Object.assign({}, mode, {
      opponentLineupId: undefined,
      contestId: undefined
   })

    this.props.updateLiveMode(newMode)
 },

  render() {
    const liveSelector = this.props.liveSelector
    const myLineup = liveSelector.lineups.mine


    // set all needed variables, and default them to lineup only
    let closeContest,
        opponentStats,
        overallStats,
        primary = myLineup.name,
        secondary,
        statsVs,
        hasContest = false


    // if watching a contest, then update the titles and ensure the overall stats are contest-based
    if (liveSelector.hasOwnProperty('contest')) {
      const contest = liveSelector.contest

      hasContest = true
      primary = contest.name
      secondary = myLineup.name
      closeContest = (
        <span className="live-scoreboard__close" onClick={this.returnToLineup}></span>
      )


      // if watching an opponent, then add in second overall stats and update the titles
      if (liveSelector.lineups.hasOwnProperty('opponent')) {
        const opponentLineup = liveSelector.lineups.opponent

        secondary = (
          <div>
            {myLineup.name} <span className="vs">vs</span> {opponentLineup.user.username}
          </div>
        )
        statsVs = (
          <div className="live-overall-stats__vs">vs</div>
        )
        opponentStats = (
          <LiveOverallStats
            hasContest
            lineup={opponentLineup}
            whichSide="opponent" />
        )
     }
   }

    return (
      <header className="cmp-live__scoreboard live-scoreboard">
        <h2 className="live-scoreboard__lineup-name">
          {secondary}
        </h2>
        <h1 className="live-scoreboard__contest-name">
          {primary}
          {closeContest}
        </h1>

        <LiveOverallStats
          lineup={myLineup}
          hasContest={hasContest}
          whichSide="mine" />

        {statsVs}
        {opponentStats}
      </header>
    )
 }
}))

module.exports = LiveHeader
