import React from 'react'
import * as ReactRedux from 'react-redux'
import renderComponent from '../../lib/render-component'

import * as AppActions from '../../stores/app-state-store.js'
import LiveContestsPaneConnected from '../live/live-contests-pane'
import LiveLineup from './live-lineup'
import LiveNBACourt from './live-nba-court'
import LiveOverallStats from './live-overall-stats'
import LivePlayerPaneConnected from '../live/live-player-pane'
import LiveStandingsPaneConnected from '../live/live-standings-pane'
import store from '../../store'
import { fetchEntriesIfNeeded, generateLineups } from '../../actions/entries'

// set up API calls to mock for now
import request from 'superagent'
import urlConfig from '../../fixtures/live-config'



/**
 * The overarching component for the live  section.
 *
 * Connects with the LiveStore for data.
 * This will be where the state changes and then properties are cascaded down to the other child components.
 */
var Live = React.createClass({

  propTypes: {
    mode: React.PropTypes.object
  },


  componentWillMount: function() {
    // Mock all API responses with fixture data.
    require('superagent-mock')(request, urlConfig)

    store.dispatch(fetchEntriesIfNeeded()).then(() => {
      store.dispatch(generateLineups())
    })
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


  render: function() {
    var moneyLine
    var bottomNavForRightPanes

    switch (this.props.mode.type) {
      case 'lineup':
        bottomNavForRightPanes = (
          <div className="live-right-pane-nav live-right-pane-nav--lineup" onClick={this.toggleContests}></div>
        )
        break
      case 'contest':
        bottomNavForRightPanes = (
          <div className="live-right-pane-nav live-right-pane-nav--contest" onClick={this.toggleStandings}></div>
        )

        moneyLine = (<section className="live-winning-graph">
          <div className="live-winning-graph__pmr-line">
            <span style={{ width: '79%'}}></span>
          </div>

          <h3 className="live-winning-graph__limits live-winning-graph__min">$0</h3>
          <h2 className="live-winning-graph__earnings">$8,221</h2>
          <h3 className="live-winning-graph__limits live-winning-graph__max">$10,000</h3>
        </section>)
    }

    return (
      <div>

        <LiveLineup whichSide="me" />

        <section className="cmp-live__court-scoreboard">
          <header className="cmp-live__scoreboard live-scoreboard">
            <h1 className="live-scoreboard__contest-name">{ this.props.mode.name }</h1>
            <LiveOverallStats whichSide="me" />

          </header>

          <LiveNBACourt />

          { moneyLine }
          { bottomNavForRightPanes }

        </section>

        <LiveLineup whichSide="opponent" />

        <section className="panes">
          <LiveContestsPaneConnected lineupInfo={ this.props.mode } />
          <LivePlayerPaneConnected />
          <LiveStandingsPaneConnected lineupInfo={ this.props.mode } />
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
    mode: state.live.mode
  }
}

// Which action creators does it want to receive by props?
function mapDispatchToProps() {
  return {}
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
