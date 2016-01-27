import * as ReactRedux from 'react-redux'
import React from 'react'
import renderComponent from '../../lib/render-component'
import { map as _map } from 'lodash'

import * as AppActions from '../../stores/app-state-store'


/**
 * When `View Contests` element is clicked, open side pane to show
 * a user's current contests for that lineup.
 */
var LiveContestsPane = React.createClass({

  propTypes: {
    changePathAndMode: React.PropTypes.func.isRequired,
    lineup: React.PropTypes.object.isRequired,
    mode: React.PropTypes.object.isRequired
  },

  viewContest(contestId) {
    const mode = this.props.mode
    const path = `/live/lineups/${mode.myLineupId}/contests/${contestId}`
    const changedFields = {
      draftGroupId: mode.draftGroupId,
      myLineupId: mode.myLineupId,
      contestId: contestId
    }

    this.props.changePathAndMode(path, changedFields)
  },

  closePane() {
    AppActions.removeClass('appstate--live-contests-pane--open')
  },

  renderContests() {
    const self = this
    const lineup = this.props.lineup

    return _map(lineup.contestsStats, function(contest, id) {
      let moneyLineClass = 'live-winning-graph'

      if (contest.percentageCanWin <= contest.currentPercentagePosition) {
        moneyLineClass += ' live-winning-graph--is-losing'
      }

      return (
        <li className="live-contests-pane__contest" key={ contest.id }>
          <div className="live-contests-pane__name">{ contest.name }</div>
          <div className="live-contests-pane__place">
            <span className="live-contests-pane__place--mine">{ contest.rank }</span> of { contest.entriesCount }
          </div>
          <div className="live-contests-pane__potential-earnings">${ contest.buyin }/${ lineup.potentialEarnings }</div>

          <section className={ moneyLineClass }>
            <div className="live-winning-graph__pmr-line">
              <div className="live-winning-graph__winners" style={{ width: contest.percentageCanWin + '%' }}></div>
              <div className="live-winning-graph__current-position" style={{ left: contest.currentPercentagePosition + '%' }}></div>
            </div>
          </section>

          <div className="live-contest-cta" onClick={ self.viewContest.bind(self, contest.id) }>Watch Live</div>
        </li>
      )
    })
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
  }
})

export default LiveContestsPane
