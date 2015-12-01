import React from 'react'
import * as ReactRedux from 'react-redux'
import renderComponent from '../../lib/render-component'

import * as AppActions from '../../stores/app-state-store'
import errorHandler from '../../actions/live-error-handler'
import LiveContestsPaneConnected from '../live/live-contests-pane'
import LiveLineup from './live-lineup'
import LiveNBACourt from './live-nba-court'
import LiveOverallStats from './live-overall-stats'
import LivePlayerPaneConnected from '../live/live-player-pane'
import LiveStandingsPaneConnected from '../live/live-standings-pane'
import store from '../../store'
import { fetchEntriesIfNeeded, generateLineups } from '../../actions/entries'
import { liveContestsStatsSelector } from '../../selectors/live-contests'
import { currentLineupsStatsSelector } from '../../selectors/current-lineups'
import { updateLiveMode } from '../../actions/live'

// set up API calls to mock for now
import request from 'superagent'
import urlConfig from '../../fixtures/live-config'
require('superagent-mock')(request, urlConfig)


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
    liveDraftGroups: React.PropTypes.object.isRequired,
    mode: React.PropTypes.object,
    prizes: React.PropTypes.object,
    entries: React.PropTypes.object,
    updateLiveMode: React.PropTypes.func
  },


  componentWillMount: function() {
    store.dispatch(
      fetchEntriesIfNeeded()
    ).catch(
      errorHandler
    )
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
    console.log('hi')
    const newMode = Object.assign({}, this.props.mode, {
      type: 'lineup'
    })

    console.log(newMode)

    this.props.updateLiveMode(newMode)
  },


  render: function() {
    const self = this

    let moneyLine,
      bottomNavForRightPanes,
      myLineup,
      myDraftGroup,
      overallStats

    if (self.props.entries.hasRelatedInfo === false) {
      return (
        <div>LOADING</div>
      )
    }

    myLineup = self.props.currentLineups.items[self.props.mode.lineupId]
    myDraftGroup = self.props.liveDraftGroups[myLineup.draft_group]

    switch (self.props.mode.type) {
      case 'lineup':
        bottomNavForRightPanes = (
          <div className="live-right-pane-nav live-right-pane-nav--lineup" onClick={self.toggleContests}></div>
        )
        overallStats = (
          <header className="cmp-live__scoreboard live-scoreboard">
            <h1 className="live-scoreboard__contest-name">
              { myLineup.name }
            </h1>
            <LiveOverallStats
              myLineup={ myLineup }
              whichSide="me" />
          </header>
        )

        break
      case 'contest':
        bottomNavForRightPanes = (
          <div className="live-right-pane-nav live-right-pane-nav--contest" onClick={self.toggleStandings}></div>
        )

        const myContest = self.props.liveContests[self.props.mode.contestId]

        overallStats = (
          <header className="cmp-live__scoreboard live-scoreboard">
            <h1 className="live-scoreboard__contest-name">
              { myContest.info.name }
              <span className="live-scoreboard__close" onClick={ self.returnToLineup }></span>
            </h1>
            <LiveOverallStats
              myLineup={ myLineup }
              liveContestsStats={ self.props.liveContestsStats }
              currentLineupsStats={ self.props.currentLineupsStats }
              whichSide="me" />
          </header>
        )

        moneyLine = (
          <section className="live-winning-graph live-winning-graph--contest-overall">
            <div className="live-winning-graph__pmr-line">
              <div className="live-winning-graph__winners" style={{ width: '50%' }}></div>
              <div className="live-winning-graph__current-position" style={{ left: 0 }}></div>
            </div>
          </section>
        )
    }

    return (
      <div>

        <LiveLineup
          whichSide="me"
          mode={ self.props.mode }
          lineup={ myLineup }
          draftGroup={ myDraftGroup } />

        <section className="cmp-live__court-scoreboard">
          { overallStats }

          <LiveNBACourt />

          { moneyLine }
          { bottomNavForRightPanes }

        </section>

        <section className="panes">
          <LiveContestsPaneConnected
            mode={ self.props.mode }
            liveContests={ self.props.liveContests }
            currentLineups={ self.props.currentLineups }
            liveContestsStats={ self.props.liveContestsStats }
            prizes={ self.props.prizes } />
          <LivePlayerPaneConnected />
          <LiveStandingsPaneConnected />
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
    liveContests: state.liveContests,
    currentLineups: state.currentLineups,
    liveDraftGroups: state.liveDraftGroups,
    entries: state.entries,
    prizes: state.prizes,
    mode: state.live.mode,
    liveContestsStats: liveContestsStatsSelector(state),
    currentLineupsStats: currentLineupsStatsSelector(state)
  }
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    updateLiveMode: (type, id) => dispatch(updateLiveMode(type, id))
  }
}

// Wrap the component to inject dispatch and selected state into it.
var LiveConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(Live)

renderComponent(
  <Provider store={store}>
    <LiveConnected />
  </Provider>,
  '.cmp-live'
)

module.exports = Live
