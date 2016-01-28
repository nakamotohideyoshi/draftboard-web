import React from 'react'
import { map as _map } from 'lodash'

import * as AppActions from '../../stores/app-state-store'
import LiveContestsPaneItem from './live-contests-pane-item'


/**
 * When `View Contests` element is clicked, open side pane to show
 * a user's current contests for that lineup.
 */
const LiveContestsPane = React.createClass({

  propTypes: {
    changePathAndMode: React.PropTypes.func.isRequired,
    lineup: React.PropTypes.object.isRequired,
    mode: React.PropTypes.object.isRequired,
  },

  viewContest(contestId) {
    const mode = this.props.mode
    const path = `/live/lineups/${mode.myLineupId}/contests/${contestId}`
    const changedFields = {
      draftGroupId: mode.draftGroupId,
      myLineupId: mode.myLineupId,
      contestId,
    }

    this.props.changePathAndMode(path, changedFields)
  },

  closePane() {
    AppActions.removeClass('appstate--live-contests-pane--open')
  },

  renderContests() {
    const lineup = this.props.lineup

    return _map(lineup.contestsStats, (contest) => (
      <LiveContestsPaneItem
        contest={contest}
        onItemClick={this.viewContest}
        key={contest.id}
        lineupPotentialEarnings={lineup.potentialEarnings || 0}
      />
    ))
  },

  render() {
    return (
      <div className="live-contests-pane live-pane live-pane--right">
        <div className="live-pane__close" onClick={this.closePane} />

        <div className="live-pane__content">
          <h2>
            My Contests
          </h2>

          <div className="live-contests-pane__list">
            <ul className="live-contests-pane__list__inner">
              {this.renderContests()}
            </ul>
          </div>
        </div>
        <div className="live-pane__left-shadow" />

        <div className="live-contests-pane__view-contest" onClick={this.viewContest} />
      </div>
    )
  },
})

export default LiveContestsPane
