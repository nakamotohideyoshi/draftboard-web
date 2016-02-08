import React from 'react'

import LiveOverallStats from './live-overall-stats'


/**
 * Return the header section of the live page, including the lineup/contest title and overall stats
 */
const LiveHeader = React.createClass({

  propTypes: {
    changePathAndMode: React.PropTypes.func.isRequired,
    liveSelector: React.PropTypes.object.isRequired,
  },

  /**
   * Used to close the current contest. Sets up parameters to then call props.changePathAndMode()
   */
  returnToLineup() {
    const mode = this.props.liveSelector.mode
    const path = `/live/lineups/${mode.myLineupId}/`
    const changedFields = {
      opponentLineupId: undefined,
      contestId: undefined,
    }

    this.props.changePathAndMode(path, changedFields)
  },

  /**
   * Typical react render method. What's interesting here is that we default to when there's just a lineup, then
   * modify the DOM elements if we're viewing a contest and/or an opponent.
   */
  render() {
    const liveSelector = this.props.liveSelector
    const myLineup = liveSelector.lineups.mine


    // set all needed variables, and default them to lineup only
    let closeContest
    let opponentStats
    let primary = myLineup.name
    let secondary
    let statsVs
    let hasContest = false


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

        let username = ''
        if (opponentLineup.hasOwnProperty('user')) {
          username = opponentLineup.user.username
        // if villian, use name
        } else if (opponentLineup.id === 1) {
          username = opponentLineup.name
        }

        secondary = (
          <div>
            {myLineup.name} <span className="vs">vs</span> {username}
          </div>
        )
        statsVs = (
          <div className="live-overall-stats__vs">vs</div>
        )
        opponentStats = (
          <LiveOverallStats
            hasContest
            lineup={opponentLineup}
            whichSide="opponent"
          />
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
          whichSide="mine"
        />

        {statsVs}
        {opponentStats}
      </header>
    )
  },
})

export default LiveHeader
