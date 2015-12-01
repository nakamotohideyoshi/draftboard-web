import React from 'react'
import * as ReactRedux from 'react-redux'
import renderComponent from '../../lib/render-component'
import { map as _map } from 'lodash'
import { updatePath } from 'redux-simple-router'
import { vsprintf } from 'sprintf-js'

import * as AppActions from '../../stores/app-state-store'
import { updateLiveMode } from '../../actions/live'
import store from '../../store'


/**
 * When `View Contests` element is clicked, open side pane to show a user's current contests for that lineup.
 */
var LiveContestsPane = React.createClass({

  propTypes: {
    liveContests: React.PropTypes.object.isRequired,
    currentLineups: React.PropTypes.object.isRequired,
    liveContestsStats: React.PropTypes.object.isRequired,
    mode: React.PropTypes.object.isRequired,
    prizes: React.PropTypes.object.isRequired,
    updateLiveMode: React.PropTypes.func,
    updatePath: React.PropTypes.func
  },


  viewContest: function(contestId) {
    const mode = this.props.mode

    this.props.updatePath(vsprintf('/live/lineups/%d/contests/%d/', [mode.lineupId, contestId]))
    this.props.updateLiveMode({
      type: 'contest',
      draftGroupId: mode.draftGroupId,
      lineupId: mode.lineupId,
      contestId: contestId
    })
  },


  closePane: function() {
    AppActions.removeClass('appstate--live-contests-pane--open')
  },


  render: function() {
    let self = this;

    if (self.props.mode.lineupId in self.props.currentLineups.items === false) {
      return (<div className="live-contests-pane live-pane live-pane--right" />)
    }

    const lineup = self.props.currentLineups.items[self.props.mode.lineupId]
    const lineupContests = _map(lineup.contests, function(key) {
      const contest = self.props.liveContests[key]
      const contestStats = self.props.liveContestsStats[key]
      const lineupStats = contestStats.entriesStats[self.props.mode.lineupId]
      const totalEntries = contestStats.rankedLineups.length
      const prizeStructure = self.props.prizes[contest.info.prize_structure].info
      const percentageCanWin = prizeStructure.payout_spots / contest.info.entries * 100
      const currentPercentagePosition = (lineupStats.currentStanding - 1) / contest.info.entries * 100

      let moneyLineClass = 'live-winning-graph'
      if (percentageCanWin <= currentPercentagePosition) {
        moneyLineClass += ' live-winning-graph--is-losing'
      }

      return (
        <li className="live-contests-pane__contest" key={ contest.id }>
          <div className="live-contests-pane__name">{ contest.info.name }</div>
          <div className="live-contests-pane__place">
            <span className="live-contests-pane__place--mine">{ lineupStats.currentStanding }</span> of { totalEntries }
          </div>
          <div className="live-contests-pane__potential-earnings">${ contest.info.buyin }/${ parseInt(lineupStats.potentialEarnings) }</div>

          <section className={ moneyLineClass }>
            <div className="live-winning-graph__pmr-line">
              <div className="live-winning-graph__winners" style={{ width: percentageCanWin + '%' }}></div>
              <div className="live-winning-graph__current-position" style={{ left: currentPercentagePosition + '%' }}></div>
            </div>
          </section>

          <div className="live-contest-cta" onClick={ self.viewContest.bind(self, contest.id) }>Watch Live</div>
        </li>
      )
    })


    return (
      <div className="live-contests-pane live-pane live-pane--right">
        <div className="live-pane__close" onClick={self.closePane} />

        <div className="live-pane__content">
          <h2>
            My Contests
          </h2>

          <div className="live-contests-pane__list">
            <ul className="live-contests-pane__list__inner">
              { lineupContests }
            </ul>
          </div>
        </div>
        <div className="live-pane__left-shadow" />

        <div className="live-contests-pane__view-contest" onClick={self.viewContest} />
      </div>
    )
  }
})


// Redux integration
let {Provider, connect} = ReactRedux

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {}
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    updateLiveMode: (type, id) => dispatch(updateLiveMode(type, id)),
    updatePath: (path) => dispatch(updatePath(path))
  }
}

// Wrap the component to inject dispatch and selected state into it.
var LiveContestsPaneConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(LiveContestsPane)

// Render the component.
renderComponent(
  <Provider store={store}>
    <LiveContestsPaneConnected />
  </Provider>,
  '.live-contests-pane'
)


module.exports = LiveContestsPaneConnected
