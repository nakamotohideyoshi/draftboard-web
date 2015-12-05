import React from 'react'
import * as ReactRedux from 'react-redux'
import renderComponent from '../../lib/render-component'
import { updatePath } from 'redux-simple-router'
import { vsprintf } from 'sprintf-js'

import * as AppActions from '../../stores/app-state-store'
import { updateLiveMode } from '../../actions/live'
import store from '../../store'


/**
 * When `View Contests` element is clicked, open side pane to show a user's current contests for that lineup.
 */
var LiveStandingsPane = React.createClass({

  propTypes: {
    mode: React.PropTypes.object.isRequired,
    updateLiveMode: React.PropTypes.func,
    updatePath: React.PropTypes.func
  },


  getInitialState: function() {
    return {
      currentTab: 'standings'
    };
  },


  viewOwnership: function() {
    this.setState({ currentTab: 'ownership' })
  },


  viewStandings: function() {
    this.setState({ currentTab: 'standings' })
  },


  viewOpponentLineup: function() {
    // change this to be a param passed in to the method. see LiveContestsPane.viewContest() as an example
    const opponentLineupId = 1

    const mode = this.props.mode

    this.props.updatePath(vsprintf('/live/lineups/%d/contests/%d/opponents/%d/', [
      mode.myLineupId,
      mode.contestId,
      opponentLineupId
    ]))
    this.props.updateLiveMode({
      opponentLineupId: opponentLineupId
    })
  },


  closePane: function() {
    AppActions.removeClass('appstate--live-standings-pane--open')
  },


  render: function() {
    let classNames = 'live-standings-pane live-pane live-pane--right live-standings-pane--' + this.state.currentTab

    return (
      <div className={classNames}>
        <div className="live-pane__close" onClick={this.closePane}></div>

        <div className="live-standings-pane__view-standings" onClick={this.viewStandings}></div>
        <div className="live-standings-pane__view-ownership" onClick={this.viewOwnership}></div>

        <div className="live-standings-pane__view-opponent-lineup" onClick={this.viewOpponentLineup}></div>
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
var LiveStandingsPaneConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(LiveStandingsPane)

// Render the component.
renderComponent(
  <Provider store={store}>
    <LiveStandingsPaneConnected />
  </Provider>,
  '.live-standings-pane'
)


module.exports = LiveStandingsPaneConnected
