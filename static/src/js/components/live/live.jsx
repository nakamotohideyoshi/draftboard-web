import React from 'react'
import * as ReactRedux from 'react-redux'
import renderComponent from '../../lib/render-component'
import { Router, Route } from 'react-router'
import createBrowserHistory from 'history/lib/createBrowserHistory'
import { syncReduxAndRouter } from 'redux-simple-router'
import { updatePath } from 'redux-simple-router'
import { vsprintf } from 'sprintf-js'

import * as AppActions from '../../stores/app-state-store'
import errorHandler from '../../actions/live-error-handler'
import LiveContestsPaneConnected from '../live/live-contests-pane'
import LiveLineup from './live-lineup'
import LiveNBACourt from './live-nba-court'
import LiveOverallStats from './live-overall-stats'
import LivePlayerPaneConnected from '../live/live-player-pane'
import LiveStandingsPaneConnected from '../live/live-standings-pane'
import store from '../../store'
import { liveContestsStatsSelector } from '../../selectors/live-contests'
import { currentLineupsStatsSelector } from '../../selectors/current-lineups'
import { liveSelector } from '../../selectors/live'
import { updateLiveMode } from '../../actions/live'


const history = createBrowserHistory()
syncReduxAndRouter(history, store)


/**
 * The overarching component for the live  section.
 *
 * Connects with the LiveStore for data.
 * This will be where the state changes and then properties are cascaded down to the other child components.
 */
var Live = React.createClass({

  propTypes: {
    liveContests: React.PropTypes.object.isRequired,
    liveContestsStats: React.PropTypes.object.isRequired,
    currentLineups: React.PropTypes.object.isRequired,
    currentLineupsStats: React.PropTypes.object.isRequired,
    liveSelector: React.PropTypes.object.isRequired,
    liveDraftGroups: React.PropTypes.object.isRequired,
    mode: React.PropTypes.object,
    params: React.PropTypes.object,
    prizes: React.PropTypes.object,
    entries: React.PropTypes.object,
    updateLiveMode: React.PropTypes.func,
    updatePath: React.PropTypes.func
  },


  componentWillMount: function() {
    const urlParams = this.props.params
    let newMode = {
      type: 'lineup',
      myLineupId: urlParams.myLineupId
    }
    if ('contestId' in urlParams) {
      newMode.type = 'contest'
      newMode.contestId = urlParams.contestId

      if ('opponentLineupId' in urlParams) {
        newMode.opponentLineupId = urlParams.opponentLineupId
      }
    }

    this.props.updateLiveMode(newMode)

    // fetchEntriesIfNeeded is called in NavScoreboard component
  },


  toggleStandings: function() {
    AppActions.toggleLiveRightPane('appstate--live-standings-pane--open')
  },


  toggleContests: function() {
    AppActions.toggleLiveRightPane('appstate--live-contests-pane--open')
  },


  getLiveClassNames: function() {
    return this.state.classNames.reduce(function(prev, curr, i, className) {
      return prev + ' ' + className
    }, 0)
  },


  returnToLineup: function() {
    this.props.updatePath(vsprintf('/live/lineups/%d/', [this.props.mode.myLineupId]))

    const newMode = Object.assign({}, this.props.mode, {
      type: 'lineup',
      opponentLineupId: undefined,
      contestId: undefined
    })

    this.props.updateLiveMode(newMode)
  },


  render: function() {
    const self = this

    // component pieces
    let
      lineups,
      liveTitle,
      moneyLine,
      bottomNavForRightPanes,
      overallStats

    const lineupNonexistant = 'myLineupId' in self.props.mode === false
    const noRelatedInfo = self.props.entries.hasRelatedInfo === false

    // if data has not loaded yet
    if (lineupNonexistant || noRelatedInfo) {
      return (
        <div>LOADING</div>
      )
    }

    if ('mine' in self.props.liveSelector.lineups) {
      var myLineup = self.props.liveSelector.lineups.mine

      console.log(self.props, 'mylineupppp')

      bottomNavForRightPanes = (
        <div className="live-right-pane-nav live-right-pane-nav--lineup" onClick={self.toggleContests}></div>
      )

      liveTitle = (
        <h1 className="live-scoreboard__contest-name">
          { myLineup.name }
        </h1>
      )

      overallStats = (
        <LiveOverallStats
          lineup={ myLineup }
          whichSide="mine" />
      )

      lineups = (
        <LiveLineup
          whichSide="mine"
          mode={ self.props.mode }
          lineup={ myLineup } />
      )
    }

    if (self.props.mode.contestId) {
      const myContest = self.props.liveSelector.contest

      bottomNavForRightPanes = (
        <div className="live-right-pane-nav live-right-pane-nav--contest" onClick={self.toggleStandings}></div>
      )

      liveTitle = (
        <h1 className="live-scoreboard__contest-name">
          { myContest.name }
          <span className="live-scoreboard__close" onClick={ self.returnToLineup }></span>
        </h1>
      )

      overallStats = (
        <LiveOverallStats
          lineup={ myLineup }
          whichSide="mine" />
      )

      moneyLine = (
        <section className="live-winning-graph live-winning-graph--contest-overall">
          <div className="live-winning-graph__pmr-line">
            <div className="live-winning-graph__winners" style={{ width: myContest.percentageCanWin + '%' }}></div>
            <div className="live-winning-graph__current-position" style={{ left: myContest.currentPercentagePosition + '%' }}></div>
          </div>
        </section>
      )

      if (self.props.mode.opponentLineupId) {
        const opponentLineup = self.props.liveSelector.lineups.opponent

        lineups = (
          <div>
            { lineups }
            <LiveLineup
              whichSide="opponent"
              lineup={ opponentLineup } />
          </div>
        )

        overallStats = (
          <div>
            { overallStats }

            <div className="live-overall-stats__vs">vs</div>

            <LiveOverallStats
              lineup={ opponentLineup }
              whichSide="opponent" />
          </div>
        )

        moneyLine = (
          <section className="live-winning-graph live-winning-graph--contest-overall">
            <div className="live-winning-graph__pmr-line">
              <div className="live-winning-graph__winners" style={{ width: myContest.percentageCanWin + '%' }}></div>
              <div className="live-winning-graph__current-position" style={{ left: myContest.currentPercentagePosition + '%' }}></div>
              <div className="live-winning-graph__current-position live-winning-graph__opponent" style={{ left: '100%' }}></div>
            </div>
          </section>
        )
      }
    }

    return (
      <div>

        { lineups }

        <section className="cmp-live__court-scoreboard">
          <header className="cmp-live__scoreboard live-scoreboard">
            { liveTitle }

            { overallStats }
          </header>

          <LiveNBACourt />

          { moneyLine }
          { bottomNavForRightPanes }

        </section>

        <section className="panes">
          <LiveContestsPaneConnected
            lineup={ myLineup }
            mode={ this.props.mode } />
          <LivePlayerPaneConnected />
          <LiveStandingsPaneConnected
            mode={ self.props.mode } />
        </section>
      </div>
    )
  }

})


// Redux integration
let {Provider, connect} = ReactRedux

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {
    // state elements
    currentLineups: state.currentLineups,
    entries: state.entries,
    liveContests: state.liveContests,
    liveDraftGroups: state.liveDraftGroups,
    mode: state.live.mode,
    prizes: state.prizes,

    // selectors
    currentLineupsStats: currentLineupsStatsSelector(state),
    liveContestsStats: liveContestsStatsSelector(state),
    liveSelector: liveSelector(state)
  }
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    updateLiveMode: (type, id) => dispatch(updateLiveMode(type, id)),
    updatePath: (path) => dispatch(updatePath(path))
  }
}

// Wrap the component to inject dispatch and selected state into it.
var LiveConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(Live)

renderComponent(
  <Provider store={store}>
    <Router history={history}>
      <Route path="/live/lineups/:myLineupId" component={LiveConnected} />
      <Route path="/live/lineups/:myLineupId/contests/:contestId/" component={LiveConnected} />
      <Route path="/live/lineups/:myLineupId/contests/:contestId/opponents/:opponentLineupId" component={LiveConnected} />
    </Router>
  </Provider>,
  '.cmp-live'
)

module.exports = Live
