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
 * When `View Contests` element is clicked, open side pane to show
 * a user's current contests for that lineup.
 */
var LiveContestsPane = React.createClass({

  propTypes: {
    lineup: React.PropTypes.object.isRequired,
    mode: React.PropTypes.object.isRequired,
    updateLiveMode: React.PropTypes.func,
    updatePath: React.PropTypes.func
  },


  viewContest: function(contestId) {
    const mode = this.props.mode

    this.props.updatePath(vsprintf('/live/lineups/%d/contests/%d/', [mode.myLineupId, contestId]))
    this.props.updateLiveMode({
      type: 'contest',
      draftGroupId: mode.draftGroupId,
      myLineupId: mode.myLineupId,
      contestId: contestId
    })
  },


  closePane: function() {
    AppActions.removeClass('appstate--live-contests-pane--open')
  },


  render: function() {
    let self = this;

    const lineup = self.props.lineup
    const lineupContests = _map(lineup.contestsStats, function(contest, id) {
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
    updateLiveMode: (newMode) => dispatch(updateLiveMode(newMode)),
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
